"""Optional AOS-W governance adapter for local single-writer file-based runs.

NOT authentication or a sandbox. File records are self-asserted and host processes can
bypass them; enforce real privileges and atomic claims at host/provider boundary.
No network, messaging, ad activation, account writes, scheduler or background loop.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'state'))
from state import RunStore, StateError, Unauthorized, atomic_write, canonical, digest, utcnow, valid_actor, valid_id, safe_output, stamp

SENSITIVE = {'stage_paused','edit_crm','deploy_dev','deploy_prod','activate_live','change_budget','send_message','emit_conversion'}
AUDIT_ROLE = {'owner','human-approver','human-reviewer'}
ALLOWED_GATES = {'deterministic','ai_independent','human','self_review'}
VERDICTS = {'PASS','REVISE','INSUFFICIENT_EVIDENCE','BLOCKED'}

def require(ok, text):
    if not ok: raise Unauthorized(text)

def identity(actor):
    require(valid_actor(actor),'Four-field [Agent | Platform | Role | Instance] provenance required')
    return tuple(actor[k].strip() for k in ('agent','platform','role','instance'))

def same_agent(a,b):
    return tuple(a[k].strip() for k in ('agent','platform','instance')) == tuple(b[k].strip() for k in ('agent','platform','instance'))

def identity_string(actor):
    return '['+' | '.join(identity(actor))+']'

def utc_parse(value):
    try:
        parsed=stamp(value)
        require(parsed.tzinfo is not None,'Timezone-aware timestamp required')
        return parsed
    except (TypeError,ValueError,AttributeError) as exc:
        raise Unauthorized('Invalid timezone-aware timestamp') from exc

def checked_id(value):
    require(valid_id(value),'Invalid record identifier')
    return value

def exact_artifacts(runroot, artifacts, expected):
    """Match *complete*, not subset, current file hashes and revisions."""
    require(isinstance(artifacts,list),'Artifact set must be explicit')
    declared={o['artifact_id']:o for o in expected if o.get('required',True)}
    seen={}
    for x in artifacts:
        name=x.get('artifact_id'); require(checked_id(name) not in seen, 'Duplicate artifact ID')
        require(name in declared, 'Unexpected artifact ID '+name)
        require(x.get('revision') and x.get('sha256') and x.get('locator')==declared[name]['path'],
                'Artifact path/version/hash required')
        f=safe_output(runroot,x['locator'])
        require(f.is_file() and digest(f.read_bytes())==x['sha256'], 'Artifact missing or digest changed')
        seen[name]=x
    require(set(seen)==set(declared),'Incomplete current required artifact set')
    return sorted((x['artifact_id'],x['locator'],x['revision'],x['sha256']) for x in seen.values())

class Governance:
    """Cooperative local adapter: permissions/QC bind actual run/graph/version/artifact evidence."""
    def __init__(self, runroot, effective_policy=None, gate_definitions=None):
        self.store=RunStore(runroot)
        self.root=self.store.root
        self.policy=effective_policy if effective_policy is not None else self._effective_policy()
        self.gates={g['gate_id']:g for g in (gate_definitions if gate_definitions is not None else self._template_gates())}
        require(isinstance(self.policy,dict),'Missing effective policy')
        # An executing agent may write only under a real run path inside agent-files.
        for name in ('claims','reviews','approvals','handoffs'):(self.root/name).mkdir(exist_ok=True)
    def _template(self):
        # Use the *pinned* graph revision, never the latest mutable master.
        p=self.store.instance/'graph-revisions'/(self.store.verified()['graph_revision']+'.yaml')
        import yaml  # optional validator adapter only; file protocol works without it
        return yaml.safe_load(p.read_text())
    def _effective_policy(self):
        data=self._template()
        return data.get('policy',{'autonomy':'bounded','allowed_actions':['read','research','write_local','review'],
          'human_required_actions':list(SENSITIVE),'default_gates':[],'max_parallel_tasks':1,'allow_dynamic_children':False})
    def _template_gates(self):
        return self._template().get('gates',[])
    def _record(self,folder,key,data):
        checked_id(key)
        location=self.root/folder/(key+'.json')
        require(not location.exists(),'Append-only record already exists: '+key)
        atomic_write(location,(json.dumps(data,indent=2,sort_keys=True)+'\n').encode())
        return location
    def _read_records(self,folder):
        result=[]
        for f in sorted((self.root/folder).glob('*.json')):
            try:
                record=json.loads(f.read_text(encoding='utf-8'))
            except (OSError,ValueError) as exc:
                raise Unauthorized('Invalid '+folder+' record '+f.name) from exc
            if folder in ('claims','reviews','approvals'):
                k=record.get('claim_id') if folder=='claims' else record.get('approval_id') if folder=='approvals' else record.get('review_id',record.get('record_id'))
                g=self.store.verified().get('governance',{})
                bucket=('claims' if folder=='claims' else 'permissions' if folder=='approvals' else
                        'remediation' if record.get('status')=='OPEN' else 'reviews')
                stored=g.get(bucket,{}).get(k)
                require(stored is not None and stored.get('record')==record,
                        'Governance record not bound to verified event history: '+f.name)
            result.append(record)
        return result
    def _now(self,when=None):return utc_parse(when or utcnow())
    def _graph(self):return self.store.verified()['graph_revision']
    def _node(self,task):
        require(checked_id(task) in self.store.node_map, 'Task unknown')
        return self.store.node_map[task]
    def _owner_role(self,actor):
        identity(actor)
        require(actor['role'] in ('owner','human-approver'),'Human owner/approver declaration required; host must independently authenticate')
    def _record_event(self,event_type,actor,task_id,record_id,data):
        self.store.append(event_type,actor,task_id=task_id,payload={'record_id':record_id,'record':data})

    def grant(self,approval_id,issuer,actions,resources,task_id=None,expires_at=None,
              artifact_refs=None,limits=None,exclusions=None,reason=None,issued_at=None):
        self._owner_role(issuer)
        checked_id(approval_id)
        require(actions and all(isinstance(x,str) for x in actions),'Explicit approved action class required')
        require(isinstance(resources,list) and resources and all(isinstance(r,str) and r for r in resources),
                'Approval must enumerate specific resources')
        require(not set(resources).intersection({'*','all'}),'No wildcard resource grants')
        graph=self._graph();policy_allowed=set(self.policy.get('allowed_actions',[]))
        require(set(actions).issubset(policy_allowed),'Cannot expand workflow permission ceiling')
        if task_id:self._node(task_id)
        created=issued_at or utcnow()
        if expires_at:require(utc_parse(expires_at)>utc_parse(created),'Approval already expired')
        for x in artifact_refs or []:require(x.get('revision') and x.get('sha256'),'Artifact-bound approval needs revisions and hashes')
        record={'schema_version':'1.0.0','approval_id':approval_id,'run_id':self.store.run_id,
                'issuer':issuer,'decision':'GRANTED','actions':sorted(set(actions)),
                'resource_ids':sorted(set(resources)), 'excluded_resource_ids':sorted(set(exclusions or [])),
                'task_id':task_id,'graph_revision':graph,'artifacts':artifact_refs or [],
                'limits':limits or {},'issued_at':created,'reason':reason or 'Explicit scoped owner approval',
                'expires_at':expires_at,'extensions':{'security_level':'cooperative_no_authentication'}}
        self._record('approvals',approval_id,record)
        self._record_event('permission_granted',issuer,task_id,approval_id,record)
        return record

    def revoke(self,approval_id,revocation_id,issuer,reason):
        self._owner_role(issuer)
        checked_id(revocation_id)
        approvals={a.get('approval_id'):a for a in self._read_records('approvals') if a.get('decision')=='GRANTED'}
        require(approval_id in approvals,'Approval not found')
        require(bool(reason and reason.strip()),'Revocation reason required')
        rec={'schema_version':'1.0.0','approval_id':revocation_id,'supersedes_id':approval_id,
             'run_id':self.store.run_id,'issuer':issuer,'decision':'REVOKED',
             'actions':approvals[approval_id]['actions'],'resource_ids':approvals[approval_id]['resource_ids'],
             'issued_at':utcnow(),'reason':reason,'extensions':{'cooperative':True}}
        self._record('approvals',revocation_id,rec)
        self._record_event('permission_revoked',issuer,None,revocation_id,rec)
        return rec

    def authorize(self,actor,action,resources,task_id=None,artifact_refs=None,amount=None,now=None):
        identity(actor)
        require(action in self.policy.get('allowed_actions',[]),'Action is outside workflow permission ceiling')
        if task_id:
            node=self._node(task_id)
            require(action in node.get('required_actions',[]),'Action outside step execution contract')
        require(isinstance(resources,list) and bool(resources) and not set(resources).intersection({'*','all'}),'Requested resources must be explicit')
        if action=='change_budget':require(amount is not None,'Budget change needs an explicit amount')
        if action not in SENSITIVE and action not in self.policy.get('human_required_actions',[]):
            return {'status':'ROUTINE_AUTHORIZED','action':action,'resources':resources,'policy':'bounded'}
        if artifact_refs:
            for a in artifact_refs:
                require(a.get('locator') and a.get('sha256') and a.get('revision'),
                        'Version-bound authorization needs complete artifact reference')
                f=safe_output(self.root,a['locator'])
                require(f.is_file() and digest(f.read_bytes())==a['sha256'],
                        'Authorization input artifact is missing or changed')
        gr=self._graph();time=self._now(now)
        approvals=self._read_records('approvals')
        revoked={x['supersedes_id'] for x in approvals if x.get('decision')=='REVOKED' and x.get('supersedes_id')}
        for a in approvals:
            if a.get('decision')!='GRANTED' or a.get('approval_id') in revoked or a.get('graph_revision')!=gr:continue
            if a.get('task_id') not in (None,task_id):continue
            if action not in a['actions'] or not set(resources).issubset(a['resource_ids']):continue
            if set(resources).intersection(a.get('excluded_resource_ids',[])):continue
            if a.get('expires_at') and time>=utc_parse(a['expires_at']):continue
            if time<utc_parse(a['issued_at']):continue
            if amount is not None:
                limit=a.get('limits',{}).get('max_amount')
                if limit is None or amount>limit:continue
            bound=a.get('artifacts',[])
            if bound:
                if not artifact_refs:continue
                incoming={(x['artifact_id'],x['revision'],x['sha256']) for x in artifact_refs}
                expected={(x['artifact_id'],x['revision'],x['sha256']) for x in bound}
                if incoming!=expected:continue
            return {'status':'APPROVED_COOPERATIVELY','approval_id':a['approval_id'],'action':action,
                    'resources':resources,'security_level':'record_check_not_authentication'}
        raise Unauthorized('No valid in-scope, nonexpired, unrevoked action authorization')

    def _can_start(self,task_id,actor,resources=None):
        node=self._node(task_id);s=self.store.verified()
        require(not s['paused'] and s['run_status'] not in ('FAILED','CANCELLED','COMPLETED'), 'Run not startable')
        require(s['tasks'][task_id]['status'] in ('WAIT_DEPENDENCY','READY'),'Task not ready')
        for d in node.get('needs',[]):
            require(s['tasks'].get(d,{}).get('status')=='COMPLETE','Unfinished dependency '+d)
        require(not (node.get('when') or node.get('join') or node.get('fanout')),
                'Conditional/join/fanout needs additional explicit verified context')
        require(not node.get('skills'),'Step skills require separate trusted just-in-time resolver')
        required=set(node.get('required_actions',[]))
        for action in required:
            request_resources=resources if action in SENSITIVE else [task_id]
            self.authorize(actor,action,request_resources,task_id=task_id)
        return True

    def claim(self,claim_id,task_id,actor,expires_at,resources=None,now=None):
        identity(actor);checked_id(claim_id)
        self._can_start(task_id,actor,resources)
        start=self._now(now);expiry=utc_parse(expires_at)
        require(expiry>start,'Claim must expire in future')
        records=self._read_records('claims')
        released={r.get('supersedes_id') for r in records if r.get('status')=='released'}
        for rec in records:
            if rec.get('task_id')==task_id and rec.get('status')=='active' and rec.get('claim_id') not in released:
                # Expiry by itself does NOT allow takeover, even locally.
                raise Unauthorized('Existing claim, including expired/stale, needs explicit reconciliation')
        s=self.store.verified()
        active=sum(q.get('status') in ('CLAIMED','RUNNING','WAIT_REVIEW','WAIT_EXTERNAL') for q in s['tasks'].values())
        require(active<int(self.policy.get('max_parallel_tasks',1)),
                'Workflow parallel execution ceiling reached')
        record={'schema_version':'1.0.0','claim_id':claim_id,'run_id':self.store.run_id,
                'task_id':task_id,'actor':actor,'resources':resources or [task_id],
                'mode':'advisory','acquired_at':start.isoformat(),
                'expires_at':expiry.isoformat(),'base_state_revision':s['state_revision'],
                'progress':'Task awaiting start','status':'active',
                'extensions':{'lease_guarantee':'none','enforcement':'single_cooperating_writer'}}
        self._record('claims',claim_id,record)
        self._record_event('claim_recorded',actor,task_id,claim_id,record)
        if s['tasks'][task_id]['status']=='WAIT_DEPENDENCY':
            self.store.append('task_ready',actor,task_id,context_checked=True)
        self.store.append('task_claimed',actor,task_id,context_checked=True)
        return record

    def _claim_for(self,task_id,actor):
        a=identity(actor)
        rec=[x for x in self._read_records('claims') if x.get('task_id')==task_id and x.get('status')=='active']
        releases={x.get('supersedes_id') for x in self._read_records('claims') if x.get('status')=='released'}
        rec=[x for x in rec if x.get('claim_id') not in releases]
        require(len(rec)==1 and identity(rec[0]['actor'])==a,'Active claim owned by current actor required')
        require(utc_parse(rec[0]['expires_at'])>self._now(),'Claim expired; reconcile before work')
        return rec[0]

    def begin(self,task_id,actor):
        claim=self._claim_for(task_id,actor)
        require(self.store.verified()['tasks'][task_id]['status']=='CLAIMED','Task not claimed')
        # A grant valid at claim time may have been revoked, expired or superseded
        # before task start. Re-check action scope at the action boundary.
        for action in self._node(task_id).get('required_actions',[]):
            self.authorize(actor,action,claim['resources'] if action in SENSITIVE else [task_id],task_id=task_id)
        attempt=f'attempt-{self.store.verified()["tasks"][task_id]["attempts"]+1:04d}'
        self.store.append('task_started',actor,task_id,attempt_id=attempt,context_checked=True)
        return {'claim_id':claim['claim_id'],'task_id':task_id,'attempt_id':attempt}

    def release(self,claim_id,release_id,actor,reason):
        checked_id(release_id);identity(actor)
        claim=next((r for r in self._read_records('claims') if r.get('claim_id')==claim_id and r.get('status')=='active'),None)
        require(claim and identity(claim['actor'])==identity(actor),'Only owning actor can release advisory claim')
        require(reason and reason.strip(),'Release reason required')
        rec={'schema_version':'1.0.0','claim_id':release_id,'supersedes_id':claim_id,'run_id':self.store.run_id,
             'task_id':claim['task_id'],'actor':actor,'mode':'advisory','acquired_at':utcnow(),
             'status':'released','reason':reason}
        self._record('claims',release_id,rec)
        self._record_event('claim_released',actor,claim['task_id'],release_id,rec)
        return rec

    def operation_intent(self,task_id,actor,action,resources,provider,resource,request,
                         amount=None,artifact_refs=None,retry_reference=None):
        """Validate saved cooperative authorization before recording provider intent.

        NO provider request is performed. Host must authenticate owner before actual send.
        """
        require(resource in resources,'Operation resource not in approved target set')
        self._claim_for(task_id,actor)
        require(self.store.verified()['tasks'][task_id]['status']=='RUNNING', 'Task not running')
        decision=self.authorize(actor,action,resources,task_id=task_id,
                                artifact_refs=artifact_refs,amount=amount)
        require(decision.get('approval_id'),'External operation requires explicit approval record')
        return self.store.operation_intent(task_id,actor,provider,resource,request,
                                           decision['approval_id'],retry_reference=retry_reference)

    def _gates_for(self,task_id):
        node=self._node(task_id)
        ids=list(dict.fromkeys((self.policy.get('default_gates') or []) + node.get('quality',{}).get('gates',[])))
        gates=[]
        for k in ids:
            require(k in self.gates,'Undefined quality gate '+k)
            gate=self.gates[k]
            require(gate.get('kind') in ALLOWED_GATES,'Unsupported quality gate '+k)
            gates.append(gate)
        return gates

    def submit_review(self,task_id,actor):
        self._claim_for(task_id,actor)
        require(self.store.verified()['tasks'][task_id]['status']=='RUNNING','Must run before review')
        self.store.append('task_submitted_review',actor,task_id)

    def _review_artifacts(self,task_id,artifacts):
        return exact_artifacts(self.root,artifacts,self._node(task_id).get('outputs',[]))

    def review(self,review_id,task_id,producer,reviewer,gate_id,artifacts,verdict,
               findings=None,rubric_revision='1',correction=None):
        identity(producer);identity(reviewer);checked_id(review_id)
        require(verdict in VERDICTS,'Unsupported review verdict')
        state=self.store.verified()
        require(state['tasks'][task_id]['status']=='WAIT_REVIEW','Task not submitted for review')
        require(identity(producer)==identity(state['tasks'][task_id]['last_attempt_owner']),
                'Submitted producer identity differs from current attempt')
        gate=next((g for g in self._gates_for(task_id) if g['gate_id']==gate_id),None)
        require(gate is not None,'Gate not required by this step')
        kind=gate['kind']
        if kind=='ai_independent':require(not same_agent(producer,reviewer), 'Independent AI reviewer must differ from producer')
        if kind=='human':require(reviewer['role'] in AUDIT_ROLE and not same_agent(producer,reviewer),
                                  'Separate declared human reviewer required')
        if kind=='self_review':require(same_agent(producer,reviewer), 'Self-review only by producer')
        if kind=='deterministic':
            require(reviewer['role'] in ('validator','deterministic-validator'),'Deterministic gate needs validator actor')
            # Artifact digest verification is automatic; this is not subjective proof of semantic fitness.
        refs=self._review_artifacts(task_id,artifacts)
        if verdict!='PASS':require(correction and correction.strip(),'Failed gate requires concrete correction instructions')
        record={'schema_version':'1.0.0','review_id':review_id,'run_id':self.store.run_id,
                'task_id':task_id,'gate_id':gate_id,'rubric_id':gate.get('rubric_id',gate_id),
                'rubric_revision':rubric_revision,'graph_revision':state['graph_revision'],
                'producer':producer,'reviewer':reviewer,'independent_required':kind in ('human','ai_independent'),
                'artifacts':artifacts,'required_artifact_ids':[a[0] for a in refs],
                'verdict':verdict,'findings':findings or [],'created_at':utcnow(),
                'correction':correction,'attempt_id':state['tasks'][task_id]['last_attempt_id'],
                'extensions':{'kind':kind,'source':'self_attestation_no_host_authentication'}}
        self._record('reviews',review_id,record)
        self._record_event('quality_recorded',reviewer,task_id,review_id,record)
        if verdict!='PASS':
            fix_id='remediation-'+review_id
            remediation={'schema_version':'1.0.0','record_id':fix_id,'run_id':self.store.run_id,
                         'task_id':task_id,'source_review_id':review_id,'correction':correction,
                         'required_new_attempt':True,'status':'OPEN','created_at':utcnow(),
                         'actor':reviewer,'graph_revision':state['graph_revision']}
            self._record('reviews',fix_id,remediation)
            self._record_event('remediation_requested',reviewer,task_id,fix_id,remediation)
            attempts=state['tasks'][task_id]['attempts']
            rule=self._node(task_id).get('retry',{'max_attempts':3,'on':['review_revise'],'backoff':'manual'})
            allowed=attempts<rule.get('max_attempts',3)
            payload={'verdict':'REVISE','review_id':review_id,'correction':correction,'rubric_version':rubric_revision,
                     'artifacts':artifacts,'retry':{'eligible':allowed,'attempts':attempts,
                     'max_attempts':rule.get('max_attempts',3),'manual_approval_required':True,'next_eligible_at':None}}
            self.store.append('review_revise',reviewer,task_id,payload=payload)
        return record

    def waive_review(self,review_id,task_id,producer,owner,gate_id,artifacts,reason,expires_at=None):
        """Explicit owner waiver; never label waived gate as evidence PASS."""
        identity(producer);self._owner_role(owner);checked_id(review_id)
        gate=next((g for g in self._gates_for(task_id) if g['gate_id']==gate_id),None)
        require(gate is not None and gate.get('waivable') is True and gate.get('kind')!='human',
                'Gate is not owner-waivable')
        require(bool(reason and reason.strip()),'Waiver needs rationale')
        st=self.store.verified();item=st['tasks'][task_id]
        require(item['status']=='WAIT_REVIEW','Waiver only for submitted current attempt')
        require(same_agent(producer,item['last_attempt_owner']),'Waiver producer mismatch')
        require(not same_agent(producer,owner),'Owner waiver must be separate from producer')
        refs=self._review_artifacts(task_id,artifacts)
        if expires_at:require(utc_parse(expires_at)>self._now(),'Expired waiver invalid')
        rec={'schema_version':'1.0.0','review_id':review_id,'run_id':self.store.run_id,
             'task_id':task_id,'gate_id':gate_id,'rubric_id':gate.get('rubric_id',gate_id),
             'rubric_revision':gate.get('rubric_revision','1'),'graph_revision':st['graph_revision'],
             'producer':producer,'reviewer':owner,'independent_required':True,
             'artifacts':artifacts,'required_artifact_ids':[x[0] for x in refs],
             'verdict':'WAIVED_BY_OWNER','findings':[reason],'created_at':utcnow(),
             'attempt_id':item['last_attempt_id'],'expires_at':expires_at,
             'extensions':{'waiver_reason':reason,'cooperative':True}}
        self._record('reviews',review_id,rec)
        self._record_event('quality_recorded',owner,task_id,review_id,rec)
        return rec

    def _passed_reviews(self,task_id,artifacts):
        s=self.store.verified();node=self._node(task_id)
        refs=self._review_artifacts(task_id,artifacts)
        attempt=s['tasks'][task_id]['last_attempt_id']
        found={}
        for r in self._read_records('reviews'):
            if r.get('task_id')!=task_id or r.get('verdict') not in ('PASS','WAIVED_BY_OWNER'):continue
            if r.get('graph_revision')!=s['graph_revision'] or r.get('attempt_id')!=attempt:continue
            current=sorted((x['artifact_id'],x['locator'],x['revision'],x['sha256']) for x in r['artifacts'])
            if current==refs:
                if r['verdict']=='WAIVED_BY_OWNER':
                    gate=self.gates.get(r['gate_id'],{})
                    if not gate.get('waivable') or (r.get('expires_at') and self._now()>=utc_parse(r['expires_at'])):continue
                found[r['gate_id']]=r
        gates=self._gates_for(task_id)
        require(all(g['gate_id'] in found for g in gates),'Every current required quality gate must pass')
        return [found[g['gate_id']] for g in gates]

    def finalize(self,task_id,actor,artifacts):
        self._claim_for(task_id,actor)
        state=self.store.verified();require(state['tasks'][task_id]['status'] in ('RUNNING','WAIT_REVIEW'), 'Task not active')
        gates=self._gates_for(task_id)
        if gates:
            require(state['tasks'][task_id]['status']=='WAIT_REVIEW','Quality review submission required')
            passed=self._passed_reviews(task_id,artifacts)
            last={'verdict':'PASS','review_id':'aggregate-'+task_id+'-'+state['tasks'][task_id]['last_attempt_id'],
                  'artifacts':artifacts,'rubric_version':'composite-current',
                  'gate_review_ids':[x['review_id'] for x in passed],
                  'waived_gate_ids':[x['gate_id'] for x in passed if x['verdict']=='WAIVED_BY_OWNER'],
                  'quality_outcome':'ACCEPTED_WITH_WAIVER' if any(x['verdict']=='WAIVED_BY_OWNER' for x in passed) else 'PASS'}
            self.store.append('review_accepted',actor,task_id,payload=last)
        self._review_artifacts(task_id,artifacts)
        return self.store.complete(task_id,actor,artifacts)

    def resubmit(self,task_id,actor,source_review_id,correction_evidence):
        identity(actor)
        require(bool(correction_evidence and correction_evidence.strip()),'Correction evidence required')
        rem=next((x for x in self._read_records('reviews') if x.get('source_review_id')==source_review_id
                  and x.get('status')=='OPEN' and x.get('task_id')==task_id),None)
        require(rem is not None,'Structured remediation request not found')
        st=self.store.verified()
        require(st['tasks'][task_id]['status']=='NEEDS_REWORK','No failed review awaiting correction')
        require(st['tasks'][task_id].get('retry',{}).get('eligible'), 'Review retry exhausted')
        # No new reviews inherit a prior PASS because attempt ID changes on restart.
        self.store.retry(task_id,actor,approval=True)
        return {'task_id':task_id,'source_review_id':source_review_id,'status':'READY_FOR_NEW_ATTEMPT',
                'correction_evidence':correction_evidence}

    def handoff(self,actor,next_action,summary=None):
        identity(actor);require(next_action and next_action.strip(),'Next action required')
        s=self.store.verified();claims=self._read_records('claims');reviews=self._read_records('reviews')
        pending=[x['gate_id'] for k,node in self.store.node_map.items()
                 for x in self._gates_for(k) if s['tasks'][k]['status'] in ('RUNNING','WAIT_REVIEW','NEEDS_REWORK')]
        ident=f'governance-handoff-{s["last_event_seq"]+1:06d}'
        data={'schema_version':'1.0.0','handoff_id':ident,'run_id':self.store.run_id,'graph_revision':s['graph_revision'],
              'actor':actor,'at':utcnow(),'last_event_seq':s['last_event_seq'], 'summary':summary or 'Task progress',
              'completed':s['completed_steps'],'active':s['active_steps'], 'ready':s['eligible_tasks'],
              'owners':s['owners'],'claims':claims,'pending_quality':sorted(set(pending)),
              'pending_provider_actions':s['pending_provider_operations'],'next_action':next_action,
              'security_level':'cooperative_no_authentication'}
        self._record('handoffs',ident,data)  # user-owned durable record, independent of generated handoff view
        self._record_event('governance_handoff',actor,None,ident,data)
        base=self.store.handoff(actor)
        base['governance_next_action']=next_action
        base['governance_pending_quality']=sorted(set(pending))
        atomic_write(self.root/'handoff.json',(json.dumps(base,indent=2,sort_keys=True)+'\n').encode())
        with (self.root/'handoff.md').open('a',encoding='utf-8') as f:
            f.write('\n## Governance handoff\n\n'+summary+'\n\nNext: '+next_action+'\n\n' if summary else '\n## Governance handoff\n\nNext: '+next_action+'\n')
        return data
