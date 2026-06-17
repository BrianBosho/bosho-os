---
title: VLM Grounding Resources
type: research-resource-map
created: 2026-06-16
tags: [research, vlm, grounding, bibliography, resources, aaai]
---

# VLM Grounding Resources

This note organizes the current project resources by how they support the paper direction:

> Can VLMs evaluate whether their own answers are visually grounded, and where does that self-evaluation fail?

## Priority Reading Order

| Priority | Resource | Why read it |
|---|---|---|
| 0 | [[#Internal progress and reports]] | Establishes what has already been done in this project. |
| 0 | [[#Core self-evaluation paper]] | Direct baseline and comparison point for the self-evaluation framing. |
| 1 | [[#Language priors and visual dependence]] | Supports the central claim that VLM answers can be driven by language priors instead of visual evidence. |
| 1 | [[#Grounding and hallucination control]] | Gives methods and baselines for detecting or reducing hallucination through visual grounding. |
| 2 | [[#Visual-representation failure and robustness]] | Supports broader failure-mode framing and diagnostic experiments. |
| 2 | [[#Grounding datasets and tasks]] | Provides spatial grounding datasets and task definitions for validation. |

## Internal progress and reports

### Visual Grounding in Vision-Language Models - Research Progress Report

- Link: [Google Drive report](https://drive.google.com/file/d/1REJtDVNQLmJMEwt-j5_zcr7G6rkFRLe9/view?usp=sharing)
- Model: `llava-hf/llava-1.5-7b-hf`
- Date in report: March 26, 2026
- Status: collaborator-facing draft

**Project-level takeaway**

The existing work already has a concrete intrinsic-grounding stack:

- **State grounding**: whether token representations move with image evidence.
- **Decision grounding**: whether next-token decisions depend on the image.
- **Causal grounding**: whether specific visual support is necessary under targeted patch ablation.

**Strongest current evidence**

- POPE official adversarial 1K is the strongest current benchmark-backed line.
- CHAIR-200 is useful but requires audit-aware interpretation.
- CHAIR flags are noisy: the report says only 13/80 audited CHAIR-flagged mentions were true fabrications.
- The main baseline uses a real-vs-null protocol with teacher forcing.
- `dataset_mean_patch` is the frozen null baseline.
- Raw Layer-32 space is the frozen primary representation choice.
- Decision interaction metrics are strong for hallucination-style targets.
- Causal metrics are strong on POPE.

**Open issues from the report**

- Need explicit comparisons against simple logit-difference or confidence baselines.
- Need stronger spatial correspondence and occlusion validation.
- Need token-class analysis at scale.
- Need subword-to-word or phrase-level aggregation.
- Need to decide whether V3B replaces or supplements the baseline stack.

## Core self-evaluation paper

### VAUQ: Vision-Aware Uncertainty Quantification for LVLM Self-Evaluation

- arXiv: [2602.21054](https://arxiv.org/abs/2602.21054)
- PDF: [arXiv PDF](https://arxiv.org/pdf/2602.21054)
- alphaXiv: [2602.21054](https://www.alphaxiv.org/abs/2602.21054)
- Role: core baseline and nearest paper.

**Why it matters**

This is the direct comparison point for the current paper direction. VAUQ frames LVLM self-evaluation as vision-aware uncertainty quantification and introduces an image-information style score measuring dependence on visual input.

**How to use it**

- Treat as the primary baseline.
- Identify what VAUQ measures at the output/self-evaluation level.
- Position this project as testing whether self-evaluation is actually grounded in decision, state, or causal visual evidence.

**Questions to extract**

- Does VAUQ evaluate answer correctness, visual dependence, or both?
- Does it localize visual evidence or only score image dependence?
- Where can decision grounding provide extra information beyond VAUQ?

## VLM evaluation and uncertainty

### Uncertainty-Aware Evaluation for Vision-Language Models

- arXiv: [2402.14418](https://arxiv.org/abs/2402.14418)
- PDF: [arXiv PDF](https://arxiv.org/pdf/2402.14418)
- Role: uncertainty and evaluation background.

**Why it matters**

This paper argues that VLM evaluation should consider uncertainty, not just accuracy. It is useful background for explaining why self-evaluation and calibration matter.

**How to use it**

- Cite in related work for uncertainty-aware VLM evaluation.
- Contrast generic uncertainty with vision-aware grounding reliability.

## Language priors and visual dependence

### VLind-Bench: Measuring Language Priors in Large Vision-Language Models

- arXiv: [2406.08702](https://arxiv.org/abs/2406.08702)
- PDF: [arXiv PDF](https://arxiv.org/pdf/2406.08702)
- alphaXiv: [overview](https://www.alphaxiv.org/overview/2406.08702?chatId=new)
- Role: benchmark for language-prior dependence.

**Why it matters**

Directly supports the claim that VLMs can answer from language priors while underusing image information.

**How to use it**

- Use as related work for language-prior confounds.
- Connect to null-image and real-vs-null evaluation.

### MIRAGE: The Illusion of Visual Understanding

- arXiv: [2603.21687](https://arxiv.org/abs/2603.21687)
- PDF: [arXiv PDF](https://arxiv.org/pdf/2603.21687)
- Role: evaluation warning about non-visual reasoning.

**Why it matters**

This paper reports strong performance and detailed reasoning even without image input in some settings. It is useful for motivating clean visual-dependence controls.

**How to use it**

- Cite as evidence that multimodal benchmark performance can be contaminated by textual cues.
- Use to justify null-image controls and private/clean visual-grounding evaluation.

### To See or To Please: Uncovering Visual Sycophancy and Split Beliefs in VLMs

- arXiv: [2603.18373](https://arxiv.org/abs/2603.18373)
- alphaXiv: [2603.18373](https://www.alphaxiv.org/abs/2603.18373)
- Role: recent diagnostic framing around visual dependence and answer decoding.

**Why it matters**

It introduces a visual-sycophancy / split-belief framing: internal evidence may be present while the decoded answer follows another pressure.

**How to use it**

- Use as related work for separating perception, visual dependency, and output alignment.
- Compare its diagnostic metrics with this project's state, decision, and causal grounding tracks.

## Grounding and hallucination control

### Multi-Modal Hallucination Control by Visual Information Grounding

- arXiv: [2403.14003](https://arxiv.org/abs/2403.14003)
- PDF: [arXiv PDF](https://arxiv.org/pdf/2403.14003)
- alphaXiv: [2403.14003](https://www.alphaxiv.org/abs/2403.14003)
- Role: contrastive / decoding-side hallucination control.

**Why it matters**

The paper studies hallucination as reduced reliance on the visual prompt during generation and proposes a decoding intervention that amplifies visual information.

**How to use it**

- Related work for contrastive decoding and visual-information grounding.
- Compare decoding-time control with diagnostic self-evaluation.

### Curing Semantic Drift: A Dynamic Approach to Grounding Generation in Large Vision-Language Models

- arXiv: [2506.21509](https://arxiv.org/abs/2506.21509)
- alphaXiv: [2506.21509](https://www.alphaxiv.org/abs/2506.21509)
- Role: token-level grounding and decoding intervention.

**Why it matters**

This paper frames hallucination as semantic drift during decoding and introduces a dynamic visual referee over token candidates.

**How to use it**

- Use for the token-level generation and intervention literature.
- Compare its "visual referee" idea against decision grounding.

### Reducing Hallucinations in Vision-Language Models via Latent Space Steering

- arXiv: [2410.15778](https://arxiv.org/abs/2410.15778)
- alphaXiv: [2410.15778](https://www.alphaxiv.org/abs/2410.15778)
- Role: latent intervention for hallucination reduction.

**Why it matters**

Useful for positioning hallucination as a latent alignment and feature-stability problem.

**How to use it**

- Related work for intervention methods.
- Contrast mitigation with measurement: this project primarily asks whether the model's own answer evaluation is visually supported.

### Beyond Logit Lens: Contextual Embeddings for Robust Hallucination Detection & Grounding in VLMs

- arXiv: [2411.19187](https://arxiv.org/abs/2411.19187)
- alphaXiv: [2411.19187](https://www.alphaxiv.org/abs/2411.19187)
- Role: internal-feature hallucination detection and grounding.

**Why it matters**

This is close to the internal diagnostics side of the project. It uses contextual embeddings rather than only logit-lens-style decoding.

**How to use it**

- Compare with state and decision grounding signals.
- Look for evaluation protocols and categories, especially spatial relations, OCR, actions, and attributes.

## Multimodal grounding methods

### F-LMM: Grounding Frozen Large Multimodal Models

- arXiv: [2406.05821](https://arxiv.org/abs/2406.05821)
- PDF: [arXiv PDF](https://arxiv.org/pdf/2406.05821)
- Role: grounding method and dataset bridge.

**Why it matters**

F-LMM grounds frozen LMMs by translating word-pixel attention weights into mask logits, aiming to preserve conversational ability while adding grounding.

**How to use it**

- Related work for grounding without full model fine-tuning.
- Dataset bridge to referring expression segmentation and panoptic narrative grounding.
- Useful for thinking about whether attention-derived support patches are enough.

## Visual-representation failure and robustness

### Hidden in plain sight: VLMs overlook their visual representations

- arXiv: [2506.08008](https://arxiv.org/abs/2506.08008)
- alphaXiv: [2506.08008](https://www.alphaxiv.org/abs/2506.08008)
- Role: underuse of visual encoder information.

**Why it matters**

This paper argues that VLMs can have visual information available in their encoders but fail to use it effectively through the language model.

**How to use it**

- Very relevant to the state-vs-decision distinction.
- Use to motivate cases where visual representation exists but output or self-evaluation does not depend on it.

### Eyes Wide Shut? Exploring the Visual Shortcomings of Multimodal LLMs

- arXiv: [2401.06209](https://arxiv.org/abs/2401.06209)
- alphaXiv: [2401.06209](https://www.alphaxiv.org/abs/2401.06209)
- Role: visual representation and CLIP-blind-pair failures.

**Why it matters**

Useful for arguing that multimodal LLM failures can originate in the visual backbone or visual representation, not just the language decoder.

**How to use it**

- Related work for visual shortcomings and grounding limitations.
- Use as background for representation-level failure modes.

### What's in the Image? A Deep-Dive into the Vision of Vision Language Models

- arXiv: [2411.17491](https://arxiv.org/abs/2411.17491)
- PDF: [arXiv PDF](https://arxiv.org/pdf/2411.17491)
- Role: attention and visual-processing analysis.

**Why it matters**

This paper empirically studies how VLMs process visual information, especially through attention modules.

**How to use it**

- Related work for mechanistic/diagnostic analysis.
- Useful for positioning layer-wise or attention-based grounding analysis.

### Unveiling the Lack of LVLM Robustness to Fundamental Visual Variations: Why and Path Forward

- arXiv: [2504.16727](https://arxiv.org/abs/2504.16727)
- alphaXiv: [2504.16727](https://www.alphaxiv.org/abs/2504.16727)
- Role: robustness to position, scale, orientation, and context variation.

**Why it matters**

This supports validation experiments where grounding scores should change predictably under visual perturbations.

**How to use it**

- Use for property-matched validation: evidence monotonicity, fragility under perturbation, and spatial robustness.

## Grounding datasets and tasks

### Panoptic Narrative Grounding

- arXiv: [2109.04988](https://arxiv.org/abs/2109.04988)
- PDF: [arXiv PDF](https://arxiv.org/pdf/2109.04988)
- Role: dense/fine-grained spatial grounding task.

**Why it matters**

This defines a spatially fine visual grounding task over natural language narratives and panoptic segmentations.

**How to use it**

- Candidate dataset/task for spatial correspondence validation.
- Especially relevant if the paper needs stronger patch-to-region evidence.

### Modeling Context in Referring Expressions

- arXiv: [1608.00272](https://arxiv.org/abs/1608.00272)
- Role: RefCOCO / RefCOCO+ / RefCOCOg background.

**Why it matters**

This is foundational for referring expression comprehension/generation and context-aware grounding.

**How to use it**

- Dataset background for RefCOCO-style grounding validation.
- Useful if the team tests whether high-support patches overlap with referred objects.

## Duplicate or repeated links

| Link / paper | Note |
|---|---|
| VAUQ: [2602.21054](https://www.alphaxiv.org/abs/2602.21054) | Appears twice; treat as core self-evaluation paper. |
| F-LMM: [2406.05821](https://arxiv.org/pdf/2406.05821) | Appears twice; treat as main multimodal grounding method paper. |
| VLind-Bench: [2406.08702](https://www.alphaxiv.org/overview/2406.08702?chatId=new) | Same paper as arXiv 2406.08702; use arXiv for stable citation. |

## Missing resource bucket

### Contrastive decoding - add more papers

Current seed:

- [Multi-Modal Hallucination Control by Visual Information Grounding](https://arxiv.org/abs/2403.14003)

Add more papers on:

- visual contrastive decoding;
- image-null or image-corrupted decoding;
- decoding-time hallucination mitigation;
- language-prior suppression during VLM generation;
- token-level visual calibration.

## Reading routes by paper direction

### Direction A: VLM self-evaluation and grounding reliability

Read in this order:

1. Internal progress report.
2. VAUQ.
3. Uncertainty-Aware Evaluation for VLMs.
4. Hidden in Plain Sight.
5. To See or To Please.
6. MIRAGE.

Goal: define the gap between output-level self-evaluation, visual uncertainty, and actual visual grounding.

### Direction B: grounding-aware hallucination detection

Read in this order:

1. Internal progress report.
2. Multi-Modal Hallucination Control by Visual Information Grounding.
3. Curing Semantic Drift.
4. Beyond Logit Lens.
5. VLind-Bench.
6. CHAIR audit section of the internal report.

Goal: decide whether hallucination should be framed as language-prior dominance, semantic drift, or failed visual support.

### Direction C: decision grounding as central method

Read in this order:

1. Internal report sections on decision grounding and `decision_delta_p`.
2. VAUQ.
3. Multi-Modal Hallucination Control by Visual Information Grounding.
4. Curing Semantic Drift.
5. Hidden in Plain Sight.

Goal: compare decision grounding to image-information scoring, decoding intervention, and underuse-of-vision claims.

### Direction D: patch attribution and metric reliability

Read in this order:

1. Internal report sections on Stage A/B/C/D, V2/V3/V3B, and open spatial questions.
2. F-LMM.
3. What's in the Image?
4. Panoptic Narrative Grounding.
5. Modeling Context in Referring Expressions.
6. Eyes Wide Shut?

Goal: decide whether patch-level support metrics are measuring spatial evidence or only representation artifacts.

## Immediate literature tasks

| Task                                | Output                                                                                                        |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Summarize VAUQ                      | One-page "what to reuse / what to challenge" note.                                                            |
| Summarize internal report           | Keep/rerun/drop table for existing experiment lines.                                                          |
| Add 3-5 contrastive decoding papers | Expanded decoding-baseline section.                                                                           |
| Extract dataset options             | POPE, CHAIR, RefCOCO, Panoptic Narrative Grounding, MMVP, VLind-Bench.                                        |
| Build related-work matrix           | Rows are papers; columns are self-eval, hallucination, grounding, internal signal, dataset, and intervention. |

