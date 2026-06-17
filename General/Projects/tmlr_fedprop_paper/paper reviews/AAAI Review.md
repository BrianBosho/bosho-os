**

#### A communication-free approach with unsatisfactorty performance

Official Reviewby Program Committee KaE624 Aug 2025, 08:20 (modified: 22 Sept 2025, 15:46)Program Chairs, Area Chairs, Senior Program Committee, Program Committee KaE6, Authors[Revisions](https://openreview.net/revisions?id=VXEtLkFm3M)

Review:

This paper proposes FedProp, a communication-free method for the federated graph neural network setup to reconstruct missing neighbor features through iterative local propagation. By assuming the 1-hop neighbor nodes are known across different clients, the paper views the problem as a missing-feature problem. Without further requiring inter-client communication or additional learnable parameters, FedProp allows each client to train a GNN using only its local graph and initial node features. Experimental results suggest that FedProp can effectively improve the local GNN training's performance.

### Summary of Strengths

1. The paper is well-written with theoretical support.
    
2. FedProp obtains the best efficiency compared with other Federated GNN baselines.
    

### Summary of Weaknesses

1. Poor performance with other federated GNN baselines such as FedGCN and FedGAT. For example, according to Table 5, FedProp fails to outperform the FedGAT baseline for both iid and non-iid settings.
    
2. FedProp initializes unknown remote nodes to zeros and aims to recover their feature vectors through residual minimization. As experimental results demonstrate, FedProp works well on an iid setup, but there is no guarantee in the non-iid setting. Normally, for graphs with high sparsity, it is hard for FedProp to recover the unknown feature vectors.
    

Rating: 5: Marginally below acceptance threshold

Confidence: 3: The reviewer is fairly confident that the evaluation is correct

Add:

#### Limited practical research delta indication form the paper and lack of formal analysis

Official Reviewby Program Committee bNK623 Aug 2025, 16:42 (modified: 22 Sept 2025, 15:46)Program Chairs, Area Chairs, Senior Program Committee, Program Committee bNK6, Authors[Revisions](https://openreview.net/revisions?id=BaFfsgGHLf)

Review:

### Strengths

1. The paper works a challenge in federated graph training where the cross-client edges can create information gaps during message passing. This is a practical problem that occurs frequently in real-world distributed graph scenarios.
    
2. FedProp leverages zero inter-client communication during training to avoid significant communication overhead.
    

### Weaknesses

1. The paper lacks comprehensive evaluation for the proposed method, speciffically, it is evaluated on three citation networks, which are relatively small and homogeneous that can not be generalized for other graph problems.
    
2. The paper claims privacy protection due to no communication, it doesn't provide a formal privacy analysis. The iterative feature propagation process might leak some information about the graph structure. A rigorous and quantifiable privacy analysis is a requirement for any privacy work.
    

Rating: 4: Ok but not good enough - rejection

Confidence: 4: The reviewer is confident but not absolutely certain that the evaluation is correct

Add:

#### More detailed analysis and experiments are needed

Official Reviewby Program Committee P23321 Aug 2025, 05:43 (modified: 22 Sept 2025, 15:46)Program Chairs, Area Chairs, Senior Program Committee, Program Committee P233, Authors[Revisions](https://openreview.net/revisions?id=lxl8O8058h)

Review:

This paper proposes FedProp, a zero-additional communication, implicit feature imputation framework for federated graph learning. The authors formulate the cross-client missing neighbor problem as a feature imputation task on graphs, leveraging local heat diffusion iterations to estimate remote node features, thereby enabling each client to train a complete GNN without exchanging any raw or intermediate data. The paper provides convergence guarantees and conducts experiments on Cora, Citeseer, and PubMed, demonstrating the effectiveness of FedProp.

Strengths  
1. The fully localized feature imputation eliminates any inter-client information exchange, maintaining the same communication cost as standard FedAvg.  
2. The manuscript exhibits a clear logical flow and the method is described with clarity.

Concerns  
1. The scenario proposed by the authors is highly similar to that described in [1], and the methodology is somewhat analogous. The difference lies in the fact that the authors do not consider cross-client propagation. Therefore, how can the consistency between the imputed cross-client features and the real features be guaranteed?  
2. The iterative feature imputation proposed by the authors is essentially equivalent to solving a Dirichlet energy minimization problem on a local subgraph, ultimately obtaining a steady-state solution that satisfies boundary constraints. However, the assumption of Dirichlet energy minimization often fails to hold on heterophilic graphs. The author should supplement theoretical analysis and experimental results on heterophilic graphs to validate the proposed method.  
3. While the authors provide Table 5 in the supplementary materials to highlight the distinctions between FedProp and prior FGL methods, the empirical evaluation does not benchmark against these methods. In particular, FedSAGE+ [2] and FedDEP [3], which are specifically designed to address cross-client feature missingness, should be included for a comprehensive evaluation.  
4. Most critically, I remain skeptical about the justification of the proposed setting. Compared with standard FGL setting [4], the proposed setup requires additional consideration of missing cross-client connections. In contrast to cross-client FGL approaches, FedProp neither considers higher-order features [3] nor verifies the discrepancy between imputed features and real features [1][2][3]. 5. Checklist is missing.

[1] Federated learning over coupled graphs. IEEE Transactions on Parallel and Distributed Systems, 2023.  
[2] Subgraph federated learning with missing neighbor generation. Neural Information Processing Systems, 2021.  
[3] Deep efficient private neighbor generation for subgraph federated learning. International Conference on Data Mining, 2024.  
[4] OpenFGL: A Comprehensive Benchmark for Federated Graph Learning. VLDB, 2025.

Rating: 3: Clear rejection

Confidence: 5: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature

  
**

**

Review:

Title: FedProp: Federated Graph Neural Networks with Feature Propagation

Synopsis of the paper The paper addresses federated training of graph neural networks in the presence of cross-client edges that prevent standard message passing. It proposes FedProp, a communication-free, model-agnostic procedure that imputes missing one-hop neighbor features locally via iterative feature propagation with boundary resets. The method is analyzed via the graph heat equation and Dirichlet energy minimization, with a convergence guarantee under suitable propagation operators. Experiments on citation benchmarks show improvements over a local-only baseline and, in independent-and-identically-distributed partitions, accuracy close to centralized training.

Summary of Review This work targets a significant obstacle in federated graph learning and offers a simple, general pre-processing mechanism that can be paired with standard graph neural networks without changing their training or requiring inter-client communication. The heat-equation view and the fixed-point update are technically clean and practically attractive, and empirical results are promising relative to a local-only baseline. However, the paper contains a key inconsistency in how boundary edges are defined and used, operator mislabeling, and a mismatch in the Dirichlet energy formulation; it also omits crucial implementation details (e.g., for the diffusion kernel) and stability conditions needed for reproducibility. The evaluation scope is narrow (small, homophilic datasets) and mixes baselines from prior work without complete apples-to-apples comparisons, and several presentation inconsistencies and unqualified claims remain. With these issues addressed, the paper could make a useful contribution as a lightweight, privacy-preserving alternative to communication- and generator-based approaches.

Strengths

- Problem significance and motivation:
    

- The paper clearly identifies the central federated graph learning challenge: cross-client edges break message passing when clients cannot exchange neighbor features. The review of generative (e.g., FedSage+, FedNI) and transmission-based (e.g., FedGCN, FedGAT) approaches and their trade-offs motivates a communication-free alternative.
    

- Conceptual simplicity with sound grounding:
    

- The missing-neighbor issue is recast as local feature imputation by iterating  with boundary resets, corresponding to explicit Euler steps on the graph heat equation with Dirichlet boundary conditions. The block update for unknown nodes,
    
- is simple and implementable, and the steady-state solution for Laplacian-based propagation,
    
- matches the Dirichlet-energy minimizer under fixed boundaries.
    

- Communication-free, model-agnostic pre-processing:
    

- The propagation step introduces no learnable parameters, preserves the communication profile of standard federated averaging, and can be paired with multiple message-passing architectures. The idea of augmenting with positional encodings is lightweight and shows gains in several settings.
    

- Empirical evidence of utility and convergence:
    

- On Cora, Citeseer, and Pubmed, FedProp variants clearly improve over the no-imputation baseline and, under independent-and-identically-distributed partitions, approach centralized accuracy. The plots of residual decay and the reported iteration counts suggest fast, stable convergence.
    

Weaknesses

- Accessible-edge inconsistency that affects correctness:
    

- The method requires nonzero cross-client boundary couplings  to propagate information into unknown nodes. The paper states that the accessible edge set “is restricted to only local edges within ,” yet simultaneously describes remote nodes as “isolated leaves connected solely through their (unknown) boundary edges to local nodes.” If only local-local edges are retained,  and the propagation cannot impute unknown features as derived. This is a critical contradiction that must be resolved by clearly defining which boundary edges are known and used during propagation (and, later, during GNN training).
    

- Operator/notation errors and overgeneralized claims:
    

- Algorithm 1 labels  as “normalized adjacency,” which is incorrect.  is the Euler diffusion operator; normalized adjacency is 
    
-  and is distinct except in special cases. The main text later lists both 
    
-  and  as alternatives; these should be presented consistently as propagation operators  with distinct fixed points.
    
- The general claim that “any symmetric propagation operator with spectral radius bounded by one” suffices is true for convergence, but the Dirichlet-energy and heat-equation interpretations and the closed-form 
    
-  apply specifically to Laplacian-based propagation. For general , the fixed point solves 
    
-  and is not, in general, the Dirichlet minimizer. The exposition conflates these.
    

- Dirichlet energy mismatch:
    

- The paper defines  and states 
    
- , and then mentions normalized features 
    
-  in prose. As written, the equality for  matches the unnormalized Laplacian, not the symmetric normalized Laplacian. This should be corrected or justified by specifying the normalization (e.g., self-loops and how they enter ).
    

- Missing stability conditions and key implementation details:
    

- The step-size  constraints for explicit Euler (e.g., ) and sufficient conditions ensuring  are deferred to the appendix and not summarized in the main text, limiting reproducibility.
    
- The paper uses the diffusion kernel  in experiments but does not state how  is approximated (e.g., truncated Chebyshev series, diagonalization, scaling-and-squaring), nor  or approximation order, which materially affects both accuracy and complexity. The stated per-iteration cost  only holds for sparse matrix-vector/matrix multiplications; without an explicit approximation,  is dense.
    

- Unclear use of boundary edges at GNN training time:
    

- After imputation, the paper says the client trains a GNN “using the imputed features  and local adjacency .” If  includes only local-local edges, then imputed remote features cannot enter message passing. If cross-client boundary edges are included, how are degrees and normalizations computed for remote neighbors, and how is privacy preserved? This ambiguity undermines the stated mechanism.
    

- Evaluation scope and comparability:
    

- Experiments are limited to small, homophilic citation graphs. There is no evidence on larger (e.g., ogbn-arxiv) or heterophilous graphs where the smoothness assumption may be weaker.
    
- Although the text claims backbone-agnosticity and mentions coupling with graph attention, the main results for FedProp use a graph convolutional backbone; no FedProp-with-graph-attention results are reported under the same splits, while comparisons to attention-based baselines are imported from prior work.
    
- Some baselines in figures (e.g., DGCN, BDS-GCN) are referenced without definitions or citations, and Table 5 includes DistGAT without a corresponding citation in the paper’s list. The communication section uses “precision” while accuracy is reported elsewhere, and the partition description flips  labels (Section 5.1 says  for independent-and-identically-distributed and  for non-independent-and-identically-distributed; later text says the opposite).
    

- Claims vs. evidence and variance:
    

- The claim of “97–99 percent of the centralized system” is supported in independent-and-identically-distributed partitions but not uniformly in non-independent-and-identically-distributed settings (e.g., Cora and Citeseer show larger gaps). Moreover, the positional-encoding variant exhibits high variance in at least one setting (Cora independent-and-identically-distributed: ), suggesting instability that should be analyzed.
    

Suggestions for Improvement

- Resolve the boundary-edge definition and privacy assumptions:
    

- Precisely define , , and the boundary set , and specify the edge sets included at each stage:  (local-local) and  (boundary) used for propagation and training, while excluding  (remote-remote) to preserve privacy. Present the block forms of , , , and  actually used.
    
- State clearly what information about cross-client edges is assumed to be known (e.g., only which local nodes have which remote neighbors, but no remote-remote connectivity) and how this information is obtained without violating privacy or adding communication. If a trusted server provides boundary adjacency metadata, state that assumption.
    
- Clarify whether boundary edges are used during GNN message passing after imputation. If yes, detail degree/normalization computation for remote nodes; if no, explain how imputed features influence aggregation despite the absence of boundary edges (the current derivation requires ).
    

- Tighten mathematical exposition:
    

- Rename  in Algorithm 1 as the “propagation operator” and distinguish the concrete choices:  (Euler diffusion on the symmetric normalized Laplacian), 
    
-  (normalized adjacency), and  (diffusion kernel). Avoid labeling  as normalized adjacency.
    
- Correct the Dirichlet energy expression to be consistent with the declared ; either adopt the unnormalized Laplacian, or keep  and write  in the corresponding form (or specify self-loop handling and the exact normalization used).
    
- In the block partition of 
    
- , fix the typo to use 
    
-  (not 
    
- ), since only the unknown block is iterated.
    
- In the main text (not only the appendix), summarize sufficient conditions for convergence: admissible  (e.g., ), assumptions ensuring  (e.g., every unknown node connects to at least one boundary node), and stopping criteria with typical tolerances.
    
- Clearly separate convergence-versus-optimality claims: when , the fixed point minimizes Dirichlet energy subject to boundary constraints; for general symmetric  with , only convergence to the fixed point of the corresponding affine map is guaranteed.
    

- Provide missing implementation details for reproducibility:
    

- Specify , , the stopping tolerance , iteration cap , and whether self-loops are used (and where); if using , describe how  is computed or approximated (e.g., Chebyshev approximation with order ), and report the resulting cost, e.g., .
    
- Describe how positional encodings are incorporated: whether they are concatenated to raw features before propagation, appended after propagation, or propagated separately and then concatenated; clarify for which nodes (local, unknown, or all) this is applied.
    
- Report all federated training details: number of clients  per experiment, Dirichlet parameter  and its mapping to independent-and-identically-distributed versus non-independent-and-identically-distributed partitions, number of communication rounds, local epochs, optimizer, learning rates, and random seeds.
    

- Strengthen and align the empirical evaluation:
    

- Include direct comparisons to generative imputation baselines (e.g., FedSage+ and FedNI) under the same splits and budgets to position FedProp against that class (Zhang et al., 2021; Peng et al., 2023).
    
- Demonstrate backbone-agnosticity by reporting FedProp with a graph attention backbone trained under the same splits and federated protocol, instead of only reusing attention-based baselines from prior work (Ambekar et al., 2024).
    
- Expand to a large-scale homophilic dataset (e.g., ogbn-arxiv, mentioned in the introduction) and a heterophilous dataset to probe the limits of the smoothness assumption. If performance degrades under heterophily, discuss the limitations and potential remedies (e.g., adaptive or edge-type-aware propagation (Fu & King, 2023)).
    
- Add ablations and error analyses: sensitivity to , , and ; effect of larger accessible radius  (with privacy discussion); performance as a function of node degree and boundary proximity; analysis of the high variance observed in some positional-encoding settings.
    
- Ensure all baselines appearing in figures (e.g., DGCN, BDS-GCN) are defined and cited, and that metric names are consistent throughout (accuracy vs. precision). Correct the flipped  labeling for independent-and-identically-distributed versus non-independent-and-identically-distributed partitions.
    

- Calibrate claims and discuss privacy:
    

- Qualify the “97–99 percent of centralized” claim to independent-and-identically-distributed settings and present a concise summary of non-independent-and-identically-distributed gaps to avoid overstatement.
    
- Elaborate on the privacy posture: does boundary metadata disclosure (which remote node identifiers are adjacent to which local nodes) pose privacy risk? How does the method align with, or differ from, privacy mechanisms used in vertical federated GNNs (Chen et al., 2022) and knowledge-transfer approaches (Huang et al., 2023)? If applicable, outline how differential privacy could be integrated into propagation or training.
    

References

- Ambekar, S., Yao, Y., Li, R., & Joe-Wong, C. (2024). FedGAT: A privacy-preserving federated approximation algorithm for graph attention networks. arXiv preprint arXiv:2412.16144.
    
- Baek, J., Jeong, W., Jin, J., Yoon, J., & Hwang, S. J. (2023). Personalized subgraph federated learning. In S. Koyejo et al. (Eds.), Proceedings of the 40th International Conference on Machine Learning (Vol. 202, pp. 1396–1415). Proceedings of Machine Learning Research.
    
- Chen, C., Zhou, J., Zheng, L., Wu, H., Lyu, L., Wu, J., Liu, Z., Wang, L., & Zheng, X. (2022). Vertically federated graph neural network for privacy-preserving node classification. In Proceedings of the 31st International Joint Conference on Artificial Intelligence (pp. 1959–1965).
    
- Fu, X., & King, I. (2023). FedHGN: A federated framework for heterogeneous graph neural networks. In Proceedings of the 32nd International Joint Conference on Artificial Intelligence (pp. 3705–3713).
    
- He, C., Ceyani, E., Balasubramanian, K., Annavaram, M., & Avestimehr, S. (2022). SpreadGNN: Decentralized multi-task federated learning for graph neural networks on molecular data. Proceedings of the AAAI Conference on Artificial Intelligence, 36(6), 6967–6975.
    
- Huang, W., Wan, G., Ye, M., & Du, B. (2023). Federated graph semantic and structural learning. In Proceedings of the 32nd International Joint Conference on Artificial Intelligence (pp. 3830–3838).
    
- Peng, L., Wang, N., Dvornek, N., Zhu, X., & Li, X. (2023). FedNI: Federated graph learning with network inpainting for population-based disease prediction. IEEE Transactions on Medical Imaging, 42(7), 2032–2043.
    
- Rossi, E., Kenlay, H., Gorinova, M. I., Chamberlain, B. P., Dong, X., & Bronstein, M. (2022). On the unreasonable effectiveness of feature propagation in learning on graphs with missing node features. arXiv preprint arXiv:2111.12128.
    
- Yao, Y., Jin, W., Ravi, S., & Joe-Wong, C. (2023). FedGCN: Convergence–communication tradeoffs in federated training of graph convolutional networks. In Advances in Neural Information Processing Systems 36 (NeurIPS 2023).
    
- Zhang, K., Yang, C., Li, X., Sun, L., & Yiu, S. M. (2021). Subgraph federated learning with missing neighbor generation. In Advances in Neural Information Processing Systems 34 (NeurIPS 2021).
    

  
**