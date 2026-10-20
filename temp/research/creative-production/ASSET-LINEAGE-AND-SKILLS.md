# Prompt 04, artifact provenance, branding skill and variant management

Source-derived findings are from the restricted files indexed in [SOURCE-INDEX-04.md](SOURCE-INDEX-04.md). All folder/layout/metadata proposals below are for later PRD review, not implemented schemas.

## Observed source packages

V3 and later creative packages commonly carried a source reference, `reference.md`, approved `copy.md`, `notes.md`, semantic audit, editable SVG(s), final PNG(s), selected screenshot/frame, messaging config and Meta staging QA. B6/B7 generated imagery and no-imagery variants, and B8 retained three named variants. Work was committed to GitHub and then read back; the upload proved persistence, not automatically the rendering quality or all placement support. [R51–R66]

Common output concepts include versioned `final-v1.png`, `final.png`, `final-imagery.png`, `final-no-imagery.png` and square variants. These are historical names only. AOS-W should use an explicit artifact manifest because `final.png` can be overwritten/superseded while an earlier selected version remains in history.

## Version and approval lineage, proposed

For each creative, persist identities for
- research source and source-creative family;
- business offer truth/approved adaptation, CTA and target destination;
- source semantic-spine audit version;
- structured primary text, headline, description and on-image text;
- production/art-direction brief revision;
- generated imagery, raster/vector source and tool provenance;
- logo asset version and explicit with/without subline requirement;
- every output variant with format, width/height, image hash and intended placements;
- QC records with which exact artifacts and rubric were checked;
- owner selection, approval, exceptions and supersession date;
- if relevant, later remote repository blob and provider media/creative mapping.

**Observed example B9**, an Oct 17 logo-free source was selected despite unusual pixel dimensions and superseded the previous logo handoff [R77]. Oct 18 approved official-logo portrait/square files became separate staged assets [R78–R80]. These must be represented as different revisions rather than all becoming one undocumented `current`.

## Canonical Ampgent branding

**Observed [R72]:** Do not have an image generator redraw the logo. Approved official exported variants include with/without `AI AGENTS + STAFF` subline. Use the correct version for the specific creative, preserve geometry/color, and roughly 5% visible safe margins. Use brand palette and readable type, avoiding generic glowing AI art.

**Observed optional skill [R73]:** `scratch/skills/add-ampgent-logo/SKILL.md` documents a deterministic helper. It can inspect corners, protect faces/headlines, remove a generated pseudo-logo region where safe, soften the backing, place canonical logo artwork, and produce a blurred-copy square. Its current implementation uses Python/Pillow and is a **non-mandatory external tool**, not the AOS-W runtime. The skill explicitly requires inspecting the actual full image and preview; numeric output alone is insufficient.

## Proposed skill binding and just-in-time loading

AOS-W user requirement says skills may be bundled within master templates, custom templates and active workflow instances, or referenced from installed skills or a repository. A creative step should declare a skill reference at the relevant moment, not load all skills at startup.

Illustrative **non-executable** assignment.
- Source check step -> competitor evidence/source-truth skill.
- Semantic strategy step -> semantic-match/source-anchors skill.
- Copywriter step -> brand voice, ad platform field conventions and policy skill.
- Background generator step -> image prompt and composition skill.
- Logo composite step -> `add-ampgent-logo` skill or equivalent compatible local installed skill. If unavailable, record blocker or manual approved compositing procedure.
- Export step -> file format and square variant guidance.
- Visual QA step -> native/mobile readability inspection skill.
- Meta handoff step -> placement preview/read-back and fingerprint conventions skill.

Proposed references need exact source locator, pinned version/hash, source trust, authorization scope and offline availability/fallback. Never import runnable code from a remote repository automatically merely because a workflow mentions its skill. Skills provide guidance and capability, **not permission to publish or spend**.

## Proposed file arrangement, as a concept only

```text
scaffold/aos-w/
  templates/
    creative-production/
      workflow definition and instructions
      skills/
        semantic-source-review/SKILL.md
        creative-visual-qa/SKILL.md
  agent-files/
    custom-templates/
      brand-campaign/
        workflow definition
        skills/
          house-style/SKILL.md
    workflows/
      example-compound-campaign/
        workflow definition and skills/
    runs/
      creative-run-001/
        source/
        brief/
        copy/
        variants/
          portrait/
          square/
        reviews/
        approvals/
        archive/
        state and history files
        skills/
          run-specific-guidance/SKILL.md
```

The folder names and manifests are **suggested**. They must be reconciled with Prompt 08 schema choices. All normal installed runtime changes remain strictly inside `agent-files/`. AOS-W base operation must remain possible without Git and without a required Python runtime.

## Rendering and storage boundary

A workflow may record an image-generation request and its output, but plain Markdown/YAML cannot itself render an image, inspect placement previews or enforce hard concurrency. Optional host-provided capabilities are needed; absence must yield a truthful pending/blocked state rather than invented success.
