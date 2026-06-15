---
type: glossary
status: active
layer: 3-concepts
tags: [glossary, concepts, vocabulary]
---

# Glossary

## Purpose

Define the vocabulary needed to engage seriously with [[01_Research/Formal Research Questions]] and [[01_Research/Reading Map]].

Rule: do not add a term unless I can write my own working definition.

## Vision-Language Models

### Vision-Language Model

A model that processes image and text inputs to produce text outputs. Common components: a vision encoder, cross-modal projector, and language model backbone.

### Vision Encoder

The component that converts an image into patch embeddings or visual tokens. Most current VLMs use a CLIP-style Vision Transformer.

### Visual Tokens

The sequence of image-derived embedding vectors that the language model can condition on. Grounding depends on whether relevant information from these tokens survives to generation.

### Cross-Modal Projector

The component that converts visual representations into the language model embedding space. This can be an MLP, Q-Former, or cross-attention module. It is a likely information bottleneck.

### Q-Former

A BLIP-2 style module that uses learned query tokens to attend to visual tokens and compress image information before passing it to a language model.

### Language Model Backbone

The autoregressive transformer that generates text conditioned on visual and text tokens.

### CLIP

A contrastively trained image-text model often used as the vision encoder in VLMs. It aligns image and text representations but may not preserve fine-grained evidence needed for grounding.

## Grounding

### Visual Grounding

The degree to which a model's textual output is causally supported by visual evidence in the input image.

Working definition: an output is visually grounded if removing the relevant visual evidence would change or remove the output claim.

### Visual Hallucination

Textual content that makes visual claims unsupported by the input image. Subtypes include object hallucination, attribute hallucination, and relationship hallucination.

### Object Hallucination

Mentioning an object that is not present in the image. POPE is the standard benchmark family for this failure mode.

### Grounding vs. Accuracy

Accuracy asks whether the answer is correct. Grounding asks whether the image was used. An answer can be correct but ungrounded.

### Visual Evidence

The image-derived information that could support a specific claim. For "the car is red," the evidence is the relevant red pixels in the car region.

Examples include object presence, object attributes, spatial relations, text/OCR, actions, temporal order, scene context, and fine-grained visual details.

### Unsupported Semantic Commitment

A claim made by the model when visual evidence is absent, ambiguous, or insufficient.

### Referring Expression Comprehension

A grounding task where the model identifies the image region described by a natural-language phrase. Common datasets: RefCOCO, RefCOCO+, RefCOCOg.

### Semantic Claim

A proposition expressed or implied by a model output.

Research use:

- convert model outputs into checkable claims
- evaluate whether each claim is visually supported
- compare claim-level grounding to answer-level accuracy

### Groundedness Score

A measure of how well a model output is supported by visual evidence.

Possible levels:

- binary: grounded / ungrounded
- ordinal: unsupported / weakly supported / strongly supported
- continuous: probability or confidence score
- claim-level: score per semantic claim
- answer-level: aggregate score for full output

### Self-Evaluation

A model's attempt to judge the quality, correctness, uncertainty, or groundedness of its own output.

Key risk: self-evaluation may be rationalization rather than inspection.

### Calibration

The alignment between a model's confidence and its actual reliability. In grounding, a well-calibrated model should be less confident when visual evidence is weak, ambiguous, missing, or contradictory.

### Abstention

The model's decision not to answer when the available evidence is insufficient.

## Mechanistic Interpretability

### Mechanistic Interpretability

Reverse-engineering the computations implemented by neural networks, with the goal of explaining model behavior in terms of components, features, circuits, or algorithms.

### Residual Stream

The vector state carried by each token through a transformer. Attention heads and MLPs read from and write to it by addition.

### Attention Head

A transformer component that moves information between token positions through query-key matching and value-vector transfer.

### Circuit

A subset of model components that implements a specific behavior or computation.

### Feature

A meaningful direction or pattern in activation space. The linear representation hypothesis says many features are represented as directions.

### Superposition

The phenomenon where a network represents more features than it has dimensions by storing features in non-orthogonal directions.

### Polysemanticity

The property of a neuron or direction responding to multiple unrelated features.

### Probing

Training a simple classifier on activations to test whether a property is encoded. Probe success does not prove the model uses the property.

### Activation Patching

Running a model on two inputs and replacing selected activations from one run with activations from the other to test causal responsibility.

### Path Patching

A more precise patching method that targets information flow along a specific edge in the computation graph.

### Causal Abstraction

A framework for testing whether an interpretable high-level causal model faithfully describes a neural network's computation.

### Evidence Flow

The movement and transformation of visual evidence through the model.

Possible path:

> image -> visual tokens -> projector -> multimodal hidden states -> output logits -> generated text

Research goal: identify where evidence is preserved, lost, or overwritten.

### Representation Geometry

The structure of model representations in vector space.

Useful questions:

- Do grounded and ungrounded answers occupy different regions?
- Are semantically similar visual concepts clustered?
- Does visual evidence become linearly decodable?
- Are hallucinations associated with representation drift?

### Causal Intervention

A method that changes internal model states to test whether those states matter for behavior.

Examples:

- activation patching
- causal tracing
- ablation
- feature steering
- representation editing

## Sparse Autoencoders

### Sparse Autoencoder

A model trained to reconstruct activations using a sparse combination of learned feature directions. Used to recover interpretable features from superposed representations.

### Dictionary

The learned set of SAE feature directions.

### Feature Activation

The scalar coefficient indicating how strongly an SAE feature is present in an activation.

### Dead Feature

An SAE feature that rarely or never activates.

### Reconstruction-Sparsity Tradeoff

The core SAE training tension between reconstructing activations accurately and using few features.

## Information Theory

### Mutual Information

A measure of how much information two variables share. For grounding, a useful intuition is how much the output depends on the image.

### Data Processing Inequality

If information flows through a processing chain, downstream transformations cannot increase mutual information with the original signal. Applied to VLMs, visual information can be lost as it flows through the model.

### Information Bottleneck

A framework in which a representation compresses input information while preserving information relevant to a target.

### MINE

Mutual Information Neural Estimation, a neural method for estimating mutual information in high-dimensional settings.

### Entropy

A measure of uncertainty or information content.

### Conditional Entropy

The remaining uncertainty about one variable after observing another.

## Evaluation And Benchmarking

### POPE

Polling-based Object Probing Evaluation, a benchmark for object hallucination using yes/no questions about object presence.

### HallusionBench

A benchmark for hallucination and visual illusion failures in VLMs.

### GQA

A structured visual reasoning dataset useful for compositional and relational grounding tasks.

### VQAv2

A standard visual question answering benchmark, but with known language-bias issues.

### Counterfactual VQA

VQA where images or questions are modified to test whether answers depend on visual evidence.

### Claim-Level Evaluation

Breaking an output into atomic semantic claims and evaluating each separately. Useful for long responses where some claims are grounded and others are hallucinated.

### Visual Dependence

The degree to which a model's answer actually depends on the image.

Tests:

- answer with image
- answer without image
- answer with corrupted image
- answer with counterfactual image
- compare hidden states/logits

## Representation Analysis

### Centered Kernel Alignment

A method for comparing neural network representations across layers or models.

### Representation Similarity Analysis

A method for comparing pairwise similarity structures in representations.

### SmartCLIP

A vision-language alignment paper by Shaoan Xie applying causal identifiability ideas to CLIP-style training. Relevant to representation geometry and grounding.

## Model Families

### LLaVA

An influential open-source VLM using a CLIP vision encoder, MLP projector, and LLaMA/Vicuna-style language model.

### InstructBLIP

A BLIP-2 variant using a Q-Former and instruction tuning.

### BLIP-2

A VLM architecture with frozen image encoder and LLM connected by a Q-Former.

### Flamingo

A DeepMind VLM using cross-attention fusion; influential but closed.

### Idefics / Idefics2

Open-source Flamingo-style VLMs useful for research.

## Safety Concepts

### Grounding Failure as Safety Failure

A VLM safety failure where the model confidently produces unsupported claims about visual evidence.

Relevant in:

- medicine
- autonomous systems
- surveillance
- robotics
- science
- assistive technology

### Safety Case

An argument, supported by evidence, that a system is acceptably safe for a given deployment context.
