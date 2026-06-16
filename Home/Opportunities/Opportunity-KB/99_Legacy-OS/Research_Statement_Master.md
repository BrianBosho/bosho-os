---
type: asset
asset-type: research-statement
version: master
last_updated: 2026-04-21
use-for: PhD applications, research fellowships
---

# Research Statement — Master Version

> Agents: this is the canonical research statement. Customize the [LAB-SPECIFIC] sections per application.
> Do not alter the core argument — only the framing and the "why here" section.

---

## The Problem

Today's multimodal foundation models suffer from a critical blind spot I call the **illusion of competence**: they achieve high accuracy on benchmarks while frequently ignoring the visual evidence they are supposed to process. Vision-language models answer questions about images by exploiting statistical correlations and language priors — not by genuinely perceiving the scene. This produces two failure modes: models that are *right for the wrong reason* (correct answer, wrong process, guaranteed to fail under distribution shift), and models that *hallucinate* (generating confident outputs unconstrained by visual input). In high-stakes applications — clinical decision support, autonomous driving, scientific imaging — either failure mode is unacceptable.

The fundamental gap is not in model scale or architecture. It is in measurement: we lack tools that can look *inside* a model and determine whether its representations are causally grounded in visual input or floating on statistical priors. External benchmarks measure outcomes, not mechanisms. My doctoral research addresses this gap directly.

---

## My Research Program

I propose to develop a **Visual Groundedness Toolkit** — a set of intrinsic diagnostic methods that measure visual grounding from internal model states, without requiring ground-truth labels or held-out test sets.

**Pillar 1 — Information-Theoretic Diagnostics.** I will define *Visual Information Gain* (VIG) as the mutual information between a model's internal representations and the visual input, compared with representations computed from text alone. By tracking VIG layer-by-layer, I can identify exactly where visual evidence enters, where it is overwritten by language priors, and where it vanishes — a mechanistic map of visual grounding across the model's depth.

**Pillar 2 — Spectral Manifold Analysis.** I will treat transformer attention maps as token graphs and apply spectral graph theory — specifically Laplacian eigenmodes and diffusion geometry — to detect *information inflation*: regimes where internal structure grows in complexity without corresponding visual input. This builds directly on my mathematical work in spectral graph theory during my federated GNN research (FedProp), now applied to the geometry of multimodal representations.

**From Diagnosis to Intervention.** Once groundedness can be measured intrinsically, the toolkit enables targeted intervention: faithfulness-aware training objectives that penalize high-confidence predictions unchanged by visual perturbation, and inference-time safeguards that can abstain or flag low-groundedness predictions before they propagate.

---

## My Preparation

My training converges on this agenda through three distinct threads.

*Robust perception under extreme conditions.* At CMU's Xulab, I built a 3D U-Net pipeline for Cryo-Electron Tomography — the noisiest visual data I have encountered. Standard models failed immediately; I had to infer biological structure from signals near the noise floor. This taught me that robust perception is not about clean benchmarks; it is about maintaining faithfulness to sparse, imperfect evidence.

*Mathematical rigor in graph signal processing.* As a Graduate Research Assistant, I designed FedProp — a federated GNN algorithm for the missing-neighbor problem. Crucially, I did not just implement it; I analyzed the propagation operator using spectral graph theory, derived convergence guarantees, and established error bounds. This mathematical foundation is the direct precursor to my proposed Spectral Manifold Analysis of VLMs, where the same Laplacian tools apply to token graphs instead of client graphs.

*Daily exposure to VLM failure modes.* As a Research Associate, I work on urban mobility analysis in Kigali using monocular cameras and foundation models. I encounter hallucinations, distribution-shift brittleness, and confident wrong predictions daily — not as academic abstractions, but as practical obstacles to deployment. This grounds my research questions in real failure.

---

## Why [LAB/PROGRAM — CUSTOMIZE THIS SECTION]

[Replace this paragraph per application. Include: specific faculty whose work connects, specific research threads that align, what Brian would contribute to the lab and what he would learn.]

Example structure:
- "Prof. [X]'s work on [Y] directly addresses [Z aspect of my project]..."
- "The lab's approach to [method] provides the [theoretical/empirical] framework I need for [specific aim]..."
- "I would contribute [specific methodological angle] to the lab's existing work on [their focus]..."

---

## Long-Term Vision

My goal is to advance the foundations of robust multimodal perception while building the conditions for African researchers to participate in frontier AI. The two are not competing: research on reliable AI in low-resource, non-Western contexts is itself important science. A PhD at [institution] is the environment where I can develop the mathematical and empirical depth to contribute to both.
