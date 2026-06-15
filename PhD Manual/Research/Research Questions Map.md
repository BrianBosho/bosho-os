---
type: research-map
status: active
tags: [research, questions, synthesis]
---

# Research Questions Map

## Purpose

Turn broad curiosity into research questions, concepts, reading plans, and project candidates.

This is the bridge between the raw idea layer and [[02_Projects/Project Pipeline]].

See also:

- [[01_Research/Research Section Index]]
- [[01_Research/Formal Research Questions]]
- [[01_Research/Glossary]]
- [[03_People/People and Labs Map]]

## Curiosities

- How does visual evidence flow through a vision-language model?
- When does a VLM answer from the image rather than from language priors?
- Can a model reliably judge whether its own answer is visually grounded?
- Are grounding failures visible in intermediate representations?
- Can mechanistic interpretability expose visual circuits or evidence pathways in VLMs?
- Can information theory provide a rigorous language for visual grounding failures?
- How do explainability and interpretability methods from medical AI transfer to multimodal foundation models?

## Informal Research Directions

### VLM grounding and self-evaluation

Can VLMs detect when their answers are unsupported, weakly supported, or contradicted by visual evidence?

Connected notes:

- [[01_Research/VLM Grounding]]
- [[02_Projects/Active/VLM Self-Evaluation and Grounding Reliability]]

### Mechanistic interpretability for visual evidence

Can internal states, attention heads, projected visual tokens, or circuits explain when visual information is used or ignored?

Connected notes:

- [[01_Research/Mechanistic Interpretability]]
- [[02_Projects/Sparks/Mechanistic Interpretability of Visual Circuits in VLMs]]

### Information-theoretic account of grounding

Can grounding be described as preservation of task-relevant visual information through the model pipeline?

Connected notes:

- [[01_Research/Information-Theoretic Vision]]
- [[02_Projects/Candidates/Information-Theoretic Framework for Visual Grounding]]

### FEUP / Portuguese visual computing fit

Can work from FEUP, INESC TEC, and the Portuguese visual computing ecosystem provide methods, collaborators, or application areas for trustworthy multimodal AI?

Connected notes:

- [[03_People/Portuguese AI and Visual Computing Ecosystem]]
- [[04_Program_Admin/Program_Contacts/Jaime Cardoso]]

## Formal Research Questions

Detailed versions live in [[01_Research/Formal Research Questions]].

### Grounding evaluation

- How accurately can a VLM estimate whether its generated answer is supported by the image?
- What failure modes appear when self-evaluation is separated from answer generation?
- Which prompt, model, or benchmark factors make self-evaluation unreliable?

### Representation and intervention

- Can grounded and ungrounded answers be distinguished from intermediate activations?
- Which model components preserve or discard visual evidence?
- Can activation patching or causal tracing identify pathways responsible for hallucination?

### Information theory

- What measurable proxy for visual mutual information can be used in practical VLM experiments?
- Can grounding failures be modeled as loss of task-relevant visual information?
- Which training or evaluation objectives actually constrain the model to preserve visual evidence?

### FEUP / applied trustworthy AI

- Which FEUP/INESC TEC explainability methods are closest to VLM grounding and interpretability?
- Are medical AI or decision-support settings useful testbeds for grounded multimodal explanations?
- Which local researchers or students have methods that can be adapted to VLMs?

## Concepts / Glossary Seeds

- visual grounding
- hallucination
- self-evaluation
- calibration
- uncertainty elicitation
- mechanistic interpretability
- causal tracing
- activation patching
- sparse autoencoders
- visual tokens
- cross-modal projection
- mutual information
- entropy
- data processing inequality
- information bottleneck
- explainability
- trustworthy AI
- medical decision support

## Reading List Seeds

- [[01_Research/Reading Map]]
- [[01_Research/Paper Inbox]]

## Key Labs

- FEUP / INESC TEC / VCMI
- CMU machine learning, vision, and AI safety-adjacent groups
- Anthropic interpretability and safety teams
- OpenAI safety and evaluations teams
- MATS mentor groups
- Cambridge AI Safety Hub
- Cambridge Boston Alignment Initiative

## Key Figures

- Jaime Cardoso
- FEUP / VCMI students and postdocs to identify
- Aashiq
- Virginia Smith
- Luis Teixeira

## Possible Project Conversions

| Direction | Pipeline target | Next artifact |
|---|---|---|
| VLM self-evaluation | Active project | Two-page project brief |
| Information-theoretic visual grounding | Candidate | One-page glossary |
| VLM mechanistic interpretability | Spark | Tool/model map |
| FEUP visual computing fit | People/research map | Portuguese ecosystem map |

## Next Actions

- Convert the strongest informal directions into one-page question notes.
- Add paper notes for the FEUP/Cardoso resources in [[01_Research/Paper Inbox]].
- Ask Jaime which FEUP researchers or students are closest to visual grounding, explainability, interpretability, and trustworthy AI.
