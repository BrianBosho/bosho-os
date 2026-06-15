---
type: reading-map
status: active
tags: [reading, vlm, grounding, interp, info-theory]
---

# Reading Map

## Purpose

Build enough local competence to make good research decisions without drowning in infinite papers.

Reading should support the research compression path:

> curiosity -> research question -> concept/glossary -> paper cluster -> synthesis -> project brief -> experiment.

Related notes:

- [[01_Research/Research Dashboard]]
- [[01_Research/Research Questions and Directions]]
- [[01_Research/Glossary]]
- [[01_Research/People and Labs Map]]

## Weekly target

- 3 light reads
- 1 deep read
- 1 written synthesis or paper note

Do not read indefinitely without producing an artifact.

Every 5-7 papers should produce one of:

- a synthesis memo
- a project brief update
- a comparison table
- a list of gaps
- a proposed experiment

## Priority tiers

- Tier 1: read first. These define the landscape.
- Tier 2: read as a specific research question develops.
- Tier 3: monitor and reference.

## Initial clusters

### Synthesis layer

- [[01_Research/Research Questions Map]] turns raw curiosities into formal questions, concepts, labs, people, and possible project conversions.
- [[01_Research/Paper Inbox]] captures links and PDFs before they are processed into paper notes or reading-map entries.

### Cluster 1: VLM grounding and hallucination

Goal: understand current benchmarks, definitions, and failure modes.

#### Starter papers

- Rohrbach et al. (2018), "Object Hallucination in Image Captioning." EMNLP. First systematic treatment of hallucination in image captioning; introduced the CHAIR metric.
- Li et al. (2023), "POPE: Polling-based Object Probing Evaluation for Object Hallucination in Vision-Language Models." EMNLP. Standard benchmark for measuring object hallucination. Start here for evaluation methods.
- Liu et al. (2023), "Visual Instruction Tuning (LLaVA)." NeurIPS. Canonical open VLM architecture; essential context for VLM grounding experiments.
- Li et al. (2023), "Evaluating Object Hallucination in Large Vision-Language Models." EMNLP. Complements POPE; broader hallucination taxonomy.
- Guan et al. (2023), "HallusionBench: An Advanced Diagnostic Suite for Entangled Language Hallucination and Visual Illusion in Large Vision-Language Models." arXiv. Tests where language priors override visual evidence, directly relevant to the active project hypothesis.

#### Papers to add as reading progresses

-

### Active project reading

This supports:

- [[02_Projects/Active/VLM Self-Evaluation and Grounding Reliability]]

Goal: understand how VLM hallucination, visual grounding, self-evaluation, and claim-level support are currently defined and measured.

Key questions:

- What counts as hallucination in VLMs?
- What counts as visual grounding?
- How are hallucinations benchmarked?
- Can models self-detect unsupported visual claims?
- What datasets/evaluation protocols are reusable?

### Cluster 2: VLM self-evaluation / self-correction

Goal: understand whether models can judge their own groundedness or hallucinations.

#### Starter papers

- Kadavath et al. (2022), "Language Models (Mostly) Know What They Know." Anthropic. Foundational paper on LLM self-knowledge and calibration. Essential framing for the active project's central question.
- Yin et al. (2023), "WOODPECKER: Hallucination Correction for Multimodal Large Language Models." arXiv. Attempts post-hoc self-correction of VLM hallucinations; good contrast case for what self-evaluation can and cannot do.
- Madaan et al. (2023), "Self-Refine: Iterative Refinement with Self-Feedback." NeurIPS. General framework for LLM self-evaluation and iterative improvement; read for methods and limits.
- Xiong et al. (2024), "Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs." ICLR. Directly on calibration of expressed uncertainty; connects to self-evaluation reliability.
- Luo et al. (2023), "HalluciDoctor: Mitigating Hallucinatory Toxicity in Visual Instruction Data." arXiv. Hallucination in instruction-following context; relevant for understanding where self-evaluation fails.

#### Papers to add as reading progresses

-

### Cluster 3: Mechanistic interpretability for multimodal models

Goal: understand whether VLM internals can be probed/intervened on meaningfully.

#### Starter papers

- Elhage et al. (2021), "A Mathematical Framework for Transformer Circuits." Anthropic. Foundational mech interp paper. Read before anything else in this cluster.
- Elhage et al. (2022), "Toy Models of Superposition." Anthropic. Core concept for understanding how models pack features into representations; essential for SAE and circuit work.
- Meng et al. (2022), "Locating and Editing Factual Associations in GPT (ROME)." NeurIPS. Canonical causal tracing method; first major paper on surgical intervention in transformer internals.
- Conmy et al. (2023), "Towards Automated Circuit Discovery for Mechanistic Interpretability." NeurIPS. Automated circuit finding; gives a sense of where the field is heading methodologically.
- Palit et al. (2023), "Towards Vision-Language Mechanistic Interpretability: A Causal Tracing Tool for BLIP-2." arXiv. One of the few direct applications of mech interp to VLMs. Read carefully because this is the gap the Spark project exists to fill.

#### Papers to add as reading progresses

-

### Cluster 4: Information-theoretic / representation-level framing

Goal: find precise ways to talk about semantic information, evidence, representation, and information flow.

These papers are the foundation of [[01_Research/Information-Theoretic Vision]].

#### Starter papers

- Shannon (1948), "A Mathematical Theory of Communication." Bell System Technical Journal. Read the original. The entropy and channel capacity definitions are foundational; the noisy channel theorem is what makes the DPI relevant.
- Cover and Thomas, *Elements of Information Theory* (2nd ed., 2006). The standard reference textbook. Read Chapter 2, entropy and mutual information, and Chapter 7, channel capacity, as foundations; return to other chapters as needed.
- Tishby and Zaslavsky (2015), "Deep Learning and the Information Bottleneck Principle." arXiv:1503.02406. Proposed applying information bottleneck ideas to deep networks. Read as the primary source of the Layer 3 vision.
- Saxe et al. (2018), "On the Information Bottleneck Theory of Deep Learning." ICLR. Important critique and refinement of Tishby. Read this before fully committing to IB framing because it shows where the theory breaks under scrutiny.
- Alemi et al. (2017), "Deep Variational Information Bottleneck." ICLR. Practical variational implementation of IB; bridges the theory to tractable experiments.

#### Papers to add as reading progresses

-

### Cluster 5: FEUP / Portuguese visual computing and explainability

Goal: understand which FEUP, INESC TEC, and VCMI work can become a methods bridge, collaborator bridge, or application area for the PhD.

Related domain track: [[01_Research/Medical VLM Explainability Study Map]].

#### Starter resources

- Cardoso-related mechanistic interpretability / interpretability work: https://ieeexplore.ieee.org/document/11375425 and https://www.authenticus.pt/en/publications/view/1433390. Verify metadata, then decide whether this belongs under mechanistic interpretability, explainability, or applied trustworthy AI.
- Springer book / consolidated reading list: https://www.authenticus.pt/en/publications/view/1433391 and https://link.springer.com/book/10.1007/978-3-032-17611-0. Treat this as a possible foundation for a niche PhD direction; extract chapters, terminology, and bibliography.
- FEUP OpenReview paper: https://openreview.net/pdf?id=nUFSrlJaUr. Verify authors and topic fit, then create a paper note if it connects to VLM grounding, interpretability, or trustworthy AI.

#### Papers to add as reading progresses

-

## Expanded Priority Clusters

Use these clusters to plan reading once the active project brief is stable.

### Cluster 6: VLM architecture foundations

Goal: understand how VLMs are built and where information can be preserved, compressed, or lost.

Tier 1:

- Radford et al. (2021), "Learning Transferable Visual Models From Natural Language Supervision" (CLIP). Foundation for most VLM vision encoders.
- Liu et al. (2023), "Visual Instruction Tuning" (LLaVA). Canonical open VLM architecture.
- Liu et al. (2023), "Improved Baselines with Visual Instruction Tuning" (LLaVA-1.5). Important for projector and resolution changes.
- Li et al. (2023), "BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models." Introduces Q-Former as an explicit bottleneck.
- Dai et al. (2023), "InstructBLIP: Towards General-purpose Vision-Language Models with Instruction Tuning." Standard instruction-tuned BLIP-style baseline.

Tier 2:

- Alayrac et al. (2022), "Flamingo: a Visual Language Model for Few-Shot Learning."
- Zhu et al. (2023), "MiniGPT-4: Enhancing Vision-Language Understanding with Advanced Large Language Models."
- Chen et al. (2023), "PaLI: A Jointly-Scaled Multilingual Language-Image Model."

### Cluster 7: VLM hallucination

Goal: understand definitions, benchmarks, and empirical findings on hallucination.

Tier 1:

- Li et al. (2023), "Evaluating Object Hallucination in Large Vision-Language Models" (POPE).
- Rohrbach et al. (2018), "Object Hallucination in Image Captioning."
- Liu et al. (2024), "HallusionBench: An Advanced Diagnostic Suite for Entangled Language Hallucination and Visual Illusion in Large Vision-Language Models."
- Guan et al. (2024), "HallucinationBench: Evaluating Perceptual, Relational, and Compositional Hallucinations."

Tier 2:

- Sun et al. (2023), "Aligning Large Multimodal Models with Factually Augmented RLHF" (RLHF-V).
- Yin et al. (2023), "WOODPECKER: Hallucination Correction for Multimodal Large Language Models."
- Leng et al. (2024), "Mitigating Object Hallucinations in Large Vision-Language Models through Visual Contrastive Decoding."

### Cluster 8: Self-evaluation and model-as-judge

Goal: understand self-evaluation and self-correction before specializing them to groundedness.

Tier 1:

- Kadavath et al. (2022), "Language Models (Mostly) Know What They Know."
- Shinn et al. (2023), "Reflexion: Language Agents with Verbal Reinforcement Learning."
- Jiang et al. (2023), work on LLM-as-a-judge / model-based evaluation.

Tier 2:

- Lee et al. (2023), "Volcano: Mitigating Multimodal Hallucination through Self-Feedback Hallucination Detection."
- Deng et al. (2024), "STIC: Improving Vision-Language Model with Self-Training on Image Comprehension."
- Zhou et al. (2023), work on analyzing and mitigating object hallucination in large VLMs.

### Cluster 9: Mechanistic interpretability foundations

Goal: master the core transformer methods before extending them to VLMs.

Tier 1:

- Olah et al. (2020), "Zoom In: An Introduction to Circuits."
- Elhage et al. (2021), "A Mathematical Framework for Transformer Circuits."
- Olsson et al. (2022), "In-context Learning and Induction Heads."
- Wang et al. (2022), "Interpretability in the Wild: A Circuit for Indirect Object Identification in GPT-2."
- Meng et al. (2022), "Locating and Editing Factual Associations in GPT" (ROME).

Tier 2:

- Nanda et al. (2023), "Progress measures for grokking via mechanistic interpretability."
- Conmy et al. (2023), "Towards Automated Circuit Discovery for Mechanistic Interpretability."
- Goldowsky-Dill et al. (2023), "Localizing Model Behavior with Path Patching."
- Todd et al. (2023), "Function Vectors in Large Language Models."

### Cluster 10: Sparse autoencoders and feature discovery

Goal: understand SAEs well enough to judge whether they can be adapted to VLM representations.

Tier 1:

- Bricken et al. (2023), "Towards Monosemanticity: Decomposing Language Models With Dictionary Learning."
- Cunningham et al. (2023), "Sparse Autoencoders Find Highly Interpretable Features in Language Models."
- Gao et al. (2024), "Scaling and Evaluating Sparse Autoencoders."

Tier 2:

- Elhage et al. (2022), "Toy Models of Superposition."
- Muhamed et al., Pando / sparse representations and distribution shift.
- Papers on L1 versus TopK regularization, dead feature prevention, and SAE evaluation.

### Cluster 11: Mechanistic interpretability for vision / VLMs

Goal: understand the sparse but growing multimodal interpretability literature.

Tier 1:

- Palit et al. (2023), "Towards Vision-Language Mechanistic Interpretability: A Causal Tracing Tool for LLaVA" or related BLIP/LLaVA causal tracing work.
- Stan and Mihalcea (2024), "LVLM-Interpret: An Interpretability Tool for Large Vision-Language Models."

Tier 2:

- CLIP interpretability papers.
- Attention visualization, GradCAM, and attention rollout papers for VLMs.
- Probing papers for spatial, attributional, and relational properties in VLM representations.

### Cluster 12: Causal methods and counterfactual evaluation

Goal: learn the methods needed to make causal claims about groundedness.

Tier 1:

- Geiger et al. (2022), "Inducing Causal Structure for Interpretable Neural Networks."
- Pearl (2009), *Causality*, chapter 3 on interventions.

Tier 2:

- Vig et al. (2020), "Investigating Gender Bias in Language Models Using Causal Mediation Analysis."
- Counterfactual data augmentation and counterfactual VQA papers.

### Cluster 13: Information theory and representation learning

Goal: build fluency with information-theoretic framing without overcommitting to weak analogies.

Tier 1:

- Tishby and Schwartz-Ziv (2017), "Opening the Black Box of Deep Neural Networks via Information."
- Belghazi et al. (2018), "Mutual Information Neural Estimation" (MINE).

Tier 2:

- Goldfeld and Polyanskiy (2020), "The Information Bottleneck Problem and Its Applications in Machine Learning."
- Alemi et al. (2017), "Deep Variational Information Bottleneck."
- Xie et al., SmartCLIP / causal identifiability for vision-language alignment.

### Cluster 14: Distribution shift and reliable ML

Goal: understand distribution shift as a reliability lens for grounding.

Tier 1:

- Koh et al. (2021), "WILDS: A Benchmark of in-the-Wild Distribution Shifts."
- Taori et al. (2020), "Measuring Robustness to Natural Distribution Shifts in Image Classification."

Tier 2:

- Raghunathan lab papers on distribution shift and reliable ML.
- Pando / sparse representations under distribution shift.

## Reading rule

Do not read indefinitely without producing an artifact.

Every 5–7 papers should produce one of:

- a synthesis memo
- a project brief update
- a comparison table
- a list of gaps
- a proposed experiment
