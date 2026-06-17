---
title: "FedProp — Experimental Plan"
type: experimental-plan
source: google-drive
drive-id: 1j7Fj9cIbmR1y0XykFgl6n5ISszjGqvACTPz2NIP53R8
created: 2026-05-01
tags: [fedprop, experiments, datasets, baselines, hyperparameters, tmlr]
project: tmlr_fedprop_paper
---

# FedProp — Experimental Plan

**Datasets, Architectures, Hyperparameters, Baselines, Results**

*Kipkirui & Barros — Carnegie Mellon University Africa*

## 1. Paper Claims and What Experiments Support Them

Every experiment in this plan exists to support one of four claims. If an experiment does not map to a claim, it does not belong in the paper.

| | |
|:-:|:-:|
| **Claim A** | Zero-additional-communication recovery. FedProp recovers a large fraction of the missing-neighbour performance gap without any inter-client feature exchange. → Supported by: R1 (main accuracy table), R2 (comm. cost plot), R3 (recovery bar plot). |
| **Claim B** | Model-agnosticity. FedProp works with both GCN and GAT backbones using standard centralised hyperparameters. → Supported by: R1b (GAT accuracy table, direct FedProp-GAT vs. FedGAT comparison). |
| **Claim C** | Partition robustness. FedProp remains useful under IID and non-IID Dirichlet partitions and across client counts. → Supported by: R4 (β sweep), R5 (K scaling). |
| **Claim D** | Homophily-dependent limitation. FedProp's smoothness prior breaks on heterophilic graphs. We quantify this honestly. → Supported by: R6 (Texas, Wisconsin). Connected to T1/T2/T3 error decomposition in theory. |

## 2. Datasets

Eight datasets in three categories. Main-paper experiments use only the main and limitation datasets. Amazon datasets are appendix. Heterophilic datasets are a required limitation study.

| **Dataset** | **Type** | **|V|** | **|E|** | **Feat F** | **C** | **Avg deg** | **Homophily h** | **Label split** | **Notes** |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **Cora** | Citation | 2,708 | 5,429 | 1,433 | 7 | 4.01 | 0.81 | Planetoid fixed 20/class : 500 : 1000 | All primary baselines use this. |
| **Citeseer** | Citation | 3,327 | 4,732 | 3,703 | 6 | 2.84 | 0.74 | Planetoid fixed 120 : 500 : 1000 | Sparser graph (avg deg 2.84). |
| **Pubmed** | Citation | 19,717 | 44,338 | 500 | 3 | 4.50 | 0.80 | Planetoid fixed 60 : 500 : 1000 | Larger citation. Low feature dim. |
| **OGBN-Arxiv** | Citation (OGB) | 169,343 | 1,166,243 | 128 | 40 | 13.7 | 0.66 | OGB standard ~54% : 18% : 28% | Scale benchmark. Conditional (Gate 1). |
| **Amazon-CS** | Co-purchase | 13,752 | 287,209 | 767 | 10 | 41.7 | 0.78 | Random 60/20/20 (10 seeds) | Appendix. Dense homophilic graph. |
| **Amazon-Photos** | Co-purchase | 7,650 | 238,162 | 745 | 8 | 62.3 | 0.83 | Random 60/20/20 (10 seeds) | Appendix. Very dense (avg deg 62). |
| **Texas** | Web graph | 183 | 325 | 1,703 | 5 | 3.6 | 0.11 | Geom-GCN 60/20/20 (10 seeds) | ⚠ Heterophilic. Required by reviewers. |
| **Wisconsin** | Web graph | 251 | 499 | 1,703 | 5 | 4.0 | 0.20 | Geom-GCN 60/20/20 (10 seeds) | ⚠ Heterophilic. Required by reviewers. |

**Split protocol notes:** Cora, Citeseer, Pubmed use Planetoid fixed splits (non-negotiable for transductive comparison). 20 nodes/class train; 500 val; 1000 test. These match FedGCN and FedGAT exactly. OGBN-Arxiv is conditional on Gate 1. Texas and Wisconsin use Pei et al. (2020) Geom-GCN splits. Amazon uses random 60/20/20 (deterministic on seed).

## 3. Architectures and Hyperparameters

All backbone hyperparameters are anchored to published sources and held fixed across all experiments for a given (dataset, backbone) pair. No tuning beyond what the source papers establish.

| **Dataset** | **Backbone** | **Layers** | **Hidden** | **Dropout** | **Optim** | **LR** | **WD** | **Epochs / Early stop** | **Source / Note** |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **Cora** | **GCN** | 2 | 16 | 0.5 | SGD | 0.5 | 5×10⁻⁴ | 600 max, ES pat. 10 | Kipf & Welling (2017) exactly. SGD + high LR from original codebase. |
| **Citeseer** | **GCN** | 2 | 16 | 0.5 | SGD | 0.5 | 5×10⁻⁴ | 600 max, ES pat. 10 | Identical to Cora. Consistent across Planetoid family. |
| **Pubmed** | **GCN** | 2 | 16 | 0.5 | Adam | 0.01 | 5×10⁻⁴ | 600 max, ES pat. 10 | Adam used here — better convergence on larger citation graph. |
| **Cora** | **GAT** | 2 | 64 (8×8) | 0.6 | Adam | 0.005 | 5×10⁻⁴ | 600 max, ES pat. 10 | Velickovic et al. (2018) exactly. Dropout on features AND attention. |
| **Citeseer** | **GAT** | 2 | 64 (8×8) | 0.6 | Adam | 0.005 | 5×10⁻⁴ | 600 max, ES pat. 10 | Identical to Cora/GAT. |
| **Pubmed** | **GAT** | 2 | 64 (8×8) | 0.6 | Adam | 0.01 | 5×10⁻⁴ | 600 max, ES pat. 10 | Higher LR for Pubmed scale (follows GAT paper). |
| **OGBN-Arxiv** | **GCN** | 3 | 256 | 0.5 | Adam | 0.01 | 0 | 500 max, ES pat. 20 | 3-layer + BatchNorm between layers (OGB convention, Hu et al. 2020). No weight decay. |
| **Amazon-CS** | **GCN** | 2 | 64 | 0.5 | Adam | 0.01 | 5×10⁻⁴ | 600 max, ES pat. 10 | Larger hidden for denser graph (avg deg 42). Appendix only. |
| **Amazon-Photo** | **GCN** | 2 | 64 | 0.5 | Adam | 0.01 | 5×10⁻⁴ | 600 max, ES pat. 10 | Consistent with Amazon-CS. Appendix only. |
| **Texas** | **GCN** | 2 | 32 | 0.5 | Adam | 0.01 | 5×10⁻⁴ | 400 max, ES pat. 20 | Smaller hidden for 183-node graph. Geom-GCN splits (Pei et al. 2020). |
| **Wisconsin** | **GCN** | 2 | 32 | 0.5 | Adam | 0.01 | 5×10⁻⁴ | 400 max, ES pat. 20 | Identical protocol to Texas. |

**Hyperparameter justification notes:** GCN on Cora/Citeseer uses SGD lr=0.5 from the Kipf & Welling (2017) original codebase (not FedGCN's Adam lr=0.01). GAT dropout=0.6 is applied to both input features AND attention coefficients. OGBN-Arxiv requires BatchNorm between layers (OGB convention) — without it, training is unstable. Weight decay=0 for OGBN-Arxiv (OGB default, Hu et al. 2020).

### 3.1 FedProp propagation settings (all datasets)

| | |
|:-:|:-:|
| **Propagation operators** | Normalised adjacency (Adj): Â = D̃⁻¹/² Ã D̃⁻¹/². Discrete diffusion (Diff): I − hL where L is the normalised graph Laplacian, h = 0.1. |
| **Iterations T** | T = 50 (justified by A3 saturation experiment). |
| **Boundary reset** | Enabled on both operators. Remote boundary nodes are reset to propagated estimates after each iteration. |
| **Accessible radius** | L = 1 (primary experiments). L = 2 in appendix A4 with privacy discussion. |
| **Positional encodings (PE)** | Disabled in main tables. Enabled for A2 ablation only. Config: R = 16 random seeds, P = 5 propagation steps. Concatenated to node features after propagation. |
| **Federated aggregation** | FedAvg, synchronous, weighted by number of local nodes per client. |
| **Local epochs per round** | 1 (standard FedAvg). |
| **Global rounds** | 200 communication rounds + ES patience 10. |

### 3.2 Federated partition settings

| | |
|:-:|:-:|
| **Partition method** | Label-based Dirichlet distribution with concentration parameter β. |
| **IID setting** | β = 10,000 — effectively uniform label distribution across clients. |
| **Non-IID setting** | β = 10 (primary non-IID for main tables). β = 1 and β = 100 added only for R4 (β sweep). |
| **Number of clients** | K = 10 (primary for all experiments). K ∈ {1, 5, 10, 20} in R5 (client scaling) only. |
| **Seeds** | 10 random seeds per configuration. Report mean ± std. |

## 4. FedProp Variants

Six variants in total. Only Diff appears in all main-paper positions. Adj appears as an ablation. +PE variants appear in the appendix only.

| **Variant** | **Operator** | **Imputation config** | **Positional encoding** | **Role** |
|:-:|:-:|:-:|:-:|:-:|
| **FedProp-Zero** | None | No imputation. Remote neighbours featureless. | None | Lower bound reference. |
| **FedProp-Full** | Oracle | Exact 1-hop remote features available (oracle only). | None | Upper bound reference. |
| **FedProp (Adj)** | Normalised Adj Â = D̃⁻¹/² Ã D̃⁻¹/² | T=50 iterations. Boundary reset. No step size. | None | Ablation (simpler operator). |
| **FedProp (Adj+PE)** | Normalised Adj | T=50 iterations. Boundary reset. | R=16 seeds, P=5 steps. Concat after propagation. | Appendix A2 only. |
| **FedProp (Diff)** | Discrete diffusion (I − hL), h=0.1 | T=50 iterations. Boundary reset. | None | PRIMARY method. Main tables + all figures. |
| **FedProp (Diff+PE)** | Discrete diffusion | T=50 iterations. Boundary reset. | R=16 seeds, P=5 steps. Concat after propagation. | Appendix A2 only. |

## 5. Baselines

Ten methods total. Six primary (appear in main tables). Four positioning-only (cited in text, not in numerical tables). The protocol-family mismatch with FedSage+ and FedDEP is the reason they are excluded from the main accuracy tables.

| **Method** | **Role in paper** | **Configuration** | **Why included** |
|:-:|:-:|:-:|:-:|
| **Centralised GCN / GAT** | Upper bound | Full graph, no federation. Standard backbone hyperparameters (see §3). | Performance ceiling. |
| **FedProp-Full (oracle)** | Upper bound | FedAvg + exact 1-hop remote features. Zero extra communication beyond FedAvg. | Shows how much performance is recoverable if missing features were perfectly known. |
| **FedProp-Zero** | Lower bound | FedAvg + no imputation. Remote neighbours are treated as zero features. | The federated baseline without any missing-neighbour handling. |
| **FedProp (Adj)** | Ours (ablation) | Normalised-adjacency propagation. T=50 iterations. No PE. | Simpler propagation operator — ablation vs. Diff. |
| **FedProp (Diff)** | Ours (primary) | Discrete-diffusion propagation. T=50 iterations. h=0.1. Boundary reset. | Primary proposed method. |
| **FedGCN (1-hop)** | Main competitor | 2-layer GCN. 1-hop pre-training communication with Homomorphic Encryption. | Closest transmission-based competitor. Same Dirichlet partition. Apples-to-apples. |
| **FedGCN (2-hop)** | Comm. plot only | As above, 2-hop feature exchange. | Appears only in accuracy-vs-communication figure. |
| **FedGAT** | GAT table only | 2-layer GAT, 8×8 heads. Chebyshev degree-16 approximation. | Direct backbone-equivalent comparison to FedProp-GAT. |
| **FedSage+ / FedDEP** | Related work only | NOT in main accuracy tables. Louvain partition + inductive 60/20/20 splits. Different protocol family. | Cited in §2 (related work) and §5.5 (cross-family discussion). |
| **FedCog** | Related work only | NOT in main accuracy tables. Shares border embeddings every round. | Dedicated contrast paragraph in §2.3: FedCog requires per-round inter-client communication; FedProp does not. |

## 6. Experiment Stack

Eleven experiments total: seven main-paper (R1–R6 including the OGBN extension) and four appendix (A1–A4). R2 and R3 are post-hoc analyses of R1 — no new training runs.

| **ID** | **Experiment** | **Datasets** | **Methods** | **β values** | **K** | **Paper artifact** |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **R1** | Core accuracy (GCN) | Cora, Citeseer, Pubmed (+OGBN-Arxiv conditional) | Centralised, FP-Full, FP-Zero, FP(Adj), FP(Diff), FedGCN-1hop | 10000, 10 | 10 | Table 1. Feeds Figure 1 (comm) and Figure 2 (recovery). |
| **R1b** | Core accuracy (GAT) | Cora, Citeseer, Pubmed | Centralised-GAT, FP-GAT-Full/Zero/Adj/Diff, FedGAT | 10000, 10 | 10 | Table 2. |
| **R2** | Accuracy vs. communication | Cora + OGBN-Arxiv | FP(Diff), FedGCN-0/1/2-hop, FedGAT | 10 (non-IID) | 10 | Figure 1. Post-hoc from R1 runs. |
| **R3** | Recovery / gap closed | Cora, Citeseer, Pubmed | FP-Zero, FP(Diff), FP-Full, Centralised | 10 (non-IID) | 10 | Figure 2. Post-hoc from R1 runs. |
| **R4** | β sweep (partition severity) | Cora | FP(Diff), FP-Zero, FP-Full, FedGCN-1hop | 10000, 100, 10, 1 | 10 | Figure 3. |
| **R5** | K scaling (client count) | Cora | FP(Diff), FP-Zero, FedGCN-1hop | 10000, 10 | 1, 5, 10, 20 | Figure 4. Two panels (IID/non-IID). |
| **R6** | Heterophilic limitation | Texas, Wisconsin | Centralised, FP-Full, FP-Zero, FP(Diff), FedGCN-1hop | 10000, 10 | 10 | Table 3 (limitation section). |
| **A1** | Amazon validation | Amazon-CS, Amazon-Photos | Same as R1 | 10000, 10 | 10 | Appendix Table A1. |
| **A2** | PE ablation | Cora, Citeseer, Pubmed | FP(Adj), FP(Adj+PE), FP(Diff), FP(Diff+PE) | 10000, 10 | 10 | Appendix Table A2. |
| **A3** | Propagation depth T | Cora, Pubmed | FP(Diff), T ∈ {10,25,50,100} | 10 | 10 | Appendix Figure A3. |
| **A4** | 1-hop vs. 2-hop | Cora, Citeseer | FP(Diff), L=1 vs L=2 | 10000, 10 | 10 | Appendix Table A4 + privacy discussion. |

## 7. Result Reporting Specification

### 7.1 Numerical reporting conventions

- Accuracy in tables: mean ± std over 10 seeds, 3 decimal places (e.g., 0.808 ± 0.007).
- Accuracy in prose / abstract: percentage with 1 decimal place (e.g., 80.8%).
- Bold the best non-oracle method per row in each table.
- Shade FedProp (Diff) rows or columns lightly to guide the reader.
- Every table caption must state: dataset, partition method, β value(s), K, number of seeds.
- Every figure caption must define metrics, axes, and panel content unambiguously.

### 7.2 Communication cost definition (for Figure 1)

All communication is measured as total bytes transferred per client over the full training run.

| **Formula** | B_total = B_pretrain + N_rounds × B_per_round |
|:-:|:-:|
| **FedProp (any variant)** | B_pretrain = 0 (no pre-training communication). B_per_round = |θ| × 4 bytes (model parameters only, float32). |
| **FedGCN (k-hop)** | B_pretrain = (volume of k-hop feature matrix exchanged) × 4 bytes. B_per_round = |θ| × 4. |
| **FedGAT** | B_pretrain = (Chebyshev coefficient block size) × 4 bytes. B_per_round = |θ| × 4. |
| **FedProp-Zero** | B_pretrain = 0. B_per_round = |θ| × 4. Plotted at same x-position as FedProp. |
| **Centralised** | Not plotted on Figure 1. Shown as horizontal reference line (Y only). |

### 7.3 Gap-closed metric (for Figure 2)

Gap closed = (FedProp(Diff) − FedProp-Zero) / (FedProp-Full − FedProp-Zero) × 100%.

A value near 100% means FedProp recovers nearly all performance lost by zero-hop local training. Values above 100% are possible (FedProp beats the oracle) — annotate but do not clip.

## 8. Paper Structure and Experiment Placement

| | |
|:-:|:-:|
| **Abstract** | Cite Claim A with one concrete number: FedProp recovers X% of the missing-neighbour performance gap on Cora (non-IID), with zero additional inter-client communication. |
| **§1 Introduction** | State all four claims. Reference Figure 1 (communication trade-off) as the motivating visual. |
| **§2 Related Work** | Two-sentence FedSage+/FedDEP paragraph (different protocol family). Dedicated FedCog contrast paragraph (same setting, different comm. cost). |
| **§4 Method** | Define FedProp-Zero, FedProp-Full, FedProp(Adj), FedProp(Diff) as the four variants. State T=50, h=0.1, boundary reset, L=1. |
| **§5.1 Setup** | State: 8 datasets, partition protocol (Dirichlet), K=10, 10 seeds, FedAvg. Reference Table of hyperparameters. |
| **§5.2 Main results (GCN)** | Table 1 + Figure 2 (recovery). Discuss Claim A. |
| **§5.3 Model-agnosticity (GAT)** | Table 2. Discuss Claim B. |
| **§5.4 Robustness** | Figure 3 (β sweep) + Figure 4 (K scaling). Discuss Claim C. |
| **§5.5 Communication efficiency** | Figure 1. State FedProp's B_pretrain = 0 explicitly. Compare to FedGCN-1hop and FedGAT. |
| **§6 Limitations** | Table 3 (heterophilic). Discuss Claim D. Connect to T1/T2/T3 error bound. |
| **Appendix** | Table A1 (Amazon), Table A2 (PE ablation), Figure A3 (T sweep), Table A4 (1-hop/2-hop + privacy). |

*End of Experimental Plan — FedProp / Kipkirui & Barros / Carnegie Mellon University Africa*
