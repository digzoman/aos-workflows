#!/usr/bin/env python3
"""OPTIONAL AOS-W developer helper: discovery, safe start and cautious status.
Python only for this convenience tool. PyYAML required ONLY for 'init'.
Manual installation and normal file-only operation never require Python.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, re, shutil, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

ID=re.compile(r'^[a-z0-9][a-z0-9._-]{0,79}$')
class OpsError(ValueError): pass

def require_id(s):
    if not ID.fullmatch(s):raise OpsError('Unsafe identifier')
    return s

def safe(root,relative):
    p=root/relative
    if p.resolve().is_relative_to(root.resolve()) is False or p.is_symlink():raise OpsError('Escaped writable root')
    return p

def store_json(path,doc):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def timestamp():return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')

def installed(root):
    root=root.resolve()
    if root.name!='aos-w' or not (root/'VERSION.json').is_file() or not (root/'agent-files').is_dir():
        raise OpsError('Not an installed AOS-W folder')
    return root

def list_work(root):
    root=installed(root)
    templates=[]
    for parent,kind in ((root/'templates','master'),(root/'agent-files'/'custom-templates','custom')):
        if not parent.exists():continue
        for p in sorted(parent.glob('*/template.yaml')):
            if p.is_symlink():continue
            templates.append({'kind':kind,'id':p.parent.name,'path':str(p.relative_to(root))})
    instances=[]
    for p in sorted((root/'agent-files'/'instances').glob('*/instance.json')):
        if p.is_symlink():continue
        try:
            data=json.loads(p.read_text());instances.append({'id':data['instance_id'],'current_graph_revision':data.get('current_graph_revision'),'runs':sorted(x.name for x in (p.parent/'runs').glob('*') if x.is_dir())})
        except Exception as e:instances.append({'id':p.parent.name,'error':'invalid instance metadata: '+str(e)})
    return {'root':str(root),'templates':templates,'instances':instances,'mode':'file-only-single-writer-default'}

def local_status(root,instance_id,run_id):
    root=installed(root)
    run=safe(root/'agent-files',f'instances/{require_id(instance_id)}/runs/{require_id(run_id)}')
    if not run.is_dir():raise OpsError('Run not found')
    state=json.loads((run/'state.json').read_text())
    log=run/'events.jsonl'
    if not log.is_file():raise OpsError('Missing event log')
    raw=log.read_bytes();lines=raw.splitlines(keepends=True)
    problems=[];seq=0
    for row in lines:
        if not row.endswith(b'\n'):problems.append('Unterminated JSONL tail');break
        try:
            e=json.loads(row);n=e['seq']
            if n!=seq+1:problems.append('Gap or duplicate event sequence');break
            seq=n
        except Exception:problems.append('Invalid event line');break
    if state.get('last_event_seq')!=seq:problems.append('Snapshot/event sequence conflict')
    instance=run.parents[1]
    graph=instance/'graph-revisions'/(state['graph_revision']+'.yaml')
    if not graph.is_file():problems.append('Pinned graph revision missing')
    # Do not pretend to verify SHA/event chain or provider state via a summary-only reader.
    return {'run':str(run),'run_status':state.get('run_status'),'graph_revision':state.get('graph_revision'),
       'snapshot_event_seq':state.get('last_event_seq'),'observed_valid_event_seq':seq,
       'next_eligible_candidates':state.get('eligible_tasks',[]),'completed':state.get('completed_steps',[]),
       'pending_provider_operations':state.get('pending_provider_operations',[]),
       'issues':problems,'verification':'advisory_only_use_tools/state/recover_for_integrity',
       'event_prefix_consistent':not problems,'authorized_to_execute':False}

def init(root,template_id,instance_id,run_id,actor,parameters):
    root=installed(root)
    for value in (template_id,instance_id,run_id):require_id(value)
    if set(actor)!={'agent','platform','role','instance'} or not all(isinstance(x,str) and x for x in actor.values()):
        raise OpsError('Provide exactly [Agent | Platform | Role | Instance]')
    try:import yaml
    except ImportError as exc:raise OpsError('Optional init helper requires PyYAML; manual file-only initialization remains available') from exc
    path=root/'templates'/template_id/'template.yaml'
    if not path.is_file():raise OpsError('Unknown master template; use manual custom overlay resolution')
    if path.is_symlink():raise OpsError('Symlink template prohibited')
    template=yaml.safe_load(path.read_bytes())
    if template.get('template_id')!=template_id or not isinstance(template.get('graph',{}).get('nodes'),list):raise OpsError('Bad template identity/graph')
    from_parent=root/'agent-files'/'instances';from_parent.mkdir(parents=True,exist_ok=True)
    target=safe(from_parent,instance_id)
    if target.exists():raise OpsError('Instance already exists: inspect and resume; never overwrite')
    declarations=template.get('parameters',{});resolved={}
    for name,definition in declarations.items():
        val=parameters.get(name,definition.get('default'))
        if val is None and definition.get('required'):raise OpsError('Required parameter missing: '+name)
        if val is not None:
            tp=definition['type']
            valid={'string':lambda x:isinstance(x,str),'array':lambda x:isinstance(x,list),'object':lambda x:isinstance(x,dict),'number':lambda x:isinstance(x,(int,float)) and not isinstance(x,bool),'boolean':lambda x:isinstance(x,bool)}[tp](val)
            if not valid:raise OpsError('Wrong parameter type: '+name)
            resolved[name]=val
    if set(parameters)-set(declarations):raise OpsError('Unexpected parameters')
    nodes=template['graph']['nodes'];ids=[n['id'] for n in nodes]
    if len(set(ids))!=len(ids) or any(n.get('needs') is None or any(d not in ids for d in n['needs']) for n in nodes):raise OpsError('Invalid graph dependencies')
    active=set();visited=set()
    def walk(k):
        if k in active:raise OpsError('Graph dependency cycle')
        if k in visited:return
        active.add(k)
        for parent in next(n for n in nodes if n['id']==k)['needs']:walk(parent)
        active.remove(k);visited.add(k)
    for k in ids:walk(k)
    ts=timestamp();content=path.read_bytes();digest=hashlib.sha256(content).hexdigest()
    stage=Path(tempfile.mkdtemp(dir=from_parent,prefix='.aosw-new-'))
    try:
        pins=stage/'template-snapshots'/('sha256-'+digest[:16]);pins.mkdir(parents=True)
        (pins/'template.yaml').write_bytes(content)
        rev=stage/'graph-revisions';rev.mkdir(parents=True)
        (rev/'g0001.yaml').write_bytes(content)
        store_json(stage/'instance.json',{'schema_version':'1.0.0','instance_id':instance_id,'name':instance_id,
            'template_id':template_id,'template_version':template['version'],'template_lock':'template-lock.json',
            'current_graph_revision':'g0001','parameters':resolved,'policy':template['policy'],
            'created_at':ts,'created_by':actor})
        store_json(stage/'template-lock.json',{'schema_version':'1.0.0','instance_id':instance_id,'template_id':template_id,
            'version':template['version'],'origin':str(path.relative_to(root)),'pinned_snapshot_path':str(pins.relative_to(stage)/'template.yaml'),
            'content_digest':'sha256:'+digest,'graph_revision':'g0001','resolved_at':ts})
        run=stage/'runs'/run_id
        for dirname in ['checkpoints','artifacts','claims','reviews','approvals','skills']:(run/dirname).mkdir(parents=True)
        for n in nodes:(run/'tasks'/n['id']/'attempts').mkdir(parents=True)
        store_json(run/'run.json',{'schema_version':'1.0.0','run_id':run_id,'instance_id':instance_id,'graph_revision':'g0001',
          'trigger_kind':'manual','created_at':ts,'created_by':actor,'mode':'standalone_single_writer',
          'capabilities':{'persistent_files':{'status':'unverified'},'exclusive_claim':{'status':'unavailable'}},'graph_digest':digest})
        # A fresh event log with a digest chain; state reducer can rebuild it.
        ev={'schema_version':'1.0.0','event_id':'evt-0001','seq':1,'run_id':run_id,
            'type':'run_created','at':ts,'actor':actor,'graph_revision':'g0001','evidence':[],
            'payload':{'source':'optional quickstart, local only'},'integrity_level':'verified','prev_digest':'0'*64}
        ev['digest']=hashlib.sha256(('0'*64+'\n'+json.dumps(ev,sort_keys=True,separators=(',',':'),ensure_ascii=False)).encode()).hexdigest()
        (run/'events.jsonl').write_text(json.dumps(ev,sort_keys=True)+'\n')
        states={n['id']:{'status':'READY' if not n['needs'] else 'WAIT_DEPENDENCY','attempts':0,'graph_revision':'g0001','owner':None,'evidence':[],'pending_actions':[],'retry':None,'last_error':None,'last_attempt_id':None,'review':None} for n in nodes}
        ready=[n['id'] for n in nodes if not n['needs']]
        store_json(run/'state.json',{'schema_version':'1.0.0','run_id':run_id,'graph_revision':'g0001',
            'run_status':'CREATED','state_revision':1,'last_event_seq':1,'last_event_digest':ev['digest'],
            'integrity_level':'verified','updated_at':ts,'tasks':states,'eligible_tasks':ready,
            'completed_steps':[],'active_steps':[],'pending_provider_operations':[],
            'governance':{'claims':{},'permissions':{},'reviews':{},'remediation':{},'handoff':None}})
        (run/'handoff.md').write_text('# AOS-W new run (not executed)\n\nRun: '+run_id+'\nTemplate: '+template_id+' @ '+template['version']+'\nGraph: g0001\nNext eligible: '+', '.join(ready)+'\nNo task has executed, no external permission granted. Read events and pinned graph before continuing.\n')
        os.replace(stage,target)
    finally:
        if stage.exists():shutil.rmtree(stage)
    return {'instance_id':instance_id,'run_id':run_id,'created':str(target),'template_pin':'sha256:'+digest,
            'ready_candidates':ready,'effect':'local agent-files only','task_executed':False}

def main(argv=None):
    p=argparse.ArgumentParser(description='OPTIONAL AOS-W local helper; no external/provider actions')
    sub=p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('list');s.add_argument('installation',type=Path)
    s=sub.add_parser('status');s.add_argument('installation',type=Path);s.add_argument('instance_id');s.add_argument('run_id')
    s=sub.add_parser('init');s.add_argument('installation',type=Path);s.add_argument('template_id');s.add_argument('instance_id');s.add_argument('run_id');s.add_argument('--actor',required=True);s.add_argument('--parameters',default='{}')
    a=p.parse_args(argv)
    try:
        data=list_work(a.installation) if a.command=='list' else (local_status(a.installation,a.instance_id,a.run_id) if a.command=='status' else init(a.installation,a.template_id,a.instance_id,a.run_id,json.loads(a.actor),json.loads(a.parameters)))
        print(json.dumps(data,sort_keys=True,indent=2));return 0
    except (OpsError,ValueError,OSError,KeyError,TypeError) as exc:
        print('BLOCKED: '+str(exc),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
