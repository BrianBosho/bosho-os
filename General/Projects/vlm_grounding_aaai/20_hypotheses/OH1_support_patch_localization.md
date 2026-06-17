---
title: OH1 - Support Patch Localization and Information Flow
type: hypothesis
status: open
created: 2026-06-16
tags: [hypothesis, spatial, pipeline]
---

# OH1: Support Patches Do Not Correspond to Bounding Box Patches at Layer 32

## Source Trace
- Absorbed from: `20_hypotheses/future_hypotheses.md` (H-A)
- Absorbed from: `70_ideas/developed.md` (Idea 1: Information flow through the pipeline)

## Observation
Early results show that the support patches identified through the grounding process (state/decision/causal) do not correlate meaningfully with the patches inside the COCO bounding box at Layer 32.

## Hypothesis
Support patches are generally not well-correlated with the ground-truth bounding box patches, and masking support patches produces a larger token-probability drop than masking bounding box patches. Visual information is "smeared" across patches during the LLM's processing — the patches no longer contain spatially localized information in the way they did earlier in the pipeline.

## Proposed Experiment: The Localization Ladder
To localize *where* the smearing happens, step back through the pipeline:
1. For a given object token, identify support patches via the grounding procedure (validated causally).
2. Also identify the bounding box patches from COCO annotation (or segmentation mask patches) at Layer 32.
3. Run two separate ablations at Layer 32:
   - Mask the **bounding box patches** → record log P drop for the target token.
   - Mask the **support patches** → record log P drop for the target token.
4. Compare: which ablation produces a larger drop?

**Cascade experiment (if OH1 is confirmed):**
- Ablate at **projector output space** (replace bounding box patches with null patches at projector output) — does this restore the correlation?
- Ablate at **CLIP space** (before the projector).
- Ablate at **pixel level**.

This creates a localization ladder: LLM layers → projector → CLIP encoder → pixel space. The point in the pipeline where bounding box ablation starts to match support patch ablation is where information dispersion begins.

## Status
- **Open**. Connects to `SPATIAL_LOCALIZATION_PROTOCOL_v1` (which ablates at projector output space, not Layer 32).
