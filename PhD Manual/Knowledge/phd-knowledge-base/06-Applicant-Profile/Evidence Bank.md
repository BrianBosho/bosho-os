# Evidence Bank

> Single source of truth for all claims across all track profiles.
> Update facts here → they cascade to all other profiles automatically.

---

## Education

| Fact | Detail |
|---|---|
| Degree | M.S. Engineering — Artificial Intelligence |
| Institution | Carnegie Mellon University Africa |
| Year | Graduated 2025 |
| Achievement | **Valedictorian** — top of M.S. Engineering AI class |
| Other degrees | B.S. Electrical & Electronics Engineering (double major: Electronics and Computer Engineering) |
| Postgraduate | Data Science certification |

---

## Publications

| Paper | Status | Venue | My role |
|---|---|---|---|
| **FedProp: Federated Graph Neural Networks with Feature Propagation** | Under review (major AI conference) | TBD | First author — algorithm, proofs, implementation, experiments |

**FedProp key results:**
- 81.0% accuracy on Cora (non-IID) with GCN backbone
- 19.1% relative improvement over federated baseline (68.0% → 81.0%)
- No inter-client communication required
- No additional parameters
- Spectral graph theory convergence guarantee

---

## Research Experience

### Research Associate — CMU-Africa Edge AI & Mobility Lab
- **Duration:** June 2025 – Present
- **Focus:** Visual grounding in low-resource settings; vision foundation models for urban traffic
- **Methods:** Diffusion models for dataset augmentation, VQA probing of VLM failure modes
- **Key insight:** VFM failures in Kigali traffic mirror CLIP null space geometry — a core research question

### Research Intern — Xulab, CMU
- **Duration:** August 2024 – December 2024 (5 months)
- **Focus:** Cryo-Electron Tomography (Cryo-ET) analysis
- **Deliverable:** Two-stage pipeline: 3D U-Net (tomogram denoising) + DeepETPicker (particle segmentation)
- **Dataset:** EMPIAR public datasets (EMPIAR 1007)
- **Outcome:** Pipeline integrated into lab workflow

### Research Assistant — Federated GNN Research
- **Duration:** Summer 2024
- **Focus:** FedProp algorithm development
- **All stages:** Conception → theoretical foundations → implementation → evaluation → paper

### Graduate Teaching Assistant — CMU-Africa
- **Duration:** September 2024 – May 2025 (9 months)
- **Courses:** Mathematical Foundations of ML, Applied Computer Vision

---

## Projects

### FedProp (star project)
**Problem:** Cross-client edges in federated GNNs → missing neighborhood features → accuracy degradation
**Solution:** Iterative feature propagation locally — no communication, no extra params
**Theory:** Convergence guarantee via spectral graph theory
**Numbers:** 81.0% (vs 68.0% baseline) on Cora non-IID, 10 clients

### Cryo-ET Pipeline (star project)
**Problem:** Cryo-ET produces noisy 3D tomograms; manual particle picking is slow
**Solution:** 3D U-Net denoise → DeepETPicker segment → validated on EMPIAR 1007
**Outcome:** Production pipeline in computational biology lab

### Depth Estimation (class project)
**Methods:** YOLO + Midas monocular depth estimation; robust implementation

### Safety-Critical Scenario Generation (class project)
**Problem:** AD planners trained on clean data fail on edge cases
**Solution:** Improved trajectory modeling for ego vehicles in safety-critical scenarios
**Applied to:** Kigali traffic analysis

---

## Awards & Fellowships

| Award | Source | Year |
|---|---|---|
| **Valedictorian** | CMU-Africa | 2025 |
| **Smart Africa Scholarship Award** | Smart Africa | — |
| **Jasiri Entrepreneurship Fellowship** | Jasiri | — |

---

## Leadership & Service

| Role | Organization | Year |
|---|---|---|
| **Local Chair** — African Computer Vision Summer School (ACVSS) 2025 | Kigali, Rwanda | 2025 |
| **Graduate Teaching Assistant** | CMU-Africa | 2024–2025 |

---

## Technical Skills

### Programming & Frameworks
`Python` `PyTorch` `TensorFlow` `scikit-learn` `JAX (familiar)` `C++` `SQL`

### ML/DL Areas
`Computer Vision` `Deep Learning` `Graph Neural Networks` `Federated Learning` `3D Vision` `Vision-Language Models` `Diffusion Models` `Self-Supervised Learning` `Medical Imaging`

### Infrastructure
`Linux` `Git` `LaTeX` `Jupyter` `SLURM` `AWS` `GCP` `Docker`

---

## Referees

| Name | Role | Institution | Contact |
|---|---|---|---|
| Prof. João Barros | Associate Director & Research Professor, ECE | CMU-Africa | jbarros@andrew.cmu.edu |
| Prof. Moise Busogi | Assistant Teaching Professor | CMU-Africa | mbusogi@andrew.cmu.edu |
| Prof. George Okeyo | Associate Teaching Professor, Director of Academics | CMU-Africa | gokeyo@andrew.cmu.edu |
| Prof. Timothy Brown | Professor, Engineering and Public Policy | CMU-Africa | timxb@cmu.edu |

---

## Numbers That Stand Out

| Metric | Value |
|---|---|
| FedProp accuracy improvement | 19.1% relative (68.0% → 81.0%) |
| Cora clients in FedProp | 10 nodes |
| Cryo-ET pipeline stages | 2 (denoise + pick) |
| EMPIAR dataset used | EMPIAR 1007 |
| Months of TA experience | 9 |
| ACVSS 2025 attendees | 10-day event, top African + international researchers |

---

## One-Line Stories

- Built a production 3D vision pipeline for cryo-ET that went from raw tomograms to picked particles
- Developed a federated learning algorithm that eliminates cross-client communication overhead in GNNs
- Diagnosed VLM hallucination failures in real African traffic scenes — revealing null space geometry as a mechanism
- Led local organization of a premier CV summer school bridging African and international researchers
- Graduated valedictorian of CMU-Africa's AI engineering master's class
