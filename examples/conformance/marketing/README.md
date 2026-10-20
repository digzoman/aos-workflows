# Sanitized Ampgent-style workflow examples (Prompt 15)

**These are public test fixtures; not real competitor research, product capability approval, owner authorization, ad assets or Meta/GHL state.** All examples are either genuinely initialized in CREATED state with **zero executed tasks**, or named `-MOCK.json` to denote a *hypothetical* QA scenario. No live external actions were performed.

## Actual file-based CREATED instance fixtures

Under `instances/` are the six completely file-initialized runs, with pinned source bytes, immutable `g0001.yaml`, real initial event, state JSON and handoff from the optional initializer:

- `demo-lifecycle`: 21-module compound lifecycle, all child work still unstarted, **no actual authorization**.
- `demo-research-coaches-r0001`, `demo-research-agencies-r0001`, `demo-research-roofing-r0001`: independent competitor investigation siblings created but not researched.
- `demo-parallel-crm`, `demo-parallel-landing`: independently initialized parallel-eligible planning workflows. Their parameter `verified_offer_ref=PENDING_OWNER_APPROVAL` is **not** a verified offer and no action may advance past the deliverability gate; these illustrate file structure only.

`portfolio-plan-MOCK.json` contains three hypothetical buyers and a simulated reviewed-plan flag solely so deterministic child IDs can be demonstrated; real owner approval is NOT present. `child-proposals-MOCK.json` remains PROPOSED, not active work. `parallel-branches-MOCK.json` illustrates parallel dependency shape but does not assert a QC PASS. `negative-gates-MOCK.json` documents failure propagation.

## Expected routing

1. Plan and keyword discovery -> proposal fanout (3 stable IDs) -> each source sweep -> each independent review -> **ALL accepted evidence join**.
2. Consolidated evidence -> scoring -> **our offer HYPOTHESIS** -> real owner **VERIFIED DELIVERABLE**.
3. Copy / creative branch; CRM and landing are sibling planning paths; tracking depends on CRM+landing; Meta preparation depends on brand-reviewed creatives and deliverable offer.
4. Integration readiness depends on final current copies/reviews and external readback. Human launch permit is a separate approval. **No execution of activation** is in the reusable compound template. Monitoring needs actual provider observations; optimization needs new scoped approval.

Test using `python -m unittest discover -s tests -p test_marketing.py -v` in an optional developer runtime. Manual file-only users need no helper or script.
