---
type: research-area
status: seed
layer: 3-audacious
tags: [area/info-theory, area/science-of-dl, area/vlm, area/safety]
---

# Information-Theoretic Vision

## What this is

This is the Layer 3 north star: a long-term research vision, not a first-year deliverable.

The ambition is to do for deep learning and multimodal perception what Shannon did for communication: build a formal, principled framework for how information is encoded, transformed, and lost as it flows through learned systems.

## The Shannon Analogy

Shannon's 1948 paper gave communication theory a mathematical foundation: channel capacity, entropy, mutual information, the noisy channel theorem. These let engineers reason precisely about what is achievable and what is impossible in communication.

The analogous question for learning systems:

> Can we build an equally rigorous theory of information flow through learned systems — covering training, representation, inference, and multimodal perception?

A successful direction here would contribute to the **science of deep learning** and the **science of intelligence**. Not just better models, but a principled account of what they are doing.

## Core ideas

### 1. LLMs as signal processors

Treat a pre-trained language or multimodal model as a signal processing system. When an input (text, image, or other modality) enters the model, it is transformed through a sequence of layers. Questions:

- What information is preserved, compressed, or lost at each layer?
- How does visual information survive or degrade as it propagates through a VLM?
- Can we characterize what a layer "extracts" in information-theoretic terms?

This is not just a conceptual framing. Signal processing and information theory offer concrete tools: mutual information, entropy, rate-distortion, Markov chain inequalities.

### 2. The Data Processing Inequality as a constraint

The **data processing inequality** (DPI) states:

> If X → Y → Z is a Markov chain, then I(X; Z) ≤ I(X; Y).

No transformation downstream can increase mutual information with the original signal.

Applied to VLMs:

- Each layer is a step in a Markov chain over the input.
- Visual evidence can only be lost, never recovered, as it flows through the network — unless it was preserved at each step.
- **Hallucination may be interpretable as a DPI violation in practice**: the model's output carries less grounded visual information than the image contained, not because the image was uninformative, but because the processing pipeline failed to preserve it.

Possible formalization:

> Training to reduce hallucination ≡ constraining the model to not violate the DPI with respect to visual evidence.

### 3. The Information Bottleneck

Tishby's **Information Bottleneck** principle (1999, extended to deep learning in 2015) proposes that each hidden layer is an optimal compression of the input that preserves information about the output:

$$\min_{p(\tilde{x}|x)} I(\tilde{X}; X) - \beta \cdot I(\tilde{X}; Y)$$

Applied to multimodal systems:

- How does visual information get compressed through the cross-modal projection?
- Is the bottleneck at the visual encoder, the projection layer, or the language model?
- Can we identify *where* visual evidence is lost in a VLM architecture by measuring mutual information at each stage?

### 4. Perceptual failures as information failures

Grounding failures, hallucination, and the MIRAGE effect can be reframed as information-processing failures:

- **Hallucination**: output distribution is not constrained by visual evidence — the model generates from language priors rather than from the image.
- **MIRAGE effect**: the model's response is systematically misled because visual information was corrupted, lost, or overridden at some processing stage.
- **Spatial/temporal failures**: relationships between objects or events require higher-order mutual information between multiple spatial or temporal tokens; the model may not preserve this structure.

### 5. Training objectives with formal grounding

A long-term direction: restate common training objectives in information-theoretic terms and derive what they formally imply.

Examples:
- **RLHF / preference learning** → can be viewed as shaping the model's output distribution to have higher mutual information with human preference signals.
- **Anti-hallucination training** → constraining the model to preserve DPI with respect to the visual evidence channel.
- **Contrastive learning** → mutual information maximization between views (InfoNCE explicitly approximates this).

If successful, this lets us say: *this objective provably does or does not prevent this class of perceptual failure*.

## Connection to current work

| Current project | Connection |
|---|---|
| [[02_Projects/Active/VLM Self-Evaluation and Grounding Reliability]] | Grounding failures as information failures; self-evaluation as measuring residual visual MI in outputs |
| [[02_Projects/Candidates/Information-Theoretic Framework for Visual Grounding]] | Direct implementation of these ideas at the candidate level |
| [[01_Research/Mechanistic Interpretability]] | Mechanistic tools (causal tracing, activation patching) can identify where information is lost |
| [[01_Research/VLM Grounding]] | Grounding = preserving visual information through the processing chain |

## Key references to engage

- Tishby & Zaslavsky (2015) — Deep Learning and the Information Bottleneck Principle ([arXiv:1503.02406](https://arxiv.org/pdf/1503.02406))
- Saxe et al. (2018) — On the Information Bottleneck Theory of Deep Learning ([ICLR 2018](https://www.researchgate.net/publication/325022755_On_the_information_bottleneck_theory_of_deep_learning)) — important critique and refinement
- Cover & Thomas — *Elements of Information Theory* (foundational)
- Shannon (1948) — *A Mathematical Theory of Communication*

## Honest constraints

- This is Layer 3. Do not let it consume Layer 1 time.
- Mutual information is notoriously hard to estimate in high dimensions — practical methods matter.
- The IB critique (Saxe et al.) shows that some IB claims for deep learning do not hold under scrutiny. Engage seriously with the counterarguments.
- The goal is *principled contribution*, not just information-theoretic vocabulary applied superficially.

## North star question

> Can we provide a formal account of why visual grounding fails — and what training objectives would, by theorem, prevent it?
