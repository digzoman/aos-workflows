"""Optional AOS-W local governance CLI. No external effects or authenticated approvals."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from governance import Governance, Unauthorized
from state import StateError

def j(value):
    if value is None:return None
    p=Path(value)
    if len(value)<400 and p.exists() and p.is_file():return json.loads(p.read_text())
    return json.loads(value)

def main(argv=None):
    p=argparse.ArgumentParser(description='AOS-W optional local governance checks (single writer; advisory)')
    p.add_argument('run_dir');p.add_argument('action',choices=['inspect','claim','begin','release','grant','revoke',
        'authorize','submit-review','review','finalize','resubmit','handoff','op-intent'])
    p.add_argument('--actor',help='JSON actor or path with [Agent|Platform|Role|Instance]')
    p.add_argument('--payload',default='{}',help='JSON object/file describing action')
    args=p.parse_args(argv)
    try:
        cfg=j(args.payload);actor=j(args.actor) if args.actor else None
        g=Governance(args.run_dir)
        a=args.action
        if a=='inspect':out={'state':g.store.verified(),'policy':g.policy,'quality_gates':g.gates}
        elif a=='claim':out=g.claim(cfg['claim_id'],cfg['task_id'],actor,cfg['expires_at'],cfg.get('resources'))
        elif a=='begin':out=g.begin(cfg['task_id'],actor)
        elif a=='release':out=g.release(cfg['claim_id'],cfg['release_id'],actor,cfg['reason'])
        elif a=='grant':out=g.grant(cfg['approval_id'],actor,cfg['actions'],cfg['resources'],task_id=cfg.get('task_id'),
            expires_at=cfg.get('expires_at'),artifact_refs=cfg.get('artifact_refs'),limits=cfg.get('limits'),
            exclusions=cfg.get('exclusions'),reason=cfg.get('reason'))
        elif a=='revoke':out=g.revoke(cfg['approval_id'],cfg['revocation_id'],actor,cfg['reason'])
        elif a=='authorize':out=g.authorize(actor,cfg['action'],cfg['resources'],task_id=cfg.get('task_id'),
            artifact_refs=cfg.get('artifact_refs'),amount=cfg.get('amount'))
        elif a=='submit-review':g.submit_review(cfg['task_id'],actor);out={'status':'WAIT_REVIEW'}
        elif a=='review':out=g.review(cfg['review_id'],cfg['task_id'],j(cfg['producer']) if isinstance(cfg['producer'],str) else cfg['producer'],
            actor,cfg['gate_id'],cfg['artifacts'],cfg['verdict'],findings=cfg.get('findings'),
            rubric_revision=cfg.get('rubric_revision','1'),correction=cfg.get('correction'))
        elif a=='finalize':out=g.finalize(cfg['task_id'],actor,cfg['artifacts'])
        elif a=='resubmit':out=g.resubmit(cfg['task_id'],actor,cfg['source_review_id'],cfg['correction_evidence'])
        elif a=='handoff':out=g.handoff(actor,cfg['next_action'],summary=cfg.get('summary'))
        elif a=='op-intent':out=g.operation_intent(cfg['task_id'],actor,cfg['action'],cfg['resources'],cfg['provider'],
            cfg['resource'],cfg['request'],amount=cfg.get('amount'),artifact_refs=cfg.get('artifact_refs'),
            retry_reference=cfg.get('retry_reference'))
        print(json.dumps(out,indent=2,sort_keys=True));return 0
    except (Unauthorized,StateError,ValueError,KeyError,OSError) as exc:
        print(json.dumps({'error':str(exc),'status':'DENIED_OR_BLOCKED'}),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
