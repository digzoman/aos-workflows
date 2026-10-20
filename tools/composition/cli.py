"""Optional, explicitly invoked AOS-W helper. pip install pyyaml if using this helper.
The ordinary Markdown/YAML/JSON workflow protocol does not need this program.
"""
import argparse, json, sys, hashlib
from pathlib import Path
from datetime import datetime, timezone
from composition import InvalidWorkflow, read_yaml, validate_graph, resolve, classify, proposals, merge, revision_impact, sha256_bytes

def save(path, value):
    path=Path(path).resolve()
    if not any(x.name=='agent-files' for x in [path,*path.parents]):
        raise InvalidWorkflow('Output must be inside user-owned agent-files')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2)+'\n', encoding='utf-8')

def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def moment(): return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def safe_path(base, child):
    b=Path(base).resolve(); p=(b/child).resolve()
    if not p.is_relative_to(b) or any(x.is_symlink() for x in [b,*p.parents] if x.exists()):
        raise InvalidWorkflow('Path escapes writable agent-files root')
    return p

def materialize(bundle, approval, template_path, agent_files, actor):
    if approval.get('decision')!='GRANTED' or approval.get('scope')!='instantiate_children' or approval.get('plan_id')!=bundle['plan_id'] or approval.get('revision')!=bundle['revision']:
        raise InvalidWorkflow('Exact scoped child-instantiation approval missing')
    allowed=set(approval.get('allowed_proposal_ids',[]))
    if allowed != {p['proposal_id'] for p in bundle['proposals']}:
        raise InvalidWorkflow('Approval does not name the exact proposed children')
    if any(not actor.get(k) for k in ('agent','platform','role','instance')):raise InvalidWorkflow('Real actor identity required')
    template_path=Path(template_path)
    template=read_yaml(template_path)
    validate_graph(template['graph'])
    digest=sha256_bytes(template_path.read_bytes())
    if approval.get('template_sha256')!=digest: raise InvalidWorkflow('Template changed after approval')
    root=Path(agent_files).resolve()
    if root.name != 'agent-files' or not root.is_dir():raise InvalidWorkflow('Existing agent-files root required')
    ts=moment()
    targets=[]
    for prop in bundle['proposals']:
        if prop['template_id'] != template['template_id'] or prop['template_version']!=template['version'] or prop['status']!='PROPOSED':
            raise InvalidWorkflow('Child template or proposal mismatch')
        target=safe_path(root,'instances/'+prop['instance_id'])
        if target.exists():raise InvalidWorkflow('Child instance exists; inspect/reconcile rather than duplicating: '+prop['instance_id'])
        targets.append((prop,target))
    created=[]
    for prop,target in targets:
        target.mkdir(parents=True,exist_ok=False);created.append(target)
        runid=prop['run_id'];run=target/'runs'/runid
        for dirname in ['skills','graph-revisions','template-snapshots/sha256-'+digest[:16],f'runs/{runid}/checkpoints',f'runs/{runid}/artifacts',f'runs/{runid}/reviews',f'runs/{runid}/approvals',f'runs/{runid}/claims',f'runs/{runid}/skills']:
            safe_path(target,dirname).mkdir(parents=True,exist_ok=True)
        for node in template['graph']['nodes']:
            safe_path(run,'tasks/'+node['id']+'/attempts').mkdir(parents=True,exist_ok=True)
        (target/'template-snapshots'/('sha256-'+digest[:16])/'template.yaml').write_bytes(template_path.read_bytes())
        (target/'graph-revisions'/'g0001.yaml').write_bytes(template_path.read_bytes())
        pol=template['policy'];node_states={n['id']:{'status':'READY' if not n['needs'] else 'WAIT_DEPENDENCY','attempts':0,'graph_revision':'g0001'} for n in template['graph']['nodes']}
        save(target/'instance.json',{'schema_version':'1.0.0','instance_id':prop['instance_id'],'name':prop['instance_id'],'template_id':template['template_id'],'template_version':template['version'],'template_lock':'template-lock.json','current_graph_revision':'g0001','parameters':prop['inputs'],'policy':pol,'created_at':ts,'created_by':actor,'parent_instance_id':bundle['plan_id']})
        save(target/'template-lock.json',{'schema_version':'1.0.0','instance_id':prop['instance_id'],'template_id':template['template_id'],'version':template['version'],'origin':str(template_path),'pinned_snapshot_path':'template-snapshots/sha256-'+digest[:16]+'/template.yaml','content_digest':'sha256:'+digest,'graph_revision':'g0001','resolved_at':ts})
        save(run/'run.json',{'schema_version':'1.0.0','run_id':runid,'instance_id':prop['instance_id'],'graph_revision':'g0001','trigger_kind':'manual','created_at':ts,'created_by':actor,'mode':'standalone_single_writer','capabilities':{'persistent_files':{'status':'unverified'},'exclusive_claim':{'status':'unavailable'}},'parent_run_id':bundle['parent_run_id']})
        ev={'schema_version':'1.0.0','event_id':'evt-0001','seq':1,'run_id':runid,'type':'run_created','at':ts,'actor':actor,'graph_revision':'g0001','evidence':[],'payload':{'proposal_id':prop['proposal_id'],'approval_id':approval.get('approval_id'),'parent_run_id':bundle['parent_run_id']},'integrity_level':'advisory'}
        (run/'events.jsonl').write_text(json.dumps(ev,sort_keys=True)+'\n',encoding='utf-8')
        ready=[n['id'] for n in template['graph']['nodes'] if not n['needs']]
        save(run/'state.json',{'schema_version':'1.0.0','run_id':runid,'graph_revision':'g0001','state_revision':1,'updated_at':ts,'last_event_seq':1,'integrity_level':'advisory','run_status':'CREATED','tasks':node_states,'eligible_tasks':ready})
        (run/'handoff.md').write_text('# New child investigation: '+prop['instance_id']+'\n\n**CREATED, not executed.**\nParent plan: '+bundle['plan_id']+' / '+bundle['revision']+'\nApproval: '+str(approval.get('approval_id'))+'\nPinned template SHA256: '+digest+'\nNext task(s): '+', '.join(ready)+'\nNo evidence or review is complete.\n',encoding='utf-8')
    return {'created':[p.name for p in created],'count':len(created),'template_sha256':digest,'effect':'local_agent_files_only','warning':'Not an atomic multi-agent transaction; interrupted partial writes require reconciliation.'}

def main():
    p=argparse.ArgumentParser(description='OPTIONAL AOS-W composition helper; never mandatory for file-only mode')
    s=p.add_subparsers(dest='cmd',required=True)
    x=s.add_parser('validate');x.add_argument('template');x.add_argument('--legacy',action='store_true')
    x=s.add_parser('resolve');x.add_argument('base');x.add_argument('--overlay');x.add_argument('--params');x.add_argument('--output',required=True)
    x=s.add_parser('classify');x.add_argument('template');x.add_argument('state');x.add_argument('--context')
    x=s.add_parser('propose');x.add_argument('plan');x.add_argument('child_template');x.add_argument('--output',required=True)
    x=s.add_parser('materialize');x.add_argument('bundle');x.add_argument('approval');x.add_argument('child_template');x.add_argument('agent_files');x.add_argument('actor')
    x=s.add_parser('merge');x.add_argument('bundle');x.add_argument('results');x.add_argument('approval');x.add_argument('--output',required=True)
    x=s.add_parser('revision-impact');x.add_argument('before');x.add_argument('after');x.add_argument('state');x.add_argument('--approval');x.add_argument('--output',required=True)
    a=p.parse_args()
    try:
        if a.cmd=='validate':out=validate_graph(read_yaml(a.template)['graph'],not a.legacy)
        elif a.cmd=='resolve':
            src=Path(a.base);out=resolve(read_yaml(src),read_yaml(a.overlay) if a.overlay else None,load(a.params) if a.params else {},sha256_bytes(src.read_bytes()));save(Path(a.output),out)
        elif a.cmd=='classify':out=classify(read_yaml(a.template)['graph'],load(a.state),load(a.context) if a.context else {})
        elif a.cmd=='propose':out=proposals(load(a.plan),read_yaml(a.child_template));save(Path(a.output),out)
        elif a.cmd=='materialize':out=materialize(load(a.bundle),load(a.approval),a.child_template,a.agent_files,load(a.actor))
        elif a.cmd=='merge':out=merge(load(a.bundle),load(a.results),load(a.approval));save(Path(a.output),out)
        elif a.cmd=='revision-impact':out=revision_impact(read_yaml(a.before)['graph'],read_yaml(a.after)['graph'],load(a.state),load(a.approval) if a.approval else None);save(Path(a.output),out)
        print(json.dumps(out,indent=2,sort_keys=True))
    except (InvalidWorkflow,KeyError,ValueError,FileNotFoundError) as e:
        print('BLOCKED: '+str(e),file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
