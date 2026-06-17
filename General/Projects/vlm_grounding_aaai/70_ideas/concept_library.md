---
title: Concept Library
type: ideas
created: 2026-06-16
tags: [concepts, dictionary, grounding, vlm]
---

# Concept Library

This document defines the core concepts explored in this project. 

## Source Trace
- Absorbed from: `70_ideas/inbox.md`
- Absorbed from: `70_ideas/developed.md`
- Absorbed from: `70_ideas/synthesis.md`

## 1. Visual Information Flow (The Localization Ladder)
At each stage of the VLM pipeline (CLIP Encoder → Projector → LLM Layers), visual information is transformed. The "localization ladder" refers to the hypothesis that spatial localization (where a patch corresponds to a specific image region) degrades as you move deeper into the pipeline. Information is "smeared" across hidden states, meaning support patches at Layer 32 may no longer correspond geographically to the original image bounding boxes.

## 2. LLM Dependence on Visual Input
A model can be correct because it genuinely relied on visual evidence, or correct because language priors guessed the answer. Dependence is measured by checking the representational similarity between the hidden states of generated tokens and the image patch hidden states. A token that strongly aligns with specific patch embeddings depends on the visual input.

## 3. Counterfactual Grounding
To isolate true visual dependence from background embedding anisotropy, we use a counterfactual subtraction. We measure the output (hidden states, logits) under the real image, and subtract the output under a "null" image. Any remaining signal is strictly attributable to the visual content.

## 4. Support Patches
The subset of image patches that contribute most strongly to the generation of a specific token. They are identified using a concept profile (Track 2) and validated causally (Track 3) by showing that ablating them causes a significant drop in the token's probability.

## 5. Null Baselines
To perform a counterfactual measurement, a baseline is needed. The `dataset-mean patch` (N0) is the canonical choice: it removes semantic content while preserving the statistical distribution of visual features in the CLIP space. Other nulls include patch-shuffle (N3), per-image-mean (N1), and white-noise (N2).

## 6. Semantic Basis
An exploratory method for determining *what* semantic content a measure picks up. By building a basis of semantic directions from CLIP patch projections and embedding-matrix samples (and subtracting a matched null basis), we can quantify whether a patch represents "dog" or "cat" to the model.

## 7. Patch Logit Lens
An interpretable patch-selection method that decodes patch embeddings directly through the LM head to see what text concepts they most strongly activate, prior to full transformer processing.
