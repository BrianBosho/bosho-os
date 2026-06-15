# PhD Profile

> For: PhD Applications — UK, Europe, Canada, Australia
> **Tagline:** "Developing foundation models that understand causality, not just correlation."

---

## Academic Statement

I am seeking a PhD position focused on **visual grounding, VLM hallucination, and causal representation learning** — with a particular interest in applications to biomedical imaging and scientific discovery.

My research journey began applying deep learning to Cryo-Electron Tomography data at CMU's Xulab, where I learned firsthand how fragile standard vision models are outside curated datasets. This experience revealed that advancing perceptual intelligence requires more than semantic alignment — it demands models that integrate **spatial, temporal, and causal reasoning**.

Since then, I have developed a principled research profile spanning three interconnected pillars:

1. **Truly Perceptual Models** — vision-first over language priors, reducing hallucinations
2. **Dynamic & Temporal Understanding** — world models that comprehend how scenes evolve
3. **Causal & Explainable AI** — causal discovery for trustworthy, interpretable outputs

---

## Research Experience

### Federated Graph Neural Networks (FedProp)
- **Problem:** Cross-client edges in federated GNNs cause information gaps degrading accuracy
- **Solution:** Feature propagation to reconstruct l-hop neighborhood features — no inter-client communication, no extra parameters
- **Contribution:** Algorithm + convergence proofs + implementation + experiments (81.0% on Cora, 19.1% relative improvement)
- **Status:** Under review at a major AI conference
- **Key insight:** Missing neighborhood information = missing-feature problem → iterative local propagation resolves it

### Cryo-ET Particle Picking Pipeline
- **Problem:** Cryo-ET produces noisy 3D tomograms requiring detection/segmentation of biological particles
- **Solution:** Two-stage pipeline: 3D U-Net denoising + DeepETPicker particle segmentation
- **Impact:** Validated on EMPIAR public datasets, integrated into lab workflow
- **Key insight:** Real biological data demands domain adaptation and self-supervised approaches, not just supervised benchmarks

### Visual Grounding in Low-Resource Settings
- **Problem:** VFMs fail in Kigali traffic scenes — domain shift, occlusion, limited labeled data
- **Approach:** Diffusion models for data augmentation + probing VLM failure modes via VQA
- **Key insight:** Hallucination in VLMs is mechanistically similar to CLIP projector null space geometry — a core research question

---

## Publications

- **FedProp: Federated Graph Neural Networks with Feature Propagation** — First author, under major AI conference review

---

## Academic Background

| Degree | Institution | Year | Notes |
|---|---|---|---|
| M.S. Engineering AI | CMU-Africa | 2025 | Valedictorian, top of class |
| B.S. Electrical & Electronics Eng. | — | — | Double major |

**Relevant coursework:** Deep Learning, Machine Learning, Computer Vision, NLP, Reinforcement Learning

---

## Supervision Preferences

| Professor | Institution | Why |
|---|---|---|
| Andrea Vedaldi | Oxford VGG | VGGT, 3D geometry grounding |
| Anna Rohrbach | Berkeley/TU Berlin | VLM hallucination |
| Aishwarya Agrawal | Mila | POPE benchmark, VQA |
| Yuki Asano | UvA | Self-supervised grounding |
| Julia Schnabel | MCML | Biomedical imaging foundation models |

---

## Why This PhD

> My path through biomedical imaging, federated learning, and urban mobility has converged on a single question: **how do we build vision models that are genuinely grounded in physical reality?** My Cryo-ET work showed me the cost of brittle models. My FedProp work showed me that principled theory and practical systems are not in tension — they reinforce each other. I want a PhD where I can ask these questions at the deepest level, with access to the computational and academic resources that world-class labs offer.

---

## Keywords
`visual grounding` `VLM hallucination` `causal representation learning` `federated learning` `3D vision` `biomedical imaging` `self-supervised learning` `multimodal models` `world models` `explainable AI`
