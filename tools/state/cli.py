"""Optional AOS-W local state CLI. No provider writes and no scheduler.

Python + PyYAML optional for pinned YAML graph loading; ordinary agents may follow
scaffold/aos-w/references/STATE-AND-RECOVERY.md instead, with no runtime.
"""
import argparse, json, sys
from pathlib import Path
from state import RunStore, StateError, CorruptLog

def js(text):
    p=Path(text)
    return json.loads(p.read_text()) if p.exists() and p.is_file() else json.loads(text)
def main(argv=None):
    p=argparse.ArgumentParser(description='Optional AOS-W file-only run-state helper (single writer)')
    p.add_argument('run_dir',help='Existing agent-files/instances/<id>/runs/<id>')
    p.add_argument('action',choices=['inspect','recover','checkpoint','handoff','task-start','task-complete',
        'task-fail','task-retry','task-pause','task-resume','task-cancel','task-unblock','review-submit','review-pass','review-revise',
        'run-pause','run-resume','run-cancel','run-fail','op-intent','op-submitted','op-ack','op-unknown',
        'op-reconcile','graph-revise'])
    p.add_argument('--actor',help='JSON string or actor.json with four identity fields')
    p.add_argument('--task')
    p.add_argument('--payload',help='JSON string or path to file with exact event payload')
    p.add_argument('--outputs',help='JSON list of output refs or file path')
    p.add_argument('--repair-tail',action='store_true',help='Explicitly quarantine and remove corrupt JSONL tail')
    p.add_argument('--approve-correction',action='store_true',help='Test/manual correction acknowledgement, not auth')
    p.add_argument('--now',help='Override present time for deterministic tests')
    p.add_argument('--new-revision')
    p.add_argument('--graph-file')
    a=p.parse_args(argv)
    try:
        st=RunStore(a.run_dir)
        if a.action=='inspect':out=st.verified()
        else:
            if not a.actor:raise StateError('Actor is required for a state change')
            actor=js(a.actor);payload=js(a.payload) if a.payload else {}
            if a.action=='recover':out={'issues':st.recover(actor,repair_tail=a.repair_tail),'state':st.verified()}
            elif a.action=='checkpoint':out=st.checkpoint(actor)
            elif a.action=='handoff':out=st.handoff(actor)
            elif a.action=='task-start':out=st.start(a.task,actor)
            elif a.action=='task-complete':out=st.complete(a.task,actor,js(a.outputs) if a.outputs else [])
            elif a.action=='task-fail':out=st.fail(a.task,actor,payload['error_class'],payload['correction'],payload.get('retry_policy'))
            elif a.action=='task-retry':out=st.retry(a.task,actor,approval=a.approve_correction,now=a.now)
            elif a.action=='graph-revise':
                if not a.graph_file or not a.new_revision:raise StateError('--graph-file and --new-revision required')
                out=st.revise(a.new_revision,Path(a.graph_file).read_bytes(),actor,payload)
            elif a.action=='op-intent':
                out=st.operation_intent(a.task,actor,payload['provider'],payload['resource'],payload['request'],payload['approval_id'],payload.get('retry_reference'))
            else:
                mapping={'task-pause':'task_paused','task-resume':'task_resumed','task-cancel':'task_cancelled','task-unblock':'task_unblocked',
                    'review-submit':'task_submitted_review','review-pass':'review_accepted',
                    'review-revise':'review_revise','run-pause':'run_paused','run-resume':'run_resumed',
                    'run-cancel':'run_cancelled','run-fail':'run_failed','op-submitted':'operation_submitted',
                    'op-ack':'operation_ack','op-unknown':'operation_unknown','op-reconcile':'operation_reconciled'}
                out=st.append(mapping[a.action],actor,task_id=a.task,payload=payload)
        print(json.dumps(out,indent=2,sort_keys=True));return 0
    except (ValueError,KeyError,OSError,StateError,CorruptLog) as exc:
        print('BLOCKED: '+str(exc),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
