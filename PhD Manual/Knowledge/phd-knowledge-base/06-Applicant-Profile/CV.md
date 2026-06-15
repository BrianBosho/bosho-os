# Curriculum Vitae — Brian Kipkirui

> Research Engineer & PhD Candidate | Computer Vision • VLM Hallucination • Federated Learning
> boshobrian@gmail.com | Kigali, Rwanda | [Google Scholar](#) | [LinkedIn](#)
> **Last updated:** April 2026

---

## Education

| | |
|---|---|
| **M.S. Engineering — Artificial Intelligence** | **2025** |
| Carnegie Mellon University Africa | *Valedictorian* — Top of class |
| **B.S. Electrical & Electronics Engineering** | |
| (Double major: Electronics and Computer Engineering) | |

---

## Research Experience

| | |
|---|---|
| **Research Associate — Edge AI & Mobility Lab** | *Jun 2025 – Present* |
| Carnegie Mellon University Africa | CMU-Africa |

Visual grounding in low-resource settings; vision foundation model (VFM) failure analysis in urban traffic scenes; diffusion models for data augmentation; VQA probing of VLM failure modes.

| | |
|---|---|
| **Research Intern — Xulab** | *Aug – Dec 2024* |
| Carnegie Mellon University | CMU |

Developed two-stage Cryo-ET pipeline for automated particle picking: 3D U-Net (tomogram denoising) + DeepETPicker (particle segmentation). Validated on EMPIAR public datasets. Pipeline integrated into lab workflow.

| | |
|---|---|
| **Researcher — Federated GNN Research** | *Summer 2024* |
| Independent | |

Designed and developed **FedProp** — a model-agnostic federated GNN framework using feature propagation to reconstruct l-hop neighborhood features for cross-client edges. Algorithm conception, convergence proofs, implementation, evaluation.

---

## Publications

**FedProp: Federated Graph Neural Networks with Feature Propagation**
*B. Kipkirui* — Under review, major AI conference

Cross-client edges in federated GNNs cause information gaps that degrade accuracy. FedProp propagates features iteratively to reconstruct missing neighborhood information — without inter-client communication or additional parameters.

- **Result:** 81.0% accuracy on Cora (non-IID) — 19.1% relative improvement over baseline (68.0%)
- **Theory:** Spectral graph theory convergence guarantee
- **Implementation:** Model-agnostic; PyTorch

---

## Awards

| | |
|---|---|
| **Valedictorian** | 2025 |
| CMU-Africa M.S. Engineering AI | Top of class |
| **Smart Africa Scholarship Award** | — |
| Merit scholarship for AI leadership in Africa | |
| **Jasiri Entrepreneurship Fellowship** | — |
| High-impact venture support in Africa | |

---

## Leadership & Service

| | |
|---|---|
| **Local Chair — African Computer Vision Summer School (ACVSS)** | 2025 |
| Kigali, Rwanda | Led planning and institutional coordination for 10-day premier event connecting African talent with international CV researchers |

| | |
|---|---|
| **Graduate Teaching Assistant** | *Sep 2024 – May 2025* |
| CMU-Africa | Courses: Mathematical Foundations of ML, Applied Computer Vision |

---

## Technical Skills

| | |
|---|---|
| **Research areas** | Computer Vision • Deep Learning • Graph Neural Networks • Federated Learning • 3D Vision • Vision-Language Models • Diffusion Models • Self-Supervised Learning • Medical Imaging |
| **Frameworks** | PyTorch • TensorFlow • scikit-learn |
| **Languages** | Python (primary) • C++ • SQL |
| **Infrastructure** | Linux • Git • SLURM • AWS • GCP • LaTeX |

---

## Referees

| | | |
|---|---|---|
| Prof. João Barros | Associate Director & Research Professor, ECE | jbarros@andrew.cmu.edu |
| Prof. Moise Busogi | Assistant Teaching Professor, CMU-Africa | mbusogi@andrew.cmu.edu |
| Prof. George Okeyo | Associate Teaching Professor, CMU-Africa | gokeyo@andrew.cmu.edu |
| Prof. Timothy Brown | Professor, CMU-Africa | timxb@cmu.edu |

---

## Research Interests

**Visual Grounding & VLM Hallucination** — Why VLMs see objects that aren't there; CLIP null space geometry; projector space null vectors as mechanism for grounding failure.

**Dynamic & Temporal Understanding** — World models; temporal and causal reasoning in vision; video understanding; 3D reconstruction.

**Causal & Explainable AI** — Causal representation learning; interpretability; applications in biomedical imaging and scientific discovery.
