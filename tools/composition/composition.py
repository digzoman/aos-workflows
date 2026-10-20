"""Optional AOS-W composition checks. Requires PyYAML only if imported/used.
Normal AOS-W agents may follow the same rules manually using YAML and files.
No network, provider mutation, scheduler or distributed claim support.
"""
from __future__ import annotations
import copy, hashlib, json, re
from pathlib import Path

ID = re.compile(r'^[a-z0-9][a-z0-9._-]{0,79}$')
DANGEROUS = {'activate_live', 'change_budget', 'deploy_prod', 'send_message', 'emit_conversion', 'stage_paused', 'edit_crm'}

class InvalidWorkflow(ValueError): pass

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()

def read_yaml(path):
    import yaml  # optional dependency, never required for plain-file agents
    return yaml.safe_load(Path(path).read_text(encoding='utf-8'))

def contract(node):
    return (isinstance(node.get('inputs'), list) and isinstance(node.get('outputs'), list)
            and isinstance(node.get('quality'), dict) and isinstance(node['quality'].get('gates'), list)
            and isinstance(node.get('contract'), dict) and bool(node['contract'].get('done_when'))
            and isinstance(node.get('instructions'), str) and bool(node['instructions'].strip()))

def validate_graph(graph, strict=True):
    nodes = graph.get('nodes')
    if not isinstance(nodes, list) or not nodes: raise InvalidWorkflow('Empty graph')
    by = {}
    for node in nodes:
        k = node.get('id')
        if not isinstance(k, str) or not ID.fullmatch(k) or k in by:
            raise InvalidWorkflow('Invalid/duplicate node ID: '+str(k))
        if not isinstance(node.get('needs'), list): raise InvalidWorkflow('Missing needs: '+k)
        if strict and not contract(node): raise InvalidWorkflow('Missing execution contract: '+k)
        for output in node.get('outputs', []):
            p = output.get('path', '')
            if p.startswith('/') or '..' in Path(p).parts or not p:
                raise InvalidWorkflow('Unsafe output path: '+k)
        by[k] = node
    active, done = set(), set()
    def visit(k):
        if k not in by: raise InvalidWorkflow('Unknown dependency: '+k)
        if k in active: raise InvalidWorkflow('Cycle: '+k)
        if k in done: return
        active.add(k)
        for parent in by[k]['needs']: visit(parent)
        for choice in by[k].get('branch_cases', []):
            for target in choice['targets']:
                if target not in by: raise InvalidWorkflow('Unknown branch target: '+target)
        for m in by[k].get('join', {}).get('members', []):
            if m not in by: raise InvalidWorkflow('Unknown join member: '+m)
        active.remove(k); done.add(k)
    for k in by: visit(k)
    return {'valid': True, 'node_ids': sorted(by)}

def resolve(base, overlay=None, parameters=None, base_digest=None):
    parameters = parameters or {}
    result = copy.deepcopy(base)
    if overlay:
        pin = overlay.get('base', {})
        if pin.get('template_id') != base['template_id'] or pin.get('version') != base['version'] or pin.get('content_digest') != base_digest:
            raise InvalidWorkflow('Overlay base revision/digest mismatch')
        result['template_id'], result['version'] = overlay['template_id'], overlay['version']
        result['name'] = overlay.get('name', result['name'])
        original = base['policy']
        patch = overlay.get('policy_overrides', {})
        unknown = set(patch) - set(original)
        if unknown: raise InvalidWorkflow('Unknown policy override '+str(unknown))
        for k, value in patch.items():
            if k == 'allowed_actions' and not set(value).issubset(set(original[k])): raise InvalidWorkflow('Action escalation')
            if k == 'human_required_actions' and not set(original[k]).issubset(set(value)): raise InvalidWorkflow('Protected human approval removed')
            if k == 'default_gates' and not set(original[k]).issubset(set(value)): raise InvalidWorkflow('Required gate removed')
            if k == 'max_parallel_tasks' and value > original[k]: raise InvalidWorkflow('Parallel limit escalated')
            if k in ('autonomy','allow_dynamic_children','allow_material_revisions') and value != original.get(k): raise InvalidWorkflow('Autonomy changed without authorization')
            result['policy'][k] = copy.deepcopy(value)
        nodes = {n['id']: n for n in result['graph']['nodes']}
        for patch in overlay.get('node_patches', []):
            ident = patch['node_id']; op = patch['op']
            if not patch.get('reason'): raise InvalidWorkflow('Patch lacks rationale')
            if op == 'add':
                if ident in nodes or patch['node']['id'] != ident: raise InvalidWorkflow('Bad add')
                if not set(patch['node'].get('required_actions', [])).issubset(set(result['policy']['allowed_actions'])): raise InvalidWorkflow('Added node action escalation')
                nodes[ident] = copy.deepcopy(patch['node'])
            elif op == 'replace':
                if ident not in nodes or patch['node']['id'] != ident: raise InvalidWorkflow('Bad replace')
                if not set(patch['node'].get('required_actions', [])).issubset(set(nodes[ident].get('required_actions', []))) or not set(patch['node'].get('required_actions', [])).issubset(set(result['policy']['allowed_actions'])):
                    raise InvalidWorkflow('Node action escalation')
                if not set(nodes[ident].get('quality',{}).get('gates', [])).issubset(set(patch['node'].get('quality',{}).get('gates', []))):
                    raise InvalidWorkflow('Cannot weaken node quality gates')
                nodes[ident] = copy.deepcopy(patch['node'])
            elif op == 'remove':
                if ident not in nodes: raise InvalidWorkflow('Unknown remove')
                del nodes[ident]
            else: raise InvalidWorkflow('Unknown patch operation')
        result['graph']['nodes'] = list(nodes.values())
        if 'trigger_override' in overlay: result['trigger'] = copy.deepcopy(overlay['trigger_override'])
    resolved = {}
    for k, decl in result.get('parameters', {}).items():
        v = parameters[k] if k in parameters else decl.get('default')
        if v is None and decl.get('required'): raise InvalidWorkflow('Required parameter missing: '+k)
        if v is not None:
            tp = decl['type']; valid = ((tp == 'string' and isinstance(v, str)) or (tp == 'number' and isinstance(v,(float,int)) and not isinstance(v,bool)) or (tp == 'boolean' and isinstance(v,bool)) or (tp == 'array' and isinstance(v,list)) or (tp == 'object' and isinstance(v,dict)))
            if not valid: raise InvalidWorkflow('Wrong parameter type: '+k)
            resolved[k] = v
    if set(parameters)-set(result.get('parameters', {})): raise InvalidWorkflow('Unknown parameters')
    result['resolved_parameters'] = resolved
    validate_graph(result['graph'])
    return result

def predicate(p, context):
    if not p: return True
    op = p['op']
    if op in ('and','or'):
        vals = [predicate(q, context) for q in p['args']]
        return (False if False in vals else None if None in vals else True) if op == 'and' else (True if True in vals else None if None in vals else False)
    if op == 'not':
        x = predicate(p['arg'], context); return None if x is None else not x
    value = context
    for part in p['path'].split('.'):
        if not isinstance(value,dict) or part not in value: return None
        value = value[part]
    if op == 'exists': return value is not None
    if value is None: return None
    if op == 'eq': return value == p.get('value')
    if op == 'neq': return value != p.get('value')
    if op == 'in': return value in p.get('value', [])
    if op == 'gte': return value >= p['value'] if isinstance(value,(int,float)) else None
    if op == 'lte': return value <= p['value'] if isinstance(value,(int,float)) else None
    raise InvalidWorkflow('Unknown predicate: '+op)

def classify(graph, state, context=None):
    context = context or {}; by={n['id']:n for n in graph['nodes']}; answer={}
    for n in graph['nodes']:
        ident=n['id']; saved=state.get(ident,{}).get('status','WAIT_DEPENDENCY')
        if saved in ('COMPLETE','ACCEPTED'):
            answer[ident]={'status':'completed','reason':'Recorded accepted result'};continue
        if saved in ('FAILED','NEEDS_REWORK'):
            answer[ident]={'status':'failed','reason':saved};continue
        if saved in ('BLOCKED','RECONCILE_REQUIRED','CANCELLED','SUPERSEDED'):
            answer[ident]={'status':'blocked','reason':saved};continue
        if saved in ('CLAIMED','RUNNING','WAIT_EXTERNAL','WAIT_REVIEW'):
            answer[ident]={'status':'waiting','reason':saved};continue
        reason=None; category='waiting'
        for dep in n['needs']:
            if state.get(dep,{}).get('status') not in ('COMPLETE','ACCEPTED'):
                reason='Dependency '+dep+' incomplete';break
            for gate in by[dep].get('quality',{}).get('gates',[]):
                if context.get('reviews',{}).get(dep+':'+gate,{}).get('verdict') != 'PASS':
                    reason='Dependency '+dep+' missing current review';break
            if reason: break
        if not reason:
            v=predicate(n.get('when'),context.get('values',{}))
            if v is None: reason='Condition UNKNOWN'
            if v is False: reason='Condition FALSE (skip path when closed)'
        for i in n.get('inputs',[]) if not reason else []:
            if i.get('required',True) and i.get('from') and not context.get('artifacts',{}).get(i['from']+':'+i['artifact_id'],{}).get('verified'):
                reason='Missing verified input';break
        if n.get('join') and not reason:
            join=n['join']; good=sum(context.get('children',{}).get(m,{}).get('status')=='ACCEPTED' and context['children'][m].get('review')=='PASS' for m in join['members'])
            need=len(join['members']) if join['policy']=='all_accepted' else (1 if join['policy']=='any_accepted' else join['threshold'])
            if join['policy']!='all_accepted' and not context.get('join_authorized'): reason='Partial join lacks approval'
            elif good<need: reason='Awaiting reviewed children'
        if n.get('kind') == 'join' and n.get('extensions', {}).get('join_source') and not reason:
            bundle = context.get('proposals')
            if not bundle or not bundle.get('proposals'):
                reason='Dynamic child proposals missing'
            elif not context.get('synthesis_approval',{}).get('valid'):
                reason='No scoped synthesis approval';category='blocked'
            else:
                missing=[p['proposal_id'] for p in bundle['proposals'] if
                         not (context.get('children',{}).get(p['proposal_id'],{}).get('status')=='COMPLETE' and
                              context['children'][p['proposal_id']].get('review',{}).get('verdict')=='PASS' and
                              context['children'][p['proposal_id']].get('artifacts'))]
                if missing: reason='Unreviewed dynamic children: '+', '.join(missing)
        if not reason:
            for skill in n.get('skills', []):
                if context.get('skills', {}).get(skill) != 'available':
                    reason='Required skill unavailable: '+skill;category='blocked';break
        if not reason:
            for capability in n.get('required_capabilities', []):
                if context.get('capabilities', {}).get(capability) != 'available':
                    reason='Required capability unavailable: '+capability;category='blocked';break
        if not reason:
            for action in n.get('required_actions',[]):
                if action not in context.get('allowed_actions',[]): reason='Missing allowed action '+action;category='blocked';break
                if action in DANGEROUS and not any(a.get('action')==action and a.get('valid') and a.get('graph_revision')==context.get('graph_revision') for a in context.get('approvals',[])):
                    reason='Missing scoped approval '+action;category='blocked';break
        if not reason and context.get('mode')=='shared_coordinated' and context.get('exclusive_claim')!='verified': reason='No exclusive claim';category='blocked'
        answer[ident]={'status':category if reason else 'ready','reason':reason or 'All declared prerequisites passed'}
    return answer

def proposals(plan, child):
    validate_graph(child['graph'])
    if not plan.get('approved_input'): raise InvalidWorkflow('Parent plan not reviewed')
    if plan['child_template_id']!=child['template_id'] or plan['child_template_version']!=child['version']: raise InvalidWorkflow('Wrong child template')
    seen=set(); out=[]
    for item in plan['items']:
        slug=item['slug']; ident=plan['plan_id']+'-'+slug+'-'+plan['revision']
        if not ID.fullmatch(ident) or ident in seen: raise InvalidWorkflow('Duplicate/unstable child ID')
        seen.add(ident)
        params={k:item[k] for k in child.get('parameters',{}) if k in item}
        for k,decl in child.get('parameters',{}).items():
            if decl.get('required') and k not in params: raise InvalidWorkflow('Child parameter missing '+k)
        out.append({'proposal_id':ident,'instance_id':ident,'run_id':'run-001','status':'PROPOSED','needs':[plan.get('approval_node','approve-plan')], 'template_id':child['template_id'],'template_version':child['version'],'inputs':params,'expected_outputs':[dict(o,step_id=n['id']) for n in child['graph']['nodes'] for o in n['outputs']], 'quality_requirements':child.get('gates',[]),'execution_contracts':[{'step_id':n['id'],'needs':n['needs'],'inputs':n['inputs'],'outputs':n['outputs'],'quality':n['quality'],'done_when':n['contract']['done_when']} for n in child['graph']['nodes']], 'authorization_required':True})
    return {'schema_version':'1.0.0','plan_id':plan['plan_id'],'revision':plan['revision'],'parent_run_id':plan['parent_run_id'],'status':'PROPOSED','authorization_required':True,'proposals':out}

def merge(bundle, results, approval):
    if not (approval.get('decision')=='GRANTED' and approval.get('scope')=='synthesize' and approval.get('plan_id')==bundle['plan_id'] and approval.get('revision')==bundle['revision']):raise InvalidWorkflow('Synthesis approval missing')
    children=[]
    for p in bundle['proposals']:
        c=results.get(p['proposal_id'],{})
        if not (c.get('status')=='COMPLETE' and c.get('review',{}).get('verdict')=='PASS' and c.get('artifacts') and c.get('graph_revision')):raise InvalidWorkflow('Child unreviewed: '+p['proposal_id'])
        children.append({'child_id':p['proposal_id'],'graph_revision':c['graph_revision'],'review_id':c['review']['review_id'],'artifacts':c['artifacts']})
    return {'plan_id':bundle['plan_id'],'revision':bundle['revision'],'status':'READY_FOR_SYNTHESIS','children':children}

def revision_impact(before,after,state,approval=None):
    validate_graph(before);validate_graph(after)
    old={n['id']:n for n in before['nodes']};new={n['id']:n for n in after['nodes']}
    changed={k for k in old.keys()|new.keys() if canonical(old.get(k))!=canonical(new.get(k))}
    invalid=set(changed)
    while True:
        more={n['id'] for n in after['nodes'] if any(p in invalid for p in n['needs'])}
        if more<=invalid:break
        invalid|=more
    executed=any(state.get(k,{}).get('status') in ('COMPLETE','ACCEPTED','RUNNING') for k in changed)
    sensitive=any(set(new[k].get('required_actions',[]))&DANGEROUS for k in changed if k in new)
    if (executed or sensitive) and not (approval and approval.get('decision')=='GRANTED' and approval.get('action')=='revise_graph'):
        raise InvalidWorkflow('Material revision requires approval')
    return {'changed':sorted(changed),'invalidated':sorted(invalid),'preserved':sorted(k for k in old if k not in invalid and state.get(k,{}).get('status')=='COMPLETE'),'requires_approval':executed or sensitive,'history_policy':'append_new_revision'}
