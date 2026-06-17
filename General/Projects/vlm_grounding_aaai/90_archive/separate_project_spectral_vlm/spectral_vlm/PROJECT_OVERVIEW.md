# Spectral VLM Hallucination Forensics — Project Overview

*Source: Visual Faithfulness Project Handbook (Tab 16, Project Recap). This is a separate project from [[10_paper/PAPER_TRACK_FROZEN_v2.md|PAPER_TRACK_FROZEN_v2]]. Related research theme: VLM reliability and faithfulness.*

---

## Core Problem

A Vision-Language Model is a **multimodal communication channel**. We do not know where the visual signal degrades. The hypothesis: hallucination is primarily a spectral rank collapse at the Projector (Station T), where the high-resolution visual signal from CLIP is discarded in favor of linguistic priors.

---

## Three-Station Framework

| Station | Component | Dim | Role |
|---|---|---|---|
| **F** (Features) | CLIP ViT-L vision encoder output | 1024-D | Raw perceptual information |
| **T** (Transition) | MLP Projector output | 4096-D | Visual→linguistic alignment |
| **z** (Semantic) | LLM final hidden state | 4096-D | Fused multimodal representation |

The pipeline is: X → F → T → z_out

**Key diagnostic ratio:** R_llm = Δ_out / Δ_proj. Low ratio = attentional bottleneck (visual signal present at input but ignored).

---

## Research Hypotheses

### H1: Projector Bottleneck
Spectral Efficiency η < 0.5 predicts hallucination with AUC > 0.70. The projector causes ~55% rank drop (eRank: 647→412) despite the 1024→4096 dimensional expansion.

### H2: Complexity Scaling
η drops as visual complexity (object density) increases. Simple scenes (1-2 objects) → η ≈ 0.75. Complex scenes (5+ objects) → η ≈ 0.45.

### H3: Cognitive Failure Mode
~25% of errors show high η + high Δ but still hallucinate. The LLM ignores available visual signal. Fixing the projector alone won't solve everything.

### H4: Spectral Steering (Intervention)
PSC (Principal Subspace Calibration) — masking nuisance axes and boosting mid-spectrum eigenvectors — improves accuracy ≥ 3 points without retraining. See [[PSC_METHODS]].

---

## Failure Mode Taxonomy

| Type | Signature | Interpretation |
|---|---|---|
| Perceptual failure | Low eRank(F), low Δ | Encoder didn't extract signal |
| Projector failure | Low η, high Δ at F | Projector compressed/lost signal |
| Cognitive failure | High η, high Δ, still hallucinates | LLM ignores available visual input |

---

## Dataset Strategy

| Tier | Dataset | n | Goal |
|---|---|---|---|
| 1 | COCO val2017 stratified | 200 | Establish spectral floors, validate η |
| 2 | POPE (Random + Popular + Adversarial) | 3000 | Link η to hallucination rate; ROC curves |
| 3 | Conflict probing (blue oranges, etc.) | 100 | Prove H3 (cognitive failure via causal patching) |

For Tier 1, four scene categories: single-object, multi-object, text-heavy, texture-rich.

---

## Spectral Floors (Baselines)

Expected η for null inputs:
- White noise → η ≈ 1.0 (high rank, uniform activation)
- Blank gray → η ≈ 0.6
- Perlin texture → η ≈ 0.5

---

## Timeline (120–180 hours)

| Phase | Hours | Goal |
|---|---|---|
| Phase 1: Build | 30–40 | Pipeline + metric implementation + spectral floors |
| Phase 2: Understand | 50–70 | POPE evaluation + failure taxonomy + PSC intervention |
| Phase 3: Distill | 40–70 | Figures + 4-6 page workshop paper |

Weekly schedule (40 hr/week):
- **Week 1–2**: Code + Tier 1 exploration
- **Week 3**: POPE full evaluation
- **Week 4**: PSC intervention test
- **Week 5**: Conflict probing / causal patching
- **Week 6**: Paper draft

---

## Success Criteria

- η achieves AUC > 0.70 on POPE (p < 0.001, consistent across 3 subsets)
- PSC improves accuracy ≥ 3 points
- 4–6 page workshop paper with 5 core figures

---

## The Story

"VLMs fail not because they can't see, but because they compress visual information too aggressively before the language model can use it. We introduce spectral efficiency η to quantify this compression and show that η < 0.5 predicts 78% of hallucinations on POPE. Our three-station framework reveals that the projector—not the vision encoder—is the primary bottleneck, and simple spectral interventions can recover 3+ points of accuracy without retraining."

---

## See Also

- [[METRIC_DEFINITIONS]] — precise math for all metrics
- [[PSC_METHODS]] — the 7 PSC intervention variants
- [[RESEARCH_DIRECTIONS]] — 6 directions, 30 micro-experiments
- [[THEORETICAL_BACKGROUND]] — physics/geometry foundations
