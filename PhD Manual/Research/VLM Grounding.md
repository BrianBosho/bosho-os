---
type: research-area
status: active
tags: [area/vlm, area/grounding]
---

# VLM Grounding

## Working Definition

Visual grounding is the degree to which a model's textual output is supported by visual evidence in the input image or video.

A grounded answer is not merely correct. It is correct **because the model used relevant visual evidence**.

---

## Why This Matters

If a model can answer fluently without correctly using visual evidence, then reliability, self-correction, deployment safety, and interpretability claims become fragile.

This is especially important for:

- medical or scientific image interpretation
- robotics and embodied AI
- autonomous systems
- assistive technologies
- surveillance or security applications
- any setting where a user trusts the model's visual claims

---

## Connection to Active Project

- [[02_Projects/Active/VLM Self-Evaluation and Grounding Reliability]] asks whether VLMs can evaluate the quality of their own grounding.
- [[01_Research/Research Questions and Directions]] holds the broader curiosity map.
- [[01_Research/Glossary]] defines grounding-related terms.
- [[01_Research/Reading Map]] tracks papers and benchmark clusters.

---

## Key Distinctions

### Correctness vs Groundedness

A model can answer correctly without grounding.

Example:

- Question: "What animal is in the image?"
- Image: a dog
- Model answer: "dog"
- But if the model would also answer "dog" without the image because of dataset priors, the answer may be correct but weakly grounded.

Research implication:

> Accuracy is not enough. We need tests of visual dependence.

---

### Hallucination vs Ambiguity

A hallucination is an unsupported claim.

Ambiguity means the image does not contain enough evidence to decide.

Research implication:

> A safe model should sometimes abstain rather than hallucinate.

---

### Output-Level vs Mechanistic Grounding

Output-level grounding asks:

> Is the answer supported by the image?

Mechanistic grounding asks:

> Did the model actually use the relevant visual evidence internally?

Research implication:

> A full theory of grounding needs both behavioral evaluation and internal evidence-flow analysis.

---

## Key Questions

### Behavioral Grounding

- What does it mean for an output to be visually grounded?
- Can grounding be measured at the answer level, claim level, or rationale level?
- When does a model answer from language priors rather than image evidence?
- Can a model detect that its own answer is unsupported by the image?
- Can counterfactual images reveal whether the model is visually dependent?

### Representation-Level Grounding

- Are grounding failures visible in intermediate representations?
- Can hidden states predict whether a model will hallucinate?
- Do visual tokens contain enough semantic evidence for the answer?
- Does the projector preserve grounding-relevant information?
- Do language layers overwrite visual evidence with priors?

### Causal Grounding

- Can activation patching restore grounded behavior?
- Can ablation remove grounding while preserving fluency?
- Which model components causally mediate visual evidence use?
- Can interventions distinguish grounded from ungrounded answers?

### Self-Evaluation

- Can models judge whether their own outputs are grounded?
- Does self-evaluation inspect the image or rationalize the text?
- Are models calibrated about visual uncertainty?
- Can self-evaluation support safety mechanisms?

---

## Possible Measurement Objects

- image regions / patches
- visual tokens
- projected multimodal representations
- language model hidden states
- output logits
- generated rationales / self-evaluations
- attention and attribution traces
- counterfactual image perturbations
- claim-level semantic units

---

## Failure Taxonomy

| Failure type | Description | Example |
|---|---|---|
| Object hallucination | Claims an object exists when it does not | "There is a cat" when no cat appears |
| Attribute hallucination | Wrong property of a real object | says shirt is red when blue |
| Relation hallucination | Wrong spatial/semantic relationship | "cup is on the table" when beside it |
| Counting failure | Wrong number of objects | says three dogs instead of two |
| OCR/text hallucination | Fabricated or wrong text | invents sign content |
| Action hallucination | Wrong action/event | says person is running when standing |
| Temporal hallucination | Wrong order or duration in video | says car turns before pedestrian crosses |
| Overconfident ambiguity | Answers when evidence is insufficient | identifies hidden object confidently |

---

## Possible Project Directions

### 1. Groundedness Self-Evaluation

Can VLMs judge whether their own answers are visually supported?

Project link:

- [[02_Projects/Active/VLM Self-Evaluation and Grounding Reliability]]

---

### 2. Grounded Answer vs Correct Answer

Can we detect when a correct answer came from visual evidence rather than priors?

Possible method:

- remove/corrupt image
- counterfactual image edits
- compare answer changes
- test hidden-state dependence on visual tokens

---

### 3. Evidence-Flow Analysis

Where does visual evidence get lost?

Possible method:

- layer-wise probing
- representation similarity
- attention/attribution
- projector bottleneck analysis
- activation patching

---

### 4. Grounded Abstention

Can models learn to say when the image lacks enough evidence?

Possible method:

- abstention benchmark
- calibration analysis
- selective prediction
- uncertainty estimation

---

### 5. Claim-Level Grounding

Can long VLM outputs be decomposed into semantic claims and evaluated individually?

Possible method:

- claim extraction
- visual verification
- human/model agreement
- hallucination taxonomy

---

## Open Problems

- Distinguishing correct answer from grounded answer.
- Distinguishing hallucination from ambiguity.
- Measuring evidence flow rather than only answer accuracy.
- Building self-evaluation protocols that cannot be gamed by fluency.
- Evaluating long-form answers where some claims are grounded and others are not.
- Creating counterfactual tests that isolate visual dependence.
- Connecting behavioral grounding to internal mechanisms.

---

## Reading Links

- [[01_Research/Reading Map]]
- [[01_Research/Research Questions and Directions]]
- [[01_Research/Glossary]]

---

## First Synthesis to Produce

Title:

`Synthesis - What Counts as VLM Grounding.md`

Question:

> What are the strongest existing definitions and benchmarks for grounding/hallucination, and what do they fail to capture?

Do not create this synthesis until at least 5 relevant papers have been read.
