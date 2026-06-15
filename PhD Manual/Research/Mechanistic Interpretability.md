---
type: research-area
status: seed
tags: [area/interp, area/safety, area/vlm, area/grounding]
---

# Mechanistic Interpretability

## Working role in the PhD

Mechanistic interpretability is not yet the active project. It is a possible deeper layer that could connect visual grounding to internal evidence pathways, circuits, causal tracing, and AI safety.

The key question is not merely:

> Can we explain a VLM?

The sharper question is:

> Can we identify internal mechanisms that determine whether a VLM actually uses visual evidence when producing an answer?

## Connection to current project pipeline

- [[02_Projects/Sparks/Mechanistic Interpretability of Visual Circuits in VLMs]]
- [[01_Research/VLM Grounding]]
- [[01_Research/Research Questions and Directions]]
- [[01_Research/Glossary]]

## Key questions

- Are there identifiable internal mechanisms for visual grounding in VLMs?
- Can we distinguish grounded and ungrounded answers by intervening on internal states?
- Do visual tokens or cross-modal projections contain measurable semantic evidence?
- Are there circuits for object recognition, spatial reasoning, OCR, counting, or hallucination?
- Can model components be causally linked to grounded answer generation?
- Which components route visual information into the language model?
- Are there layers where visual evidence disappears or becomes inaccessible?
- Do grounded and hallucinated answers differ before decoding?
- Are hallucinations caused by absence of visual information, suppression of visual information, or dominance of language priors?

## Method families

### Probing

Use probes to test whether information is present in a representation.

Caution: probing shows that information is decodable. It does not prove the model uses that information.

### Activation patching

Patch activations from a clean or grounded run into a corrupted or hallucinating run. If patching a specific layer or component restores the grounded answer, that component may causally mediate grounding.

### Causal tracing

Locate components that causally influence a model's answer and trace where visual information enters the answer-generation pathway.

### Ablation

Remove or corrupt components, tokens, or features and measure output change.

### Sparse autoencoders

Train sparse feature decompositions over activations to identify features corresponding to objects, attributes, OCR, uncertainty, or grounding-related signals.

## First useful artifact

A tool/model map:

| Model | Open weights? | Supports image? | Interp tooling? | Compute needs | Notes |
|---|---|---|---|---|---|
| LLaVA family | Yes, variants | Yes | likely feasible | moderate | common open VLM target |
| Qwen-VL / Qwen2-VL family | Yes, variants | Yes | to verify | moderate/high | strong open VLM family |
| InternVL family | Yes, variants | Yes | to verify | moderate/high | strong multimodal family |
| BLIP / InstructBLIP | Yes, variants | Yes | feasible for architecture study | moderate | useful for grounding architecture understanding |
| CLIP | Yes | image-text embeddings | strong tooling | low/moderate | useful for representation baseline, not full VLM generation |

Next step:

- verify which model is easiest to run locally or on available compute
- identify whether hidden states and visual tokens are easy to extract
- identify one small grounding task for intervention

## Papers / resources to add

- Cardoso-related FEUP/Portuguese ecosystem work from [[01_Research/Paper Inbox]].
- FEUP OpenReview paper from [[01_Research/Paper Inbox]], if metadata and topic fit check out.

## FEUP / Portugal fit

Use [[03_People/Portuguese AI and Visual Computing Ecosystem]] to identify local researchers, students, and papers that connect mechanistic interpretability to visual computing, explainability, medical AI, or trustworthy AI.

## Candidate first experiment

Question:

> Can internal representations distinguish grounded from ungrounded VLM answers before the answer is generated?

Sketch:

1. Choose an open VLM.
2. Build a small dataset of grounded vs hallucinated answers.
3. Extract hidden states from visual tokens, projector outputs, and language layers.
4. Train simple probes to classify grounded vs ungrounded cases.
5. Validate with counterfactual image perturbations.
6. If promising, attempt activation patching.

Possible output:

- feasibility memo
- tool/model map
- preliminary result table

## Do not over-invest until

- there is a tractable open model
- hidden states are accessible
- there is an intervention method
- there is a small grounding task
- there is a feedback source in mech interp
- the active project has not been neglected

Rule:

> This direction becomes real only when there is a runnable model, a small task, and one causal/intervention experiment.

## Reading links

- [[01_Research/Reading Map]]
- [[01_Research/People and Labs Map]]
- [[01_Research/Glossary]]
