"""Optional, local-only AOS-W event store and recovery helper.

Requires Python standard library; PyYAML ONLY for loading pinned YAML graphs/revisions.
Pure file protocol in scaffold/aos-w/PROTOCOL.md remains the mandatory portable standard.
Single cooperating writer; no remote mutex, scheduler, provider requests or authenticated permissions.
"""
from __future__ import annotations
import copy, datetime as dt, hashlib, json, os, re, tempfile
from pathlib import Path

GENESIS = '0'*64
ID = re.compile(r'^[a-z0-9][a-z0-9._-]{0,79}$')
TERMINAL = {'COMPLETE', 'CANCELLED', 'SUPERSEDED', 'FAILED'}
TASK_STATUS = {'PROPOSED','WAIT_AUTHORIZATION','WAIT_DEPENDENCY','READY','CLAIMED','RUNNING',
               'WAIT_EXTERNAL','WAIT_REVIEW','NEEDS_REWORK','BLOCKED','RECONCILE_REQUIRED',
               'PAUSED','COMPLETE','SKIPPED','CANCELLED','SUPERSEDED','FAILED'}
RUN_STATUS = {'CREATED','ACTIVE','PAUSED','WAITING','BLOCKED','COMPLETED','FAILED','CANCELLED','SUPERSEDED'}
SIDE_EFFECTS = {'stage_paused','edit_crm','deploy_dev','deploy_prod','activate_live',
                'change_budget','send_message','emit_conversion'}

class StateError(ValueError): pass
class CorruptLog(StateError): pass
class Unauthorized(StateError): pass

def ensure(cond, message):
    if not cond: raise StateError(message)

def utcnow(): return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def stamp(value):
    return dt.datetime.fromisoformat(value.replace('Z','+00:00'))
def canonical(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(value): return hashlib.sha256(value).hexdigest()
def jsonbytes(value): return (json.dumps(value,indent=2,ensure_ascii=False,sort_keys=True)+'\n').encode()
def valid_id(value): return isinstance(value,str) and bool(ID.fullmatch(value))
def valid_actor(actor): return isinstance(actor,dict) and all(isinstance(actor.get(k),str) and actor[k].strip() for k in ('agent','platform','role','instance'))

def atomic_write(path:Path,data:bytes):
    path.parent.mkdir(parents=True,exist_ok=True)
    # Temporary file in same directory; atomic rename if host supports it. No network or durable FS claim.
    fd,tmp=tempfile.mkstemp(prefix='.aosw-',dir=str(path.parent))
    try:
        with os.fdopen(fd,'wb') as f:
            f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
        try:
            directory_fd=os.open(path.parent,os.O_RDONLY)
            try: os.fsync(directory_fd)
            finally: os.close(directory_fd)
        except OSError: pass
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def read_graph(instance:Path,revision:str):
    ensure(valid_id(revision),'Invalid graph revision')
    path=instance/'graph-revisions'/(revision+'.yaml')
    ensure(path.is_file(),'Pinned graph revision missing: '+str(path))
    try:
        import yaml # explicitly OPTIONAL, not installed with the downloaded folder
    except ImportError as e:
        raise StateError('Optional helper requires PyYAML for YAML graph; file-only agents may read manually') from e
    source=yaml.safe_load(path.read_text(encoding='utf-8'))
    graph=source.get('graph',source)
    ensure(isinstance(graph,dict) and isinstance(graph.get('nodes'),list),'Graph invalid')
    return graph

def enforce_root(runroot:Path):
    root=runroot.resolve(strict=False)
    ensure('agent-files' in root.parts,'Run root must reside under agent-files')
    ensure('instances' in root.parts and 'runs' in root.parts,'Not an instance run root')
    ensure(not runroot.is_symlink(),'Run root may not be a symlink')
    return root

def safe_output(runroot:Path,relpath:str):
    ensure(isinstance(relpath,str) and relpath and not relpath.startswith('/') and '..' not in Path(relpath).parts,'Unsafe artifact path')
    root=enforce_root(runroot)
    dest=(root/relpath).resolve(strict=False)
    ensure(dest.is_relative_to(root),'Output escaped run root')
    return dest

def init_state(run_id,graph,graph_revision='g0001'):
    return {'schema_version':'1.0.0','run_id':run_id,'graph_revision':graph_revision,
      'run_status':'CREATED','state_revision':0,'last_event_seq':0,'last_event_digest':GENESIS,
      'integrity_level':'verified','updated_at':utcnow(),'paused':False,
      'tasks':{n['id']:{'status':'WAIT_DEPENDENCY','attempts':0,'graph_revision':graph_revision,
                         'owner':None,'evidence':[],'pending_actions':[],
                         'retry':None,'last_error':None,'last_attempt_id':None,'review':None} for n in graph['nodes']},
      'operations':{},'pending_provider_operations':[], 'eligible_tasks':[],
      'blocked_reasons':[], 'completed_steps':[], 'active_steps':[],
      'owners':{},'evidence_refs':[], 'checkpoints':[], 'audit_warnings':[],
      'governance':{'claims':{},'permissions':{},'reviews':{},'remediation':{},'handoff':None}}

def reduce_event(state,event):
    s=state
    t=event['type'];p=event.get('payload') or {}; tid=event.get('task_id')
    item=s['tasks'].get(tid) if tid else None
    def task(*allowed):
        ensure(item is not None,'Unknown task '+str(tid))
        if allowed: ensure(item['status'] in allowed,'Invalid '+t+' from '+item['status'])
        return item
    if t=='run_created':
        ensure(s['last_event_seq']==0,'Duplicate run_created')
    elif t=='task_ready': task('WAIT_DEPENDENCY','BLOCKED','NEEDS_REWORK','PAUSED','READY')['status']='READY'
    elif t=='task_claimed':
        q=task('READY');q.update(status='CLAIMED',owner=event['actor'])
    elif t=='task_started':
        q=task('CLAIMED','READY');ensure(valid_id(event.get('attempt_id')),'Attempt ID required')
        q.update(status='RUNNING',owner=event['actor'],last_attempt_owner=event['actor'],started_at=event['at'],
                 attempts=q['attempts']+1,last_attempt_id=event['attempt_id'],retry=None)
    elif t=='task_submitted_review': task('RUNNING')['status']='WAIT_REVIEW'
    elif t=='review_accepted':
        q=task('WAIT_REVIEW');ensure(p.get('verdict')=='PASS' and p.get('review_id') and p.get('artifacts') and p.get('rubric_version'),'Current review evidence missing');q['review']=p
    elif t=='review_revise':
        q=task('WAIT_REVIEW');q.update(status='NEEDS_REWORK',review=p,last_error={'class':'review_revise','correction':p.get('correction')},retry=p.get('retry'))
    elif t=='task_completed':
        q=task('RUNNING','WAIT_REVIEW');ensure(bool(event.get('evidence')),'Cannot complete without artifact evidence')
        ensure(not q.get('pending_actions'),'External effects must be reconciled before completion')
        if q['status']=='WAIT_REVIEW': ensure((q.get('review') or {}).get('verdict')=='PASS','Missing accepted quality review')
        q.update(status='COMPLETE',evidence=event['evidence'],owner=None,retry=None)
    elif t=='task_failed':
        q=task('RUNNING','WAIT_EXTERNAL','WAIT_REVIEW');ensure(p.get('error_class') and p.get('correction'),'Failure needs class and correction')
        q.update(status='FAILED' if p.get('terminal') else 'BLOCKED',last_error={'class':p['error_class'],'correction':p['correction']},owner=None,retry=p.get('retry'))
    elif t=='task_requeued':
        q=task('BLOCKED','NEEDS_REWORK','FAILED');ensure(p.get('reason'),'Retry needs reason');q.update(status='READY',retry=None,review=None)
    elif t=='task_blocked': task('WAIT_DEPENDENCY','READY','RUNNING','CLAIMED','WAIT_REVIEW','BLOCKED')['status']='BLOCKED'
    elif t=='task_unblocked':
        q=task('BLOCKED');ensure(p.get('reason'),'Unblock requires documented reason')
        ensure(not q['pending_actions'],'Unresolved operation blocks unblocking')
        q['status']='RUNNING' if p.get('resume_existing_attempt') else 'READY'
        if not p.get('resume_existing_attempt'):q['owner']=None
    elif t=='task_paused':
        q=task('READY','RUNNING','BLOCKED','WAIT_DEPENDENCY','WAIT_REVIEW');q['resume_status']=q['status'];q['status']='PAUSED'
    elif t=='task_resumed':
        q=task('PAUSED')
        prior=q.get('resume_status','WAIT_DEPENDENCY')
        if q.get('pending_actions'):q['status']='RECONCILE_REQUIRED'
        elif prior in ('RUNNING','CLAIMED'):q['status']='READY'  # explicit operator resume starts a fresh bounded attempt
        else:q['status']=prior
        q['owner']=None
    elif t=='task_cancelled':
        q=task(*tuple(TASK_STATUS-TERMINAL));q.update(status='CANCELLED',owner=None)
    elif t=='run_paused': ensure(s['run_status'] not in ('CANCELLED','FAILED','COMPLETED'),'Terminal run');s['paused']=True;s['run_status']='PAUSED'
    elif t=='run_resumed': ensure(s['run_status']=='PAUSED','Run not paused');s['paused']=False;s['run_status']='ACTIVE'
    elif t=='run_cancelled': ensure(s['run_status'] not in ('CANCELLED','COMPLETED'),'Already terminal');s['run_status']='CANCELLED';s['paused']=False
    elif t=='run_failed': ensure(s['run_status'] not in ('CANCELLED','COMPLETED'),'Already terminal');s['run_status']='FAILED'
    elif t=='operation_intent':
        q=task('RUNNING');key=p.get('operation_key');ensure(valid_id(key),'Operation key invalid')
        ensure(key not in s['operations'],'Operation already recorded: '+str(key))
        if p.get('retry_reference'):
            prior=s['operations'].get(p['retry_reference'])
            ensure(prior and prior['status']=='NOT_APPLIED' and prior['provider']==p['provider']
                   and prior['resource']==p['resource'] and prior['request_digest']==p['request_digest'],
                   'Retry reference must be a reconciled NOT_APPLIED equivalent operation')
        ensure(p.get('approval_id') and p.get('provider') and p.get('resource') and p.get('request_digest'),'Operation intent missing scoped details')
        resource=(p['provider'],p['resource']);ensure(not any((o['provider'],o['resource'])==resource and o['status']!='NOT_APPLIED' for o in s['operations'].values()),'Potential duplicate/conflicting resource operation')
        s['operations'][key]={**p,'task_id':tid,'status':'INTENT_RECORDED','created_at':event['at']};q['pending_actions'].append(key)
    elif t=='operation_submitted':
        key=p.get('operation_key');o=s['operations'].get(key);ensure(o and o['status']=='INTENT_RECORDED','Operation not at intent boundary');o['status']='REQUEST_SUBMITTED'
    elif t=='operation_ack':
        key=p.get('operation_key');o=s['operations'].get(key);ensure(o and o['status']=='REQUEST_SUBMITTED','Operation not submitted')
        ensure(p.get('ack') in ('accepted','rejected','ambiguous'),'Invalid operation ack');o['status']='REQUEST_ACCEPTED' if p['ack']=='accepted' else 'RECONCILE_REQUIRED' if p['ack']=='ambiguous' else 'REJECTED';o['ack']=p['ack'];o['ack_evidence']=p.get('evidence')
        if o['status']=='RECONCILE_REQUIRED':s['tasks'][o['task_id']]['status']='RECONCILE_REQUIRED'
    elif t=='operation_unknown':
        key=p.get('operation_key');o=s['operations'].get(key);ensure(o and o['status'] in ('INTENT_RECORDED','REQUEST_SUBMITTED','REQUEST_ACCEPTED','RECONCILE_REQUIRED'),'Unknown operation state');o['status']='RECONCILE_REQUIRED';s['tasks'][o['task_id']]['status']='RECONCILE_REQUIRED'
    elif t=='operation_reconciled':
        key=p.get('operation_key');o=s['operations'].get(key);ensure(o and o['status'] in ('RECONCILE_REQUIRED','REQUEST_ACCEPTED','REJECTED'),'No unresolved operation')
        ensure(p.get('readback_source') and p.get('observed_at') and p.get('readback_ref'),'Provider readback reference required')
        ensure(p.get('result') in ('APPLIED','NOT_APPLIED','MISMATCH'),'Invalid reconciliation status')
        o['status']=p['result'];o['readback']={k:p[k] for k in ('readback_source','observed_at','readback_ref','result')}
        q=s['tasks'][o['task_id']]
        if key in q['pending_actions']:q['pending_actions'].remove(key)
        if q['status']=='RECONCILE_REQUIRED':q['status']='BLOCKED' # deliberate manual re-evaluation before further work
    elif t=='graph_revised':
        ensure(p.get('base_revision')==s['graph_revision'] and valid_id(p.get('new_revision')),'Stale graph revision')
        ensure(p.get('approval_id') and p.get('graph_digest') and isinstance(p.get('invalidated'),list),'Graph revision requires approval, hash, impact')
        s['graph_revision']=p['new_revision']
        new_ids=set(p.get('remaining_nodes',[]))
        s.setdefault('superseded_results',[])
        for nid in p['invalidated']:
            if nid in s['tasks']:
                q=s['tasks'][nid]
                s['superseded_results'].append({'task_id':nid,'prior_graph_revision':q['graph_revision'],
                   'previous_status':q['status'],'attempts':q['attempts'],'evidence':copy.deepcopy(q['evidence']),
                   'review':copy.deepcopy(q['review']),'event_seq':event['seq']})
                q.update(status='WAIT_DEPENDENCY' if nid in new_ids else 'SUPERSEDED',
                   graph_revision=p['new_revision'],owner=None,review=None,evidence=[],last_attempt_id=None,retry=None)
        for nid in p.get('new_nodes',[]):
            ensure(nid not in s['tasks'],'New node already exists');s['tasks'][nid]={'status':'WAIT_DEPENDENCY','attempts':0,'graph_revision':p['new_revision'],'owner':None,'evidence':[],'pending_actions':[],'retry':None,'last_error':None,'last_attempt_id':None,'review':None}
    elif t in ('claim_recorded','claim_released','permission_granted','permission_revoked',
               'quality_recorded','remediation_requested','governance_handoff'):
        g=s.setdefault('governance',{'claims':{},'permissions':{},'reviews':{},'remediation':{},'handoff':None})
        bucket={'claim_recorded':'claims','claim_released':'claims',
                'permission_granted':'permissions','permission_revoked':'permissions',
                'quality_recorded':'reviews','remediation_requested':'remediation',
                'governance_handoff':'handoff'}[t]
        if bucket=='handoff':g['handoff']=dict(p)
        else:
            rid=p.get('record_id');ensure(valid_id(rid),'Governance event record ID missing')
            ensure(rid not in g[bucket],'Duplicate governance event '+rid)
            g[bucket][rid]={'type':t,'at':event['at'],'actor':event['actor'],**p}
        if t=='claim_released' and item is not None and item.get('status')=='CLAIMED':
            item.update(status='READY',owner=None)
    elif t in ('checkpoint_created','recovery_checked','handoff_updated','task_wait_external'):
        if t=='task_wait_external':task('RUNNING')['status']='WAIT_EXTERNAL'
        if t=='checkpoint_created':s['checkpoints'].append(p.get('checkpoint_id','unknown'))
    else:raise StateError('Unknown event type '+t)
    if t=='task_started' and s['run_status']=='CREATED': s['run_status']='ACTIVE'
    if s['run_status'] not in ('FAILED','CANCELLED','SUPERSEDED') and not s['paused']:
        if s['tasks'] and all(q['status'] in ('COMPLETE','SKIPPED') for q in s['tasks'].values()):s['run_status']='COMPLETED'
        elif s['run_status']=='COMPLETED' and t=='graph_revised':s['run_status']='ACTIVE'
    s['last_event_seq']=event['seq'];s['last_event_digest']=event['digest'];s['state_revision']=event['seq'];s['updated_at']=event['at']
    s['pending_provider_operations']=[k for k,o in s['operations'].items() if o['status'] in ('INTENT_RECORDED','REQUEST_SUBMITTED','REQUEST_ACCEPTED','RECONCILE_REQUIRED')]
    s['owners']={k:v['owner'] for k,v in s['tasks'].items() if v['owner'] is not None}
    s['completed_steps']=[k for k,v in s['tasks'].items() if v['status']=='COMPLETE']
    s['active_steps']=[k for k,v in s['tasks'].items() if v['status'] in ('RUNNING','CLAIMED','WAIT_EXTERNAL','WAIT_REVIEW')]
    s['evidence_refs']=[dict(artifact,task_id=k) for k,v in s['tasks'].items() for artifact in v['evidence']]
    return s

class RunStore:
    def __init__(self,root,graph=None):
        self.root=enforce_root(Path(root))
        self.run_data=json.loads((self.root/'run.json').read_text())
        ensure(self.run_data.get('schema_version')=='1.0.0','Unsupported run schema')
        self.run_id=self.run_data['run_id'];self.instance=self.root.parents[1]
        if self.run_data.get('graph_digest'):
            initial=self.instance/'graph-revisions'/(self.run_data['graph_revision']+'.yaml')
            ensure(initial.is_file() and digest(initial.read_bytes())==self.run_data['graph_digest'],
                   'Original pinned graph digest does not match immutable source')
        self.graph=graph or read_graph(self.instance,self.run_data.get('current_graph_revision',self.run_data['graph_revision']))
        ensure(isinstance(self.graph.get('nodes'),list),'Run graph missing nodes')
        self.node_map={n['id']:n for n in self.graph['nodes']}
        ensure(len(self.node_map)==len(self.graph['nodes']),'Duplicate graph node ID')

    @classmethod
    def create(cls,root,graph,run_id,actor,graph_revision='g0001'):
        root=enforce_root(Path(root));ensure(valid_actor(actor) and valid_id(run_id),'Invalid run identity')
        ensure(not (root/'run.json').exists(),'Existing run cannot be overwritten')
        root.mkdir(parents=True,exist_ok=True)
        data={'schema_version':'1.0.0','run_id':run_id,'instance_id':root.parents[1].name,
              'graph_revision':graph_revision,'trigger_kind':'manual','created_at':utcnow(),
              'created_by':actor,'mode':'standalone_single_writer','capabilities':{},
              'graph_digest':digest((root.parents[1]/'graph-revisions'/(graph_revision+'.yaml')).read_bytes())}
        atomic_write(root/'run.json',jsonbytes(data));atomic_write(root/'events.jsonl',b'')
        store=cls(root,graph)
        store.append('run_created',actor,payload={'source':'optional local helper'})
        return store

    def scan(self):
        """Read event bytes, verify the full accepted prefix; never assume state.json is canonical."""
        raw=(self.root/'events.jsonl').read_bytes() if (self.root/'events.jsonl').exists() else b''
        state=init_state(self.run_id,read_graph(self.instance,self.run_data['graph_revision']) if self.run_data.get('current_graph_revision') else self.graph,self.run_data['graph_revision'])
        old_hash=GENESIS;legacy=False;good=0;error=None
        for line in raw.splitlines(keepends=True):
            if not line.endswith(b'\n'):
                error='Partial terminal JSONL line';break
            try:
                e=json.loads(line)
                ensure(e['seq']==state['last_event_seq']+1,'Event sequence gap/duplicate')
                ensure(e['run_id']==self.run_id,'Wrong run ID')
                ensure(valid_actor(e.get('actor')),'Event actor missing')
                ensure(e['graph_revision']==state['graph_revision'],'Wrong graph revision event')
                provided=e.pop('digest',None)
                prev=e.get('prev_digest')
                if prev is None:
                    legacy=True
                else:ensure(prev==old_hash,'Digest predecessor mismatch')
                computed=digest((old_hash+'\n'+canonical(e)).encode())
                if provided is not None:ensure(provided==computed,'Digest mismatch')
                elif prev is not None:raise StateError('Missing event digest')
                e['digest']=computed
                reduce_event(state,e)
                old_hash=computed;good+=len(line)
            except (Exception,) as exc:
                error=str(exc);break
        state['integrity_level']='advisory' if legacy else 'verified'
        # If a graph_rev event was committed but run.json pointer was not (crash),
        # resume from the event's pinned immutable revision, never a changing master.
        if not error and state['graph_revision']!=self.run_data.get('current_graph_revision',self.run_data['graph_revision']):
            revision=state['graph_revision']
            path=self.instance/'graph-revisions'/(revision+'.yaml')
            if not path.is_file():
                error='Revised graph file missing: '+revision
            else:
                change=next((x for x in reversed(self._events_from_valid_bytes(raw[:good]))
                             if x['type']=='graph_revised' and x.get('payload',{}).get('new_revision')==revision),None)
                if not change or change['payload'].get('graph_digest')!=digest(path.read_bytes()):
                    error='Revised graph digest mismatch: '+revision
                else:
                    self.graph=read_graph(self.instance,revision)
                    self.node_map={n['id']:n for n in self.graph['nodes']}
                    self.run_data['current_graph_revision']=revision
        self._compute_eligible(state)
        return state,raw[:good],raw[good:],error

    @staticmethod
    def _events_from_valid_bytes(data):
        return [json.loads(line) for line in data.splitlines() if line]

    def verified(self):
        state,_,tail,error=self.scan()
        if tail or error:raise CorruptLog('Event stream needs explicit repair: '+str(error))
        return state

    def append(self,event_type,actor,task_id=None,payload=None,evidence=None,attempt_id=None,context_checked=False):
        ensure(valid_actor(actor),'Actor provenance required')
        ensure(self.run_data.get('mode','standalone_single_writer')!='shared_coordinated',
               'Shared coordinated writes require an independently verified claim adapter (not provided here)')
        state=self.verified();ensure(not state['paused'] or event_type in ('run_resumed','run_cancelled','recovery_checked','checkpoint_created'),'Run is paused')
        ensure(state['run_status'] not in ('FAILED','CANCELLED','COMPLETED') or event_type in ('recovery_checked','checkpoint_created','handoff_updated','graph_revised'),'Run terminal')
        if event_type in ('task_ready','task_claimed','task_started'):
            ensure(task_id in self.node_map,'Unknown task')
            node=self.node_map[task_id]
            ensure(all(state['tasks'].get(dep,{}).get('status')=='COMPLETE' for dep in node.get('needs',[])),
                   'Task cannot bypass dependencies')
            ensure(context_checked or not (node.get('when') or node.get('join') or node.get('fanout') or node.get('skills')
                    or any(a in SIDE_EFFECTS for a in node.get('required_actions',[]))),
                   'Context-dependent work requires manual or independently authorized gate')
        if event_type=='task_completed':
            self._validate_outputs(task_id,evidence or [],state)
        event={'schema_version':'1.0.0','event_id':f'evt-{state["last_event_seq"]+1:06d}','seq':state['last_event_seq']+1,
          'run_id':self.run_id,'type':event_type,'at':utcnow(),'actor':actor,
          'graph_revision':state['graph_revision'],'evidence':evidence or [],'payload':payload or {},
          'prev_digest':state['last_event_digest']}
        if task_id:event['task_id']=task_id
        if attempt_id:event['attempt_id']=attempt_id
        event['digest']=digest((event['prev_digest']+'\n'+canonical({k:v for k,v in event.items() if k!='digest'})).encode())
        next_state=reduce_event(copy.deepcopy(state),copy.deepcopy(event))
        with (self.root/'events.jsonl').open('ab',buffering=0) as f:
            f.write((canonical(event)+'\n').encode());os.fsync(f.fileno())
        self._snapshot(next_state)
        return next_state

    def _compute_eligible(self,state):
        # Candidate readiness; verify that completed local evidence still matches its recorded digest.
        blocked=[];eligible=[]
        for tid,item in state['tasks'].items():
            if item['status']!='COMPLETE':continue
            for artifact in item.get('evidence',[]):
                if artifact.get('locator') and artifact.get('sha256'):
                    try:
                        file=safe_output(self.root,artifact['locator'])
                        intact=file.is_file() and digest(file.read_bytes())==artifact['sha256']
                    except (StateError,OSError):intact=False
                    if not intact:
                        item['status']='BLOCKED'
                        item['last_error']={'class':'stale_evidence','correction':'Reconcile the changed/missing artifact with an authorized revision; history remains intact'}
                        state['audit_warnings'].append('stale_evidence:'+tid+':'+artifact['locator'])
                        blocked.append({'task_id':tid,'reason':'Completed output missing or hash mismatch'})
                        break
        state['completed_steps']=[k for k,v in state['tasks'].items() if v['status']=='COMPLETE']
        if blocked and state['run_status']=='COMPLETED':state['run_status']='BLOCKED'
        by=self.node_map
        for tid,node in by.items():
            s=state['tasks'].get(tid,{})
            if s.get('status') not in ('WAIT_DEPENDENCY','READY'):continue
            if state['paused'] or state['run_status'] in ('FAILED','CANCELLED','COMPLETED'):continue
            if all(state['tasks'].get(dep,{}).get('status')=='COMPLETE' for dep in node.get('needs',[])):
                # Do not guess approval, skills, dynamic joins, predicates or provider truth.
                if node.get('when') or node.get('join') or node.get('fanout') or node.get('skills') or any(a in SIDE_EFFECTS for a in node.get('required_actions',[])):
                    blocked.append({'task_id':tid,'reason':'Context/approval/condition must be independently verified'})
                else:eligible.append(tid)
        state['eligible_tasks']=eligible;state['blocked_reasons']=blocked
        return state

    def _snapshot(self,state):
        self._compute_eligible(state)
        atomic_write(self.root/'state.json',jsonbytes(state))
        for tid,t in state['tasks'].items():
            attempt_id=t.get('last_attempt_id')
            if attempt_id:
                ensure(valid_id(tid) and valid_id(attempt_id),'Invalid attempt path')
                attempt=self.root/'tasks'/tid/'attempts'/(attempt_id+'.json')
                status='succeeded' if t['status']=='COMPLETE' else 'failed' if t['status']=='FAILED' else 'blocked' if t['status'] in ('BLOCKED','RECONCILE_REQUIRED','NEEDS_REWORK') else 'running'
                detail={'schema_version':'1.0.0','run_id':self.run_id,'task_id':tid,'attempt_id':attempt_id,
                    'graph_revision':t['graph_revision'],'actor':t.get('last_attempt_owner') or t.get('owner') or self.run_data['created_by'],
                    'started_at':t.get('started_at',self.run_data['created_at']), 'status':status,
                    'input_refs':[],'output_refs':t['evidence'],
                    'extensions':{'aosw':{'current_task_status':t['status'],'attempt_count':t['attempts'],
                    'error':t['last_error'],'retry':t['retry'],'derived_from_event_seq':state['last_event_seq']}}}
                atomic_write(attempt,jsonbytes(detail))

    def checkpoint(self,actor):
        state=self.verified();ident=f'checkpoint-{state["last_event_seq"]:06d}'
        cp={'schema_version':'1.0.0','checkpoint_id':ident,'run_id':self.run_id,
            'graph_revision':state['graph_revision'],'event_seq':state['last_event_seq'],
            'event_digest':state['last_event_digest'],'state_revision':state['state_revision'],
            'created_at':utcnow(),'created_by':actor,'integrity_level':state['integrity_level'],
            'completed_tasks':state['completed_steps'],'pending_tasks':[k for k in state['tasks'] if k not in state['completed_steps']],
            'blocked_tasks':[k for k,v in state['tasks'].items() if v['status'] in ('BLOCKED','RECONCILE_REQUIRED','FAILED')],
            'next_eligible_tasks':state['eligible_tasks'],
            'verified_artifacts':[{k:v for k,v in a.items() if k!='task_id'} for a in state['evidence_refs']],
            'provider_unknown_operations':state['pending_provider_operations'],'sync_status':'local_only'}
        dest=self.root/'checkpoints'/(ident+'.json')
        ensure(not dest.exists(),'Checkpoint already exists')
        atomic_write(dest,jsonbytes(cp))
        # Only append checkpoint_created after the checkpoint file is durably written.
        self.append('checkpoint_created',actor,payload={'checkpoint_id':ident,'event_seq':cp['event_seq'],'event_digest':cp['event_digest']})
        self.handoff(actor)
        return cp

    def handoff(self,actor):
        s=self.verified()
        data={'schema_version':'1.0.0','run_id':self.run_id,'graph_revision':s['graph_revision'],
              'last_event_seq':s['last_event_seq'],'last_event_digest':s['last_event_digest'],
              'checkpoint_id':s['checkpoints'][-1] if s['checkpoints'] else None,
              'generated_at':utcnow(),'prepared_by':actor,'completed':s['completed_steps'],
              'ready':s['eligible_tasks'],'active':s['active_steps'],'owners':s['owners'],
              'pending_approvals':[],'source_references':[],
              'blocked':s['blocked_reasons'],'pending_provider_reconciliations':s['pending_provider_operations'],
              'run_status':s['run_status'],'next_action':'Inspect eligible work and verify untrusted context; no automatic dispatch',
              'sync_status':'local_only'}
        atomic_write(self.root/'handoff.json',jsonbytes(data))
        body=(f'# AOS-W handoff — {self.run_id}\n\nGraph: {s["graph_revision"]}, event sequence: {s["last_event_seq"]}, '
             f'integrity: {s["integrity_level"]}, status: {s["run_status"]}.\n\n'
             f'Completed: {", ".join(s["completed_steps"]) or "none"}\n\n'
             f'Ready candidates (context check required): {", ".join(s["eligible_tasks"]) or "none"}\n\n'
             f'Active owners: {canonical(s["owners"])}\n\n'
             f'Pending provider operations: {", ".join(s["pending_provider_operations"]) or "none"}\n\n'
             'Only act with verified scope, current artifacts, permissions and claim capability.\n')
        atomic_write(self.root/'handoff.md',body.encode())
        return data

    def start(self,task_id,actor,context_checked=False):
        s=self.verified();ensure(task_id in self.node_map,'Unknown task')
        ensure(s['tasks'][task_id]['status'] in ('READY','WAIT_DEPENDENCY'),'Not startable')
        node=self.node_map[task_id]
        ensure(all(s['tasks'].get(dep,{}).get('status')=='COMPLETE' for dep in node.get('needs',[])),'Incomplete dependencies')
        ensure(context_checked or not (node.get('when') or node.get('join') or node.get('fanout') or node.get('skills') or any(a in SIDE_EFFECTS for a in node.get('required_actions',[]))),'Required context must be checked via manual gate')
        if s['tasks'][task_id]['status']!='READY':self.append('task_ready',actor,task_id,context_checked=context_checked)
        self.append('task_claimed',actor,task_id,context_checked=context_checked)
        attempt=f'attempt-{self.verified()["tasks"][task_id]["attempts"]+1:04d}'
        return self.append('task_started',actor,task_id,attempt_id=attempt,context_checked=context_checked)

    def _validate_outputs(self,task_id,output_refs,s):
        ensure(task_id in s['tasks'] and s['tasks'][task_id]['status'] in ('RUNNING','WAIT_REVIEW'),'Task not running')
        node=self.node_map[task_id];need={x['artifact_id']:x for x in node.get('outputs',[]) if x.get('required',True)}
        good={}
        for a in output_refs:
            name=a.get('artifact_id');ensure(name in {o['artifact_id'] for o in node.get('outputs',[])},'Undeclared output')
            expected=next(o for o in node['outputs'] if o['artifact_id']==name)
            ensure(a.get('locator')==expected['path'],'Output locator differs from contract')
            f=safe_output(self.root,a['locator']);ensure(f.is_file(),'Missing artifact '+a['locator'])
            ensure(a.get('sha256')==digest(f.read_bytes()),'Artifact SHA-256 mismatch')
            ensure(bool(a.get('revision')),'Artifact revision missing');good[name]=a
        ensure(need.keys()<=good.keys(),'Required evidence missing')
        if node.get('quality',{}).get('gates'):
            review=s['tasks'][task_id].get('review') or {}
            ensure(s['tasks'][task_id]['status']=='WAIT_REVIEW' and review.get('verdict')=='PASS','Required quality gate not passed')
            expected={(x['artifact_id'],x['sha256'],x['revision']) for x in output_refs}
            received={(x.get('artifact_id'),x.get('sha256'),x.get('revision')) for x in review.get('artifacts',[])}
            ensure(expected<=received, 'Accepted review does not bind current artifact revision/hash')
        return True

    def complete(self,task_id,actor,output_refs):
        self._validate_outputs(task_id,output_refs,self.verified())
        return self.append('task_completed',actor,task_id,evidence=output_refs)

    def fail(self,task_id,actor,error_class,correction,policy=None):
        s=self.verified();t=s['tasks'].get(task_id);ensure(t and t['status'] in ('RUNNING','WAIT_REVIEW','WAIT_EXTERNAL'),'Not active')
        rule=policy or self.node_map[task_id].get('retry',{'max_attempts':1,'on':[],'backoff':'manual'})
        cap=rule.get('max_attempts',1);can=error_class in rule.get('on',[]) and t['attempts']<cap
        waiting=None
        if can and rule.get('backoff') in ('fixed','exponential'):
            delay=rule.get('delay_seconds',60)
            if rule['backoff']=='exponential':delay*=2**max(0,t['attempts']-1)
            waiting=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(seconds=delay)).isoformat(timespec='seconds').replace('+00:00','Z')
        retry={'eligible':can,'next_eligible_at':waiting,'max_attempts':cap,'attempts':t['attempts'],'error_class':error_class,'manual_approval_required':error_class in ('review_revise','incomplete_evidence','human_intervention')}
        return self.append('task_failed',actor,task_id,payload={'error_class':error_class,'correction':correction,'retry':retry,'terminal':not can})

    def retry(self,task_id,actor,approval=False,now=None):
        s=self.verified();q=s['tasks'].get(task_id);ensure(q is not None,'Unknown task')
        ensure(q['status'] in ('BLOCKED','NEEDS_REWORK','FAILED'),'Not retryable')
        rr=q.get('retry');ensure(rr and rr['eligible'],'Retry exhausted or unauthorized')
        if rr['manual_approval_required']:ensure(approval,'Manual review of correction required')
        if rr['next_eligible_at']:
            ensure(stamp(now or utcnow())>=stamp(rr['next_eligible_at']),'Retry delay not elapsed')
        ensure(not any(o['task_id']==task_id and o['status'] in ('INTENT_RECORDED','REQUEST_SUBMITTED','REQUEST_ACCEPTED','RECONCILE_REQUIRED') for o in s['operations'].values()),'Unreconciled external operation')
        return self.append('task_requeued',actor,task_id,payload={'reason':'Explicit retry after correction/reconciliation'})

    def operation_key(self,task_id,provider,resource,request,retry_reference=None):
        ensure(all(isinstance(x,str) and x for x in (task_id,provider,resource)),'Missing operation identity')
        return 'op-'+digest(canonical({'run':self.run_id,'task':task_id,'provider':provider,'resource':resource,'request':request,'retry_reference':retry_reference}).encode())[:40]

    def operation_intent(self,task_id,actor,provider,resource,request,approval_id,retry_reference=None):
        # **Never performs** external provider requests. Requires caller-verified approval ID.
        key=self.operation_key(task_id,provider,resource,request,retry_reference)
        p={'operation_key':key,'provider':provider,'resource':resource,'request_digest':digest(canonical(request).encode()),'approval_id':approval_id}
        if retry_reference:p['retry_reference']=retry_reference
        return self.append('operation_intent',actor,task_id,payload=p)

    def revise(self,new_revision,new_yaml_bytes,actor,approval):
        """Applies a pre-approved graph revision; records immutable graph and invalidation event.

        Does not mutate history or perform provider actions. Owner approval text is not authenticated.
        """
        s=self.verified();ensure(valid_id(new_revision) and new_revision!=s['graph_revision'],'New graph revision required')
        ensure(approval.get('decision')=='GRANTED' and approval.get('action')=='revise_graph'
               and approval.get('base_revision')==s['graph_revision'] and approval.get('approval_id'),'Scoped revision approval required')
        import yaml # optional helper only
        content=yaml.safe_load(new_yaml_bytes)
        next_graph=content.get('graph',content)
        from pathlib import Path as P
        # Isolated import from adjacent optional helper; runtime-independent manual procedure remains available.
        import sys
        sys.path.insert(0,str(P(__file__).resolve().parents[1]/'composition'))
        from composition import validate_graph,revision_impact
        validate_graph(next_graph,strict=True)
        impact=revision_impact(self.graph,next_graph,s['tasks'],approval={'decision':'GRANTED','action':'revise_graph'})
        ensure(not any(s['tasks'][nid]['status'] in ('RUNNING','CLAIMED','WAIT_EXTERNAL','RECONCILE_REQUIRED') for nid in impact['invalidated'] if nid in s['tasks']),'Cannot revise active/ambiguous task')
        target=self.instance/'graph-revisions'/(new_revision+'.yaml')
        ensure(not target.exists(),'Graph revision exists')
        ensure(target.resolve().is_relative_to(self.instance.resolve()),'Graph path traversal')
        atomic_write(target,new_yaml_bytes)
        graph_digest=digest(new_yaml_bytes)
        payload={'base_revision':s['graph_revision'],'new_revision':new_revision,'graph_digest':graph_digest,
                 'remaining_nodes':[n['id'] for n in next_graph['nodes']],
                 'approval_id':approval['approval_id'],'changed':impact['changed'],'invalidated':impact['invalidated'],
                 'new_nodes':[k for k in {n['id'] for n in next_graph['nodes']} if k not in s['tasks']],
                 'preserved':impact['preserved']}
        updated=self.append('graph_revised',actor,payload=payload)
        self.graph=next_graph;self.node_map={n['id']:n for n in next_graph['nodes']}
        self.run_data['current_graph_revision']=new_revision
        atomic_write(self.root/'run.json',jsonbytes(self.run_data))
        inst_file=self.instance/'instance.json'
        if inst_file.exists():
            inst=json.loads(inst_file.read_text());inst['current_graph_revision']=new_revision;atomic_write(inst_file,jsonbytes(inst))
        self._snapshot(updated);self.handoff(actor)
        return payload

    def _checkpoint_issues(self,valid_prefix):
        digest_map={}
        recorded=set()
        for line in valid_prefix.splitlines():
            e=json.loads(line);digest_map[e['seq']]=e.get('digest')
            if e['type']=='checkpoint_created':recorded.add(e.get('payload',{}).get('checkpoint_id'))
        issues=[]
        for p in sorted((self.root/'checkpoints').glob('*.json')):
            try:
                cp=json.loads(p.read_text())
                seq=cp['event_seq']
                if seq not in digest_map or (cp.get('event_digest') and cp['event_digest']!=digest_map[seq]):
                    issues.append('invalid_checkpoint_anchor:'+p.name)
                elif cp.get('checkpoint_id') not in recorded:
                    issues.append('orphan_checkpoint_without_event:'+p.name)
            except (OSError,KeyError,ValueError):
                issues.append('unreadable_checkpoint:'+p.name)
        return issues

    def recover(self,actor,repair_tail=False):
        state,valid,tail,error=self.scan()
        issues=list(state.get('audit_warnings',[]))
        if tail and not repair_tail:
            raise CorruptLog('Explicit repair required; no journal modification: '+str(error))
        if error and not tail:
            raise CorruptLog('Missing or altered graph/checkpoint source: '+str(error))
        issues.extend(self._checkpoint_issues(valid))
        if self.run_data.get('current_graph_revision',self.run_data['graph_revision'])!=json.loads((self.root/'run.json').read_text()).get('current_graph_revision',self.run_data['graph_revision']):
            path=self.root/'run.json'
            atomic_write(self.root/'recovery'/('run-pointer-before-'+utcnow().replace(':','-')+'.json'),path.read_bytes())
            atomic_write(path,jsonbytes(self.run_data))
            issues.append('reconciled_graph_pointer_from_verified_event')
        if tail or error:
            issues.append('corrupt_or_partial_tail: '+str(error))
            quarantine=self.root/'recovery'/('corrupt-tail-'+digest(tail)[:24]+'.bin')
            ensure(not quarantine.exists(),'Tail already quarantined')
            atomic_write(quarantine,tail)
            # Accepted prefix remains byte-for-byte intact; discarded suspect tail retained in recovery/.
            atomic_write(self.root/'events.jsonl',valid)
        file=self.root/'state.json'
        try: snapshot=json.loads(file.read_text())
        except (OSError,ValueError):snapshot=None
        if not snapshot or snapshot.get('last_event_seq')!=state['last_event_seq'] or snapshot.get('last_event_digest')!=state['last_event_digest'] or snapshot.get('tasks')!=state['tasks'] or snapshot.get('run_status')!=state['run_status']:
            issues.append('stale_or_inconsistent_state')
            if file.exists():atomic_write(self.root/'recovery'/('snapshot-before-'+utcnow().replace(':','-')+'.json'),file.read_bytes())
            self._snapshot(state)
        self.append('recovery_checked',actor,payload={'issues':issues,'repair_tail':bool(tail and repair_tail)})
        self.handoff(actor)
        return issues


def inspect_child_batch(agent_files, proposals):
    """Read-only detection of incomplete Prompt 10 fan-out after a crash.

    Does not create, repair or delete any child; explicit authorization/recovery required.
    """
    root=Path(agent_files).resolve(strict=True)
    ensure(root.name=='agent-files','Child root must be agent-files')
    results=[]
    for row in proposals.get('proposals',[]):
        ident=row['instance_id'];run_id=row['run_id']
        ensure(valid_id(ident) and valid_id(run_id),'Unsafe child identity')
        child=root/'instances'/ident
        if not child.exists():status='MISSING'
        elif child.is_symlink() or not child.resolve().is_relative_to(root):status='UNSAFE'
        else:
            files=['instance.json','template-lock.json',f'runs/{run_id}/run.json',
                   f'runs/{run_id}/events.jsonl',f'runs/{run_id}/state.json']
            missing=[f for f in files if not (child/f).is_file()]
            if missing:status='PARTIAL'
            else:
                try:
                    instance=json.loads((child/'instance.json').read_text())
                    run=json.loads((child/'runs'/run_id/'run.json').read_text())
                    status='INITIALIZED' if instance['instance_id']==ident and run['run_id']==run_id else 'CONFLICT'
                except (ValueError,KeyError):status='CONFLICT'
        results.append({'child_id':ident,'status':status,'action':
            'Inspect and reconcile original directory; do not recreate or overwrite'
            if status in ('PARTIAL','CONFLICT','UNSAFE') else
            'No child exists; owner authorization required before creating' if status=='MISSING'
            else 'Inspect actual run event/checkpoint before continuing'})
    return {'plan_id':proposals.get('plan_id'),'results':results,
            'all_initialized':all(x['status']=='INITIALIZED' for x in results)}
