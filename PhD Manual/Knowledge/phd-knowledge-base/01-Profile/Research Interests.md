# Research Interests

> Brian's PhD research is centered on developing Foundation Models that move beyond static pattern recognition to achieve a deep, causal understanding of the physical world.

---

## Three Research Pillars

### 1. Truly Perceptual Models
**Goal:** Build models that prioritize visual and geometric evidence over linguistic priors — reducing hallucinations and improving grounding.

- Vision-language models (VLMs) often over-rely on language priors, leading to hallucination
- Interested in the **geometry of CLIP null spaces** and **projector space null vectors** as a mechanism for grounding failure (Visual Faithfulness work)
- Condition dilution in autoregressive VLMs — mechanistically similar to the null space approach
- **Target labs:** BAIR (Rohrbach), VGG (Vedaldi)

### 2. Dynamic & Temporal Understanding
**Goal:** Design models that learn explicit temporal and causal relationships — enabling "world models" that understand how scenes evolve.

- Video understanding, 3D reconstruction, SLAM-inspired representations
- Temporal and causal reasoning in dynamic systems
- **Related work:** VGGT (Visual Geometry Grounded Transformer) — CVPR 2025 Best Paper
- **Target labs:** VIS Lab (Asano/Gavves), CVG ETH (Van Gool), VGG Oxford (Vedaldi/Rupprecht)

### 3. Causal & Explainable AI
**Goal:** Models that understand causal dynamics in their input to provide explainable, trustworthy outputs.

- Causal representation learning for instantaneous and temporal effects
- Applications in biology and medicine
- **Related work:** Mechanistic Neural Networks, Latent field discovery (Kofinas et al. 2023)
- **Target labs:** Akata group, MCML ( Schnabel), Cremers lab (3D vision + SLAM)

---

## Applications Focus

### Biomedical Imaging
- Cryo-Electron Tomography (Cryo-ET) — 3D particle picking, tomogram denoising
- Medical VLM reasoning, interpretability
- Foundation models for cancer research (FOMO lab)

### Urban Mobility & Autonomous Systems
- Safety-critical scenario generation for AD planners
- Visual grounding in low-resource settings
- Traffic scene understanding using VFMs

### Federated & Privacy-Preserving ML
- FedProp: Federated GNNs with feature propagation (under review)
- Communication-efficient decentralized learning

---

## Advisor Alignment

| Professor | Institution | Research Area | Alignment |
|---|---|---|---|
| [[Anna Rohrbach]] | Berkeley/BAIR | VLM hallucinations | Pillar 1 |
| [[Aishwarya Agrawal]] | Mila | VQA, POPE benchmark | Pillar 1 |
| [[Andrea Vedaldi]] | Oxford VGG | VGGT, 3D geometry | Pillar 2 |
| [[Christian Rupprecht]] | Oxford VGG | Visual grounding | Pillar 2 |
| [[Yuki Asano]] | UvA VIS Lab | Self-supervised grounding | Pillar 2 |
| [[Samuel Albanie]] | Cambridge VGG | VLM probing | Pillar 1 |
| [[Luc Van Gool]] | ETH CVG | CV + multimodal | Pillars 2&3 |
| [[Julia Schnabel]] | MCML/Helmholtz | Biomedical imaging | Pillar 3 |
| [[Zeynep Akata]] | MCML/TU Berlin | Explainability | Pillar 3 |
| [[Niki Kilbertus]] | MCML | Causal discovery | Pillar 3 |
| [[Daniel Cremers]] | TUM | 3D vision, SLAM | Pillar 2 |
| [[Björn Ommer]] | LMU Munich | Generative vision | Pillar 1 |
