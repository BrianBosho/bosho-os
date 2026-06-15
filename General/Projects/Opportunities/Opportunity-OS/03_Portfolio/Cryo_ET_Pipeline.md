---
project: Cryo-ET Pipeline
type: research
status: completed
year: 2024
tags: [computer-vision, biomedical-imaging, deep-learning, 3D-vision, U-Net, scientific-imaging]
---

# Automated Cryo-ET Particle Picking Pipeline

## One-Line Summary
End-to-end deep learning pipeline for tomogram denoising and automated particle picking in Cryo-Electron Tomography, enabling reproducible biological structure analysis from extremely noisy 3D microscopy data.

## Two-Line Summary (for CVs)
Developed a two-stage Cryo-ET pipeline integrating 3D U-Net denoising (ccpem-denoiser) and automated particle picking (DeepETPicker) into a unified workflow. Applied and validated on public EMPIAR datasets, reducing manual inspection bottlenecks in structural biology research.

## Problem
Cryo-Electron Tomography generates 3D volumetric images of biological specimens, but raw tomograms are extremely noisy (low SNR) and weakly labeled. Finding and localizing specific biological particles (proteins, complexes) requires hours of manual expert inspection — a bottleneck for large-scale structural biology research.

## Brian's Role
- Developed the full two-stage pipeline: denoising → particle picking
- Integrated `ccpem-denoiser` (3D U-Net architecture) for tomogram denoising
- Integrated `DeepETPicker` for automated particle detection and localization
- Built reproducible workflow on public EMPIAR datasets
- Validated results against known biological ground truth

## Methods and Tools
- 3D U-Net (volumetric convolutional neural network)
- Deep learning for object detection in 3D space
- Cryo-ET data formats and preprocessing
- EMPIAR public dataset infrastructure
- Python, PyTorch

## Key Results
- End-to-end pipeline reducing manual tomogram inspection
- Reproducible results on EMPIAR benchmark datasets
- Demonstrated applicability on real biological data (not synthetic only)

## Why It Matters
Drug discovery, vaccine design, and understanding disease mechanisms depend on knowing 3D protein structures. Automating particle picking accelerates structural biology and enables analysis at scales impossible with manual methods.

## Core Lesson Brian Draws From This
"Standard vision models fracture immediately when exposed to raw Cryo-ET data — the SNR is too low, the labels too sparse. This experience taught me that robust perception is not about fitting clean benchmarks; it is about inferring structure from uncertainty. That conviction now drives my interest in models that are reliably grounded in their inputs."

## Variants for Different Applications

### Research framing (PhD apps)
"My Cryo-ET work was formative: I encountered, at first hand, the failure of standard computer vision models outside controlled settings. Working with weakly labeled, noise-dominated biological data crystallized my belief that robust perception requires more than accuracy on curated datasets — it requires inference from sparse, imperfect signals. This conviction directly motivates my current research on visual groundedness."

### Biomedical AI framing
"Built a fully automated Cryo-ET analysis pipeline integrating 3D denoising and particle picking, validated on the EMPIAR benchmark. Reduced dependence on manual expert annotation in structural biology workflows."

### Applied CV framing
"3D computer vision pipeline for scientific imaging — extreme noise conditions, weakly labeled data, reproducible research infrastructure."

## Links
- Code: [GitHub link — confirm public]
- Supervisor: Prof. Min Xu, Xulab, Carnegie Mellon University
