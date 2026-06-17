---
title: OH3 - Contrastive Decoding as a Grounding Baseline
type: hypothesis
status: open
created: 2026-06-16
tags: [hypothesis, baselines, causal]
---

# OH3: Contrastive Decoding as a Grounding Baseline

## Source Trace
- Absorbed from: `20_hypotheses/future_hypotheses.md` (H-C)

## Question
Can contrastive decoding logit difference serve as a strong baseline for grounding?

Contrastive decoding tells us whether a token is hallucinated or not by comparing logits under real vs. corrupted input. This is essentially what the causal grounding track computes.

## Idea
Treat contrastive decoding as the baseline grounding signal. Then show that adding state and decision grounding on top provides additional discriminative value.

## Extension
Can we design a training-free intervention (based on current grounding work) that improves downstream grounding scores? And then, can the grounding signal be used as a training signal?

## Status
- **Open**. `causal_delta_logp_random` (AUC 0.7667 on POPE-1K) is already essentially a contrastive decoding metric. The question is whether this becomes a formal baseline comparison in the paper.
