# Research Identity

## Core Identity Statement

**I am interested in the science of reliable multimodal perception: how foundation models represent, transform, and use evidence, and how we can tell when their outputs are genuinely grounded rather than merely plausible.**

Even more compactly: I want to build the measurement science for evidence-grounded AI systems.

The deeper through-line across all my work is **evidence use**: when an AI system says something, what inside the model and what in the world actually supports that statement?

## The Central Research Question

**How can we measure whether a model's output is genuinely supported by perceptual evidence rather than by language priors, dataset biases, or accidental correlations?**

This appears in several forms:
- Did the model answer from the image, or from priors?
- Which patches or regions support a concept?
- Does removing visual evidence reduce the probability of the token?
- Can we detect answers that are correct but not grounded?
- Can we distinguish hallucination from blindness, misreading, and annotation gaps?
- Where does semantic information enter, transform, disappear, or become usable for language-level reasoning?

This moves the research focus away from "does the model get the answer right?" toward "what evidence did the model use to get there?"

## Recurring Research Themes

### 1. Correctness is not enough

A model can be:
- **Correct and grounded** — the ideal case
- **Correct but ungrounded** — accidentally correct, prior-driven, fragile; will fail under small perturbation
- **Incorrect but grounded** — a visually based misread
- **Incorrect and ungrounded** — hallucination or language-prior fabrication

Many benchmarks reward the first two equally. The phrase **"correct for the wrong reason"** is central to this research identity.

### 2. Intrinsic measurement instruments

The VLM grounding pipeline is best understood as an instrument — not a model improvement, but a diagnostic tool. It measures token-level evidence through three signal families:

1. **State grounding** — whether internal hidden states shift in response to visual evidence
2. **Decision grounding** — whether the image changes the model's probability distribution and token choice
3. **Causal grounding** — whether removing selected support patches reduces the probability of the corresponding token

### 3. Counterfactual thinking

Hold the text fixed. Hold the generated token sequence fixed. Change the visual evidence. Measure what changes.

Methods: real-vs-null image comparison, teacher-forced counterfactual scoring, patch ablations, corruption sensitivity, targeted vs. random ablation, and enhancement analysis.

### 4. Semantic information flow

- What semantic information is present in visual patch embeddings?
- How is that information transformed by the projector?
- Which layers preserve, distort, or suppress it?
- When does information become usable for next-token prediction?
- How does grounded information differ from prior-driven information?

This connects visual grounding to representation geometry, probing, and information flow — a bridge into mechanistic interpretability.

### 5. Failure taxonomy

"Hallucination" is too coarse. The real taxonomy:
- **Hallucination** — model asserts something absent
- **Blindness** — relevant evidence present but not used
- **Misread** — visual evidence used but interpreted incorrectly
- **Annotation gap** — label is incomplete, not model failure
- **Prior-driven correctness** — accidentally right because of learned co-occurrence

### 6. Reliability in real-world perception

Application motivation comes from: mobility and transport, medical visual question answering (MedVQA), edge AI and low-resource contexts, safety-critical decision support. These domains make the grounding problem concrete and high-stakes.

## Research Identity Map

| Dimension | Description |
|---|---|
| Core identity | Evidence-grounded multimodal intelligence |
| Main question | When a model says something, what evidence supports it? |
| Current object of study | Vision-language models |
| Method family | Intrinsic, counterfactual, token-level grounding metrics |
| Key tools | Teacher forcing, real-vs-null baselines, hidden-state shifts, token probability shifts, patch ablations, perturbation analysis |
| Failure modes studied | Hallucination, blindness, accidentally correct answers, misreads, annotation gaps |
| Long-term intellectual home | Mechanistic evaluation, trustworthy multimodal AI, representation-level reliability |
| Application motivations | Medical AI, mobility, transport, low-resource perception, safety-critical systems |

## Three-Pillar Research Agenda

### Pillar 1: Evidence-grounded multimodal models
**Core question:** Are model outputs actually supported by perceptual evidence?

Projects: real-vs-null grounding metrics; token-level visual evidence dependence; patch-level causal support; hallucination/correctness decomposition; grounding under corruptions and distribution shift.

Venues: ICLR, NeurIPS, ICML, CVPR, ICCV, ECCV, ACL/EMNLP for multimodal NLP angles, TMLR.

### Pillar 2: Representation and mechanism of evidence use
**Core question:** Where is evidence encoded, transformed, lost, or causally used inside the model?

Projects: layerwise semantic information in VLMs; vision encoder/projector analysis; real/null subspace analysis; encoding-versus-use decomposition; mechanistic studies of hallucination and grounding failure.

Venues: ICLR, NeurIPS, ICML, TMLR, mechanistic interpretability workshops.

### Pillar 3: Reliability under missing and low-resource context
**Core question:** How can models remain reliable when the evidence needed for reasoning is missing, private, noisy, or scarce?

Projects: federated graph learning with missing neighbor context (FedProp); low-resource traffic scene understanding; MedVQA under privacy/domain constraints; weak supervision and dataset bootstrapping; grounding evaluation in underrepresented environments.

Venues: NeurIPS/ICLR/ICML for methods, CVPR/ICCV/ECCV for vision, ML4H for medical AI.

### How the pillars connect

- Pillar 1 asks: Does the model use evidence?
- Pillar 2 asks: How is evidence represented and used internally?
- Pillar 3 asks: What happens when evidence is incomplete or scarce?

## Researcher Temperament

Repeatedly drawn to:
- A diagnostic instrument, not a benchmark result
- A conceptual decomposition and a new way of measuring something important
- A bridge between empirical behavior and mechanism
- A method that reveals hidden structure

Repeatedly dissatisfied with:
- Leaderboard chasing and small benchmark improvements
- Narrow engineering tweaks without a strong question
- Application papers without conceptual depth

**Natural research style:** Notice a conceptual confusion → name the distinction clearly → design a counterfactual or diagnostic protocol → measure across models or datasets → show that standard metrics hide something important → propose a better evaluation or analysis framework.

## Research Identity in Different Registers

**For research conversations:** My research focuses on reliable multimodal foundation models, especially how they represent and use perceptual evidence. I develop intrinsic, counterfactual, and causal evaluation methods to distinguish genuinely grounded outputs from prior-driven or accidentally correct ones.

**For a PhD statement:** I am interested in mechanistic evaluation of multimodal models: measuring how semantic evidence flows from visual inputs through internal representations into language-level decisions, and using this to diagnose hallucination, blindness, and ungrounded correctness.

**For a short email:** My interests are in trustworthy multimodal perception, with a focus on visual grounding, hallucination analysis, and intrinsic methods for testing whether model outputs are supported by evidence.

**For the most ambitious formulation:** I want to build the measurement science for evidence-grounded AI systems.

## Advisor and Lab Fit

Best fit: advisors interested in trustworthy machine learning, multimodal foundation models, interpretability and explainability, robust perception, evaluation of generative AI systems, causal analysis of model behavior, representation learning, or AI safety-adjacent reliability.

The ideal advisor does not need to work on exactly the same current method. The deeper fit is with people who care about model reliability, evidence, representation, and evaluation.

## What This Is Not

- Building better VLMs (improving accuracy)
- Benchmarking models on standard accuracy alone
- Detecting hallucinations only from output text
- Doing generic explainable AI visualizations
- Applying AI to mobility or medicine without a deeper methodological question

Instead: **Developing rigorous methods to determine whether multimodal model outputs are supported by perceptual evidence.**

## Related

- [PhD Strategy](./PhD_Strategy.md)
- [Research Direction](./Research_Direction.md)
- [Artifact Pipeline](./Artifact_Pipeline.md)
- [Technical Skill Development](./Technical_Skill_Development.md)
- [VLM Grounding Research Notes](../12_Research/VLM_Grounding.md)
- [Intrinsic Grounding Instrument](../12_Research/Intrinsic_Grounding_Instrument.md)
