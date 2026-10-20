# Ampgent-inspired reusable marketing workflow library (0.7.0)

Each **master** is separately instantiable by a capable agent without Python or Git. Modules are instructions/contracts, not completed provider actions. Optional helper tools are in the developer repo. Default manual/one-off; no real ad/CRM/website writes.

| Module | Stage | Gate |
| --- | --- | --- |
| [marketing-research-plan](marketing-research-plan/README.md) | research_plan | plan-scope |
| [marketing-keyword-discovery](marketing-keyword-discovery/README.md) | research_discovery | keyword-coverage |
| [marketing-competitor-execution](marketing-competitor-execution/README.md) | competitor_observation | evidence-integrity |
| [marketing-research-quality-review](marketing-research-quality-review/README.md) | quality | qc-independent |
| [marketing-evidence-consolidation](marketing-evidence-consolidation/README.md) | independent module | consolidation |
| [marketing-opportunity-scoring](marketing-opportunity-scoring/README.md) | independent module | scoring |
| [marketing-offer-strategy](marketing-offer-strategy/README.md) | offer_hypothesis | offer-claims |
| [marketing-offer-deliverability](marketing-offer-deliverability/README.md) | offer_truth | deliverability |
| [marketing-ad-copy](marketing-ad-copy/README.md) | independent module | copy-semantic |
| [marketing-creative-brief](marketing-creative-brief/README.md) | independent module | brief-visual |
| [marketing-image-generation](marketing-image-generation/README.md) | independent module | image-pixel |
| [marketing-creative-quality](marketing-creative-quality/README.md) | independent module | image-pixel |
| [marketing-brand-verification](marketing-brand-verification/README.md) | independent module | brand-integrity |
| [marketing-meta-campaign-preparation](marketing-meta-campaign-preparation/README.md) | independent module | campaign-plan |
| [marketing-crm-preparation](marketing-crm-preparation/README.md) | independent module | crm-routing |
| [marketing-landing-page-setup](marketing-landing-page-setup/README.md) | independent module | landing-readiness |
| [marketing-tracking-verification](marketing-tracking-verification/README.md) | independent module | conversion-truth |
| [marketing-integration-readiness](marketing-integration-readiness/README.md) | independent module | integration-readiness |
| [marketing-launch-approval](marketing-launch-approval/README.md) | independent module | launch-permit |
| [marketing-campaign-monitoring](marketing-campaign-monitoring/README.md) | independent module | monitoring-evidence |
| [marketing-optimization](marketing-optimization/README.md) | independent module | optimization-authorization |
| [marketing-lifecycle-compound](marketing-lifecycle-compound/README.md) | full lifecycle | human launch-permit + exact child QC |

## Three separate evidentiary states

1. **OBSERVED_COMPETITOR**: public ad/source with date, source limitations, actual observed offer. Not proof of our product features, results or a live ad being delivered.
2. **HYPOTHESIS**: a proposed buyer benefit/price/creative mechanism. Not a promise; downstream copy/media cannot use unverified deliverability claims.
3. **VERIFIED_DELIVERABLE**: actual owner-accepted versioned product capability, commercial terms and scope supported by authoritative evidence. Change invalidates dependent creative and launch QA.

Research QA PASS never means launching/spending is authorized. Image QC PASS never means creative placement or Meta configured status PASS. Approval for *PAUSED staging* is distinct from *live activation*; live publication always defaults to a separate authenticated human permit and provider readback. Tracking terms Schedule/Good Lead/Purchase have distinct sources of truth.

## Usage

Read a module README and `template.yaml`; supply required parameters and real versioned input references; instantiate under `agent-files/` with pinned SHA; work stepwise with source evidence, reviews, human gates and handoffs. To compose, use `marketing-lifecycle-compound` or smaller approved child sets. All instances begin CREATED, not completed. Templates are protected; only `agent-files/` is normally writable.

**Source grounding:** `temp/research/candidate-templates/{CATALOG,CREATIVE-CATALOG,OPERATIONS-CATALOG}.md`, `temp/research/creative-production/QA-GATES-AND-APPROVALS.md` and `temp/research/campaign-operations/{WORKFLOW-MODEL,CRM-TRACKING-LESSONS}.md` in the public development repository. These are historical reconstruction and candidate design, not provider verification in this run.