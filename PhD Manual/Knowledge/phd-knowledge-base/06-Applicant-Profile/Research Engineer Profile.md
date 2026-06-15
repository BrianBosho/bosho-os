# Research Engineer Profile

> For: Industry R&D (Meta, Google DeepMind, Cohere, startup AI labs, etc.)
> **Tagline:** "Builds AI that understands the physical world — from cryo-ET pipelines to federated learning on sparse graphs."

---

## Elevator Pitch

I am a research engineer who bridges the gap between **algorithm design** and **production systems**. At CMU-Africa's Xulab, I built a two-stage Cryo-ET pipeline integrating 3D U-Nets and DeepETPicker to process tomographic data — combining custom deep learning with real scientific workflows. I developed FedProp, a federated GNN framework that achieves near-centralized accuracy without inter-client communication, delivering both the theoretical convergence guarantees and the production-ready implementation.

I am particularly interested in roles focused on **vision-language models, multimodal AI, and trust/grounding** — where the gap between recognition and true understanding is the core engineering problem.

---

## Technical Skills

### Deep Learning & AI
- **Frameworks:** PyTorch, TensorFlow, scikit-learn, JAX (familiar)
- **Research areas:** Computer Vision, Graph Neural Networks, Federated Learning, 3D Vision, Vision-Language Models, Diffusion Models
- **Specializations:** VLM hallucination mitigation, visual grounding, self-supervised learning

### Engineering
- **Languages:** Python (primary), C++, SQL
- **MLOps:** SLURM, AWS, GCP, Docker
- **Tools:** Git, LaTeX, Jupyter, Linux

### Domain
- **Medical imaging:** Cryo-ET, tomogram denoising, particle picking, EMPIAR datasets
- **Mobility:** Traffic scene understanding, scenario generation for autonomous driving
- **Low-resource AI:** Diffusion-based data augmentation, federated learning

---

## Key Projects

### FedProp: Federated GNN Framework
- **What:** Model-agnostic algorithm for training GNNs across decentralized clients with cross-client edges
- **How:** Feature propagation to reconstruct missing l-hop neighborhood information — no inter-client communication, no extra parameters
- **Impact:** 81.0% accuracy on Cora (non-IID) — 19.1% relative improvement over federated baseline
- **My role:** Algorithm conception, convergence proofs, implementation, experimental evaluation
- **Status:** Under review at a major AI conference

### Cryo-ET Particle Picking Pipeline
- **What:** Two-stage deep learning pipeline for Cryo-Electron Tomography analysis
- **How:** 3D U-Net for tomogram denoising + DeepETPicker for particle segmentation
- **Impact:** Automated processing of EMPIAR public datasets; pipeline integrated into lab workflow
- **My role:** End-to-end development, model integration, dataset curation

### Vision Foundation Models for Urban Mobility
- **What:** Data curation pipelines using diffusion models for augmentation; visual grounding in low-resource settings
- **Context:** CMU-Africa Edge AI & Mobility Lab
- **Focus:** Understanding why VFMs fail in Kigali traffic scenes — probing spatial, occlusion, and domain-shift failure modes

### Depth Estimation & AD Scenario Generation
- **Depth:** YOLO + Midas for monocular depth estimation (course project, robust implementation)
- **Scenario:** Safety-critical scenario generation for AD planners — improved trajectory modeling for underrepresented edge cases

---

## Experience

| Role | Organization | Period | Focus |
|---|---|---|---|
| Research Associate | CMU-Africa | Jun 2025 – Present | VFMs, visual grounding, low-resource AI |
| Research Intern | Xulab, CMU | Aug–Dec 2024 | Cryo-ET pipeline, 3D deep learning |
| Graduate TA | CMU-Africa | Sep 2024 – May 2025 | Math Foundations of ML, Applied Computer Vision |

---

## Education

- **M.S. Engineering — Artificial Intelligence**, Carnegie Mellon University Africa — *Valedictorian* (2025)
- **B.S. Electrical & Electronics Engineering** (Double major: Electronics and Computer Engineering)

---

## Why This Role

> I want to work on the **hard problems in vision-language models** — specifically why they hallucinate and how to build systems that are grounded in physical reality. I bring both the engineering skill to build pipelines that work at scale and the research instinct to diagnose failure modes at a mechanistic level.

---

## Example Application Text

**For Meta AI (FAIR) or similar:**

> I am drawn to [team]'s work on [specific project] because it addresses a problem I have been investigating from two angles: (1) as a researcher diagnosing VLM failure modes in real-world urban scenes, and (2) as an engineer who has built and deployed production deep learning pipelines for scientific imaging. At CMU-Africa, I developed FedProp — a federated GNN algorithm that achieves near-centralized accuracy without inter-client communication — contributing both the algorithm and its theoretical convergence guarantees. I am eager to apply my background in visual grounding and multimodal reasoning to [specific team problem].

---

## Keywords for ATS
`computer vision` `deep learning` `vision-language models` `graph neural networks` `federated learning` `3D vision` `medical imaging` `multimodal AI` `self-supervised learning` `PyTorch` `research engineering`
