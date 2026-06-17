---
title: "Literature Review — Federated Graph Learning for Node Classification"
type: literature-review
source: google-drive
drive-id: 1x7gtendu3Q7jyoWqeMzJc9qv0_pzWoDgYw2PRXu1N8U
created: 2026-05-01
tags: [fedprop, literature, review, federated-learning, graph-neural-networks, tmlr]
project: tmlr_fedprop_paper
---

# Tab 2  

# **Dirichlet Energy Minimization for Feature Propagation on Graphs**

Dirichlet energy provides a way to measure how “smooth” a feature signal is over a graph: low energy means neighboring nodes have similar feature values. Many recent methods use **minimizing Dirichlet energy** to propagate known features to unknown nodes by enforcing this smoothness under boundary constraints.

## **How Dirichlet Energy Is Defined and Interpreted**

### **Smoothness Functional on a Graph**

  - For node features (x), Dirichlet energy on an undirected graph is typically  
     (E(x) = \\tfrac12 \\sum_{i,j} \\tilde a_{ij}(x_i - x_j)^2 = \\tfrac12 x^\\top L x), where (\\tilde a_{ij}) are (normalized) adjacencies and (L) is the Laplacian (Rossi et al., 2021; Zhou et al., 2025; Kumar et al., 2022; Xie et al., 2025).
  - Low energy means **neighboring nodes have similar features**, i.e., the signal is smooth and homophilous (Rossi et al., 2021; Di Giovanni et al., 2022; Zhou et al., 2025; Kumar et al., 2022; Xie et al., 2025).

## **Core Propagation Mechanism: Gradient Flow and Diffusion**

### **From Energy Minimization to Feature Propagation**

  - Feature Propagation (FP) for missing node attributes is formulated as  
     “find (x) that minimizes Dirichlet energy, subject to keeping known node features fixed” (Dirichlet boundary conditions) (Rossi et al., 2021; Zhou et al., 2025; Guan & Shi, 2025).
  - Direct closed-form minimizers exist but are expensive on large graphs, so methods use **gradient flow**:  
     (\\dot x(t) = -\\nabla E(x(t))), with known-node values clamped (Rossi et al., 2021; Zhou et al., 2025).
  - For Dirichlet energy, (\\nabla E(x) = Lx), giving a **heat-diffusion equation on the graph**; its long-time limit on unknown nodes gives the interpolated features (Rossi et al., 2021; Zhou et al., 2025).

### **Discrete Iterative Propagation**

A common discrete scheme is repeatedly multiplying by a diffusion matrix and resetting observed nodes:

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| **Step** | **Operation (conceptual)** | **Role** | **Citations** |
| 1 | Initialize (x^{(0)}) with known + guesses | Start state | (Rossi et al., 2021; Zhou et al., 2025; Guan & Shi, 2025) |
| 2 | (x^{(k+1)} \\\\leftarrow \\\\tilde A x^{(k)}) | Diffuse features | (Rossi et al., 2021; Zhou et al., 2025; Guan & Shi, 2025) |
| 3 | Reset known nodes to original values | Enforce boundary | (Rossi et al., 2021; Zhou et al., 2025; Guan & Shi, 2025) |

**Figure 1:** Iterative diffusion that minimizes graph Dirichlet energy

This forward-Euler discretization of gradient flow converges to the Dirichlet-energy minimizer on unknown nodes, i.e., a **harmonic extension** of known features (Rossi et al., 2021; Zhou et al., 2025; Guan & Shi, 2025).

## **Extensions and Applications**

  - **Directed graphs:** DEFP4D extends Dirichlet energy to directed graphs via a modified operator (P = (D_o + D_I)^{-1}(A + A^\\top)), and uses the same gradient-flow + discretization idea for traffic-state estimation (Zhou et al., 2025).
  - **Cold-start and boundary design:** AttriReBoost explicitly views FP as Dirichlet-energy minimization, then modifies boundary conditions and graph connectivity (virtual edges) to improve propagation and convergence when many nodes have missing or low-degree attributes (Guan & Shi, 2025).
  - **Pre-coding / preprocessing:** Other models use a Dirichlet-energy-based feature “precoding” step before downstream GNNs or contrastive learning, treating propagation as structure–attribute energy minimization to reconstruct missing attributes (Rossi et al., 2021; Zhang et al., 2023; Zhou et al., 2021; Xie et al., 2025).

## **Conclusion**

Dirichlet energy minimization is used for feature propagation by treating node attributes as a graph signal and finding the **smoothest extension** of known features over the graph, under fixed boundary constraints. In practice this is implemented via graph heat diffusion (gradient flow of Dirichlet energy) with repeated diffusion and clamping of observed nodes, and can be generalized to directed graphs and integrated as a fast, scalable preprocessing or decoding step before more complex GNN models.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Di Giovanni, F., Rowbottom, J., Chamberlain, B., Markovich, T., & Bronstein, M. (2022). Understanding convolution on graphs via energies. *Trans. Mach. Learn. Res., 2023*.

Guan, W., & Shi, Z. (2025). Measuring Over-smoothing beyond Dirichlet energy. *ArXiv, abs/2512.06782*.[ https://doi.org/10.48550/arxiv.2512.06782](https://doi.org/10.48550/arxiv.2512.06782)

Kumar, M., Sharma, A., & Kumar, S. (2022). A Unified Framework for Optimization-Based Graph Coarsening. *ArXiv, abs/2210.00437*.[ https://doi.org/10.48550/arxiv.2210.00437](https://doi.org/10.48550/arxiv.2210.00437)

Rossi, E., Kenlay, H., Gorinova, M., Chamberlain, B., Dong, X., & Bronstein, M. (2021). On the Unreasonable Effectiveness of Feature propagation in Learning on Graphs with Missing Node Features. *ArXiv, abs/2111.12128*.

Xie, K., Yang, R., & Wang, S. (2025). Diffusion-based Graph-agnostic Clustering. *Proceedings of the ACM on Web Conference 2025*.[ https://doi.org/10.1145/3696410.3714652](https://doi.org/10.1145/3696410.3714652)

Zhang, X., Li, M., Wang, Y., & Fei, H. (2023). AmGCL: Feature Imputation of Attribute Missing Graph via Self-supervised Contrastive Learning. *ArXiv, abs/2305.03741*.[ https://doi.org/10.48550/arxiv.2305.03741](https://doi.org/10.48550/arxiv.2305.03741)

Zhou, Q., Zhang, Y., Makridis, M., Kouvelas, A., Wang, Y., & Hu, S. (2025). Network-Wide Freeway Traffic Estimation Using Sparse Sensor Data: A Dirichlet Graph Auto-Encoder Approach. *IEEE Transactions on Intelligent Transportation Systems, 26*, 22161-22177.[ https://doi.org/10.1109/tits.2025.3610911](https://doi.org/10.1109/tits.2025.3610911)

Zhou, K., Huang, X., Zha, D., Chen, R., Li, L., Choi, S., & Hu, X. (2021). Dirichlet Energy Constrained Learning for Deep Graph Neural Networks. **, 21834-21846.

  
  

# Tab 3**  
**

## **Graph Laplacian Regularization for Smoothness on Graphs**

Graph Laplacian regularization enforces that a signal (labels, features, or images) varies smoothly across connected nodes. It appears in semi‑supervised learning, graph signal processing, inverse problems, and GNNs as a core smoothness prior.

### **Basic Idea and Standard Laplacian Regularizer**

  - The usual quadratic regularizer is (x^\\top L x), where (L) is the (normalized or unnormalized) graph Laplacian; this is small when neighboring nodes with large edge weights have similar values, thus enforcing **graph smoothness** (Chen et al., 2022; Pang & Cheung, 2016).
  - In semi‑supervised learning, the Dirichlet energy based on (L) is minimized subject to label constraints, yielding graph‑harmonic (smooth) solutions (Flores et al., 2019; Slepčev & Thorpe, 2017; Wang et al., 2016).
  - In image and signal restoration, the same term combined with an ℓ₂ data‑fidelity term yields a linear system that can be solved efficiently and acts as a low‑pass graph filter (Chen et al., 2022; Cai et al., 2024; Pang & Cheung, 2016).

### **p‑Laplacian and Variants**

  - **ℓ_p / p‑Laplacian regularization** replaces the quadratic form by a p‑Dirichlet energy, penalizing large gradients more strongly and avoiding degenerate, “spiky” solutions when labels are very sparse (Alaoui, 2016; Alaoui et al., 2016; Flores et al., 2019; Slepčev & Thorpe, 2017).
  - Theory shows a **phase transition**: for dimension (d), (p \\le d) leads to degenerate, spiky estimates; (p \\ge d+1) yields smooth, non‑degenerate functions while retaining sensitivity to the unlabeled data distribution (Alaoui, 2016; Alaoui et al., 2016).
  - On k‑NN graphs, high‑p / Lipschitz learning keeps information about data density, unlike some random geometric graph settings (Rios et al., 2022; Flores et al., 2019).

### **Weighting, Deformation, and Learned Laplacians**

  - Properly **re‑weighting edges** in Laplacian regularization can remove degeneracy and give stable, well‑posed estimators that converge to smooth continuum limits even with very few labels (Calder & Slepčev, 2018; Chen et al., 2023).
  - **Deformed or coupled Laplacians** modify the local smoothness term or combine anchor and sample graphs to better handle ambiguous samples and multi‑scale structure in SSL (Gong et al., 2015; Zhao et al., 2018; Wang et al., 2016).
  - Several works **learn Laplacians from data** (e.g., enforcing that observed signals are smooth on the learned graph, or building Laplacians from preliminary reconstructions), giving adaptive, data‑dependent regularizers that improve reconstruction quality (Dong et al., 2014; Chen et al., 2022; Bianchi et al., 2023).

### **Beyond Simple Smoothness: Higher‑Order and Gradient Laplacians**

  - Standard Laplacian priors tend to promote **piecewise constant** signals and can cause staircase artifacts; **gradient graph Laplacian regularizers (GGLR)** instead promote planar or piecewise planar reconstructions, better matching manifold‑like data (Chen et al., 2022; Cai et al., 2024).
  - Continuous‑domain analyses interpret Laplacian regularization as **anisotropic diffusion**, clarifying that it can both smooth and sharpen, and linking it to total variation and optimal metric choices for denoising (Pang & Cheung, 2016).
  - Recent GNN work generalizes Laplacian‑based smoothing to **relaxed or even negative Laplacian regularization** to capture both low‑ and high‑frequency information on heterophilic graphs (Li et al., 2024; Salim & Sumitra, 2022).

## **Conclusion**

Across settings, graph Laplacian regularization enforces that solutions change slowly along strongly connected edges, acting as a graph‑based smoothness prior. Extensions via p‑Laplacians, careful weighting, learned/adaptive Laplacians, and higher‑order (gradient) regularizers address degeneracy with few labels, staircase effects, and oversmoothing, while giving stronger theoretical guarantees and improved empirical performance.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Alaoui, A. (2016). Asymptotic behavior of (\\ell_p)-based Laplacian regularization in semi-supervised learning. **, 879-906.

Alaoui, A., Cheng, X., Ramdas, A., Wainwright, M., & Jordan, M. (2016). Asymptotic behavior of ℓp-based Laplacian regularization in semi-supervised learning. *ArXiv, abs/1603.00564*.

Bianchi, D., Evangelista, D., Aleotti, S., Donatelli, M., Piccolomini, E., & Li, W. (2023). A data-dependent regularization method based on the graph Laplacian. *SIAM J. Sci. Comput., 47*, 369-.[ https://doi.org/10.48550/arxiv.2312.16936](https://doi.org/10.48550/arxiv.2312.16936)

Cai, J., Cheung, G., & Chen, F. (2024). Unrolling Plug-and-Play Gradient Graph Laplacian Regularizer for Image Restoration. *IEEE Transactions on Image Processing, 35*, 1817-1831.[ https://doi.org/10.1109/tip.2025.3562425](https://doi.org/10.1109/tip.2025.3562425)

Calder, J., & Slepčev, D. (2018). Properly-Weighted Graph Laplacian for Semi-supervised Learning. *Applied Mathematics & Optimization, 82*, 1111 - 1159.[ https://doi.org/10.1007/s00245-019-09637-3](https://doi.org/10.1007/s00245-019-09637-3)

Chen, F., Cheung, G., & Zhang, X. (2022). Manifold Graph Signal Restoration Using Gradient Graph Laplacian Regularizer. *IEEE Transactions on Signal Processing, 72*, 744-761.[ https://doi.org/10.1109/tsp.2023.3343560](https://doi.org/10.1109/tsp.2023.3343560)

Chen, Z., Wu, Z., Lin, Z., Wang, S., Plant, C., & Guo, W. (2023). AGNN: Alternating Graph-Regularized Neural Networks to Alleviate Over-Smoothing. *IEEE Transactions on Neural Networks and Learning Systems, 35*, 13764-13776.[ https://doi.org/10.1109/tnnls.2023.3271623](https://doi.org/10.1109/tnnls.2023.3271623)

Dong, X., Thanou, D., Frossard, P., & Vandergheynst, P. (2014). Learning Laplacian Matrix in Smooth Graph Signal Representations. *IEEE Transactions on Signal Processing, 64*, 6160-6173.[ https://doi.org/10.1109/tsp.2016.2602809](https://doi.org/10.1109/tsp.2016.2602809)

Flores, M., Calder, J., & Lerman, G. (2019). Analysis and algorithms for $\\ell_p$-based semi-supervised learning on graphs. **.

Gong, C., Liu, T., Tao, D., Fu, K., Tu, E., & Yang, J. (2015). Deformed Graph Laplacian for Semisupervised Learning. *IEEE Transactions on Neural Networks and Learning Systems, 26*, 2261-2274.[ https://doi.org/10.1109/tnnls.2014.2376936](https://doi.org/10.1109/tnnls.2014.2376936)

Li, Z., Jia, M., Wei, Z., & Wang, J. (2024). Beyond smoothness: A general optimization framework for graph neural networks with negative Laplacian regularization. *Neural networks : the official journal of the International Neural Network Society, 180*, 106704.[ https://doi.org/10.1016/j.neunet.2024.106704](https://doi.org/10.1016/j.neunet.2024.106704)

Pang, J., & Cheung, G. (2016). Graph Laplacian Regularization for Image Denoising: Analysis in the Continuous Domain. *IEEE Transactions on Image Processing, 26*, 1770-1785.[ https://doi.org/10.1109/tip.2017.2651400](https://doi.org/10.1109/tip.2017.2651400)

Rios, M., Calder, J., & Lerman, G. (2022). Analysis and algorithms for ℓ-based semi-supervised learning on graphs. *Applied and Computational Harmonic Analysis*.[ https://doi.org/10.1016/j.acha.2022.01.004](https://doi.org/10.1016/j.acha.2022.01.004)

Salim, A., & Sumitra, S. (2022). Spectral Graph Convolutional Neural Networks in the Context of Regularization Theory. *IEEE Transactions on Neural Networks and Learning Systems, 35*, 4373-4384.[ https://doi.org/10.1109/tnnls.2022.3177742](https://doi.org/10.1109/tnnls.2022.3177742)

Slepčev, D., & Thorpe, M. (2017). Analysis of $p$-Laplacian Regularization in Semi-Supervised Learning. *SIAM J. Math. Anal., 51*, 2085-2120.[ https://doi.org/10.1137/17m115222x](https://doi.org/10.1137/17m115222x)

Wang, M., Fu, W., Hao, S., Tao, D., & Wu, X. (2016). Scalable Semi-Supervised Learning by Efficient Anchor Graph Regularization. *IEEE Transactions on Knowledge and Data Engineering, 28*, 1864-1877.[ https://doi.org/10.1109/tkde.2016.2535367](https://doi.org/10.1109/tkde.2016.2535367)

Zhao, X., Wang, D., Zhang, X., Gu, N., & Ye, X. (2018). Semi-supervised Learning Based on Coupled Graph Laplacian Regularization. *Proceedings of 2018 Chinese Intelligent Systems Conference*.[ https://doi.org/10.1007/978-981-13-2288-4_14](https://doi.org/10.1007/978-981-13-2288-4_14)

  
  

# Tab 4**  
**

## **Propagation operators in GNNs beyond normalized adjacency**

In a GNN layer, the “propagation operator” is the matrix (or kernel) used to mix each node with its neighbors before applying learnable weights. While the classic choice is the (renormalized) adjacency, many alternative operators and aggregation rules are used.

## **Laplacian, diffusion, and spectral operators**

  - Many GNNs use the **graph Laplacian** (or its polynomial filters) as the basic propagation/shift operator instead of normalized adjacency, especially in spectral or diffusion-based designs (Eliasof et al., 2022; Spinelli et al., 2020; Han et al., 2023; Stachenfeld et al., 2020; Khemani et al., 2024).
  - Spectral Graph Networks explicitly use **Laplacian eigenvectors** and perform message passing in a “spectral graph” built from these eigenvectors, so propagation happens in the spectral domain rather than only via Â (Stachenfeld et al., 2020).
  - Continuous‑dynamics and heat‑diffusion views treat propagation as solving a **graph diffusion / heat equation** driven by the Laplacian or related operators (Han et al., 2023).

### **Examples of non‑Â propagation matrices**

|  |  |  |
| :-: | :-: | :-: |
| **Operator family** | **Example use in GNNs** | **Citations** |
| Laplacian / Laplacian polynomials | Spectral CNNs, diffusion‑style GCNs | (Eliasof et al., 2022; Spinelli et al., 2020; Han et al., 2023; Stachenfeld et al., 2020; Khemani et al., 2024) |
| Spectral-domain shift (eigenvector graph) | Spectral Graph Network | (Stachenfeld et al., 2020) |
| PageRank-like / diffusion variants | Alternative propagation to avoid oversmoothing | (Spinelli et al., 2020; Han et al., 2023) |

**Figure 1:** Main non-adjacency propagation families in GNNs

## **Learnable and mixed propagation operators**

  - **ωGNN** introduces several fixed smoothing and **sharpening** operators (e.g., Laplacian-based, possibly with negative entries) and learns channel‑wise mixing weights ω to form a trainable propagation operator per layer, going beyond a single normalized adjacency (Eliasof et al., 2022).
  - Implicit GNNs with **flexible propagation operators** derive an implicit message‑passing rule from an optimization objective and allow the operator to depend on both dynamic semantics and topology, rather than a fixed Â (Pi et al., 2025).
  - Centrality Graph Shift Operators normalize adjacency by **global centrality scores** (PageRank, k‑core, walk counts), yielding centrality‑aware GSOs that can replace Â in any GNN (Abbahaddou et al., 2024).

## **Alternative aggregation kernels and similarity-based operators**

  - Message passing with **mean, sum, max, and attention** aggregators defines effective propagation operators that are not strictly normalized adjacency; convergence results cover attention‑based, max‑convolutional, and moment‑based aggregation GNNs (Cordonnier et al., 2023; Zheng et al., 2023; Chen et al., 2020; Wu et al., 2021).
  - Similarity‑Navigated GNNs replace Â with a **node similarity matrix** coupled with mean aggregation, so propagation follows similarity instead of raw edges (Zou et al., 2023).
  - Hierarchical and temporal GNNs introduce **multi-level or time-aware propagation kernels**, e.g., hierarchical super‑graphs with intra‑/inter‑level propagation (Zhong et al., 2020)or temporal aggregation–propagation blocks over unfolded temporal graphs (Zheng et al., 2023).

## **Conclusion**

Beyond normalized adjacency, GNNs propagate with Laplacian and diffusion operators, spectral-domain shifts, centrality-based GSOs, similarity matrices, and a wide range of learnable mixtures and attention-based aggregators. Many recent models explicitly learn or adapt propagation operators (ωGNN, flexible/implicit operators, CGSOs), or redefine the underlying shift (hierarchical, temporal, spectral graphs) to better capture structure, heterophily, and long-range dependencies.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Abbahaddou, Y., Malliaros, F., Lutzeyer, J., & Vazirgiannis, M. (2024). Centrality Graph Shift Operators for Graph Neural Networks. *ArXiv, abs/2411.04655*.[ https://doi.org/10.48550/arxiv.2411.04655](https://doi.org/10.48550/arxiv.2411.04655)

Chen, Y., Tang, X., Qi, X., Li, C., & Xiao, R. (2020). Learning Graph Normalization for Graph Neural Networks. *ArXiv, abs/2009.11746*.[ https://doi.org/10.1016/j.neucom.2022.01.003](https://doi.org/10.1016/j.neucom.2022.01.003)

Cordonnier, M., Keriven, N., Tremblay, N., & Vaiter, S. (2023). Convergence of Message Passing Graph Neural Networks with Generic Aggregation On Large Random Graphs. *ArXiv, abs/2304.11140*.[ https://doi.org/10.48550/arxiv.2304.11140](https://doi.org/10.48550/arxiv.2304.11140)

Eliasof, M., Ruthotto, L., & Treister, E. (2022). Improving Graph Neural Networks with Learnable Propagation Operators. **, 9224-9245.

Han, A., Shi, D., Lin, L., & Gao, J. (2023). From Continuous Dynamics to Graph Neural Networks: Neural Diffusion and Beyond. *ArXiv, abs/2310.10121*.[ https://doi.org/10.48550/arxiv.2310.10121](https://doi.org/10.48550/arxiv.2310.10121)

Khemani, B., Patil, S., Kotecha, K., & Tanwar, S. (2024). A review of graph neural networks: concepts, architectures, techniques, challenges, datasets, applications, and future directions. *Journal of Big Data, 11*, 1-43.[ https://doi.org/10.1186/s40537-023-00876-4](https://doi.org/10.1186/s40537-023-00876-4)

Pi, Y., Huang, Y., Shi, Y., Chen, F., & Wang, S. (2025). Implicit graph neural networks with flexible propagation operators. *Neural networks : the official journal of the International Neural Network Society, 194*, 108143.[ https://doi.org/10.1016/j.neunet.2025.108143](https://doi.org/10.1016/j.neunet.2025.108143)

Spinelli, I., Scardapane, S., & Uncini, A. (2020). Adaptive Propagation Graph Convolutional Network. *IEEE Transactions on Neural Networks and Learning Systems, 32*, 4755-4760.[ https://doi.org/10.1109/tnnls.2020.3025110](https://doi.org/10.1109/tnnls.2020.3025110)

Stachenfeld, K., Godwin, J., & Battaglia, P. (2020). Graph Networks with Spectral Message Passing. *ArXiv, abs/2101.00079*.

Wu, M., Pan, S., Du, L., & Zhu, X. (2021). Learning Graph Neural Networks with Positive and Unlabeled Nodes. *ACM Transactions on Knowledge Discovery from Data (TKDD), 15*, 1 - 25.[ https://doi.org/10.1145/3450316](https://doi.org/10.1145/3450316)

Zheng, T., Wang, X., Feng, Z., Song, J., Hao, Y., Song, M., Wang, X., Wang, X., & Chen, C. (2023). Temporal Aggregation and Propagation Graph Neural Networks for Dynamic Representation. *IEEE Transactions on Knowledge and Data Engineering, 35*, 10151-10165.[ https://doi.org/10.1109/tkde.2023.3265271](https://doi.org/10.1109/tkde.2023.3265271)

Zhong, Z., Li, C., & Pang, J. (2020). Hierarchical message-passing graph neural networks. *Data Mining and Knowledge Discovery, 37*, 381-408.[ https://doi.org/10.1007/s10618-022-00890-9](https://doi.org/10.1007/s10618-022-00890-9)

Zou, M., Gan, Z., Cao, R., Guan, C., & Leng, S. (2023). Similarity-navigated graph neural networks for node classification. *Inf. Sci., 633*, 41-69.[ https://doi.org/10.1016/j.ins.2023.03.057](https://doi.org/10.1016/j.ins.2023.03.057)

  
  

# Tab 5**  
**

## **Heat Kernel vs. Personalized PageRank vs. Chebyshev in GNN Propagation**

Heat kernel, personalized PageRank (PPR), and Chebyshev propagation are all ways to define how information diffuses on a graph, but they differ in their diffusion profile, hyperparameters, and computational handling in GNNs.

## **Propagation Behavior and Bias**

  - **Personalized PageRank (PPR):****  
    ** Uses a geometric decay over walk lengths, with teleport probability α. It can be seen as “infinite-depth” neighborhood aggregation with weights θₖ = α(1−α)ᵏ on k-hop walks (Klicpera et al., 2019; Klicpera et al., 2018). PPR emphasizes relatively shorter walks but still includes long-range information.
  - **Heat kernel:****  
    ** Uses Poisson-decayed walk lengths θₖ = e⁻ᵗ tᵏ/k! with diffusion time t (Klicpera et al., 2019; Yang et al., 2024; Wang et al., 2021). Compared to PPR, it yields a different bias over path lengths; in practice, both are strong choices for graph diffusion convolution (GDC) and often outperform learned θₖ (Klicpera et al., 2019). Heat kernels strongly emphasize **low-frequency** (smooth) components and can flexibly choose neighborhoods via diffusion, as in GraphHeat (Xu et al., 2019).
  - **Chebyshev propagation:****  
    ** Does not define a diffusion by itself; instead it **approximates** a chosen diffusion (e.g., heat kernel, PPR, fractional heat) by a truncated Chebyshev polynomial of the Laplacian or transition matrix, enabling multi-hop spectral filters without eigendecomposition (Bozorgnia et al., 2025; Xu et al., 2019; Huang et al., 2019; Huang et al., 2025).

### **Diffusion profiles in GNNs**

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| **Operator** | **Walk-weight pattern θₖ** | **Typical use in GNNs** | **Citations** |
| PPR | Geometric decay in k | APPNP/PPNP, GDC | (Klicpera et al., 2019; Klicpera et al., 2018; Wu et al., 2022) |
| Heat kernel | Poisson decay in k | GraphHeat, GDC, HK-based GNNs | (Xu et al., 2019; Klicpera et al., 2019; Bozorgnia et al., 2025; Huang et al., 2025) |
| Chebyshev poly. | Polynomial in Laplacian/transition | Fast approx of above | (Bozorgnia et al., 2025; Xu et al., 2019; Huang et al., 2019; Huang et al., 2025; Yang et al., 2024) |

**Figure 1:** High-level comparison of three propagation operators

## **Expressiveness, Oversmoothing, and Depth**

  - **PPR-based propagation (PPNP/APPNP):****  
    ** Decouples prediction and propagation, allowing effectively infinite-hop aggregation while mitigating oversmoothing compared to plain repeated graph convolution, but theory shows PPR architectures still perform best at shallow to moderate depth and can be outperformed by standard convolutions on some graphs (Klicpera et al., 2018; Wu et al., 2022).
  - **Heat-kernel-based GNNs:****  
    ** GraphHeat builds a convolution that explicitly boosts low-frequency filters and discounts high-frequency variations, yielding strong semi-supervised accuracy, especially with low label rates (Xu et al., 2019). Fractional heat kernels (fractional Laplacian) further enable **nonlocal, multi-hop diffusion** that is advantageous when labels are extremely scarce (Bozorgnia et al., 2025).
  - **Chebyshev vs. direct diffusion:****  
    ** Chebyshev polynomial approximations let GNNs implement complex heat or fractional heat filters efficiently on large graphs (Bozorgnia et al., 2025; Huang et al., 2019; Huang et al., 2025), and more generally accelerate computation of heat kernel and PPR-based propagation with provable convergence and speedups (≈O(√N) over naive power iteration) (Yang et al., 2024; Bai et al., 2024; Huang et al., 2019).

## **Computational and Practical Considerations**

  - **Efficiency:****  
    ** Direct PPR or heat kernel matrices are dense and expensive; practical GNNs use:  
     – Precomputed diffusions (GDC, APPNP) using power iteration/local solvers (Klicpera et al., 2019; Klicpera et al., 2018; Bai et al., 2024; Wang et al., 2021)– Chebyshev approximations to avoid eigen-decomposition and speed diffusion on big graphs (Bozorgnia et al., 2025; Huang et al., 2019; Huang et al., 2025; Yang et al., 2024).
  - **Hyperparameter choice:****  
    ** In GDC, fixed PPR and heat-kernel coefficient families with tuned α or t outperform learned θₖ and tend to have stable good ranges (α≈0.05–0.2, t≈1–10) (Klicpera et al., 2019). Heat-based methods often require choosing diffusion time; recent work proposes information-theoretic criteria to set it automatically (He, 2025).

## **Conclusion**

In GNNs, PPR and heat kernels are **diffusion families** with different path-length weightings and smoothness biases, both strong in practice; Chebyshev methods are primarily **computational tools** to approximate such diffusions (including fractional variants) efficiently and at scale. PPR-based propagation (APPNP/PPNP, GDC) is widely used for leveraging large neighborhoods while controlling oversmoothing, whereas heat-kernel-based filters (including fractional versions) emphasize spectral smoothness and can excel with very limited labels; Chebyshev polynomials make these operators practical on large graphs by turning them into fast, localized polynomial filters.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Bai, J., Zhou, B., Yang, D., & Xiao, Y. (2024). Faster Local Solvers for Graph Diffusion Equations. *ArXiv, abs/2410.21634*.[ https://doi.org/10.48550/arxiv.2410.21634](https://doi.org/10.48550/arxiv.2410.21634)

Bozorgnia, F., Kungurtsev, V., Kadyrov, S., & Yousefnezhad, M. (2025). Fractional Heat Kernel for Semi-Supervised Graph Learning with Small Training Sample Size. *ArXiv, abs/2510.04440*.[ https://doi.org/10.48550/arxiv.2510.04440](https://doi.org/10.48550/arxiv.2510.04440)

He, Z. (2025). Constrained Heat Kernel Graph Diffusion Convolution: A High-Dimensional Statistical Approximation via Information Theory. *IEEE Access, 13*, 90912-90920.[ https://doi.org/10.1109/access.2024.3425607](https://doi.org/10.1109/access.2024.3425607)

Huang, S., Lyu, I., Qiu, A., & Chung, M. (2019). Fast Polynomial Approximation of Heat Kernel Convolution on Manifolds and Its Application to Brain Sulcal and Gyral Graph Pattern Analysis. *IEEE Transactions on Medical Imaging, 39*, 2201-2212.[ https://doi.org/10.1109/tmi.2020.2967451](https://doi.org/10.1109/tmi.2020.2967451)

Huang, J., Zhou, X., Chen, H., & Wang, H. (2025). Deep Graph Wavelet Neural Networks Using Heat Kernel for Semi-supervised Node Classification. *2025 IEEE 6th International Conference on Pattern Recognition and Machine Learning (PRML)*, 101-107.[ https://doi.org/10.1109/prml66062.2025.11159794](https://doi.org/10.1109/prml66062.2025.11159794)

Huang, S., Lyu, I., Qiu, A., & Chung, M. (2019). Fast Polynomial Approximation of Heat Diffusion on Manifolds and Its Application to Brain Sulcal and Gyral Graph Pattern Analysis. *ArXiv, abs/1911.02721*.

Klicpera, J., Weißenberger, S., & Günnemann, S. (2019). Diffusion Improves Graph Learning. **, 13333-13345.

Klicpera, J., Bojchevski, A., & Günnemann, S. (2018). Predict then Propagate: Graph Neural Networks meet Personalized PageRank. **.

Wang, H., He, M., Wei, Z., Wang, S., Yuan, Y., Du, X., & Wen, J. (2021). Approximate Graph Propagation. *Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining*.[ https://doi.org/10.1145/3447548.3467243](https://doi.org/10.1145/3447548.3467243)

Wu, X., Chen, Z., Wang, W., & Jadbabaie, A. (2022). A Non-Asymptotic Analysis of Oversmoothing in Graph Neural Networks. *ArXiv, abs/2212.10701*.[ https://doi.org/10.48550/arxiv.2212.10701](https://doi.org/10.48550/arxiv.2212.10701)

Xu, B., Shen, H., Cao, Q., Cen, K., & Cheng, X. (2019). Graph Convolutional Networks using Heat Kernel for Semi-supervised Learning. **, 1928-1934.[ https://doi.org/10.24963/ijcai.2019/267](https://doi.org/10.24963/ijcai.2019/267)

Yang, Y., Li, R., Liao, M., Lin, L., & Wang, G. (2024). Scaling Up Graph Propagation Computation on Large Graphs: A Local Chebyshev Approximation Approach. *ArXiv, abs/2412.10789*.[ https://doi.org/10.48550/arxiv.2412.10789](https://doi.org/10.48550/arxiv.2412.10789)

  
  

# Tab 6**  
**

## **Subgraph federated learning with missing neighbors: main method families**

In subgraph federated learning (SFL), each client only sees a local fragment of a global graph, so many true neighbors (and cross‑subgraph edges) are missing. Methods focus either on explicitly reconstructing those neighbors/links, or on designing architectures/aggregation that remain robust despite missing topology.

## **1. Local missing‑neighbor generation (client-side)**

  - **FedSage / FedSage+** jointly train a GraphSAGE model with a **missing neighbor generator**. Each client self‑supervises the generator by hiding nodes/edges, learning to generate potential missing neighbors and links, then runs FedSage on the “mended” subgraph (Zhang et al., 2021).
  - **FedNI** uses a **graph GAN** to inpaint missing nodes and edges locally; clients federatively train missing‑node and missing‑edge predictors, then train a GCN on the completed graphs (Peng et al., 2021).
  - **FedMpa(e)** first learns global node features via an MLP, then propagates these to local structures and reconstructs subgraphs by forming **super‑nodes** that implicitly encode missing neighbors/edges instead of explicitly generating them (Tang et al., 2024).

### **Example design patterns**

|  |  |  |
| :-: | :-: | :-: |
| **Pattern** | **Key idea** | **Citations** |
| Self-supervised neighbor generator | Mask local nodes/edges, train generator to recover | (Zhang et al., 2021) |
| GAN-based inpainting | GAN predicts missing nodes/edges before GNN | (Peng et al., 2021) |
| Super-node reconstruction | Pool missing neighbors into new super-nodes | (Tang et al., 2024) |

**Figure 1:** Client-side strategies for repairing missing neighbors

## **2. Global or cross-client generation / reconstruction**

  - **FedDEP** improves on FedSage+ with: deep neighbor generation from **GNN embeddings** of potential neighbors; **pseudo-FL with embedding prototypes** for efficient generator training; and privacy via edge‑local differential privacy (Zhang et al., 2024).
  - **MN‑FGAGN** (also called FGAGN) splits a **GAN** into a **server-side generator** and **client-side discriminators** so the generator learns a **global feature distribution** and produces pseudo nodes that better approximate real missing neighbors while preserving privacy (Liu et al., 2025).
  - **FGL‑CMLR** trains a **federated GCN-based link predictor** focused on clustered “central/edge” nodes to repair cross‑subgraph links and update embeddings (Ceyani et al., 2025).
  - **SpreadFGL** learns an **adaptive graph imputation generator** plus an assessor to infer potential links between clients’ subgraphs without raw data sharing (Zhong et al., 2024; Zhong et al., 2026).
  - **FedGGR** instead reconstructs a **global graph on the server** via graph structure learning, avoiding per‑client neighbor prediction and client‑to‑client exchange (Liu et al., 2024).
  - **LLM4FGL** uses a large language model to **generate missing neighbors and infer edges** for text‑attributed graphs in a federated way (Yan et al., 2025).
  - A VAE‑based approach reconstructs missing neighbors specifically to reduce the impact of missing links on **conformal prediction** uncertainty sets in federated GNNs (Akgül et al., 2024).

## **3. Architectures robust to missing neighbors**

  - **FedGT** uses a scalable **Graph Transformer** where each node attends to sampled local neighbors plus **curated global nodes**; this preserves a global receptive field and makes the model more robust to missing links without explicit link recovery (Zhang et al., 2024).
  - **Personalized SFL methods** (FED‑PUB, FedGrAINS, FedSG, FedPPD) primarily tackle heterogeneity but assume or plug into the above neighbor‑generation or reconstruction schemes rather than directly solving missing neighbors (Baek et al., 2022; Ceyani et al., 2025; Wang et al., 2024; Wang et al., 2023; Lin et al., 2025).

## **Conclusion**

Main methods for SFL with missing neighbors are: (1) client‑side missing‑neighbor generation (FedSage+, FedNI, FedMpae), (2) global or cross‑client generation and graph reconstruction (FedDEP, MN‑FGAGN, FGL‑CMLR, SpreadFGL, FedGGR, LLM4FGL, VAE‑based reconstruction), and (3) architectures like FedGT that use global attention or prototypes to reduce reliance on exact local neighborhoods. These approaches differ in how they balance utility, communication, and privacy while approximating training on the full global graph.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Akgül, Ö., Kannan, R., & Prasanna, V. (2024). Conformal Prediction for Federated Graph Neural Networks with Missing Neighbor Information. **, 45-63.[ https://doi.org/10.48550/arxiv.2410.14010](https://doi.org/10.48550/arxiv.2410.14010)

Baek, J., Jeong, W., Jin, J., Yoon, J., & Hwang, S. (2022). Personalized Subgraph Federated Learning. *ArXiv, abs/2206.10206*.[ https://doi.org/10.48550/arxiv.2206.10206](https://doi.org/10.48550/arxiv.2206.10206)

Ceyani, E., Xie, H., Buyukates, B., Yang, C., & Avestimehr, A. (2025). FedGrAINS: Personalized SubGraph Federated Learning with Adaptive Neighbor Sampling. **, 598-607.[ https://doi.org/10.48550/arxiv.2501.12592](https://doi.org/10.48550/arxiv.2501.12592)

Lin, Q., Jia, J., Zhu, Y., Li, X., Jiang, B., & Qu, M. (2025). FedPPD: Towards effective subgraph federated learning via pseudo prototype distillation. *Neural networks : the official journal of the International Neural Network Society, 189*, 107541.[ https://doi.org/10.1016/j.neunet.2025.107541](https://doi.org/10.1016/j.neunet.2025.107541)

Liu, Y., He, Z., Wang, S., Wang, Y., Wang, P., Huang, Z., & Sun, Q. (2025). Federated Subgraph Learning via Global-Knowledge-Guided Node Generation. *Sensors (Basel, Switzerland), 25*.[ https://doi.org/10.3390/s25072240](https://doi.org/10.3390/s25072240)

Liu, Z., Zhou, H., Xia, F., Shen, G., Saikrishna, V., He, X., Du, J., & Kong, X. (2024). Subgraph Federated Learning with Global Graph Reconstruction. **, 158-173.[ https://doi.org/10.1007/978-981-97-2303-4_11](https://doi.org/10.1007/978-981-97-2303-4_11)

Peng, L., Wang, N., Dvornek, N., Zhu, X., & Li, X. (2021). FedNI: Federated Graph Learning With Network Inpainting for Population-Based Disease Prediction. *IEEE Transactions on Medical Imaging, 42*, 2032-2043.[ https://doi.org/10.1109/tmi.2022.3188728](https://doi.org/10.1109/tmi.2022.3188728)

Tang, B., Chen, X., Wang, S., Xuan, Y., & Zhao, Z. (2024). Federated Learning with Limited Node Labels. *ArXiv, abs/2406.12435*.[ https://doi.org/10.48550/arxiv.2406.12435](https://doi.org/10.48550/arxiv.2406.12435)

Wang, Y., Guo, S., Qiao, D., Liu, G., & Li, M. (2024). FedSG: A Personalized Subgraph Federated Learning Framework on Multiple Non-IID Graphs. *IEEE Transactions on Emerging Topics in Computational Intelligence, 8*, 3678-3690.[ https://doi.org/10.1109/tetci.2024.3372381](https://doi.org/10.1109/tetci.2024.3372381)

Wang, Y., Guo, S., & Qiao, D. (2023). FedSG: Subgraph Federated Learning on Multiple Non-IID Graphs. *2023 19th International Conference on Mobility, Sensing and Networking (MSN)*, 504-511.[ https://doi.org/10.1109/msn60784.2023.00078](https://doi.org/10.1109/msn60784.2023.00078)

Yan, B., Zhang, Z., Sun, H., Zhang, M., Cao, Y., & Shi, C. (2025). Data-centric Federated Graph Learning with Large Language Models. *ArXiv, abs/2503.19455*.[ https://doi.org/10.48550/arxiv.2503.19455](https://doi.org/10.48550/arxiv.2503.19455)

Zhang, K., Yang, C., Li, X., Sun, L., & Yiu, S. (2021). Subgraph Federated Learning with Missing Neighbor Generation. *ArXiv, abs/2106.13430*.

Zhang, K., Sun, L., Ding, B., Yiu, S., & Yang, C. (2024). Deep Efficient Private Neighbor Generation for Subgraph Federated Learning. **, 806-814.[ https://doi.org/10.48550/arxiv.2401.04336](https://doi.org/10.48550/arxiv.2401.04336)

Zhang, Z., Hu, Q., Yu, Y., Gao, W., & Liu, Q. (2024). FedGT: Federated Node Classification with Scalable Graph Transformer. *ArXiv, abs/2401.15203*.[ https://doi.org/10.48550/arxiv.2401.15203](https://doi.org/10.48550/arxiv.2401.15203)

Zhong, L., Pi, Y., Chen, Z., Yu, Z., Miao, W., Chen, X., & Min, G. (2024). SpreadFGL: Edge-Client Collaborative Federated Graph Learning with Adaptive Neighbor Generation. *IEEE INFOCOM 2024 - IEEE Conference on Computer Communications*, 1141-1150.[ https://doi.org/10.1109/infocom52122.2024.10621368](https://doi.org/10.1109/infocom52122.2024.10621368)

Zhong, L., Zhang, J., Chen, Z., Li, J., & Min, G. (2026). Subtopology-Assisted Federated Graph Learning With Adaptive Neighbor Generation in Edge-Client Collaborative Networks. *IEEE Transactions on Networking, 34*, 957-972.[ https://doi.org/10.1109/ton.2025.3613257](https://doi.org/10.1109/ton.2025.3613257)

  
  

# Tab 7**  
**

## **Harmonic Extension on Graphs via the Laplacian and Dirichlet Problem**

On graphs, harmonic extension solves a discrete analogue of the classical Dirichlet problem: extend given boundary values (labels) on a subset of nodes to all nodes by enforcing graph-harmonicity. This underlies many Laplacian-based semi-supervised learning methods.

## **Formulation as a Graph Dirichlet Problem**

  - Given labels on a subset (B) of nodes, harmonic extension finds the **smoothest function** (u) on all nodes with (u|*B = g) by minimizing graph Dirichlet energy**  
    * *(E(u)=\\sum*{i,j}w_{ij}(u_i-u_j)^2) over all (u) agreeing with (g) on (B) (Shi & Tian, 2015; Song et al., 2021).
  - The minimizer satisfies a discrete **Dirichlet problem**:
      
      - (Lu = 0) on unlabeled nodes, i.e., each unlabeled value is the **weighted average of its neighbors** (harmonicity) (Song et al., 2021).
      - (u = g) on labeled nodes (boundary condition) (Shi & Tian, 2015; Song et al., 2021).
  - This is equivalent to Gaussian Fields and Harmonic Functions and Laplacian-regularized label propagation (Zhu et al., 2018; Sousa, 2015; Song et al., 2021).

## **Well-Posedness and Degeneracy**

  - With very **low labeling rate**, Laplacian harmonic extension on random geometric graphs becomes **degenerate**: solutions are nearly constant with spikes at labeled nodes; this occurs when the label rate (\\beta \\ll \\varepsilon^2) (graph length scale (\\varepsilon)) (Calder et al., 2020).
  - If labels grow fast enough, (\\beta \\gg \\varepsilon^2), the discrete solution is **well-posed** and converges to a continuum Laplace-Dirichlet problem, with error (O(\\varepsilon \\beta^{-1/2})) (Calder et al., 2020).
  - More generally, minimizing graph Dirichlet energy with pointwise constraints is asymptotically ill-posed in dimension (d>1); higher-order (fractional) Sobolev-type regularizers are needed for continuity (Weihs & Thorpe, 2023).

### **Label Rate / Regularity Effects**

|  |  |  |
| :-: | :-: | :-: |
| **Setting** | **Behavior of harmonic extension** | **Citations** |
| (\\\\beta \\\\ll \\\\varepsilon^2) | Spikes at labels, almost-constant elsewhere | (Calder et al., 2020) |
| (\\\\beta \\\\gg \\\\varepsilon^2) | Converges to continuum Laplace-Dirichlet PDE | (Calder et al., 2020) |
| Finite labels, (d\\>1) | Continuum minimizer discontinuous | (Sevi, 2018; Weihs & Thorpe, 2023) |

**Figure 1:** Regimes for Laplacian harmonic extension on graphs

## **Refinements of Graph-Laplacian Harmonic Extension**

  - **Point Integral / Volume Constraint methods**: standard graph Laplacian may fail to approximate classical harmonic functions near boundaries; PIM and volume-constraint methods discretize an **integral equation** to obtain harmonic extensions with convergence guarantees (Shi & Tian, 2015).
  - **Weighted nonlocal Laplacians**: reweighting labeled nodes more heavily (WNLL) improves continuity and interpolation of boundary values at low label rates (Streicher & Gilboa, 2023).
  - **Time-dependent harmonic extension**: a time-dependent Dirichlet problem is used for node classification, and performance is improved by learning the initialization on unlabeled nodes; parameter (t) controls diffusion extent (Azad, 2022).

## **Summary**

Harmonic extension on graphs solves a Laplacian-based Dirichlet problem: extend boundary labels by enforcing graph-harmonicity (zero Laplacian) on unlabeled nodes. This can approximate continuum Laplace-Dirichlet solutions when label rate and graph scale are properly balanced, but becomes degenerate with too few labels or in higher dimensions, motivating weighted, higher-order, or integral-equation-based variants for stable, accurate semi-supervised learning.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Azad, A. (2022). Learning Label Initialization for Time-Dependent Harmonic Extension. *ArXiv, abs/2205.01358*.[ https://doi.org/10.48550/arxiv.2205.01358](https://doi.org/10.48550/arxiv.2205.01358)

Calder, J., Slepčev, D., & Thorpe, M. (2020). Rates of convergence for Laplacian semi-supervised learning with low labeling rates. *Research in the Mathematical Sciences, 10*, 1-42.[ https://doi.org/10.1007/s40687-022-00371-x](https://doi.org/10.1007/s40687-022-00371-x)

Sevi, H. (2018). Analyse harmonique sur graphes dirigés et applications: de l'analyse de Fourier aux ondelettes. (Harmonic Analysis on directed graphs and applications: From Fourier analysis to wavelets). *Applied and Computational Harmonic Analysis*.[ https://doi.org/10.1016/j.acha.2022.10.003](https://doi.org/10.1016/j.acha.2022.10.003)

Shi, Z., & Tian, M. (2015). Harmonic Extension. *ArXiv, abs/1509.06458*.

Song, Z., Yang, X., Xu, Z., & King, I. (2021). Graph-Based Semi-Supervised Learning: A Comprehensive Review. *IEEE Transactions on Neural Networks and Learning Systems, 34*, 8174-8194.[ https://doi.org/10.1109/tnnls.2022.3155478](https://doi.org/10.1109/tnnls.2022.3155478)

Sousa, C. (2015). An overview on the Gaussian Fields and Harmonic Functions method for semi-supervised learning. *2015 International Joint Conference on Neural Networks (IJCNN)*, 1-8.[ https://doi.org/10.1109/ijcnn.2015.7280491](https://doi.org/10.1109/ijcnn.2015.7280491)

Streicher, O., & Gilboa, G. (2023). Graph Laplacian for Semi-Supervised Learning. **, 250-262.[ https://doi.org/10.48550/arxiv.2301.04956](https://doi.org/10.48550/arxiv.2301.04956)

Weihs, A., & Thorpe, M. (2023). Consistency of Fractional Graph-Laplacian Regularization in Semisupervised Learning with Finite Labels. *SIAM J. Math. Anal., 56*, 4253-4295.[ https://doi.org/10.1137/23m1559087](https://doi.org/10.1137/23m1559087)

Zhu, X., Lafferty, J., & Ghahramani, Z. (2018). Semi-supervised learning : from Gaussian fields to Gaussian processes. **.[ https://doi.org/10.1184/r1/6609434.v1](https://doi.org/10.1184/r1/6609434.v1)

  
  

# Tab 8**  
**

## **Stability of explicit Euler for the (graph) heat equation and spectral radius**

The papers relate stability of explicit time-stepping for diffusion/heat dynamics to **spectral properties** (eigenvalues, spectral radius, spectral gaps) of the underlying operator or marching matrix.

## **General relation: explicit Euler and spectral radius**

For a linear ODE (x' = Ax), explicit Euler gives (x^{k+1} = (I + \\Delta t,A)x^k). Stability requires the eigenvalues of (I+\\Delta t,A) lie in (or on) the unit disk, i.e. a constraint on (\\Delta t) in terms of the **spectrum of (A)**. This is the standard spectral-radius-based Euler condition which is explicitly “contextualized” and sharpened for graph p-Laplacian diffusion in a discrete-time setting (Alpay & Alakkad, 2025).

## **Graph / p-Laplacian diffusion and discrete-time stability**

  - A calibrated diffusion framework combines **linear Laplacian smoothing**, **nonlinear graph p‑Laplacian flows**, and a **learnable dissipation term** on graphs (Alpay & Alakkad, 2025).
  - For this class of graph-based diffusions, the authors derive **sharp constants for discrete-time stability**, including a “necessary and sufficient Euler step-size” condition that depends on the **graph spectrum (p‑gap, spectral properties)** (Alpay & Alakkad, 2025).
  - They provide **explicit lower bounds on the graph p‑gap** on canonical graphs, which enter the decay rates and allowable Euler step sizes (Alpay & Alakkad, 2025).
  - The results also cover **stochastic discrete-time diffusion**, with a strengthened analysis of the noise floor and stability conditions (Alpay & Alakkad, 2025).

### **Discrete-time graph diffusion ingredients**

|  |  |  |
| :-: | :-: | :-: |
| **Quantity** | **Role in stability/decay** | **Citations** |
| Graph Laplacian / p‑Laplacian spectrum | Governs decay rates and admissible steps | (Alpay & Alakkad, 2025) |
| Graph p‑gap lower bounds | Provide explicit p‑dependent constants | (Alpay & Alakkad, 2025) |
| Learnable dissipation term | Adjusts effective spectrum, enabling calibration | (Alpay & Alakkad, 2025) |

**Figure 1:** Spectral quantities controlling Euler stability on graphs

## **Continuous-domain heat equation: explicit Euler via integral operators**

  - For classical heat equations solved by **boundary integral (Volterra) formulations**, the forward Euler marching matrix can be shown **unconditionally stable** in several settings, by bounding its **spectral radius** directly (Barnett et al., 2019).
  - On the unit ball (Dirichlet/Neumann) and smooth convex domains, explicit Euler for the Volterra integral equation has spectral radius \< 1 for any (\\Delta t) (for fixed final time (T)), giving unconditional stability (Barnett et al., 2019).
  - For the Robin problem on a half-space with coefficient (\\kappa), they obtain a sharp condition (\\Delta t \< C/\\kappa^2) (with an explicit constant (C)) using new spectral bounds for symmetric Toeplitz matrices (Barnett et al., 2019).

## **Summary**

Stability of explicit Euler for heat or diffusion dynamics—on graphs or in continuum—is fundamentally a **spectral condition**: the step size must be chosen based on the eigenvalues / spectral radius or gaps of the evolution operator. On graphs, recent work makes these constants explicit for p‑Laplacian flows and ties them to graph spectral gaps; in boundary-integral formulations of the (continuous) heat equation, explicit spectral-radius bounds of the marching matrix even yield **unconditional stability** in several geometries.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Alpay, F., & Alakkad, H. (2025). Calibrated Semantic Diffusion: A p-Laplacian Synthesis with Learnable Dissipation, Quantified Constants, and Graph-Aware Calibration. **.

Barnett, A., Epstein, C., Greengard, L., Jiang, S., & Wang, J. (2019). Explicit unconditionally stable methods for the heat equation via potential theory. *Pure and Applied Analysis*.[ https://doi.org/10.2140/paa.2019.1.709](https://doi.org/10.2140/paa.2019.1.709)

  
  

# Tab 9**  
**

## **Graph signal smoothness, Dirichlet energy, and heterophily**

Graph **Dirichlet energy** measures how much a signal changes across edges: low energy = smooth (homophilic) signal, high energy = sharp (heterophilic) signal. Recent work connects this directly to when GNNs succeed or fail on heterophilous graphs.

## **Dirichlet energy as a smoothness / heterophily metric**

  - Dirichlet energy (or Laplacian total variation) is defined as (E(X)=\\mathrm{tr}(X^\\top L X)); small values indicate that neighboring nodes have similar features (high homophily) (Ajorlou et al., 2025; Di Giovanni et al., 2022; Zheng et al., 2025; Li et al., 2025).
  - A node-classification task is heterophilic when adjacent nodes often have different labels; then the **label signal has high Dirichlet energy**, so enhancing high-frequency components can help separate classes (Di Giovanni et al., 2022; Gao et al., 2023; Li et al., 2025).
  - Several works show empirically that as **homophily increases**, Dirichlet energy of labels/features/embeddings **decreases monotonically**, and conversely energy is higher in heterophilous graphs (Chen et al., 2023; Li et al., 2025).

### **Smoothness, homophily, and energy**

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| **Regime** | **Typical Dirichlet energy** | **Interpretation** | **Citations** |
| High homophily | Low | Smooth labels/features | (Ajorlou et al., 2025; Di Giovanni et al., 2022; Li et al., 2025) |
| High heterophily | High | Rapid label changes | (Di Giovanni et al., 2022; Gao et al., 2023; Li et al., 2025) |

**Figure 1:** How homophily level relates to Dirichlet energy

## **Oversmoothing vs “energy-enhancing” designs**

  - Standard message-passing GNNs often **decrease Dirichlet energy layer by layer**, acting as low-pass filters; this leads to oversmoothing and failures on heterophilic graphs where high energy is needed (Chen et al., 2023; Di Giovanni et al., 2022; Zheng et al., 2025; Guan & Shi, 2025; Cai & Wang, 2020).
  - On synthetic SBM graphs, Dirichlet energy of GCN features **decreases as homophily decreases** at fixed depth, linking heterophily and oversmoothing: in heterophily, smoothing destroys already fragile class structure (Chen et al., 2023).
  - Multiple models now **explicitly keep Dirichlet energy from collapsing**:
      
      - Framelet-based EEConv provably **enhances** Dirichlet energy and keeps high-pass components large on heterophilous graphs, improving deep GNN performance (Chen et al., 2023).
      - p-Laplacian framelet GCNs maintain **non-zero generalized Dirichlet energy at convergence**, avoiding oversmoothing and adapting to both homophilic and heterophilic data (Shi et al., 2023).
      - UniFilter mixes homophily and heterophily spectral bases so that energy **stays bounded away from zero** as depth grows when the heterophily basis is used (Huang et al., 2024).
      - Fractional Laplacian neural ODEs generalize Dirichlet energy and allow non-local diffusion, keeping energy higher and mitigating oversmoothing across homophily levels (Maskey et al., 2023).
      - GDendrite dynamically **modulates Dirichlet energy** via “dendritic” amplification/inhibition, targeting higher energy (less smooth) representations in heterophilous contexts (Li et al., 2025).

## **Spectral view: heterophily ↔ high frequency**

  - Viewing labels as graph signals, the **smoothness index** (a Rayleigh quotient involving the Laplacian) equals the heterophily ratio for binary labels, so higher heterophily corresponds to more energy in high Laplacian frequencies (Gao et al., 2023).
  - Spectral results show that the **spectral energy distribution shifts to higher frequencies** as heterophily increases, implying that optimal filters should become more high-pass on heterophilous graphs (Gao et al., 2023; Di Giovanni et al., 2022; Li et al., 2025).

## **Dirichlet energy under diffusion/aggregation**

  - Analyses derive **decay rates of Dirichlet energy** under heat diffusion and random-walk aggregation and connect them to Laplacian eigenvalues; larger spectral gap means faster energy decay (stronger oversmoothing) (Guan & Shi, 2025; Di Giovanni et al., 2022).
  - This formalizes that purely smoothing dynamics are ideal for homophilic label signals (low initial energy) but systematically harmful when the target signal is heterophilic (high initial energy) (Di Giovanni et al., 2022; Maskey et al., 2023).

## **Summary**

Dirichlet energy is a precise way to quantify **graph signal smoothness** and thus homophily: low energy for smooth, homophilic signals; high energy for sharp, heterophilic ones. Classical GNNs monotonically reduce this energy, which fits homophilic tasks but leads to oversmoothing and poor performance under heterophily, where discriminative information lives in high-energy/high-frequency components. New architectures explicitly control or enhance Dirichlet energy—via framelets, p-Laplacian, fractional Laplacians, and adaptive spectral bases—to retain or emphasize these high-frequency signals and perform better on heterophilous graphs.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Ajorlou, H., Mateos, G., & Ruiz, L. (2025). Dirichlet Meets Horvitz and Thompson: Estimating Homophily in Large Networks via Sampling. **.

Cai, C., & Wang, Y. (2020). A Note on Over-Smoothing for Graph Neural Networks. *ArXiv, abs/2006.13318*.

Chen, J., Wang, Y., Bodnar, C., Ying, R., Liò, P., & Wang, Y. (2023). Dirichlet Energy Enhancement of Graph Neural Networks by Framelet Augmentation. *ArXiv, abs/2311.05767*.[ https://doi.org/10.48550/arxiv.2311.05767](https://doi.org/10.48550/arxiv.2311.05767)

Di Giovanni, F., Rowbottom, J., Chamberlain, B., Markovich, T., & Bronstein, M. (2022). Understanding convolution on graphs via energies. *Trans. Mach. Learn. Res., 2023*.

Gao, Y., Wang, X., He, X., Liu, Z., Feng, H., & Zhang, Y. (2023). Addressing Heterophily in Graph Anomaly Detection: A Perspective of Graph Spectrum. *Proceedings of the ACM Web Conference 2023*.[ https://doi.org/10.1145/3543507.3583268](https://doi.org/10.1145/3543507.3583268)

Guan, W., & Shi, Z. (2025). Measuring Over-smoothing beyond Dirichlet energy. *ArXiv, abs/2512.06782*.[ https://doi.org/10.48550/arxiv.2512.06782](https://doi.org/10.48550/arxiv.2512.06782)

Huang, K., Wang, Y., Li, M., & Liò, P. (2024). How Universal Polynomial Bases Enhance Spectral Graph Neural Networks: Heterophily, Over-smoothing, and Over-squashing. *ArXiv, abs/2405.12474*.[ https://doi.org/10.48550/arxiv.2405.12474](https://doi.org/10.48550/arxiv.2405.12474)

Li, R., Xiao, Y., , X., Vasnev, A., & Gao, J. (2025). GDendrite: On Heterophilous Graph Contexts Mining with Versatile Neural Dendrites Framework. *Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2*.[ https://doi.org/10.1145/3711896.3736975](https://doi.org/10.1145/3711896.3736975)

Maskey, S., Paolino, R., Bacho, A., & Kutyniok, G. (2023). A Fractional Graph Laplacian Approach to Oversmoothing. *ArXiv, abs/2305.13084*.[ https://doi.org/10.48550/arxiv.2305.13084](https://doi.org/10.48550/arxiv.2305.13084)

Shi, D., Shao, Z., Guo, Y., Zhao, Q., & Gao, J. (2023). Revisiting Generalized p-Laplacian Regularized Framelet GCNs: Convergence, Energy Dynamic and Training with Non-Linear Diffusion. *ArXiv, abs/2305.15639*.[ https://doi.org/10.48550/arxiv.2305.15639](https://doi.org/10.48550/arxiv.2305.15639)

Zheng, H., Yang, R., Zhou, Y., & Xu, J. (2025). Rethinking Message Passing Neural Networks with Diffusion Distance-guided Stress Majorization. *ArXiv, abs/2511.19984*.[ https://doi.org/10.48550/arxiv.2511.19984](https://doi.org/10.48550/arxiv.2511.19984)

  
  

# Tab 10**  
**

## **Spectral graph filters with heat kernels and Chebyshev approximation**

Spectral GNNs often define filters as functions of the Laplacian eigenvalues, then approximate these filters with Chebyshev polynomials to avoid eigendecomposition. Heat kernels are a key low‑pass choice; Chebyshev expansions make them scalable and localized.

## **Heat-kernel-based spectral filters**

  - **Heat kernel form:** Filters are defined as (g(\\lambda)=e^{-s\\lambda}) (or compositions of such terms), which strongly **attenuate high frequencies** and emphasize smooth signals. GraphHeat uses this to “discount high‑frequency basic filters” and enforce label/feature smoothness on the graph (Xu et al., 2019).
  - GraphHeat builds convolution kernels by weighting basis filters with factors (e^{-ks\\lambda_i}), decreasing in the eigenvalue, acting as a **low-pass graph filter** (Xu et al., 2019).
  - The generalized heat-kernel smoothing filter extends this idea using **p‑power Laplacians** to adjust passband flatness and transition steepness for denoising (Tseng & Lee, 2024).
  - In deep settings, DHK composes multiple heat-kernel components and truncates the first two terms to create an efficient convolution operator that stabilizes very deep GNNs (Huang et al., 2025).
  - HeatGSNs integrate **learnable low-pass graph heat kernels** into spectral GNNs for brain tumor tasks, deriving a continuous propagation mechanism from the graph heat equation (Bae et al., 2024).

### **Chebyshev approximation of heat and other spectral filters**

|  |  |  |
| :-: | :-: | :-: |
| **Use case** | **What Chebyshev does** | **Citations** |
| GraphHeat | Approximates (e^{-sL}) without eigendecomposition | (Xu et al., 2019; Huang et al., 2019) |
| DHK, SGWN | Approximates wavelet/heat kernels for fast multiscale filters | (Huang et al., 2025; Li et al., 2023; Huang et al., 2019) |
| LB‑CNN, manifolds | Approximates Laplace–Beltrami heat kernel; avoids eigen solve | (Huang et al., 2020; Huang et al., 2019) |

**Figure 1:** Where Chebyshev approximates heat-type spectral filters

GraphHeat explicitly states that (e^{-sL}) is implemented via **Chebyshev polynomials**, achieving linear complexity in edges and making heat-kernel filtering scalable (Xu et al., 2019). Fast polynomial approximation of heat kernel convolution on manifolds uses Chebyshev and other orthogonal polynomials to avoid computing Laplace–Beltrami eigenfunctions, again leveraging recurrence relations for efficiency (Huang et al., 2019). SGWN similarly approximates its scaling and wavelet kernel functions with Chebyshev polynomials to speed computation while extracting both low-pass and band-pass graph features (Li et al., 2023).

## **Chebyshev interpolation vs. classical ChebNet**

  - Classical ChebNet parametrizes filters as Chebyshev polynomials of the Laplacian; later work shows performance issues come from **unconstrained coefficients**, not from the Chebyshev basis itself (He et al., 2022).
  - ChebNetII and ChebyCF instead use **Chebyshev interpolation**, directly learning filter values at Chebyshev nodes to approximate arbitrary spectral filters with optimal convergence, without eigen-decomposition (He et al., 2022; Kim et al., 2025).
  - Other work designs minimax Chebyshev graph filters so the **peak spectral error** is minimized, using FIR filter design tools and recurrence implementations (Tseng & Lee, 2021).

## **Summary**

Heat-kernel spectral filters provide principled low-pass smoothing on graphs; Chebyshev polynomial approximation is the main tool to implement these (and other) spectral filters efficiently and locally. Modern GNNs combine heat-kernel design with Chebyshev interpolation/approximation to get flexible, stable, and scalable graph convolutions across tasks from semi-supervised node classification to recommendation and medical imaging.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Bae, J., Lee, H., & Hu, J. (2024). HeatGSNs: integrating eigenfilters and low-pass graph heat kernels into graph spectral convolutional networks for brain tumor segmentation and classification. *Biomedical Physics & Engineering Express, 11*.[ https://doi.org/10.1088/2057-1976/ada1db](https://doi.org/10.1088/2057-1976/ada1db)

He, M., Wei, Z., & Wen, J. (2022). Convolutional Neural Networks on Graphs with Chebyshev Approximation, Revisited. *ArXiv, abs/2202.03580*.[ https://doi.org/10.52202/068431-0527](https://doi.org/10.52202/068431-0527)

Huang, J., Zhou, X., Chen, H., & Wang, H. (2025). Deep Graph Wavelet Neural Networks Using Heat Kernel for Semi-supervised Node Classification. *2025 IEEE 6th International Conference on Pattern Recognition and Machine Learning (PRML)*, 101-107.[ https://doi.org/10.1109/prml66062.2025.11159794](https://doi.org/10.1109/prml66062.2025.11159794)

Huang, S., Chung, M., Qiu, A., & Initiative, A. (2020). Revisiting convolutional neural network on graphs with polynomial approximations of Laplace–Beltrami spectral filtering. *Neural Computing and Applications, 33*, 13693 - 13704.[ https://doi.org/10.1007/s00521-021-06006-6](https://doi.org/10.1007/s00521-021-06006-6)

Huang, S., Lyu, I., Qiu, A., & Chung, M. (2019). Fast Polynomial Approximation of Heat Kernel Convolution on Manifolds and Its Application to Brain Sulcal and Gyral Graph Pattern Analysis. *IEEE Transactions on Medical Imaging, 39*, 2201-2212.[ https://doi.org/10.1109/tmi.2020.2967451](https://doi.org/10.1109/tmi.2020.2967451)

Kim, C., Sung, J., Han, Y., & Lee, J. (2025). Graph Spectral Filtering with Chebyshev Interpolation for Recommendation. *Proceedings of the 48th International ACM SIGIR Conference on Research and Development in Information Retrieval*.[ https://doi.org/10.1145/3726302.3729991](https://doi.org/10.1145/3726302.3729991)

Li, T., Sun, C., Fink, O., Yang, Y., Chen, X., & Yan, R. (2023). Filter-Informed Spectral Graph Wavelet Networks for Multiscale Feature Extraction and Intelligent Fault Diagnosis. *IEEE Transactions on Cybernetics, 54*, 506-518.[ https://doi.org/10.1109/tcyb.2023.3256080](https://doi.org/10.1109/tcyb.2023.3256080)

Tseng, C., & Lee, S. (2024). A Generalized Heat Kernel Smoothing Filter for Signal Denoising over Graph. *2024 IEEE International Symposium on Circuits and Systems (ISCAS)*, 1-5.[ https://doi.org/10.1109/iscas58744.2024.10558098](https://doi.org/10.1109/iscas58744.2024.10558098)

Tseng, C., & Lee, S. (2021). Minimax Design of Graph Filter Using Chebyshev Polynomial Approximation. *IEEE Transactions on Circuits and Systems II: Express Briefs, 68*, 1630-1634.[ https://doi.org/10.1109/tcsii.2021.3065977](https://doi.org/10.1109/tcsii.2021.3065977)

Xu, B., Shen, H., Cao, Q., Cen, K., & Cheng, X. (2019). Graph Convolutional Networks using Heat Kernel for Semi-supervised Learning. **, 1928-1934.[ https://doi.org/10.24963/ijcai.2019/267](https://doi.org/10.24963/ijcai.2019/267)

  
  

# Tab 11**  
**

# **Feature Propagation for Initializing Missing Node Features in GNNs**

When node features are partially missing, a common strategy is to first reconstruct (impute) features by propagating observed values over the graph, then run a standard GNN. The papers focus on how this **feature propagation (FP)** works, why it is effective, and how to improve it.

## **Core Feature Propagation Idea**

  - FP treats known features as boundary conditions and **minimizes Dirichlet energy**, leading to a diffusion-type process on the graph (Rossi et al., 2021; Song et al., 2025; Li et al., 2025).
  - In practice, FP iteratively multiplies features by a normalized adjacency (diffusion) matrix and then **resets known entries** to their original values each iteration until convergence (Rossi et al., 2021; Song et al., 2025; Yun et al., 2025; Li et al., 2025).
  - This yields a reconstructed, fully dense feature matrix that can be fed to any downstream GNN (Rossi et al., 2021; Song et al., 2025).

### **Basic FP Update (conceptual)**

|  |  |  |
| :-: | :-: | :-: |
| **Step** | **Operation (per iteration)** | **Citations** |
| 1 | Diffuse: (X \\\\leftarrow \\\\tilde{A} X) | (Rossi et al., 2021; Song et al., 2025; Li et al., 2025) |
| 2 | Reset known features | (Rossi et al., 2021; Song et al., 2025; Li et al., 2025) |

**Figure 1:** Standard diffusion-and-reset loop in FP

## **Effectiveness and Limitations**

  - FP is **simple, fast, and scalable**, handling graphs with millions of nodes and still working when up to 99–99.5% of features are missing, with modest accuracy drop (Rossi et al., 2021; Um et al., 2023).
  - It generally outperforms earlier GCN variants for missing features (e.g., SAT, GCNMF, PaGNN) on node classification and link prediction (Rossi et al., 2021; Um et al., 2023; Bayram et al., 2020).
  - Key limitations:
      
      - Assumes mainly **homophilic** graphs; diffusion can over-smooth features (Rossi et al., 2021; Song et al., 2025).
      - Struggles on **disconnected graphs** and in **inductive** settings due to distribution shift at inference (Song et al., 2025).
      - Suffers from **cold-start nodes** (low degree / far from known features) (Li et al., 2025).

## **Improved Propagation-Based Imputation**

  - **GOODIE** uses FP as one branch and combines it with label propagation and structure–feature attention to stay effective even when very few features are observed (Yun et al., 2025).
  - **DDFI** keeps FP as a base but adds:
      
      - Co-Label Linking to connect same-label nodes across components.
      - A graph Masked AutoEncoder and a **two-step inference** to reduce over-smoothing and inductive shift (Song et al., 2025).
  - **AttriReBoost** modifies boundary conditions and adds **virtual edges** to improve connectivity and tackle cold start without gradients, with proven convergence (Li et al., 2025).
  - **PCFI** augments diffusion with **channel-wise confidence** and inter-channel propagation, improving performance at extremely high missing rates (e.g., 99.5%) (Um et al., 2023).
  - **FSD-CAP** uses **fractional diffusion** and progressive local subgraph expansion, then class-aware refinement, to avoid global error propagation and over-smoothing under extreme sparsity (Qiao et al., 2026).
  - **Hypergraph FP (SGHFP)** builds and fuses feature and pseudo-label hypergraphs before propagation, capturing higher-order correlations when reconstructing features (Lei et al., 2023).

## **Broader Imputation Alternatives**

  - Some methods integrate missing-feature handling into the GNN itself (e.g., GCNMF’s Gaussian mixture modeling of missing entries) instead of an explicit FP pre-step (Bayram et al., 2020).
  - Others use multi-relational or clustering-aware propagation for specific settings (knowledge graphs, deep graph clustering), often citing FP as the basic propagation baseline to improve (Bayram et al., 2020; Hu et al., 2025; Yu et al., 2022).

## **Conclusion**

Feature propagation provides a theoretically grounded and highly scalable way to initialize missing node features by graph diffusion with boundary resets. It is remarkably robust to extreme missingness but can over-smooth, struggle with disconnected or inductive scenarios, and under-serve low-degree nodes. Recent work extends FP with confidence weights, hypergraphs, autoencoders, fractional diffusion, and connectivity enhancements to address these issues while keeping the core propagation-based initialization idea.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Bayram, E., García-Durán, A., & West, R. (2020). Node Attribute Completion in Knowledge Graphs with Multi-Relational Propagation. *ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 3590-3594.[ https://doi.org/10.1109/icassp39728.2021.9414016](https://doi.org/10.1109/icassp39728.2021.9414016)

Hu, Y., Tu, W., Liu, Y., Li, M., Lu, W., Luo, Z., Liu, X., & Chen, P. (2025). Divide-Then-Rule: A Cluster-Driven Hierarchical Interpolator for Attribute-Missing Graphs. *Proceedings of the 33rd ACM International Conference on Multimedia*.[ https://doi.org/10.1145/3746027.3755070](https://doi.org/10.1145/3746027.3755070)

Lei, C., Fu, S., Wang, Y., Qiu, W., Hu, Y., Peng, Q., & You, X. (2023). Self-Supervised Guided Hypergraph Feature Propagation for Semi-Supervised Classification with Missing Node Features. *ICASSP 2023 - 2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 1-5.[ https://doi.org/10.1109/icassp49357.2023.10094867](https://doi.org/10.1109/icassp49357.2023.10094867)

Li, M., Ding, C., Chen, J., Xing, W., Ye, C., Zhang, R., Zhuang, S., Hu, J., Qiu, T., & Gao, H. (2025). AttriReBoost: A Gradient-Free Propagation Optimization Method for Cold Start Mitigation in Attribute Missing Graphs. *ArXiv, abs/2501.00743*.[ https://doi.org/10.48550/arxiv.2501.00743](https://doi.org/10.48550/arxiv.2501.00743)

Qiao, X., Sun, S., Dong, A., Hua, C., Zhao, X., Zhang, L., Zhu, G., & Zhang, L. (2026). FSD-CAP: Fractional Subgraph Diffusion with Class-Aware Propagation for Graph Feature Imputation. *ArXiv, abs/2601.18938*.[ https://doi.org/10.48550/arxiv.2601.18938](https://doi.org/10.48550/arxiv.2601.18938)

Rossi, E., Kenlay, H., Gorinova, M., Chamberlain, B., Dong, X., & Bronstein, M. (2021). On the Unreasonable Effectiveness of Feature propagation in Learning on Graphs with Missing Node Features. *ArXiv, abs/2111.12128*.

Song, Y., Yu, F., Luo, Y., Tao, X., Qiu, S., Han, K., & Tang, J. (2025). DDFI: Diverse and Distribution-aware Missing Feature Imputation via Two-step Reconstruction. **.

Um, D., Park, J., Park, S., & Choi, J. (2023). Confidence-Based Feature Imputation for Graphs with Partially Known Features. *ArXiv, abs/2305.16618*.[ https://doi.org/10.48550/arxiv.2305.16618](https://doi.org/10.48550/arxiv.2305.16618)

Yu, W., Lin, X., Liu, J., Ge, J., Ou, W., & Qin, Z. (2022). Self-Propagation Graph Neural Network for Recommendation. *IEEE Transactions on Knowledge and Data Engineering, 34*, 5993-6002.[ https://doi.org/10.1109/tkde.2021.3076772](https://doi.org/10.1109/tkde.2021.3076772)

Yun, S., Liu, X., Oh, Y., Lee, J., Chen, T., Murata, T., & Park, C. (2025). Oldie but Goodie: Re-illuminating Label Propagation on Graphs with Partially Observed Features. *Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2*.[ https://doi.org/10.1145/3711896.3737067](https://doi.org/10.1145/3711896.3737067)

  
  

# Tab 12**  
**

## **Adaptive propagation depth in GNNs: main ideas**

Work on adaptive depth tries to decide “how far to propagate” per node, feature, or graph, instead of using a single fixed number of layers. This is mainly to avoid over-smoothing and redundancy while still leveraging large receptive fields.

## **1. Node-wise adaptive propagation depth**

  - **Curvature-based depth**: A learnable Bakry–Émery curvature is used to capture both structure and diffusion; nodes with **high curvature stop earlier**, low-curvature nodes propagate deeper. This yields a depth-adaptive GNN where message-passing layers are dynamically adjusted per vertex and improves many GNN backbones (Hevapathige et al., 2025).
  - **Local homophily-based depth (AD-GNN)**: A theoretical framework links local structure/label composition to node-wise “optimal depth”; a **Depth Benefit Metric** evaluates whether extra layers help or hurt each node. The model then selects node-specific aggregation depths, handling both homophilic and heterophilic graphs in one architecture (Hevapathige et al., 2025).
  - **Node-adaptive propagation for inference (NAP)**: For scalable inference, each node gets a personalized depth based on (i) distance between its current and stationary features, or (ii) learned gates; nodes whose features are already “smooth enough” stop early, giving large speedups (Gao et al., 2023).
  - **VEM-based ‘learning to propagate’**: Optimal propagation steps are treated as latent variables, learned via a variational EM framework, yielding **personalized and interpretable propagation strategies** per node and graph (Xiao et al., 2021).

### **Examples of per-node depth adaptation**

|  |  |  |
| :-: | :-: | :-: |
| **Method** | **Signal to decide depth** | **Citations** |
| Curvature-GNN | Learnable Bakry–Émery curvature | (Hevapathige et al., 2025) |
| AD-GNN | Depth Benefit Metric from local labels | (Hevapathige et al., 2025) |
| NAP (ICDE) | Feature–stationary distance / gates | (Gao et al., 2023) |
| Learn-to-prop | Latent optimal steps via VEM | (Xiao et al., 2021) |

**Figure 1:** Different signals used for node-wise depth selection

## **2. Adaptive combination of multi-hop propagation**

  - **DAGNN (Deep Adaptive GNN)** decouples transformation and propagation, propagates features up to a fixed depth (k), then learns **per-node attention weights over 0…k hops**, effectively choosing how much each node relies on shallow vs deep neighborhoods (Liu et al., 2020).
  - **AP-DGNN** learns **node- and class-specific weights** over multiple high-order GCN layers; this reconstructs high-order GCNs while adaptively emphasizing useful propagation distances and avoiding performance drops from too-short or too-long paths (Chen et al., 2024).
  - **BBAD framework** stacks blocks of decoupled propagation with identity gates per layer; gates close to zero skip propagation, so each block’s effective depth is **learned** and can differ per node via “flexible receptive fields” (Shen et al., 2022).
  - **SAGN** aggregates precomputed multi-hop features with an attention mechanism that **adaptively gathers information from different hops** for each node, improving scalable training (Sun & Wu, 2021).

## **3. Graph- or attribute-level depth adaptation**

  - **DGNAS-PD** performs neural architecture search over decoupled GNNs, jointly choosing **propagation operations and suitable depth per graph**, rather than always using deep DGNNs (Gao et al., 2023).
  - In recommendation, **PDA-GNN** and **PDKGNN** split user/item attributes into channels, each with its own **propagation depth**, then use attention to reweight attributes with different effective ranges (Wu et al., 2023; Huo et al., 2025).

## **4. Related adaptive propagation mechanisms**

  - A data-driven propagation mechanism learns forward layer connections via bi-level optimization, effectively selecting useful **layer combinations** and reducing redundancy and over-smoothing (Wu et al., 2022).
  - Block-based decoupling (Shen et al., 2022)and AIR residuals (Zhang et al., 2022)indirectly modulate effective propagation depth by controlling how much each layer’s propagation is retained.

## **Conclusion**

Adaptive propagation depth in GNNs is implemented mainly by (1) node-wise stopping rules driven by curvature, homophily, or feature smoothness; (2) attention or gating over multi-hop propagations; and (3) architecture search or attribute-channel designs that choose depth at graph or facet level. These methods consistently aim to keep beneficial long-range information while avoiding over-smoothing and unnecessary computation.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Chen, W., Yan, W., & Wang, W. (2024). Adaptive propagation deep graph neural networks. *Pattern Recognit., 154*, 110607.[ https://doi.org/10.1016/j.patcog.2024.110607](https://doi.org/10.1016/j.patcog.2024.110607)

Gao, J., He, C., Chen, J., Li, Q., & Wang, Y. (2023). Decoupled Graph Neural Architecture Search with Variable Propagation Operation and Appropriate Depth. *Proceedings of the 35th International Conference on Scientific and Statistical Database Management*.[ https://doi.org/10.1145/3603719.3603729](https://doi.org/10.1145/3603719.3603729)

Gao, X., Zhang, W., Yu, J., Shao, Y., Nguyen, Q., Cui, B., & Yin, H. (2023). Accelerating Scalable Graph Neural Network Inference with Node-Adaptive Propagation. *2024 IEEE 40th International Conference on Data Engineering (ICDE)*, 3042-3055.[ https://doi.org/10.1109/icde60146.2024.00236](https://doi.org/10.1109/icde60146.2024.00236)

Hevapathige, A., Zehmakan, A., & Wang, Q. (2025). Depth-Adaptive Graph Neural Networks via Learnable Bakry-Émery Curvature. *Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2*.[ https://doi.org/10.1145/3711896.3736905](https://doi.org/10.1145/3711896.3736905)

Hevapathige, A., Wijesinghe, A., & Zehmakan, A. (2025). Beyond Fixed Depth: Adaptive Graph Neural Networks for Node Classification Under Varying Homophily. *ArXiv, abs/2511.06608*.[ https://doi.org/10.48550/arxiv.2511.06608](https://doi.org/10.48550/arxiv.2511.06608)

Huo, Z., Liu, H., Li, Y., Xia, C., & Ge, B. (2025). Propagation depth-aware knowledge graph neural networks for recommendation. *, 13794*, 1379429 - 1379429-12.[ https://doi.org/10.1117/12.3083392](https://doi.org/10.1117/12.3083392)

Liu, M., Gao, H., & Ji, S. (2020). Towards Deeper Graph Neural Networks. *Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining*.[ https://doi.org/10.1145/3394486.3403076](https://doi.org/10.1145/3394486.3403076)

Shen, X., Zhang, Y., Xie, Y., Wong, K., & Peng, C. (2022). A Block-Based Adaptive Decoupling Framework for Graph Neural Networks. *Entropy, 24*.[ https://doi.org/10.3390/e24091190](https://doi.org/10.3390/e24091190)

Sun, C., & Wu, G. (2021). Scalable and Adaptive Graph Neural Networks with Self-Label-Enhanced training. *Pattern Recognit., 160*, 111210.[ https://doi.org/10.1016/j.patcog.2024.111210](https://doi.org/10.1016/j.patcog.2024.111210)

Wu, X., He, H., Yang, H., Tai, Y., Wang, Z., & Zhang, W. (2023). PDA-GNN: propagation-depth-aware graph neural networks for recommendation. *World Wide Web, 26*, 3585 - 3606.[ https://doi.org/10.1007/s11280-023-01200-z](https://doi.org/10.1007/s11280-023-01200-z)

Wu, Y., Hu, X., Fan, X., , W., & Gao, Q. (2022). Learning Data-Driven Propagation Mechanism for Graph Neural Network. *Electronics*.[ https://doi.org/10.3390/electronics12010046](https://doi.org/10.3390/electronics12010046)

Xiao, T., Chen, Z., Wang, D., & Wang, S. (2021). Learning How to Propagate Messages in Graph Neural Networks. *Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining*.[ https://doi.org/10.1145/3447548.3467451](https://doi.org/10.1145/3447548.3467451)

Zhang, W., Sheng, Z., Yin, Z., Jiang, Y., Xia, Y., Gao, J., Yang, Z., & Cui, B. (2022). Model Degradation Hinders Deep Graph Neural Networks. *Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*.[ https://doi.org/10.1145/3534678.3539374](https://doi.org/10.1145/3534678.3539374)

  
  

# Graph Feature Propagation on Heterophilic Graphs**  
**

## **Graph Feature Propagation on Heterophilic Graphs**

In heterophilic graphs, neighboring nodes often have different labels or features, so naive feature propagation (simple smoothing) can wash out useful information. Recent work designs **adaptive or non‑uniform propagation rules** that distinguish homophilic from heterophilic relations and often combine low‑pass and high‑pass behaviors.

## **Why Standard Propagation Fails under Heterophily**

  - Classical GCN-style propagation assumes neighbors are similar, so it **smooths features**, which degrades discrimination when many neighbors are of different classes (Rossi et al., 2021; Wen, 2025).
  - Experiments on synthetic graphs show that standard feature diffusion quickly loses performance as homophily decreases, becoming barely better than trivial baselines at zero homophily (Rossi et al., 2021).

## **Adaptive, Heterophily-Aware Propagation Mechanisms**

### **Node-/edge-wise adaptive propagation**

  - **HOG-GCN** learns a **homophily degree matrix** from topology and attributes; propagation weights between node pairs are increased for likely same-class neighbors and decreased for likely different-class ones. This allows the model to automatically change the propagation process according to local homophily/heterophily and to constrain representation similarity based on homophily degree (Wang et al., 2022).
  - **H²GNN** explicitly separates **similar vs. dissimilar neighbor features**, performing dual aggregations so that both homophilic and heterophilic information are preserved and propagated, improving node classification across homophily levels (Jing et al., 2024).
  - **Graph neural convection–diffusion** uses a PDE-based propagation: a **diffusion term** for homophilic neighbors and a **learnable convection term** that controls information flow along heterophilic edges, enabling non-smoothing propagation where needed (Kang et al., 2023).

### **Global / structure-aware propagation**

  - **GSF-GNN** introduces a **Structure-based Global Propagation (SGP)** module that builds global connections and adaptively reweights edges, together with a feature-augmentation module; this alleviates over-smoothing and preserves useful high-order information on heterophilic graphs (Liu et al., 2025).
  - **TDGNN** decomposes neighborhoods into a tree, then uses **graph diffusion within this decomposition** to aggregate multi-hop information while explicitly mitigating feature smoothing across layers, which is especially beneficial on heterophily networks (Wang & Derr, 2021).
  - **ES-GNN** performs **edge splitting** into task-relevant and irrelevant subgraphs and propagates separately on them, effectively denoising heterophilic edges and reducing harmful smoothing (Guo et al., 2022).

### **Label/feature propagation variants for heterophily**

  - **nCASH** performs **feature-enhanced label propagation** to obtain soft labels and node-wise homophily scores, then builds a **heterophily-aware Laplacian** and applies **low-pass filters in homophilous regions and high-pass filters in heterophilous regions**, emphasizing high-frequency (heterophilic) signals where needed (Pirrò, 2024).
  - **LPkG** improves label propagation on heterophilic graphs by constructing an auxiliary **k‑NN graph in a latent space** (homophilic), running LP there, and combining it with a GNN, consistently boosting accuracy on standard heterophilic benchmarks (Park & Park, 2024).
  - **HL-Net** for scene graph generation includes a **Relationship Feature Propagation** module based on a modified PageRank scheme that acts as a **high-pass filter** (via negative teleport probability), explicitly propagating **high-frequency heterophilic signals** between relationship nodes (Lin et al., 2022).

### **Propagation for missing features on heterophilic data**

  - **Feature Propagation (FP)** minimizes Dirichlet energy and behaves as a **low-pass diffusion**, working very well on homophilic graphs but degrading severely as homophily drops; the authors note that **non-homogeneous, feature-dependent diffusion** is needed for low-homophily settings (Rossi et al., 2021).
  - Newer imputation methods (e.g., **PCFI**, **FSD-CAP**) replace global diffusion with **localized or confidence-/class-aware propagation**, and report strong performance even on heterophily and large-scale datasets by limiting error spread and tailoring diffusion to structure and (pseudo-)labels (Qiao et al., 2026; Um et al., 2023).
  - A relation-aware diffusion scheme for **heterogeneous graphs with missing features** adds “virtual features” for undefined nodes and learns **edge-type importance during diffusion**, maintaining the advantages of diffusion-based imputation in more complex, potentially heterophilic settings (Um et al., 2025).

## **Design Patterns for Heterophilic Feature Propagation**

### **Key strategies and their roles**

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| **Strategy type** | **Example methods** | **Role in heterophilic propagation** | **Citations** |
| Edge/node homophily weighting | HOG-GCN, nCASH | Modulate propagation strength based on estimated homophily/heterophily | (Wang et al., 2022; Pirrò, 2024) |
| Dual / separated channels | H²GNN, ES-GNN | Separate homophilic vs. heterophilic signals or relevant vs. irrelevant edges | (Jing et al., 2024; Guo et al., 2022) |
| PDE / diffusion variants | Graph convection–diffusion, GIND, TDGNN | Combine diffusion with additional terms or implicit nonlinear diffusion to avoid oversmoothing | (Kang et al., 2023; Chen et al., 2022; Wang & Derr, 2021) |
| High-pass / mixed spectral filters | HL-Net, nCASH, DGAC | Explicitly pass high-frequency components in heterophilic regions | (Lin et al., 2022; Pirrò, 2024; Xie et al., 2025) |
| Auxiliary / modified graphs | LPkG, DGAC | Build homophilic or affinity graphs from features to support propagation | (Park & Park, 2024; Xie et al., 2025) |
| Localized / class-aware imputation | FSD-CAP, PCFI, relation-aware diffusion | Restrict and weight diffusion when imputing missing features under heterophily | (Qiao et al., 2026; Um et al., 2023; Um et al., 2025) |

**Figure 1:** Common propagation designs tailored to heterophilic graphs

## **When to Use What**

  - **Pure diffusion (low-pass) FP** is suitable mainly for high-homophily graphs and will likely harm performance in strongly heterophilic regimes (Rossi et al., 2021).
  - For **node classification on heterophilic graphs**, methods that (i) estimate homophily per edge/node and adapt propagation (HOG-GCN, nCASH), (ii) maintain separate channels for similar and dissimilar neighbors (H²GNN), or (iii) use high-pass/mixture spectral filters (HL-Net, DGAC) provide more robust propagation (Wang et al., 2022; Jing et al., 2024; Pirrò, 2024; Lin et al., 2022; Xie et al., 2025).
  - For **missing-feature imputation** under heterophily or noisy topology, localized and confidence- or class-aware diffusion (FSD-CAP, PCFI) avoids global over-smoothing and error spread while still leveraging propagation benefits (Qiao et al., 2026; Um et al., 2023).

## **Conclusion**

For heterophilic graphs, effective feature propagation must **break the uniform smoothing paradigm**: it should attenuate or reshape information flow along heterophilic edges, selectively preserve or enhance high-frequency components, and often operate differently in distinct regions of the graph. Across node classification, clustering, scene graph generation, and feature imputation, the most successful methods combine **adaptive edge/node weights, dual homophilic–heterophilic channels, high-pass or mixed spectral filters, and localized/class-aware diffusion**, consistently outperforming standard low-pass propagation on heterophilic benchmarks.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Chen, Q., Wang, Y., Wang, Y., Yang, J., & Lin, Z. (2022). Optimization-Induced Graph Implicit Nonlinear Diffusion. *ArXiv, abs/2206.14418*.[ https://doi.org/10.48550/arxiv.2206.14418](https://doi.org/10.48550/arxiv.2206.14418)

Guo, J., Huang, K., Yi, X., & Zhang, R. (2022). ES-GNN: Generalizing Graph Neural Networks Beyond Homophily With Edge Splitting. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 46*, 11345-11360.[ https://doi.org/10.1109/tpami.2024.3459932](https://doi.org/10.1109/tpami.2024.3459932)

Jing, S., Chen, L., Li, Q., & Wu, D. (2024). H2GNN: Graph Neural Networks with Homophilic and Heterophilic Feature Aggregations. **, 342-352.[ https://doi.org/10.1007/978-981-97-5572-1_23](https://doi.org/10.1007/978-981-97-5572-1_23)

Kang, Q., Song, Y., She, R., Wang, S., & Tay, W. (2023). Graph Neural Convection-Diffusion with Heterophily. *ArXiv, abs/2305.16780*.[ https://doi.org/10.48550/arxiv.2305.16780](https://doi.org/10.48550/arxiv.2305.16780)

Lin, X., Ding, C., Zhan, Y., Li, Z., & Tao, D. (2022). HL-Net: Heterophily Learning Network for Scene Graph Generation. *2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 19454-19463.[ https://doi.org/10.1109/cvpr52688.2022.01887](https://doi.org/10.1109/cvpr52688.2022.01887)

Liu, H., Ruan, S., Liu, Q., Cheng, M., Huang, Z., Liu, Y., Chen, E., & He, Y. (2025). Global Structure-aware and Feature-augmented Graph Neural Network for Heterophilic Graphs. *ACM Transactions on Information Systems*.[ https://doi.org/10.1145/3775057](https://doi.org/10.1145/3775057)

Park, H., & Park, H. (2024). Enhancing Heterophilic Graph Neural Network Performance Through Label Propagation in K-Nearest Neighbor Graphs. *2024 IEEE International Conference on Big Data and Smart Computing (BigComp)*, 337-344.[ https://doi.org/10.1109/bigcomp60711.2024.00060](https://doi.org/10.1109/bigcomp60711.2024.00060)

Pirrò, G. (2024). Adaptive Spectral-Heterophily for Node Classification. **, 2338-2345.[ https://doi.org/10.3233/faia240758](https://doi.org/10.3233/faia240758)

Qiao, X., Sun, S., Dong, A., Hua, C., Zhao, X., Zhang, L., Zhu, G., & Zhang, L. (2026). FSD-CAP: Fractional Subgraph Diffusion with Class-Aware Propagation for Graph Feature Imputation. *ArXiv, abs/2601.18938*.[ https://doi.org/10.48550/arxiv.2601.18938](https://doi.org/10.48550/arxiv.2601.18938)

Rossi, E., Kenlay, H., Gorinova, M., Chamberlain, B., Dong, X., & Bronstein, M. (2021). On the Unreasonable Effectiveness of Feature propagation in Learning on Graphs with Missing Node Features. *ArXiv, abs/2111.12128*.

Um, D., Lee, Y., Park, J., Park, S., Yeo, Y., & Ahn, S. (2025). Relation-Aware Diffusion for Heterogeneous Graphs with Partially Observed Features. **.

Um, D., Park, J., Park, S., & Choi, J. (2023). Confidence-Based Feature Imputation for Graphs with Partially Known Features. *ArXiv, abs/2305.16618*.[ https://doi.org/10.48550/arxiv.2305.16618](https://doi.org/10.48550/arxiv.2305.16618)

Wang, T., Jin, D., Wang, R., He, D., & Huang, Y. (2022). Powerful Graph Convolutional Networks with Adaptive Propagation Mechanism for Homophily and Heterophily. **, 4210-4218.[ https://doi.org/10.1609/aaai.v36i4.20340](https://doi.org/10.1609/aaai.v36i4.20340)

Wang, Y., & Derr, T. (2021). Tree Decomposed Graph Neural Network. *Proceedings of the 30th ACM International Conference on Information & Knowledge Management*.[ https://doi.org/10.1145/3459637.3482487](https://doi.org/10.1145/3459637.3482487)

Wen, Q. (2025). Modeling Higher-Order Interactions in Graphs Through Combinatorial Arc-Transitive Structure Using Graph Convolutional Network. *IEEE Access, 13*, 55899-55914.[ https://doi.org/10.1109/access.2025.3555011](https://doi.org/10.1109/access.2025.3555011)

Xie, K., Yang, R., & Wang, S. (2025). Diffusion-based Graph-agnostic Clustering. *Proceedings of the ACM on Web Conference 2025*.[ https://doi.org/10.1145/3696410.3714652](https://doi.org/10.1145/3696410.3714652)

  
  

# Tab 13**  
**

# **Handling Missing Node Features in GNNs: Key Method Families**

Many recent works relax the “complete features” assumption in GNNs and design methods that explicitly model or reconstruct missing node attributes, often jointly with structure.

## **1. Classical Imputation vs. Graph-Aware Imputation**

  - **Pre-GNN imputation (non-graph-aware):** Mean imputation, SVD-based soft imputation, k‑NN, random forest, autoencoders, and GANs fill missing entries before running a standard GNN, but feature filling and graph learning are decoupled and can be unstable when many values are missing (Taguchi et al., 2020; You et al., 2020; Chen et al., 2021).
  - **Graph-based imputation:** GRAPE builds a bipartite graph of samples and features and treats imputation as an edge-prediction task solved by a GNN, jointly with label prediction (Song et al., 2025). GRIMP and M³‑Impute similarly convert relational/tabular data to heterogeneous/bipartite graphs and learn GNN-based imputers (Cappuzzo et al., 2024; Yu et al., 2024).

### **Main design idea**

|  |  |  |
| :-: | :-: | :-: |
| **Approach type** | **How missing features are handled** | **Citations** |
| Pre‑GNN imputation | Fill matrix, then run any GNN | (Taguchi et al., 2020; You et al., 2020; Chen et al., 2021) |
| Graph-based imputation | Treat imputation as graph prediction (edges/values) | (Song et al., 2025; Cappuzzo et al., 2024; Yu et al., 2024) |
| In‑GNN modeling | Modify GNN to reason over missingness | (Taguchi et al., 2020; Chen et al., 2020; Huo et al., 2022; Chen et al., 2021; Jiang et al., 2024; Spinelli et al., 2019; Rossi et al., 2021) |

**Figure 1:** Main families of methods for missing node features in GNNs

## **2. GNNs That Directly Model Missing Features**

  - **Probabilistic first-layer modeling:** GCNMF represents missing entries with a **Gaussian Mixture Model** and computes expected activations in the first GCN layer, learning GMM + GCN end‑to‑end; it outperforms imputation‑then‑GCN on node classification and link prediction (Taguchi et al., 2020; You et al., 2020; Tu et al., 2023).
  - **Distributional node embeddings:** WGNN decomposes the attribute matrix into low‑dimensional **distributions** per node and performs message passing in Wasserstein space, capturing uncertainty from missing attributes and supporting both classification and value recovery (Chen et al., 2021).
  - **Partial message passing / tolerance:** Methods like PaGNN (cited within ASD‑VAE) propagate only observed attributes; other works randomly assign or infer attributes from topology (e.g., SAT, SVGA, PCFI) (Jiang et al., 2024).
  - **Feature Propagation:** Minimizes graph Dirichlet energy to diffuse known features over the graph, yielding a very simple and scalable reconstruction that remains accurate even when 99% of features are missing (Rossi et al., 2021).

## **3. Joint Attribute–Structure Modeling and Completion**

  - **Structure–attribute transformers / VAEs:** SAT assumes a shared latent space and matches the joint distribution of structure and attributes to complete missing node features and perform link prediction (Chen et al., 2020; Huo et al., 2022; Jiang et al., 2024). ASD‑VAE encodes attributes and structure into a **shared latent space** via coupled–decoupled variational autoencoding, then imputes attributes from this space, improving robustness at high missing rates (Jiang et al., 2024).
  - **Teacher–student and evolving graphs:** T2‑GNN builds separate feature‑level and structure‑level teacher models to distill knowledge into a base GNN on graphs with both feature and structure incompleteness (Huo et al., 2022). EGS alternates between reconstructing node attributes and dynamically updating graph structure under a Dirichlet energy objective (Song et al., 2025).
  - **Imputation networks on attribute-missing graphs:** ITR and MATE use structure-based initialization and refinement or multi‑view graph diffusion in the input space to iteratively improve attribute estimates (Tu et al., 2022; Peng et al., 2023). WAGE adds weight-sharing between attribute and structure encoders and K‑NN–based non‑local learning to enhance reconstruction (Spinelli et al., 2019). RITR extends these ideas to jointly handle attribute‑incomplete and attribute‑missing nodes (Tu et al., 2023; Tu et al., 2022).

## **4. Special Settings: No or Completely Missing Features**

  - **Graphs without features:** exopGCN designs a new convolutional operator based on **path-driven neighborhoods** and an “extensional adjacency” matrix to classify nodes when no features exist at all, improving many GNNs on such graphs (Jiao et al., 2024).
  - **Feature-missing graphs (entire nodes without any attributes):** GNN‑FIC generates missing feature information directly in the embedding space with a dedicated Feature Information Generator plus alignment and relation constraints (Hu et al., 2023). FS‑GNN, in recommendation, combines a trainable feature completion module (leveraging language models) with a structure completion module and integrates them adaptively (Lei et al., 2025).

## **Conclusion**

Research offers three main strategies for missing node features in GNNs: (1) impute first (sometimes graph-based) then apply standard GNNs; (2) modify GNNs to explicitly model missingness via probabilistic layers, diffusion/Dirichlet minimization, or uncertainty-aware embeddings; and (3) jointly learn structure and attributes in a shared latent or teacher–student framework. Simple diffusion (Feature Propagation) and integrated models like GCNMF, SAT, ASD‑VAE, WGNN, ITR/MATE, and WAGE provide strong, often state‑of‑the‑art performance across varying missingness regimes.

*These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at*[ *https://consensus.app*](https://consensus.app/)*. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent.*

## **References**

Cappuzzo, R., Thirumuruganathan, S., & Papotti, P. (2024). Relational Data Imputation with Graph Neural Networks. **, 221-233.[ https://doi.org/10.48786/edbt.2024.20](https://doi.org/10.48786/edbt.2024.20)

Chen, X., Chen, S., Yao, J., Zheng, H., Zhang, Y., & Tsang, I. (2020). Learning on Attribute-Missing Graphs. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 44*, 740-757.[ https://doi.org/10.1109/tpami.2020.3032189](https://doi.org/10.1109/tpami.2020.3032189)

Chen, Z., , T., Song, Y., & Wang, Y. (2021). Wasserstein Graph Neural Networks for Graphs With Missing Attributes. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 47*, 7010-7020.[ https://doi.org/10.1109/tpami.2025.3568480](https://doi.org/10.1109/tpami.2025.3568480)

Hu, J., Wang, J., Wei, Q., Kai, D., & Li, X. (2023). Learning Graph Neural Networks on Feature-Missing Graphs. **, 255-262.[ https://doi.org/10.1007/978-3-031-40283-8_22](https://doi.org/10.1007/978-3-031-40283-8_22)

Huo, C., Jin, D., Li, Y., He, D., Yang, Y., & Wu, L. (2022). T2-GNN: Graph Neural Networks for Graphs with Incomplete Features and Structure via Teacher-Student Distillation. *ArXiv, abs/2212.12738*.[ https://doi.org/10.48550/arxiv.2212.12738](https://doi.org/10.48550/arxiv.2212.12738)

Jiang, X., Qin, Z., Xu, J., & Ao, X. (2024). Incomplete Graph Learning via Attribute-Structure Decoupled Variational Auto-Encoder. *Proceedings of the 17th ACM International Conference on Web Search and Data Mining*.[ https://doi.org/10.1145/3616855.3635769](https://doi.org/10.1145/3616855.3635769)

Jiao, Q., Zhang, H., Wu, J., Wang, N., Liu, G., & Liu, Y. (2024). A simple and effective convolutional operator for node classification without features by graph convolutional networks.. *PloS one, 19 4*, e0301476.[ https://doi.org/10.1371/journal.pone.0301476](https://doi.org/10.1371/journal.pone.0301476)

Lei, S., Chang, X., Yu, Z., He, D., Huo, C., Wang, J., & Jin, D. (2025). Feature-Structure Adaptive Completion Graph Neural Network for Cold-start Recommendation. **, 12022-12030.[ https://doi.org/10.1609/aaai.v39i11.33309](https://doi.org/10.1609/aaai.v39i11.33309)

Peng, X., Cheng, J., Tang, X., Zhang, B., & Tu, W. (2023). Multi-view graph imputation network. *Inf. Fusion, 102*, 102024.[ https://doi.org/10.1016/j.inffus.2023.102024](https://doi.org/10.1016/j.inffus.2023.102024)

Rossi, E., Kenlay, H., Gorinova, M., Chamberlain, B., Dong, X., & Bronstein, M. (2021). On the Unreasonable Effectiveness of Feature propagation in Learning on Graphs with Missing Node Features. *ArXiv, abs/2111.12128*.

Song, X., Zhou, B., Wang, Y., & Liu, W. (2025). Dynamic graph structure evolution for node classification with missing attributes. *Scientific Reports, 15*.[ https://doi.org/10.1038/s41598-025-09840-z](https://doi.org/10.1038/s41598-025-09840-z)

Spinelli, I., Scardapane, S., & Uncini, A. (2019). Missing Data Imputation with Adversarially-trained Graph Convolutional Networks. *Neural networks : the official journal of the International Neural Network Society, 129*, 249-260.[ https://doi.org/10.1016/j.neunet.2020.06.005](https://doi.org/10.1016/j.neunet.2020.06.005)

Taguchi, H., Liu, X., & Murata, T. (2020). Graph Convolutional Networks for Graphs Containing Missing Features. *ArXiv, abs/2007.04583*.[ https://doi.org/10.1016/j.future.2020.11.016](https://doi.org/10.1016/j.future.2020.11.016)

Tu, W., Xiao, B., Liu, X., Zhou, S., Cai, Z., & Cheng, J. (2023). Revisiting Initializing Then Refining: An Incomplete and Missing Graph Imputation Network. *IEEE Transactions on Neural Networks and Learning Systems, 36*, 3244-3257.[ https://doi.org/10.1109/tnnls.2024.3349850](https://doi.org/10.1109/tnnls.2024.3349850)

Tu, W., Zhou, S., Liu, X., Liu, Y., Cai, Z., Zhu, E., Zhang, C., & Cheng, J. (2022). Initializing Then Refining: A Simple Graph Attribute Imputation Network. **, 3494-3500.[ https://doi.org/10.24963/ijcai.2022/485](https://doi.org/10.24963/ijcai.2022/485)

You, J., , X., Ding, D., Kochenderfer, M., & Leskovec, J. (2020). Handling Missing Data with Graph Representation Learning. *ArXiv, abs/2010.16418*.

Yu, Z., Wu, Z., Zhong, S., Su, W., Chan, S., Lee, C., & Zhuo, W. (2024). M3-Impute: Mask-guided Representation Learning for Missing Value Imputation. *ArXiv, abs/2410.08794*.[ https://doi.org/10.48550/arxiv.2410.08794](https://doi.org/10.48550/arxiv.2410.08794)

  
  