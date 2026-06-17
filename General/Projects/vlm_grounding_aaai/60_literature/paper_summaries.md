# Literature Review: Consolidated Paper Summaries

This document consolidates the reviews of the 21 foundational and adjacent papers relevant to our AAAI visual grounding project. The papers are organized into 5 thematic groups.

## Table of Contents
- [Vision-Aware & LLM Self-Evaluation / Uncertainty](#vision-aware-llm-self-evaluation-uncertainty)
  - [VAUQ: Vision-Aware Uncertainty Quantification for LVLM Self-Evaluation](#vauq-vision-aware-uncertainty-quantification-for-lvlm-self-evaluation)
  - [Language Models (Mostly) Know What They Know](#language-models-mostly-know-what-they-know)
  - [Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation](#semantic-uncertainty-linguistic-invariances-for-uncertainty-estimation-in-natural-language-generation)
  - [Uncertainty-Aware Evaluation for Vision-Language Models](#uncertainty-aware-evaluation-for-vision-language-models)
- [Decoding-Time Grounding & Hallucination Interventions](#decoding-time-grounding-hallucination-interventions)
  - [Mitigating Object Hallucinations in Large Vision-Language Models through Visual Contrastive Decoding](#mitigating-object-hallucinations-in-large-vision-language-models-through-visual-contrastive-decoding)
  - [Multi-Modal Hallucination Control by Visual Information Grounding](#multi-modal-hallucination-control-by-visual-information-grounding)
  - [Curing Semantic Drift: A Dynamic Approach to Grounding Generation in Large Vision-Language Models](#curing-semantic-drift-a-dynamic-approach-to-grounding-generation-in-large-vision-language-models)
- [Internal Representation Mechanics & Probing](#internal-representation-mechanics-probing)
  - [Beyond Logit Lens: Contextual Embeddings for Robust Hallucination Detection & Grounding in VLMs](#beyond-logit-lens-contextual-embeddings-for-robust-hallucination-detection-grounding-in-vlms)
  - [INSIDE: LLMs' Internal States Retain the Power of Hallucination Detection](#inside-llms-internal-states-retain-the-power-of-hallucination-detection)
  - [HaloScope: Harnessing Unlabeled LLM Generations for Hallucination Detection](#haloscope-harnessing-unlabeled-llm-generations-for-hallucination-detection)
  - [Hidden in plain sight: VLMs overlook their visual representations](#hidden-in-plain-sight-vlms-overlook-their-visual-representations)
- [Causal Attribution & Explainability Frameworks](#causal-attribution-explainability-frameworks)
  - [ERASER: A Benchmark to Evaluate Rationalized NLP Models](#eraser-a-benchmark-to-evaluate-rationalized-nlp-models)
  - [A Benchmark for Interpretability Methods in Deep Neural Networks](#a-benchmark-for-interpretability-methods-in-deep-neural-networks)
  - [What's in the Image? A Deep-Dive into the Vision of Vision Language Models](#whats-in-the-image-a-deep-dive-into-the-vision-of-vision-language-models)
  - [F-LMM: Grounding Frozen Large Multimodal Models](#f-lmm-grounding-frozen-large-multimodal-models)
- [Hallucination Benchmarks & Evaluation Substrates](#hallucination-benchmarks-evaluation-substrates)
  - [Object Hallucination in Image Captioning](#object-hallucination-in-image-captioning)
  - [AMBER: An LLM-free Multi-dimensional Benchmark for MLLMs Hallucination Evaluation](#amber-an-llm-free-multi-dimensional-benchmark-for-mllms-hallucination-evaluation)
  - [Aligning Large Multimodal Models with Factually Augmented RLHF](#aligning-large-multimodal-models-with-factually-augmented-rlhf)
  - [HallusionBench: An Advanced Diagnostic Suite for Entangled Language Hallucination and Visual Illusion in Large Vision-Language Models](#hallusionbench-an-advanced-diagnostic-suite-for-entangled-language-hallucination-and-visual-illusion-in-large-vision-language-models)
  - [FaithScore: Fine-grained Evaluations of Hallucinations in Large Vision-Language Models](#faithscore-fine-grained-evaluations-of-hallucinations-in-large-vision-language-models)
  - [Evaluating Object Hallucination in Large Vision-Language Models](#evaluating-object-hallucination-in-large-vision-language-models)

---

## Vision-Aware & LLM Self-Evaluation / Uncertainty

> [!NOTE]
> This category explores how language models and vision-language models assess their own performance, correctness, and dependency on visual context. It details the shift from output-level confidence scoring (P(True), Semantic Uncertainty) to vision-aware uncertainty measures (VAUQ, Uncertainty-Aware Evaluation). These works establish the context for measuring when a model's generation is grounded in visual evidence versus relying blindly on text priors.

### VAUQ: Vision-Aware Uncertainty Quantification for LVLM Self-Evaluation
- **ArXiv Link:** [arXiv:2602.21054](https://arxiv.org/abs/2602.21054) | [PDF](https://arxiv.org/pdf/2602.21054)
- **Metadata:** Tier 1 | Serves CQ: [2, 7] | Role: neighbor

**What it does:** Proposes a vision-aware uncertainty quantification framework for LVLM self-evaluation that explicitly measures how strongly a model's output depends on visual evidence. It introduces the Image-Information Score (IS) to capture uncertainty reduction attributable to visual input and an unsupervised core-region masking strategy.

**Mechanism:** It computes an Image-Information Score (IS) which measures the difference in predictive uncertainty (entropy) between predictions conditioned on the full image and predictions on core-masked regions, combined with baseline predictive entropy to yield a training-free correctness score.

**Difference from us:** VAUQ focuses on overall answer correctness (output-level self-evaluation) and uses region masking to test dependence via scalar scores, whereas we focus on per-token, internal state, and decision-level causal spatial grounding.

**What to reuse:** The framing of LVLM self-evaluation vs standard LLM self-evaluation; the concept of evaluating image-dependence as a core component of correctness.

**What to challenge:** VAUQ relies heavily on output-level uncertainty scalars which do not perfectly localize the internal usage of patches per-token.

**Cite for:** A primary baseline for vision-aware self-evaluation and image-dependence scoring in VLMs.

---

### Language Models (Mostly) Know What They Know
- **ArXiv Link:** [arXiv:2207.05221](https://arxiv.org/abs/2207.05221) | [PDF](https://arxiv.org/pdf/2207.05221)
- **Metadata:** Tier 3 | Serves CQ: [2, 7] | Role: background

**What it does:** Studies whether language models can evaluate the validity of their own claims and predict which questions they will be able to answer correctly. It introduces the P(True) formulation, showing that models can estimate the validity of their answers.

**Mechanism:** Measures P(True) by prompting the model to output yes/no on the correctness of its proposed answers or using the log-probabilities of answer verification tokens.

**Difference from us:** Focuses on text-only LLMs and general semantic correctness rather than visual-grounding dependencies and cross-modal counterfactual image evaluations.

**What to reuse:** The general framing of self-evaluation and the concept of calibration and self-assessment in models.

**What to challenge:** Output-level self-evaluation is heavily influenced by text priors and lacks anchoring in visual inputs, meaning high confidence can exist without visual support.

**Cite for:** Foundational self-evaluation and self-calibration via P(True) in language models.

---

### Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation
- **ArXiv Link:** [arXiv:2302.09664](https://arxiv.org/abs/2302.09664) | [PDF](https://arxiv.org/pdf/2302.09664)
- **Metadata:** Tier 3 | Serves CQ: [2, 7] | Role: background

**What it does:** Proposes Semantic Uncertainty (using Semantic Entropy) to address the problem of semantic equivalence in free-form generation. By clustering semantically identical responses, it measures uncertainty over meanings rather than specific word choices.

**Mechanism:** Generates multiple response samples, groups them using a classifier (like NLI or LLM) to check semantic equivalence, and computes the entropy over these semantic clusters.

**Difference from us:** Operates on text generation outputs to measure linguistic uncertainty, whereas we evaluate spatial visual-grounding dependencies of generated tokens.

**What to reuse:** Semantic grouping concept for free-form responses when analyzing hallucinations.

**What to challenge:** Calculating semantic entropy requires generating multiple samples and clustering them, which is computationally slow and does not map back to visual-image token dependencies.

**Cite for:** Measuring uncertainty in natural language generation via semantic equivalence clustering.

---

### Uncertainty-Aware Evaluation for Vision-Language Models
- **ArXiv Link:** [arXiv:2402.14418](https://arxiv.org/abs/2402.14418) | [PDF](https://arxiv.org/pdf/2402.14418)
- **Metadata:** Tier 2 | Serves CQ: [2, 7] | Role: neighbor

**What it does:** Evaluates 20+ VLMs on multiple-choice VQA using conformal prediction to incorporate uncertainty quantification, showing that VLM accuracy does not align with uncertainty.

**Mechanism:** Applies conformal prediction to construct prediction sets with coverage guarantees, analyzing how uncertainty relates to the language model vs. vision components.

**Difference from us:** Uses output-level conformal prediction sets to bound overall task uncertainty, whereas we analyze fine-grained, token-level visual grounding.

**What to reuse:** The finding that VLM uncertainty is strongly correlated with its language model priors.

**What to challenge:** Multiple-choice prediction sets do not provide localized or causal patch-level explanations for where the model relies on visual evidence.

**Cite for:** Conformal prediction and uncertainty-accuracy misalignment in VLMs.

---

## Decoding-Time Grounding & Hallucination Interventions

> [!NOTE]
> This group covers active intervention methods that modify the model's generation process during inference to calibrate output distributions and mitigate object hallucinations. These approaches contrast with our passive self-evaluation framing by actively altering token selection probabilities using either contrastive decoding distributions (VCD, M3ID) or dynamic reference baselines (Curing Semantic Drift).

### Mitigating Object Hallucinations in Large Vision-Language Models through Visual Contrastive Decoding
- **ArXiv Link:** [arXiv:2311.16922](https://arxiv.org/abs/2311.16922) | [PDF](https://arxiv.org/pdf/2311.16922)
- **Metadata:** Tier 1 | Serves CQ: [1, 7] | Role: foundational

**What it does:** Introduces Visual Contrastive Decoding (VCD), a training-free method to mitigate object hallucinations during text generation.

**Mechanism:** Contrasts output distributions (logits) derived from the original visual input and distorted (noisy/blurred) visual inputs, penalizing tokens triggered by statistical bias or unimodal language priors.

**Difference from us:** VCD uses contrastive decoding to steer generation and relies on distorted images, whereas we use a static, content-free null patch for passive measurement of causal/spatial grounding.

**What to reuse:** The premise that language priors cause object hallucinations; contrastive analysis as a lens on visual dependence.

**What to challenge:** VCD is an active intervention, not an evaluation instrument. Distorting images might introduce out-of-distribution confounds compared to our strict dataset-mean null baseline.

**Cite for:** Contrastive decoding for hallucination mitigation and language prior suppression.

---

### Multi-Modal Hallucination Control by Visual Information Grounding
- **ArXiv Link:** [arXiv:2403.14003](https://arxiv.org/abs/2403.14003) | [PDF](https://arxiv.org/pdf/2403.14003)
- **Metadata:** Tier 2 | Serves CQ: [1, 7] | Role: neighbor

**What it does:** Shows that hallucination stems from excessive reliance on language priors which increases as more tokens are generated. Proposes Multi-Modal Mutual-Information Decoding (M3ID) to amplify visual influence.

**Mechanism:** A sampling method that amplifies the influence of the reference image over the language prior by favoring tokens with higher mutual information with the visual prompt. Also proposes a DPO pairing for training.

**Difference from us:** M3ID intervenes at decoding time to amplify mutual information between image and text, whereas our approach is a passive diagnostic tool assessing per-token causal spatial grounding.

**What to reuse:** The insight that visual reliance decays over decoding steps, and framing hallucination as a drop in image mutual information.

**What to challenge:** Active intervention shifts the underlying token distribution; we want to evaluate the original unsteered model's grounding reliability.

**Cite for:** Decoding-time hallucination control and visual mutual information amplification.

---

### Curing Semantic Drift: A Dynamic Approach to Grounding Generation in Large Vision-Language Models
- **ArXiv Link:** [arXiv:2506.21509](https://arxiv.org/abs/2506.21509) | [PDF](https://arxiv.org/pdf/2506.21509)
- **Metadata:** Tier 1 | Serves CQ: [5, 7] | Role: neighbor

**What it does:** Frames hallucination as a progressive detachment from the image (semantic drift) during decoding. It proposes Dynamic Logits Calibration (DLC), where a visual referee intervenes at the token level during generation to favor visually grounded candidates.

**Mechanism:** At each decoding step, DLC assesses top-k candidates for intrinsic visual relevance and contextual visual coherence against a historical baseline. It computes a relative visual advantage to dynamically calibrate logits and select grounded tokens.

**Difference from us:** It is an active decoding-time intervention (steering) to correct semantic drift, whereas we are building a passive measurement instrument for self-evaluation.

**What to reuse:** The token-level diagnosis framework (showing hallucination is a failure of token selection against linguistic priors) and its evaluation protocol on free-form generation (e.g. CHAIR).

**What to challenge:** Intervention changes the model's natural distribution; our goal is to evaluate the model's unsteered outputs and their inherent visual dependence.

**Cite for:** Token-level grounding evaluation, semantic drift diagnosis, and decoding interventions against language priors.

---

## Internal Representation Mechanics & Probing

> [!NOTE]
> These papers analyze the internal representations of VLMs to detect grounding and hallucination directly from the embedding or activation space. They show that visual features exist inside internal states even when omitted from output decisions (Hidden in Plain Sight, Beyond Logit Lens) and design metrics like EigenScore (INSIDE) or weakly-supervised classifiers (HaloScope) to tap into this dense internal information.

### Beyond Logit Lens: Contextual Embeddings for Robust Hallucination Detection & Grounding in VLMs
- **ArXiv Link:** [arXiv:2411.19187](https://arxiv.org/abs/2411.19187) | [PDF](https://arxiv.org/pdf/2411.19187)
- **Metadata:** Tier 1 | Serves CQ: [3, 7] | Role: neighbor

**What it does:** Introduces ContextualLens, a training-free hallucination detection and grounding technique that leverages contextual token embeddings from middle layers of LMMs rather than standard logit lens methods.

**Mechanism:** Reads internal contextual token embeddings (middle layers) to detect hallucinations and perform grounding across diverse categories (spatial relations, OCR, actions) to yield precise bounding boxes.

**Difference from us:** Uses intermediate token embeddings directly for generalized hallucination detection, whereas we focus on the real-vs-null causal ablation and spatial variance at the final layer.

**What to reuse:** The observation that internal representations contain robust visual evidence, and the evaluation categories (spatial relations, OCR, actions) for grounding.

**What to challenge:** Representation-reading can suffer from anisotropy and does not isolate causal necessity as cleanly as targeted patch ablation.

**Cite for:** Internal-signal hallucination detection and reading contextual embeddings for grounding.

---

### INSIDE: LLMs' Internal States Retain the Power of Hallucination Detection
- **ArXiv Link:** [arXiv:2402.03744](https://arxiv.org/abs/2402.03744) | [PDF](https://arxiv.org/pdf/2402.03744)
- **Metadata:** Tier 2 | Serves CQ: [3, 7] | Role: neighbor

**What it does:** Proposes the INSIDE framework, which uses dense semantic information in LLM internal states to detect hallucinations. Introduces EigenScore to measure response consistency in the embedding space.

**Mechanism:** Computes eigenvalues of the covariance matrix of internal state activations across multiple sampled generations to measure semantic consistency/diversity.

**Difference from us:** Operates on internal activations of text generations without cross-modal image-null counterfactuals, whereas we isolate visual-grounding dependencies using spatial variance and causal ablation.

**What to reuse:** The use of internal activations/states (rather than output logits) as a richer detector of hallucination.

**What to challenge:** EigenScore requires sampling multiple responses and computing covariance matrices, which is computationally expensive and does not localize visual reliance.

**Cite for:** Hallucination detection using dense semantic information in LLM internal states (EigenScore).

---

### HaloScope: Harnessing Unlabeled LLM Generations for Hallucination Detection
- **ArXiv Link:** [arXiv:2409.17504](https://arxiv.org/abs/2409.17504) | [PDF](https://arxiv.org/pdf/2409.17504)
- **Metadata:** Tier 2 | Serves CQ: [3, 7] | Role: neighbor

**What it does:** Introduces a training-free/weakly-supervised hallucination detection framework that trains a classifier on unlabeled generations. Uses an automated membership estimation score to estimate the truthfulness of LLM generations.

**Mechanism:** Approximates a membership estimation score based on semantic similarity of generated content to build a classifier without human labeling.

**Difference from us:** Trains an external classifier on text outputs for offline hallucination detection, whereas we passively measure internal grounding during inference.

**What to reuse:** The concept of utilizing model generations in the wild for training truthfulness detectors.

**What to challenge:** Relies on external training and lacks direct alignment with the model's visual input, making it less suitable for passive self-evaluation.

**Cite for:** Unsupervised/weakly-supervised hallucination detection using unlabeled model outputs.

---

### Hidden in plain sight: VLMs overlook their visual representations
- **ArXiv Link:** [arXiv:2506.08008](https://arxiv.org/abs/2506.08008) | [PDF](https://arxiv.org/pdf/2506.08008)
- **Metadata:** Tier 2 | Serves CQ: [3, 7] | Role: neighbor

**What it does:** Demonstrates that VLMs often fail to utilize visual encoder representations during language decoding, leading to situations where the visual features exist in early layers but are ignored in the final decision.

**Mechanism:** Analyzes the representation overlap and linear probe accuracy of visual encoder features vs. VLM hidden states across layers, highlighting a bottleneck in multimodal integration.

**Difference from us:** Focuses on visual-encoder representation analysis and probing, whereas we measure token-level decision, state, and causal grounding at the language generation boundary.

**What to reuse:** The insight that internal representations can retain visual features even when the final output decision is ungrounded (the state-decision gap).

**What to challenge:** Probing early visual features doesn't give a direct token-level self-evaluation score for generation control.

**Cite for:** The gap between early VLM visual representations and final decoded output decisions.

---

## Causal Attribution & Explainability Frameworks

> [!NOTE]
> This category reviews methods that investigate how models attribute their predictions to specific inputs and how to causally verify this relationship. It covers text classification rationales (ERASER) and deep learning feature attribution baselines (ROAR) alongside VLM cross-attention maps (F-LMM, What's in the Image) to guide our project's spatial localization and causal validation tracks.

### ERASER: A Benchmark to Evaluate Rationalized NLP Models
- **ArXiv Link:** [arXiv:1911.03429](https://arxiv.org/abs/1911.03429) | [PDF](https://arxiv.org/pdf/1911.03429)
- **Metadata:** Tier 2 | Serves CQ: [4, 7] | Role: foundational

**What it does:** Introduces a benchmark for explainability in NLP models, standardizing metrics like comprehensiveness and sufficiency to evaluate rationales (supporting text segments).

**Mechanism:** Measures comprehensiveness (does removing the rationale drop model accuracy?) and sufficiency (is the rationale alone enough to keep prediction accuracy high?).

**Difference from us:** Evaluates text rationales for NLP classification tasks, while we evaluate spatial image patches for VLM grounding.

**What to reuse:** The conceptual definitions of comprehensiveness (causal necessity) and sufficiency.

**What to challenge:** Textual rationale deletion does not account for continuous spatial visual inputs and the distribution shift under visual masking.

**Cite for:** Standardizing comprehensiveness and sufficiency metrics for model rationales and feature attribution.

---

### A Benchmark for Interpretability Methods in Deep Neural Networks
- **ArXiv Link:** [arXiv:1806.10758](https://arxiv.org/abs/1806.10758) | [PDF](https://arxiv.org/pdf/1806.10758)
- **Metadata:** Tier 2 | Serves CQ: [4, 7] | Role: foundational

**What it does:** Proposes the Remove-And-Retrain (ROAR) framework to evaluate feature attribution methods. Argues that perturbing inputs at test-time introduces distribution shift, and retraining is needed to isolate true causal importance.

**Mechanism:** Removes top-k features identified by an attribution method, retrains the model on the masked dataset, and measures the drop in accuracy.

**Difference from us:** Requires full model retraining, whereas we evaluate test-time visual-patch importance under passive zero-shot measurement.

**What to reuse:** The paradigm of evaluating feature attribution via systematic removal and measuring performance drop.

**What to challenge:** Retraining is computationally prohibitive for large VLMs, meaning test-time ablation with proper control baselines (e.g., random/null) is the only practical alternative.

**Cite for:** The Remove-And-Retrain (ROAR) framework and warning about distribution shifts in feature perturbation.

---

### What's in the Image? A Deep-Dive into the Vision of Vision Language Models
- **ArXiv Link:** [arXiv:2411.17491](https://arxiv.org/abs/2411.17491) | [PDF](https://arxiv.org/pdf/2411.17491)
- **Metadata:** Tier 2 | Serves CQ: [4, 7] | Role: neighbor

**What it does:** Performs a mechanistic study of visual processing in VLMs, focusing on how attention layers route visual token information.

**Mechanism:** Tracks cross-modal attention maps and token similarity across layers to understand how the model represents and utilizes visual patches.

**Difference from us:** Mechanistic visualization of visual token attention, while we measure grounding counterfactually via patch ablation and real-vs-null subtraction.

**What to reuse:** Cross-modal attention routing analysis to understand visual grounding bottlenecks.

**What to challenge:** Attention weights alone are not causal evidence of prediction necessity (attention is not explanation).

**Cite for:** Mechanistic analysis of visual token routing and cross-modal attention in VLMs.

---

### F-LMM: Grounding Frozen Large Multimodal Models
- **ArXiv Link:** [arXiv:2406.05821](https://arxiv.org/abs/2406.05821) | [PDF](https://arxiv.org/pdf/2406.05821)
- **Metadata:** Tier 2 | Serves CQ: [4, 7] | Role: neighbor

**What it does:** Proposes F-LMM to add visual grounding capabilities to frozen LMMs without fine-tuning, mapping word-pixel attention weights to segmentation mask predictions.

**Mechanism:** Utilizes cross-attention maps between text and visual tokens to generate bounding boxes or masks for grounded phrases.

**Difference from us:** Focuses on predicting spatial boundaries (segmentation/detection) from attention weights, whereas we measure internal and causal necessity of visual regions for text decisions.

**What to reuse:** Visual attention maps as a candidate baseline for visual localization.

**What to challenge:** F-LMM relies on attention maps, which have well-known causal limitations (e.g. attention doesn't imply necessity).

**Cite for:** Grounding frozen LMMs using cross-attention maps for spatial localization.

---

## Hallucination Benchmarks & Evaluation Substrates

> [!NOTE]
> This section evaluates existing benchmarks designed to measure multimodal hallucinations. It highlights the design trade-off between open-ended free-form generation metrics (CHAIR, AMBER, MMHal-Bench, FaithScore, HallusionBench) and polling-based yes/no existence queries (POPE). The limitations of open-ended generation benchmarks under partial annotations motivate our choice of POPE as our primary quantitative evaluation format.

### Object Hallucination in Image Captioning
- **ArXiv Link:** [arXiv:1809.02156](https://arxiv.org/abs/1809.02156) | [PDF](https://arxiv.org/pdf/1809.02156)
- **Metadata:** Tier 2 | Serves CQ: [5, 7] | Role: foundational

**What it does:** Introduces the Caption Hallucination Assessment with Image Relevance (CHAIR) metric to evaluate object hallucination in image captioning. Studies the role of language priors in driving hallucinations.

**Mechanism:** Compares nouns in generated captions against ground-truth MSCOCO object segments, computing CHAIR-s (sentence-level) and CHAIR-i (instance-level) scores.

**Difference from us:** Evaluates free-form image captioning models against annotated MSCOCO ground truths, whereas we evaluate per-token grounding in general QA.

**What to reuse:** The analysis of how language priors drive hallucinated content; the concept of matching generated nouns against object labels.

**What to challenge:** CHAIR is highly noisy because missing annotations in the ground-truth database count as false-positive hallucinations.

**Cite for:** CHAIR metric for object hallucination in image captioning.

---

### AMBER: An LLM-free Multi-dimensional Benchmark for MLLMs Hallucination Evaluation
- **ArXiv Link:** [arXiv:2311.07397](https://arxiv.org/abs/2311.07397) | [PDF](https://arxiv.org/pdf/2311.07397)
- **Metadata:** Tier 2 | Serves CQ: [5, 7] | Role: dataset

**What it does:** Proposes AMBER, an evaluation suite for MLLM hallucination that does not rely on an external evaluator (like GPT-4). Evaluates both generative (captioning) and discriminative (yes/no) hallucinations.

**Mechanism:** Measures hallucination rate, attention focus, and boundary localization across existence, attribute, and relation categories.

**Difference from us:** A benchmark suite that measures overall hallucination rates on fixed questions, while our instrument measures grounding across any generated tokens.

**What to reuse:** The separation of hallucination into existence, attributes, and relations.

**What to challenge:** Still suffers from incomplete annotations in open-ended generation, necessitating closed-query evaluation (like POPE).

**Cite for:** AMBER benchmark for evaluating multi-dimensional hallucination in MLLMs without LLM-based evaluators.

---

### Aligning Large Multimodal Models with Factually Augmented RLHF
- **ArXiv Link:** [arXiv:2309.14525](https://arxiv.org/abs/2309.14525) | [PDF](https://arxiv.org/pdf/2309.14525)
- **Metadata:** Tier 2 | Serves CQ: [5, 7] | Role: dataset

**What it does:** Introduces MMHal-Bench and factually augmented RLHF to align LMMs and reduce hallucinations. MMHal-Bench contains 96 questions from 8 categories of images.

**Mechanism:** Evaluates open-ended responses by feeding them, along with ground-truth image facts, to GPT-4, which scores the response from 0 to 6.

**Difference from us:** Relies on an external GPT-4 judge for evaluation, while we propose a training-free, internal evaluation metric that requires no external LLMs.

**What to reuse:** The taxonomy of open-ended question categories.

**What to challenge:** GPT-4 evaluations can be inconsistent, biased towards style, and lack mechanistic connection to the target VLM's internal representations.

**Cite for:** MMHal-Bench and factual RLHF for LMM alignment.

---

### HallusionBench: An Advanced Diagnostic Suite for Entangled Language Hallucination and Visual Illusion in Large Vision-Language Models
- **ArXiv Link:** [arXiv:2310.14566](https://arxiv.org/abs/2310.14566) | [PDF](https://arxiv.org/pdf/2310.14566)
- **Metadata:** Tier 2 | Serves CQ: [5, 7] | Role: dataset

**What it does:** Introduces HallusionBench to separate language hallucination (driven by text priors) from visual illusion (failures in visual perception). Contains 346 images and 1129 expert-crafted question pairs.

**Mechanism:** Employs control groups (questions with and without visual context, or visual variations) to analyze logical consistency and response bias.

**Difference from us:** Focuses on visual QA pair consistency to diagnose failures, whereas we measure the VLM's internal state and decision grounding.

**What to reuse:** The diagnostic breakdown between language priors (hallucination) and perception failures (illusion).

**What to challenge:** Requires hand-crafted question pairs, which limits scalability.

**Cite for:** Diagnostic suite separating language hallucination and visual illusion in VLMs.

---

### FaithScore: Fine-grained Evaluations of Hallucinations in Large Vision-Language Models
- **ArXiv Link:** [arXiv:2311.01477](https://arxiv.org/abs/2311.01477) | [PDF](https://arxiv.org/pdf/2311.01477)
- **Metadata:** Tier 2 | Serves CQ: [5, 7] | Role: neighbor

**What it does:** Introduces FaithScore, a fine-grained, reference-free evaluation metric for free-form responses. It decomposes sentences into atomic facts and verifies them against the image using a VLM.

**Mechanism:** Identifies descriptive claims, extracts atomic facts, and uses a VLM (or external API) to verify each atomic fact against the image.

**Difference from us:** Computes factuality at the text-matching level using an external model, whereas we compute token-level grounding internally during generation.

**What to reuse:** Atomic fact decomposition as a principle for analyzing fine-grained claims.

**What to challenge:** Decomposing facts and running a second VLM for verification adds huge computational overhead and propagates errors from the verification VLM.

**Cite for:** Fine-grained, fact-decomposition based hallucination evaluation (FaithScore).

---

### Evaluating Object Hallucination in Large Vision-Language Models
- **ArXiv Link:** [arXiv:2305.10355](https://arxiv.org/abs/2305.10355) | [PDF](https://arxiv.org/pdf/2305.10355)
- **Metadata:** Tier 2 | Serves CQ: [6, 7] | Role: foundational

**What it does:** Introduces the Polling-based Object Probing Evaluation (POPE) benchmark. Diagnoses that open-ended evaluation is unstable, and proposes binary classification queries (yes/no) to measure hallucinations.

**Mechanism:** Forms binary queries ('Is there a [object] in the image?') for random, popular, and adversarial objects, evaluating accuracy, precision, recall, and F1.

**Difference from us:** A fixed evaluation dataset using closed question formats, while our instrument measures grounding across any generated tokens.

**What to reuse:** The adversarial polling format to bypass visual generation bias and the language model's generation-style confounds.

**What to challenge:** POPE is restricted to simple object existence queries and does not evaluate relations, attributes, or open-ended generation grounding.

**Cite for:** The POPE benchmark and polling-based object hallucination evaluation in VLMs.

---

