---
title: "Comprehensive Experimental Literature Report — Federated Graph Learning"
type: experimental-literature-report
source: google-drive
drive-id: 19VSJYHKSypmUnpELBx9ABAmd3sBUwnRzAYWwnc47YXs
created: 2026-05-01
tags: [fedprop, experiments, literature, baselines, hyperparameters, protocols, tmlr]
project: tmlr_fedprop_paper
---

**Comprehensive Experimental Literature Report**

**Federated Graph Learning — Subgraph Node Classification**

*FedProp — Kipkirui & Barros, Carnegie Mellon University Africa | Working Reference*

  

# **1.  Purpose and Scope**

This document is a single, unified reference for all experimental setup details relevant to FedProp. It combines source-verified hyperparameter facts pulled directly from arXiv, per-paper experimental summaries, corrections to prior claims, heterophilic dataset handling, a complete dataset statistics catalogue, and compute resource reporting. All facts marked ✓ were verified from the primary arXiv source. Discrepancies with prior discussion are flagged and corrected.

Papers are organised into four groups: (i) centralised GNN backbones that define upper-bound targets; (ii) transmission-based federated methods; (iii) generative/imputation federated methods; (iv) FedProp itself. Additionally, a separate section covers the heterophilic literature, which none of the four primary comparison papers address.

  

> **IMPORTANT:** FedSage+ and FedDEP use inductive 60/20/20 splits with Louvain partitioning. FedGCN, FedGAT, and FedProp use transductive Planetoid fixed splits with Dirichlet partitioning. These are different learning settings and cannot be placed in the same accuracy table without an explicit protocol disclaimer.

  

# **2.  Source Verification & Corrections**

Several hyperparameter claims circulating in prior discussion do not match the primary arXiv sources. The following corrections were verified by fetching and reading the actual paper PDFs and HTML mirrors.

  

| **Paper** | **Claimed in prior discussion** | **Verified from arXiv source ✓** | **Implication for our paper** |
| :-- | :-- | :-- | :-- |
| **FedGCN** arXiv:2201.12433 | SGD, lr=0.5, 300 iters, 3 local steps/round | Paper states: 'we use a 2-layer GCN with Kipf & Welling (2016)'s hyper-parameters.' That is Adam lr=0.01, hidden 16, dropout 0.5, wd=5e-4. No mention of SGD or 300 rounds for Cora/Citeseer. | FedProp's own choice of SGD lr=0.5 is NOT borrowed from FedGCN. It must be independently justified in our paper — e.g., cite Kipf & Welling's original code which supports both Adam and SGD. |
| **FedGAT** arXiv:2412.16144 | Adam lr=0.1, reg=0.001, no dropout in comparison setup | Paper states: 'All model parameters kept the same as the centralised GAT.' That is Adam lr=0.005, hidden 8×8=64, dropout=0.6, wd=5e-4. Chebyshev degree-16 approximation. | FedGAT and FedProp-GAT use the same backbone hyperparameters (both inherit from Velickovic et al.). This strengthens our backbone-agnostic claim. |
| **FedSage+** arXiv:2106.13430 | 50 epochs, train/val/test=60/20/20 | Local epoch = 1 per FL round (not 50). 60/20/20 confirmed. Adam lr=0.001, batch=64, sample=5/layer confirmed. Compute: 8× NVIDIA GTX 1080 Ti. 4th dataset is MSAcademic, not Flickr/Reddit. | FedSage+ is inductive (60/20/20); FedProp is transductive (Planetoid fixed splits). These are different learning settings — not directly comparable without explicit disclaimer. |
| **FedDEP** arXiv:2401.04336 | 50 epochs, Adam optimizer | SGD (not Adam), lr=0.1, batch=32, sample=5/layer. Embedding dim: 128 Cora, 64 CiteSeer, 256 Pubmed/MSAcademic. Same Louvain+60/20/20 as FedSage+. | FedDEP uses SGD lr=0.1 while FedSage+ uses Adam lr=0.001 — optimizer sensitivity within the generative family. Confirms FedProp should document optimizer choice carefully. |

  

# **3.  Centralised Backbone Papers**

These two papers define the standard architectures and hyperparameters used as backbones in all federated methods. Their centralized performance is the upper bound every federated paper targets.

  

## **3.1  Graph Convolutional Networks (GCN)**

**Reference:** Kipf, T. N. & Welling, M. (ICLR 2017). Semi-Supervised Classification with Graph Convolutional Networks. *arXiv:1609.02907.*

  

| **Setting**          | **Value**                                                                                              |
| :------------------- | :----------------------------------------------------------------------------------------------------- |
| **Task**             | Semi-supervised node classification (transductive)                                                     |
| **Datasets**         | Cora, Citeseer, Pubmed — Planetoid citation networks                                                   |
| **Architecture**     | 2-layer GCN; ReLU first layer, Softmax output; self-loop augmented adjacency Â = D̃^{-1/2} Ã D̃^{-1/2} |
| **Hidden dimension** | 16 units (2 layers). Scaled to 256 for OGBN datasets in federated extensions.                          |
| **Dropout**          | 0.5 on both feature matrix and hidden representations                                                  |
| **Optimizer**        | Adam                                                                                                   |
| **Learning rate**    | 0.01                                                                                                   |
| **Weight decay**     | 5 × 10⁻⁴ on all parameters                                                                             |
| **Training**         | 200 max epochs; early stopping on validation loss, patience 10                                         |
| **Data splits**      | Standard Planetoid: 20 nodes/class train, 500 val, 1000 test — fixed                                   |
| **Metric**           | Test accuracy (%) on the fixed 1000-node test set                                                      |
| **Reported runs**    | Single run in original paper. Federated extensions typically average over 10 runs.                     |
| **Note**             | BatchNorm1d added between layers when applied to OGBN-Arxiv (follows OGB convention, Hu et al. 2020).  |

  

## **3.2  Graph Attention Networks (GAT)**

**Reference:** Velickovic, P. et al. (ICLR 2018). Graph Attention Networks. *arXiv:1710.10903.*

  

| **Setting** | **Value** |
| :-- | :-- |
| **Task** | Semi-supervised node classification (transductive); inductive on PPI |
| **Datasets** | Cora, Citeseer, Pubmed, PPI |
| **Architecture** | 2 attention layers. Hidden: 8 attention heads × 8 features = 64-dim. Output: 1 head (multi-class); 6 heads (PPI). ELU activation between layers. |
| **Dropout** | 0.6 — applied to both input features and attention coefficients |
| **Optimizer** | Adam |
| **Learning rate** | 0.005 (Cora, Citeseer, PPI); 0.01 (Pubmed) |
| **Weight decay** | 5 × 10⁻⁴ (Cora, Citeseer, Pubmed); 0 (PPI — inductive) |
| **Training** | Up to 100,000 gradient steps; early stopping patience 100 on validation accuracy |
| **Data splits** | Standard Planetoid splits (identical to GCN paper) |
| **Metric** | Test accuracy (%) averaged over 10 runs (mean ± std) |
| **Reported runs** | 10 runs — the original GAT paper is the first to report 10-run statistics |
| **Note** | All federated GAT methods (FedGAT, FedProp-GAT) inherit these exact architecture parameters. |

  

# **4.  Federated Methods — Transmission-Based**

These methods share encrypted features or polynomial approximations once before training. After the pre-training round, only model parameters are exchanged during FedAvg aggregation.

  

## **4.1  FedGCN**

**Reference:** Yao, Y., Jin, W., Ravi, S., & Joe-Wong, C. (NeurIPS 2024). FedGCN: Convergence-Communication Tradeoffs in Federated Training of Graph Convolutional Networks. *arXiv:2201.12433.*

  

| **Setting** | **Value** |
| :-- | :-- |
| **Datasets** | Cora (2,708 nodes / 5,429 edges); Citeseer (3,327 / 4,732); Ogbn-Arxiv (169,343 / 1.17M); Ogbn-Products (2.45M / 61.9M) |
| **Architecture** | 2-layer GCN for Cora/Citeseer; 3-layer GCN + BatchNorm for Ogbn-Arxiv; 2-layer GraphSAGE for Ogbn-Products |
| **Hyperparameters** | Cora/Citeseer: Kipf & Welling (2016) defaults — Adam, lr=0.01, hidden=16, dropout=0.5, wd=5e-4. Ogbn: Hu et al. (2020) OGB defaults — Adam, hidden=256, dropout=0.5. |
| **Partitioning** | Dirichlet label distribution with parameter β. Large β ≈ IID; small β ≈ non-IID |
| **Clients** | 10 primary; 1–20 tested in scaling experiments |
| **Communication** | ONE pre-training round: 1-hop (or 2-hop) encrypted neighbor features using Homomorphic Encryption. Zero inter-client communication per round thereafter. |
| **Aggregation** | FedAvg (synchronous, weighted by client data size) |
| **Metric** | Test accuracy (%). Communication cost (MB). Convergence speed. |
| **Reported runs** | 10 runs averaged. Mean ± std reported. |
| **Key finding** | 1-hop pre-training is sufficient for GCNs up to 10 layers. 100× less communication than prior methods. 51.7% faster convergence on average. |
| **Hardware** | Not reported. |

  

## **4.2  FedGAT**

**Reference:** Ambekar, S., Yao, Y., Li, R., & Joe-Wong, C. (arXiv 2024). FedGAT: A Privacy-Preserving Federated Approximation Algorithm for Graph Attention Networks. *arXiv:2412.16144.*

  

| **Setting** | **Value** |
| :-- | :-- |
| **Datasets** | Cora, Citeseer, Pubmed |
| **Architecture** | 2-layer GAT; 8 heads × 8 features = 64 hidden; 1 output head; ELU activation. Degree-16 Chebyshev polynomial approximation of attention coefficients. |
| **Hyperparameters** | Identical to centralised GAT (Velickovic et al. 2018): Adam lr=0.005, dropout=0.6, wd=5e-4, hidden 8×8=64 |
| **Partitioning** | Dirichlet β=1 (non-IID); β=10,000 (IID) |
| **Clients** | 1–20; primary comparison at 10 |
| **Communication** | ONE pre-training round: communicates polynomial approximation terms. Zero inter-client communication per round. Optionally uses HE for privacy. |
| **Aggregation** | FedAvg (synchronous) |
| **Metric** | Test accuracy (%) averaged over 10 runs |
| **Reported runs** | 10 runs |
| **Key finding** | Nearly matches centralised GAT accuracy. Robust to client count and data distribution. Outperforms FedGCN on all benchmarks. |
| **Hardware** | Not reported. |

  

# **5.  Federated Methods — Generative / Imputation**

These methods generate missing cross-client neighbor features locally using trained models. They incur ongoing communication overhead every round because generator parameters and embeddings are continuously shared.

  

## **5.1  FedSage+**

**Reference:** Zhang, K., Yang, C., Li, X., Sun, L., & Yiu, S. M. (NeurIPS 2021). Subgraph Federated Learning with Missing Neighbor Generation. *arXiv:2106.13430.*

  

> **PROTOCOL DIFFERENCE:** FedSage+ uses Louvain community partitioning and inductive 60/20/20 splits. FedProp uses Dirichlet partitioning and transductive Planetoid fixed splits. These protocols must not be compared in the same accuracy table without an explicit disclaimer.

  

| **Setting** | **Value** |
| :-- | :-- |
| **Datasets** | Cora, Citeseer, Pubmed, MSAcademic — 4 datasets |
| **Architecture** | 2-layer GraphSAGE with mean aggregator. Missing neighbor generator (NeighGen) built on top of local GraphSAGE embeddings. |
| **Hyperparameters** | Adam, lr=0.001; batch size=64; 5 nodes sampled per layer; local epoch=1 per FL round |
| **Data splits** | Train/Val/Test = 60%/20%/20% (random, inductive — NOT Planetoid fixed splits) |
| **Graph impairment ratio** | h% ∈ [5%, 15%] — proportion of nodes held out to train the generator |
| **Partitioning** | Louvain community detection (not Dirichlet). 3, 5, and 10 clusters of similar sizes. |
| **Clients** | 3, 5, and 10 — all reported |
| **Communication** | HIGH: generator parameters AND generated node embeddings shared every round. Per-round cross-client exposure. |
| **Aggregation** | FedAvg for both node classifier and missing neighbor generator parameters |
| **Metric** | Test accuracy (%) on the global test set |
| **Reported runs** | ~5 runs (count not explicitly stated in main paper) |
| **Hardware** | Server with 8× NVIDIA GeForce GTX 1080 Ti GPUs — only paper in this comparison to report hardware explicitly. |
| **Key finding** | FedSage+ outperforms local training and FedSage (no generator) across all settings. Performance gap widens as client count increases. |

  

## **5.2  FedDEP — Deep Efficient Private Neighbor Generation**

**Reference:** Zhang, K. et al. (SDM 2024). Deep Efficient Private Neighbor Generation for Subgraph Federated Learning. *arXiv:2401.04336.*

  

| **Setting** | **Value** |
| :-- | :-- |
| **Datasets** | Cora, CiteSeer, Pubmed, MSAcademic — same 4 datasets as FedSage+ for direct comparison |
| **Architecture** | 2-layer GraphSAGE + DGen (deep GNN generator using multi-hop embeddings) + Embedding-Fused Graph Convolution (EFGC) |
| **Hyperparameters** | SGD (not Adam), lr=0.1; batch size=32; 5 nodes sampled per layer; local epoch=1 per FL round |
| **Embedding dimension dz** | 128 (Cora), 64 (CiteSeer), 256 (Pubmed/MSAcademic) — selected from {64, 128, 256} |
| **Data splits** | 60/20/20 (same as FedSage+, inductive) |
| **Partitioning** | Louvain (same as FedSage+ — direct comparison is valid between the two) |
| **Clients** | 3, 5, 10 |
| **Communication** | Medium–high: GNN embedding prototypes shared (more efficient than FedSage+'s per-node embeddings) |
| **Privacy** | Edge-local Differential Privacy via NFDP (noise-free DP using embedding geometry) |
| **Aggregation** | FedAvg |
| **Metric** | Test accuracy (%). Communication cost comparison to FedSage+. |
| **Hardware** | Not reported. |
| **Key advantage over FedSage+** | Multi-hop context from DGen; more efficient prototype sharing; formal privacy via NFDP. |

  

## **5.3  FedCog — Federated Learning over Coupled Graphs**

**Reference:** Lei, R. et al. (IEEE TPDS 2023). Federated Learning over Coupled Graphs. *arXiv:2301.11099. IEEE Trans. Parallel Distrib. Syst., 34(4), 1159–1172.*

  

> **NOVELTY THREAT:** Multiple FedProp reviewers flagged FedCog as similar. Key difference: FedCog requires sharing intermediate embeddings of border nodes between neighbouring clients every round. FedProp performs all propagation purely locally with zero inter-client communication. This distinction must be made explicit in the paper.

  

| **Setting** | **Value** |
| :-- | :-- |
| **Datasets** | 12 datasets: Cora, Citeseer, Pubmed, DBLP, Amazon-CS, Amazon-Photo, Coauthor-CS, Coauthor-Phy, ACM, Flickr, UAI, Reddit |
| **Architecture** | 2-layer GCN (SGC-simplified); decoupled into internal graph + border graph (bipartite between internal and external nodes) |
| **Graph convolution** | Two-step: (1) intra-client convolution on internal graph; (2) inter-client convolution on border graph using received embeddings. Mathematically equivalent to full GCN on global graph. |
| **Hyperparameters** | Adam, lr=0.01, wd=5e-4; 100-dim embedding for link prediction tasks |
| **Partitioning** | METIS (balanced/structural). K-Means (feature-skewed/unbalanced). Both tested. |
| **Clients** | 3, 10, and 100 — very large scale tested |
| **Communication** | HIGH: border node intermediate embeddings shared between neighbouring clients every round. Cost ∝ |E*| (number of cross-client edges). |
| **Privacy** | LNNC (Local Noise for Neighbour Concealment): controlled noise injection on border embeddings before transmission. Formally proven secure. |
| **Metric** | Test accuracy (%) for node classification; AUC for link prediction |
| **Key finding** | Up to 14.7% improvement over FedAvg on Cora with 100 clients. Stable across METIS/K-Means partitioning. |
| **Limitation** | Communication cost ∝ graph size — expensive on large graphs. Not tested on heterophilic graphs. Requires knowledge of inter-client edge topology. |
| **Hardware** | Not reported. |

  

# **6.  FedProp — Current Experimental Setup**

Documented here for cross-reference alongside the baselines above.

  

| **Setting** | **Value** |
| :-- | :-- |
| **Backbone** | GCN or GAT (model-agnostic). Backbone hyperparameters inherited from Kipf & Welling (GCN) and Velickovic et al. (GAT). |
| **Propagation** | T=50 iterative propagation steps per client (local, zero inter-client cost). Operators: normalised adjacency (Adj) or discrete diffusion (Diff). Optionally: RFP positional encodings R=16 seeds, P=5 steps. |
| **GCN architecture** | 2 layers (3 for OGBN-Arxiv). Hidden: 16 (256 for OGBN). ReLU, Softmax. Dropout 0.5. Weight decay 5×10⁻⁴. |
| **GAT architecture** | 2 layers. 8 attention heads × 8 features = hidden 64. ELU. Dropout 0.6 (features + attention). Weight decay 5×10⁻⁴. |
| **Optimizer (Cora/Citeseer)** | SGD, lr=0.5, wd=5×10⁻⁴ |
| **Optimizer (Pubmed/Amazon/OGBN)** | Adam, lr=0.01, wd=5×10⁻⁴ |
| **Training** | 600 max local epochs per round; early stopping on validation loss (patience 10) |
| **Global rounds** | ~200 (controlled by early stopping) |
| **Partitioning** | Label Dirichlet distribution: β=10,000 (IID); β=10 and β=1 (non-IID). 10 clients primary; 1–20 tested. |
| **Data splits** | Standard Planetoid splits for Cora/Citeseer/Pubmed (transductive). Random 60/20/20 for Amazon datasets. |
| **Aggregation** | FedAvg (synchronous). Zero inter-client communication — only model parameters aggregated at server. |
| **Datasets completed** | Cora, Citeseer, Pubmed, Amazon-Computers, Amazon-Photos |
| **Datasets pending** | OGBN-Arxiv, Texas (required), Wisconsin (required) |
| **Reported runs** | 10 seeds; mean ± std on test split |
| **Metric** | Test accuracy (%) |
| **Hardware** | Not yet reported — should be added to paper |

  

# **7.  Master Hyperparameter Comparison — All Papers**

All source-verified facts. ✓ = directly verified from arXiv. ▲ = corrected from prior discussion. Purple = FedProp (ours).

  

| **Paper / Source** | **Backbone** | **Datasets** | **Partition** | **Optim** | **LR** | **Hidden** | **Dropout** | **Batch/Sample** | **Rounds/Epochs** | **Clients K** | **Compute** |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| **GCN** Kipf & Welling ICLR 2017 | 2L GCN ReLU→Softmax | Cora, Citeseer Pubmed | Planetoid (fixed splits) | Adam | 0.01 | 16 (256 OGBN) | 0.5 | Full graph (transductive) | 200 ep + ES pat.10 | N/A central. | Not reported |
| **GAT** Velickovic et al. ICLR 2018 | 2L GAT 8h×8f, ELU 1h output | Cora, Citeseer Pubmed, PPI | Planetoid (fixed splits) | Adam | 0.005 Cora/Cite 0.01 Pubmed | 64 (8×8) | 0.6 feat+attn | Full graph (transductive) | 100k iters + ES pat.100 | N/A central. | Not reported |
| **FedGCN ✓** Yao et al. NeurIPS 2024 | 2L GCN (3L+BN OGBN) GSAGE Prods | Cora, Citeseer Ogbn-Arxiv Ogbn-Products | Dirichlet β IID/non-IID | Adam (Kipf & Welling) | 0.01 Cora/Cite OGB default | 16 Cora/Cite 256 OGBN | 0.5 | Full graph (transductive) | Not stated (≈200–300) | 10 (1–20) | Not reported |
| **FedGAT ✓** Ambekar et al. arXiv 2412.16144 | 2L GAT 8h×8f, ELU Chebyshev d=16 | Cora, Citeseer Pubmed | Dirichlet β=1 (non-IID) β=10000 (IID) | Adam (Velickovic) | 0.005 | 64 (8×8) | 0.6 | Full graph (transductive) | Not stated (≈200) | 10 (1–20) | Not reported |
| **FedSage+ ✓** Zhang et al. NeurIPS 2021 | 2L GraphSAGE mean agg. 5 neigh/layer | Cora, Citeseer Pubmed MSAcademic | Louvain 3/5/10 clusters | Adam | 0.001 | Task-specific | — | Batch=64 Sample=5 | 1 ep/round (FL rounds) | 3/5/10 | 8× GTX 1080 Ti |
| **FedDEP ✓** Zhang et al. SDM 2024 | 2L GraphSAGE + DGen encoder mean agg. | Cora, CiteSeer Pubmed MSAcademic | Louvain 3/5/10 clusters | SGD | 0.1 | 128/64/256 (per dataset) | — | Batch=32 Sample=5 | 1 ep/round | 3/5/10 | Not reported |
| **FedCog** Lei et al. IEEE TPDS 2023 | 2L GCN/SGC decoupled border+internal | 12 datasets incl. Cora–Reddit (see §5) | METIS + K-Means both tested | Adam | 0.01 | 100-dim (link pred) | — | Full graph | Not stated | 3/10/100 | Not reported |
| **FedStruct** arXiv 2402.19163 | Decoupled GCN + Hop2Vec struct. embeds | Cora, Citeseer Pubmed Chameleon ⚠ Amazon Photo Amazon Ratings ⚠ | Random + Louvain + K-Means | Adam | Tuned per dataset | Tuned | Tuned | Full graph | Not stated | 2/5/10/20 | Not reported |
| **FedProp (ours)** Kipkirui & Barros CMU Africa | GCN or GAT agnostic T=50 prop, R=16 PE | Cora, Citeseer Pubmed ✓ Amazon CS/Photo ✓ OGBN-Arxiv (plan) Texas/Wisc. (plan) | Dirichlet β=10000 (IID) β=10/1 (non-IID) | SGD (Cora/Cite) Adam (rest) | 0.5 SGD 0.01 Adam | 16 GCN 64 GAT (256 OGBN) | 0.5 GCN 0.6 GAT | Full graph (transductive) | 600 ep + ES pat.10 | 10 (1–20) | TBD |

  

# **8.  Two Distinct Training Families**

Comparing papers across families in the same accuracy table is methodologically incorrect without a protocol disclaimer.

  

## **Family A — Message-passing federated baselines (FedProp's family)**

- Same transductive setting; Planetoid fixed splits; standard GCN/GAT backbones; Dirichlet partitioning.
- FedGCN: Adam lr=0.01, 2L GCN hidden 16, Dirichlet, Planetoid splits, transductive.
- FedGAT: Adam lr=0.005, 2L GAT 8×8, Dirichlet, Planetoid splits, transductive.
- FedProp: SGD lr=0.5 (Cora/Cite) or Adam lr=0.01, same splits and partition. Model-agnostic.
- **Comparisons within this family are CLEAN — protocols match exactly.**

  

## **Family B — Generative / inductive subgraph-FL methods**

- Inductive 60/20/20 splits; Louvain community partitioning; GraphSAGE backbone; per-round communication.
- FedSage+: Adam lr=0.001, batch=64, GraphSAGE, Louvain, 60/20/20, 8× GTX 1080 Ti.
- FedDEP: SGD lr=0.1, batch=32, GraphSAGE+DGen, Louvain, 60/20/20.
- **Cross-family comparison (Family A vs. B) requires re-running under a unified protocol, OR a clear disclaimer stating the protocol mismatch.**

  

# **9.  Heterophilic Dataset Handling — Dedicated Section**

None of the four primary comparison papers (FedGCN, FedGAT, FedSage+, FedDEP) test on heterophilic graphs. Heterophilic experiments come from a parallel literature strand. FedProp reviewers require at least Texas or Wisconsin.

  

| **Paper** | **Heterophilic datasets** | **Technique for heterophily** | **Partition / clients** | **Training setup** | **Key findings** |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **FedStruct** arXiv:2402.19163 | Chameleon (h=0.23) Squirrel (h=0.22) Amazon Ratings (h=0.38) | Decoupled GCN + Hop2Vec structural encodings. No raw features shared — only topological embeddings. Avoids homophily assumption entirely. | Random (primary) Louvain, K-Means 2/5/10/20 clients | Adam, tuned LR/dropout per dataset. 60/20/20 splits. | Only subgraph-FL method that explicitly handles heterophilic graphs. Claims first-in-class for heterophilic subgraph FL. Near-centralized accuracy on Chameleon/Squirrel. Direct reference point for FedProp Texas/Wisconsin. |
| **AdaFGL** arXiv:2401.11750 | Texas (h=0.11) Wisconsin (h=0.20) Cornell (h=0.30) Chameleon (h=0.23) | Topology-aware averaging. Adapts aggregation per client based on local homophily/heterophily. Does not require feature sharing. | Louvain 10 clients | Adam. Standard hyperparams per GNN backbone. Evaluates topology-heterogeneous FL. | Strong results on all four heterophilic datasets. Must be cited in related work when FedProp reports Texas/Wisconsin. Positions well against FedProp's expected degradation. |
| **FGSSL** arXiv:2406.18937 | Actor (h≈0.22) Cornell (h=0.30) Texas (h=0.11) | Federated semantic + structural learning. Contrasts nodes across classes for discrimination; structural alignment for heterophilic setting. | Louvain 10 clients | Adam, standard hyperparams. | One of few FL methods testing on Actor. Relevant as additional related work alongside AdaFGL. |
| **FedProp (ours) ⚠ REQUIRED** | Texas (h=0.11) — REQUIRED by reviewers Wisconsin (h=0.20) — REQUIRED by reviewers | Dirichlet energy minimisation assumes smoothness. Violated under heterophily. Expected performance degradation — must be quantified via 3-part error bound (T1 propagation, T2 boundary, T3 irreducible heterophily). | Dirichlet β=10 (non-IID) β=10000 (IID) 10 clients | Same as Cora/Cite: GCN 2L hidden 16, SGD lr=0.5, wd=5e-4, ES patience 10, 10 seeds. Both datasets run in minutes (<300 nodes each). | Expected: FedProp degrades on heterophilic graphs. Frame as acknowledged limitation tied to smoothness assumption. Compare to FedStruct and AdaFGL as het.-capable baselines. |

  

> **ACTION PLAN FOR FEDPROP:**
> 1. Run Texas (183 nodes) and Wisconsin (251 nodes) — both complete in under 5 minutes on any GPU.
> 2. Expected outcome: accuracy degrades vs. homophilic datasets — document and quantify this using the 3-part error decomposition.
> 3. Frame the result as: 'We quantify FedProp's limitation on heterophilic graphs and provide a theoretical account via T1 (propagation error), T2 (boundary bias), T3 (irreducible heterophily).'
> 4. Compare against FedStruct (arXiv:2402.19163) and AdaFGL (arXiv:2401.11750) as heterophilic-capable baselines.
> 5. Note: Texas/Wisconsin have duplicate node issues in some versions. Use the cleaned splits from Pei et al. (Geom-GCN, ICLR 2020).

  

# **10.  Benchmark Dataset Statistics**

All datasets used across the compared papers. ▲ = homophilic (high h). ▼ = heterophilic (low h). ★ = required for FedProp by reviewers. Homophily h = fraction of edges connecting same-label nodes (Zhu et al. 2020).

  

| **Dataset** | **Graph type** | **|V| nodes** | **|E| edges** | **Feat F** | **Classes C** | **Avg deg.** | **Homophily h** | **Label split** | **Used by** |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| **Citation Networks — Homophilic** |  |  |  |  |  |  |  |  |  |
| **Cora** | Citation network | 2,708 | 5,429 | 1,433 | 7 | 4.01 | 0.81 ▲ | 140/500/1000 Planetoid fixed | All papers |
| **Citeseer** | Citation network | 3,327 | 4,732 | 3,703 | 6 | 2.84 | 0.74 ▲ | 120/500/1000 Planetoid fixed | All papers |
| **Pubmed** | Citation network | 19,717 | 44,338 | 500 | 3 | 4.50 | 0.80 ▲ | 60/500/1000 Planetoid fixed | All papers |
| **DBLP** | Co-author/citation | 17,716 | 105,734 | 1,639 | 4 | ~12 | High ▲ | Paper-specific | FedCog only |
| **MSAcademic** | Citation/coauth. hybrid | ~18,333 | ~163,788 | varies | varies | ~18 | High ▲ | 60/20/20 random | FedSage+, FedDEP |
| **Ogbn-Arxiv** | Citation (OGB large) | 169,343 | 1,166,243 | 128 | 40 | 13.7 | 0.66 ▲ | OGB std 54/18/28% | FedGCN; FedProp (planned) |
| **Ogbn-Products** | Co-purchase (OGB XL) | 2,449,029 | 61,859,140 | 100 | 47 | 50.5 | High ▲ | OGB std | FedGCN only |
| **Co-purchase & Co-authorship Networks — Homophilic** |  |  |  |  |  |  |  |  |  |
| **Amazon-Computers** | Co-purchase | 13,752 | 287,209 | 767 | 10 | 41.7 | 0.78 ▲ | Random 60/20/20 | FedCog; FedProp ✓ |
| **Amazon-Photos** | Co-purchase | 7,650 | 238,162 | 745 | 8 | 62.3 | 0.83 ▲ | Random 60/20/20 | FedCog; FedStruct; FedProp ✓ |
| **Coauthor-CS** | Co-authorship | 18,333 | 163,788 | 6,805 | 15 | 17.9 | High ▲ | Paper-specific | FedCog only |
| **Coauthor-Phy** | Co-authorship | 34,493 | 495,924 | 8,415 | 5 | 28.7 | High ▲ | Paper-specific | FedCog only |
| **ACM** | Paper network | 3,025 | 26,256 | 1,870 | 3 | 17.4 | High ▲ | Paper-specific | FedCog only |
| **Social & Large-Scale Networks** |  |  |  |  |  |  |  |  |  |
| **Flickr** | Social (image sharing) | 89,250 | 899,756 | 500 | 7 | ~20 | Low–med. | Louvain random | FedSage+; FedDEP; FedCog |
| **Reddit** | Social (discussion) | 232,965 | 11,606,919 | 602 | 41 | 99.7 | High ▲ | Louvain random | FedSage+; FedDEP; FedCog |
| **UAI 2010** | Social (Alchemy) | ~3,067 | ~28,311 | 4,973 | 2 | ~18 | Low–med. | Paper-specific | FedCog only |
| **Heterophilic Benchmarks — Low Homophily** |  |  |  |  |  |  |  |  |  |
| **Chameleon ⚠** | Wikipedia pages | 2,277 | 36,101 | 2,325 | 5 | 31.6 | 0.23 ▼ | Random 60/20/20 | FedStruct; AdaFGL |
| **Squirrel ⚠** | Wikipedia pages | 5,201 | 217,073 | 2,089 | 5 | 83.5 | 0.22 ▼ | Random 60/20/20 | FedStruct (appendix) |
| **Amazon Ratings ⚠** | Rating network | 24,492 | 93,050 | 300 | 5 | 7.6 | 0.38 ▼ | Random 50/25/25 | FedStruct only |
| **Actor ⚠** | Actor co-appear. | 7,600 | 33,544 | 931 | 5 | ~7 | 0.22 ▼ | Random 60/20/20 | FGSSL only |
| **Texas ⚠ ★** | Web graph (univ.) | 183 | 325 | 1,703 | 5 | 3.6 | 0.11 ▼▼ | 5-fold CV / 60/20/20 | FedProp REQUIRED ★ |
| **Wisconsin ⚠ ★** | Web graph (univ.) | 251 | 499 | 1,703 | 5 | 4.0 | 0.20 ▼▼ | 5-fold CV / 60/20/20 | FedProp REQUIRED ★ |
| **Cornell ⚠** | Web graph (univ.) | 183 | 298 | 1,703 | 5 | 3.3 | 0.30 ▼ | 5-fold CV / 60/20/20 | FedProp fallback |

  

> **DATASET USAGE NOTES:**
> - Cora/Citeseer/Pubmed — Planetoid fixed splits are non-negotiable for transductive comparison. Never use random splits for these datasets unless explicitly studying split sensitivity.
> - Amazon-CS / Amazon-Photos — No standard split. Use 60/20/20 random with 10 seeds. FedProp has already run these.
> - MSAcademic — Used only by FedSage+ and FedDEP. Not required for FedProp's primary comparison.
> - Texas / Wisconsin — Small enough to run in minutes. Use 5-fold CV or 60/20/20 random splits with 10 seeds.
> - Chameleon / Squirrel — Platonov et al. (ICLR 2023) found significant data leakage in standard versions. Consider Amazon Ratings as a cleaner heterophilic alternative.
> - Ogbn-Arxiv — Use OGB standard splits (≈54%/18%/28%). Requires 3-layer GCN + BatchNorm (OGB convention).

  

# **11.  Compute Resources — What Papers Report**

Compute reporting is sparse across the field. Only FedSage+ explicitly states hardware. The table below records what is reported.

  

| **Paper** | **Hardware stated in paper** | **Training time reported** | **Notes** |
| :-- | :-- | :-- | :-- |
| **GCN (Kipf 2017)** | Not reported | Not reported | Small datasets — seconds on any modern GPU. |
| **GAT (Velickovic 2018)** | Not reported | Not reported | Up to 100k iterations — minutes on GPU. |
| **FedGCN (Yao 2024)** | Not explicitly reported in NeurIPS version | Not reported per dataset | HE encryption overhead measured separately in Appendix E. Code available at github.com/yh-yao/FedGCN. |
| **FedGAT (Ambekar 2024)** | Not reported | Not reported | Chebyshev pre-training communication overhead analysed theoretically. Polynomial degree d=16 chosen as trade-off. |
| **FedSage+ (Zhang 2021) ✓** | Server with 8× NVIDIA GeForce GTX 1080 Ti GPUs (explicitly stated in paper — only paper to report hardware) | Not reported per dataset | Generator pre-training + FL rounds run on same server. Batch-based — GPU utilisation differs structurally from transductive full-graph methods. |
| **FedDEP (Zhang 2024)** | Not reported | Not reported | Same codebase family as FedSage+. Likely similar hardware. |
| **FedCog (Lei 2023)** | Not reported | Not reported | Communication cost analysed analytically: proportional to |E*| border edges between clients. |
| **FedStruct (2024)** | Not reported | Not reported | Structural encoding (Hop2Vec) computed locally — cheaper than feature-sharing methods. No theoretical compute analysis. |
| **FedProp (ours) ⚠ Should report** | Not yet reported — SHOULD BE ADDED to the paper | Not yet reported — SHOULD BE ADDED | FedProp has zero inter-client communication. Compute = local propagation (T=50 sparse mat-mul iters) + FedAvg aggregation. Measure and report: (a) wall-clock per round by dataset, (b) pre-computation cost of propagation (one-time per client). Position propagation as a one-time local cost vs FedSage+'s per-round communication cost. |

  

> **ACTION ITEM** — FedProp should be the first paper in this comparison set to formally report compute.
>
> Suggested text: 'All experiments were run on [hardware]. Mean wall-clock time per global round was X seconds for Cora and Y seconds for Ogbn-Arxiv. Feature propagation (T=50 sparse matrix-vector multiply iterations) adds Z seconds of pre-computation per client, which is non-recurring and scales as O(T × |E_k|) for client k with |E_k| local edges.'
>
> This positions FedProp's compute cost favourably: propagation is a one-time local overhead, not per-round communication like FedSage+/FedCog.

  

# **12.  Summary of Field Norms — What to Adopt in FedProp**

Distilled from the full review above. These are the settings consistently observed across the federated graph learning literature.

  

## **Architecture**

- GCN: 2 layers, hidden 16 (Cora/Citeseer), 256 (OGBN). Dropout 0.5. Weight decay 5×10⁻⁴.
- GAT: 2 layers, 8 heads × 8 features = 64 hidden. Dropout 0.6 (feat + attn). Weight decay 5×10⁻⁴.
- BatchNorm1d between layers for OGBN-Arxiv — required to match OGB baselines.
- GraphSAGE (FedSage+/FedDEP family): 2 layers, mean agg., hidden 256, sample 5 per layer — NOT used in FedProp.

  

## **Optimisation**

- Adam lr=0.01 is the most common single choice. FedProp's split (SGD lr=0.5 for Cora/Cite, Adam lr=0.01 for Pubmed+) must be documented and justified.
- Early stopping with patience 10 is the standard. The only outlier (10,000 rounds) is outside community norms.
- 200–500 global communication rounds is the accepted range for federated GNN training.
- Local epoch = 1 per round is standard for FedAvg. FedSage+/FedDEP confirm this.

  

## **Federated protocol**

- FedAvg (synchronous) is universal for node classification benchmarks.
- 10 clients is the standard test configuration; 1–20 tested for scaling.
- Dirichlet β distribution: β=10,000 for IID, β=1 and β=10 for non-IID — standard in the FedGCN/FedGAT line.
- Louvain partitioning is standard in the FedSage+/FedDEP line. The two protocol families must not be mixed.

  

## **Evaluation**

- 10 seeds with mean ± std is the gold standard. FedProp already complies — state this explicitly.
- Test accuracy (%) on Planetoid fixed test split for citation datasets.
- Centralized GNN (full graph) as upper bound AND local GNN (zero communication) as lower bound must both appear in every results table.
- Communication cost (MB or parameter-transfer count) reported separately from accuracy — this is the second axis.

  

---

*End of Comprehensive Experimental Literature Report — FedProp / Kipkirui & Barros / Carnegie Mellon University Africa*
