---
type: research-map
status: active
tags: [research, questions, vlm, grounding, interp, info-theory]
---

# Research Questions and Directions

This note is the top-to-bottom map of possible PhD research directions.

It starts with loose curiosities and compresses them into more formal research questions, topic names, concepts, reading clusters, and eventually project briefs.

Rule:

> Curiosity is allowed here. Projects live in [[02_Projects/Project Pipeline]].

---

## 0. North-Star Curiosity

Can we understand multimodal foundation models as information-processing systems that transform perceptual evidence into semantic commitments?

More concretely:

> When a VLM answers a question about an image, what visual evidence did it use, where was that evidence represented, how did it flow through the model, and why does this process sometimes fail?

---

## 1. Loose Curiosities

These are intentionally informal. They are things I would like to understand.

### Visual Grounding and Hallucination

- Why do VLMs hallucinate objects, attributes, relationships, or scenes that are not visually supported?
- When a VLM gives a correct answer, how do we know it used the image rather than language priors?
- Can a model be right for the wrong reason in multimodal tasks?
- What does it mean for an answer to be visually grounded?
- Are some hallucinations caused by lack of visual evidence, while others are caused by the model ignoring available evidence?
- Can we separate ambiguity, uncertainty, and hallucination?
- When should a VLM say "I cannot tell from the image"?
- Can grounding be measured without relying entirely on human judgment?
- Are grounding failures more common for objects, attributes, spatial relations, counting, text/OCR, or temporal relations?

### VLM Self-Evaluation

- Can a VLM judge whether its own answer is supported by the image?
- Does self-evaluation actually inspect the image, or does it merely rationalize the generated answer?
- Are VLMs better at detecting other models' hallucinations than their own?
- Can self-evaluation improve after forcing the model to point to visual evidence?
- Are models calibrated about their visual uncertainty?
- What kinds of grounding failures are easiest or hardest for models to self-detect?
- Can a self-evaluation score predict whether an answer is visually grounded?
- Does chain-of-thought or explanation help grounding, or simply make hallucinations more persuasive?

### Evidence Flow and Representation

- Where in a VLM is visual evidence represented?
- How does information move from image patches to visual tokens to projected embeddings to language model states to output tokens?
- Does the cross-modal projector preserve or distort semantic information?
- Do later language layers retain visual evidence, or do they increasingly rely on language priors?
- Can we identify layers where grounding is lost?
- Can hidden states distinguish grounded from ungrounded answers before generation?
- Are there representation-level signatures of hallucination?
- Can we measure the amount of visual evidence supporting a generated claim?

### Information-Theoretic Framing

- Can hallucination be formalized as unsupported semantic commitment: output information not justified by input evidence?
- Can grounding be treated as preserving task-relevant mutual information between image and output?
- What is the right random variable for "visual evidence"?
- What is the right random variable for "semantic claim"?
- Can we model VLM inference as a noisy channel from perceptual input to language output?
- Is the visual-language projector an information bottleneck?
- Can we use rate-distortion, information bottleneck, or causal information measures to reason about grounding?
- What would a theorem about hallucination or grounding even look like?

### Mechanistic Interpretability

- Are there identifiable circuits for visual grounding in VLMs?
- Are there circuits for object identity, spatial relation, counting, OCR, or attribute binding?
- Can activation patching restore grounded answers?
- Can causal tracing reveal whether a model used visual evidence?
- Are some attention heads responsible for routing visual information into language generation?
- Can sparse autoencoders reveal multimodal features?
- Can we intervene on visual concepts inside a VLM?
- Are grounded and hallucinated answers mechanistically different?

### Video, Space, and Time

- Why do models struggle with spatial and temporal relationships?
- What does it mean for a model to understand a video rather than a set of frames?
- Can temporal grounding failures be viewed as loss of relational information?
- Are action and event representations preserved through video-language architectures?
- Can a model distinguish object permanence, causality, and temporal order?

### Safety and Reliability

- Why is visual grounding an AI safety problem rather than only a benchmark problem?
- Can ungrounded multimodal outputs create dangerous overconfidence in high-stakes settings?
- Can grounding failures be detected before deployment?
- Can interpretability tools certify when a model used the relevant evidence?
- Can self-evaluation be made robust enough to support safety cases?
- What would a safety case for a VLM look like?

---

## 2. More Formal Research Questions

These are stronger candidates for project briefs.

### RQ1: Self-Evaluation Reliability

**Question:** Can VLMs reliably evaluate whether their own answers are grounded in visual evidence?

Subquestions:

- How well do VLM self-evaluation scores correlate with human grounding judgments?
- Does access to the image during self-evaluation improve reliability?
- Are self-evaluations calibrated across object, attribute, spatial, counting, OCR, and relational tasks?
- Do models systematically overrate the groundedness of their own outputs?

Possible artifact:

- benchmark + empirical analysis + failure taxonomy

Project link:

- [[02_Projects/Active/VLM Self-Evaluation and Grounding Reliability]]

---

### RQ2: Grounded Answer vs Correct Answer

**Question:** Can we distinguish answers that are correct because of visual evidence from answers that are correct because of priors or dataset bias?

Subquestions:

- How often do VLMs answer correctly when visual evidence is removed, corrupted, or contradicted?
- Can counterfactual image edits reveal whether the answer depends on the image?
- Can causal interventions identify visual dependence?

Possible artifact:

- evaluation protocol using counterfactual images/prompts or image ablations

---

### RQ3: Evidence Flow Across Model Components

**Question:** Where is visual evidence preserved, transformed, or lost as it moves through a VLM?

Subquestions:

- What information is present in visual tokens?
- What is lost in the projector?
- Do language model layers retain or overwrite visual evidence?
- Can representation probes predict groundedness?
- Can activation patching restore grounded outputs?

Possible artifact:

- layer-wise evidence-flow analysis on open VLMs

---

### RQ4: Representation-Level Hallucination Signatures

**Question:** Are hallucinated outputs associated with identifiable internal representation patterns before the output is generated?

Subquestions:

- Can hidden states predict whether a model will hallucinate?
- Are hallucinations preceded by low visual-evidence signals or high language-prior signals?
- Do grounded and ungrounded answers separate in representation space?

Possible artifact:

- classifier/probe + causal validation + interpretability analysis

---

### RQ5: Information-Theoretic Grounding

**Question:** Can visual grounding be formalized as the preservation of task-relevant semantic information from image input to language output?

Subquestions:

- How should semantic information be operationalized?
- Can we estimate mutual information or proxy quantities in practical VLMs?
- Can grounding failures be framed as information loss, bottleneck failure, or unsupported semantic generation?

Possible artifact:

- conceptual framework + small empirical case study

Project link:

- [[01_Research/Information-Theoretic Vision]]

---

### RQ6: Mechanistic Grounding Circuits

**Question:** Are there causal mechanisms or circuits inside VLMs that mediate visual grounding?

Subquestions:

- Which components route visual information into language generation?
- Can intervening on those components change groundedness?
- Are there features corresponding to objects, attributes, spatial relations, OCR, or uncertainty?

Possible artifact:

- tool/model map + small activation patching or causal tracing study

Project link:

- [[01_Research/Mechanistic Interpretability]]

---

### RQ7: Abstention and Visual Uncertainty

**Question:** Can VLMs learn when not to answer because the image does not contain enough evidence?

Subquestions:

- Can models distinguish missing evidence from difficult evidence?
- Can uncertainty calibration reduce hallucination?
- Are abstention decisions grounded in visual evidence or language patterns?

Possible artifact:

- abstention benchmark + calibration method

---

## 3. Named Research Directions

These are possible thesis/paper direction names.

### Direction A: Self-Evaluating Groundedness

Focus:

- Can VLMs evaluate their own visual grounding?
- How reliable are their self-judgments?
- Can self-evaluation become a safety mechanism?

Closest project:

- [[02_Projects/Active/VLM Self-Evaluation and Grounding Reliability]]

---

### Direction B: Evidence Flow in VLMs

Focus:

- How visual information travels across model stages.
- Where evidence is lost, distorted, or overwritten.
- How this relates to hallucination.

Likely methods:

- probing
- representation analysis
- attribution
- causal intervention
- layer-wise analysis

---

### Direction C: Information-Theoretic Grounding

Focus:

- Grounding as preservation of semantic information.
- Hallucination as unsupported semantic commitment.
- Projector and language-model layers as bottlenecks.

Likely methods:

- conceptual formalization
- proxy MI estimates
- representation similarity
- bottleneck analysis
- controlled synthetic tasks

---

### Direction D: Mechanistic Grounding

Focus:

- Finding circuits/features/pathways involved in grounding.
- Using causal tools to test whether internal states mediate visual evidence use.

Likely methods:

- activation patching
- causal tracing
- sparse autoencoders
- attention/head analysis
- feature attribution

---

### Direction E: Grounded Abstention and Calibration

Focus:

- Teaching or evaluating models to say when evidence is insufficient.
- Visual uncertainty and safe non-answering.

Likely methods:

- calibration metrics
- selective prediction
- abstention benchmarks
- uncertainty estimation

---

### Direction F: Spatiotemporal Grounding

Focus:

- Understanding objects, relations, actions, and time in video VLMs.
- Studying failures in spatial/temporal relational information.

Likely methods:

- video QA
- temporal perturbations
- counterfactual clips
- relation probes

---

## 4. Compression Path

How curiosities become projects:

1. Put raw question here.
2. Rewrite it as a formal RQ.
3. Name the topic/concepts in [[01_Research/Glossary]].
4. Add 3-5 papers to [[01_Research/Reading Map]].
5. Identify 2-3 people/labs in [[01_Research/People and Labs Map]].
6. Write a project brief using [[07_Templates/Template - Project Brief]].
7. Move to [[02_Projects/Project Pipeline]].

Hard rule:

> If a curiosity consumes serious attention for more than two weeks, run [[02_Projects/Anti-Diffusion Protocol]].
