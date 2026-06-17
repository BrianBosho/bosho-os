---
title: Future Work Directions
type: ideas
created: 2026-06-16
tags: [future-work, ideas, paper-directions]
---

# Future Work Directions

These are alternative paper framings and future experiments that were explored but placed out of scope for the current AAAI 2027 paper track.

## Source Trace
- Absorbed from: `90_archive/old_direction_notes/VLM Grounding Synthesis.md`
- Absorbed from: `90_archive/old_direction_notes/VLM Grounding Direction.md`
- Absorbed from: `70_ideas/synthesis.md`

## Direction B: Grounding-aware hallucination detection
**Working question:** Can visual grounding signals distinguish faithful VLM answers from hallucinated answers better than answer-only confidence or self-critique?
**Idea:** Use visual support diagnostics to improve or audit hallucination detection. The main result would be that hallucination is not only an output-level failure, but a grounding mismatch.
**Why it was shelved:** POPE may be too weak or misaligned for the core grounding question; evaluating this requires extremely clean hallucination labels mapped to specific visual support, which goes beyond the scope of a measurement paper.

## Direction C: Decision grounding as the central method
**Working question:** Can decision-grounding signals reveal whether a VLM's answer depends on the right image evidence?
**Idea:** Focus entirely on the `dec_dp_x_cvar` metric.
**Why it was shelved:** The current AAAI paper focuses on the three-track instrument as a whole (State, Decision, Causal) to provide a complete picture, rather than isolating one track as the sole contribution.

## The Smearing Hypothesis / Full Pipeline Information Flow
An extensive study measuring representational alignment (CKA, RDM) between each stage's output (CLIP, Projector, LLM L8, L16, L32) and the ground-truth spatial annotation. 
**Why it was shelved:** This is a dissertation-scale contribution. The current AAAI paper accepts L32 as the final point of decision influence and leaves the layer-by-layer traversal as future work.

## Alternative Null Constructions (N1-N4)
Exploring the effects of patch-shuffle (N3), per-image-mean (N1), and white-noise (N2).
**Why it was shelved:** N0 (dataset-mean patch) proved to be empirically superior for maintaining CLIP distribution properties while stripping semantic content.

## Training-Free Interventions
Can we design a training-free intervention (based on the grounding score) that improves downstream outputs? Can the grounding signal be used as a training objective?
**Why it was shelved:** Scope containment. We must first establish that the instrument works before attempting to use it as an optimization target.
