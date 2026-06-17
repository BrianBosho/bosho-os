---
title: Analysis-Paper Scoping — is "detect ungrounded answers" a gap?
type: paper-notes
created: 2026-06-17
tags: [paper, aaai, grounding, vlm, scoping, novelty]
status: active
---

# Analysis-Paper Scoping

Question being tested: is there white space for an **analysis paper** that evaluates whether self-evaluation / grounding methods can detect *ungrounded-but-correct* VLM answers, using behavioral-ungroundedness labels (MIRAGE / DriveBench style)?

**Short answer: the generic version is largely occupied — chiefly by VAUQ. A narrower version survives.** Details below.

## The decisive finding — VAUQ already did much of this

VAUQ ([arXiv:2602.21054](https://arxiv.org/abs/2602.21054)) is not just a baseline. Verified from the paper's HTML:

- **It already ran the "baselines fail under counterfactual images" study.** Pilot (their Figure 1) on the **ViLP** dataset with LLaVA-1.5-7B: Entropy, Verbalized Confidence, Semantic Entropy, and EigenScore *all* degrade on counterfactual images (Entropy −40.9%, EigenScore −26.0%), "strongly driven by language priors and fail to reliably incorporate visual evidence." That is the first half of the thesis we were considering — **already demonstrated.**
- **Its method is close to our instrument.** Image-Information Score = uncertainty reduction with vs. without the image (a with/without-image counterfactual), plus **unsupervised core-region masking** (mask the top-K *most-attended* patches and check that uncertainty rises). That is a correlational cousin of our null-counterfactual + concept-profile ablation.

**What VAUQ does NOT do — the surviving white space:**

| VAUQ | Us (open territory) |
|---|---|
| **Response-level** (explicitly dismisses token-level/object methods as "not response-applicable") | **Token-level** grounding per generated token |
| **Correctness-keyed** ("reliably reflects answer correctness"; self-eval AUROC vs. correct/incorrect) | **Correct-but-ungrounded** decoupling — flag answers that are *right yet not image-dependent* |
| Masks top-**attended** patches; correlational; no random control | **Causal necessity**: targeted-vs-matched-random ablation (+ sufficiency) |
| Null = "blank" image / attention masking | Null = dataset-mean patch (distribution-matched) |

So the cleanest differentiators remain **causal necessity + token-level + the correct-but-ungrounded target**. These are exactly the original instrument's distinctive parts — VAUQ validates the framing but leaves these open.

## The substrate to adopt — ViLP (better than DriveBench for us)

**ViLP — Probing Visual Language Priors in VLMs** ([arXiv:2501.00569](https://arxiv.org/abs/2501.00569), ICML 2025). Each question has **three images** (one solvable from text priors, two requiring visual reasoning) + OOD synthesized images. It is purpose-built to separate prior-driven from vision-driven answers, used on **LLaVA-1.5** (white-box friendly), and already the substrate VAUQ used for its counterfactual pilot.

- **Why it beats DriveBench for our needs:** DriveBench is driving-domain and centers on a mix of (often closed) models; our instrument needs hidden states + patch ablation = open weights. ViLP gives counterfactual triplets on LLaVA-1.5 with no partial-label trap.
- **Role:** primary counterfactual substrate; MIRAGE for breadth/severity context; POPE as controlled anchor.

## New neighbor cluster (add to matrix later)

Label key: **C** = correctness-keyed (labels hallucinated = incorrect) · **U** = ungrounded-but-correct decoupled · **causal** = uses ablation-necessity.

| Paper | arXiv | What it is | Label | Causal? | Role to us |
|---|---|---|---|---|---|
| VAUQ | [2602.21054](https://arxiv.org/abs/2602.21054) | Vision-aware self-eval; IS + core-region masking | C | No | **Primary baseline + nearest method**; owns the counterfactual-failure pilot |
| ViLP | [2501.00569](https://arxiv.org/abs/2501.00569) | Counterfactual-triplet benchmark for visual language priors | — (dataset) | — | **Primary substrate** |
| HARMONY | [2510.22171](https://arxiv.org/abs/2510.22171) | Token-level UE fusing hidden states + MaxProb | C | No | Internal-signal competitor (closest on "internal + token") |
| HalDec-Bench | [2511.20515](https://arxiv.org/abs/2511.20515) / [2603.15253](https://arxiv.org/abs/2603.15253) | Benchmark of hallucination detectors; ~90K correct/incorrect sentences, segment labels | C | No | Detector-evaluation genre template; correctness-keyed |
| EnsemHalDet | [2604.02784](https://arxiv.org/abs/2604.02784) | Ensemble of internal-state hallucination detectors, AUROC | C | No | Internal-signal competitor |
| MIRAGE | [2603.21687](https://arxiv.org/abs/2603.21687) | Image-removal exposes ungrounded success; proposes B-Clean | behavioral | No (re-run) | Phenomenon + breadth label source |
| DriveBench | [2501.04003](https://arxiv.org/abs/2501.04003) | Driving VLM reliability across 17 settings incl. text-only | behavioral | No (re-run) | Phenomenon; domain-shifted, mostly closed models |
| Beyond the Global Scores | [2604.04863](https://arxiv.org/abs/2604.04863) | Per-token grounding as hallucination detector; attention-dispersion | C (token) | No | Closest on token-grounding axis — verify exact claims |

**Pattern:** every method-paper in this cluster is **correctness-keyed**; none isolates correct-but-ungrounded, none uses causal necessity. The behavioral benchmarks (MIRAGE, DriveBench) detect ungroundedness only by the expensive image-removal re-run.

## Implication for paper framing

1. **Do NOT pitch this as "do self-eval methods detect ungrounded answers?"** — VAUQ + ViLP substantially own that question.
2. **The defensible contribution is the intersection the original instrument already targets:** causal-necessity, token-level grounding, evaluated on the **correct-but-ungrounded** slice (the case all correctness-keyed detectors are blind to by construction), on ViLP/POPE with white-box models.
3. This **re-validates the method direction** rather than replacing it with a pure analysis paper — but with much sharper positioning: VAUQ is the primary baseline, ViLP the primary substrate, and "necessity + correct-but-ungrounded" the wedge.

## Still to verify
- **Beyond the Global Scores ([arXiv:2604.04863](https://arxiv.org/abs/2604.04863))** exact metrics/labels — closest on the token-grounding axis.
- Whether any cluster member ever reports an **ungrounded-correct** breakdown (would narrow the wedge further).
