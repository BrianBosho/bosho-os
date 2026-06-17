The paper needs a **narrower experimental spine**, not a larger collection of loosely connected experiments. The strongest story is:

On homophilic node-classification graphs where partitioning creates a measurable full-to-local performance gap, FedProp recovers a substantial fraction of the lost accuracy through client-local feature propagation, while introducing zero additional graph-data communication beyond standard FedAvg.

This is more defensible than saying simply “communication-free.” FedProp still uses ordinary federated model aggregation, and some variants assume that neighborhood topology is already available. The current draft already motivates FedProp as local reconstruction of inaccessible neighbor features and reports improvements without inter-client feature communication; the revised claim should make the communication baseline and scope explicit.

## 1. Make “performance recovery” the primary result

For every dataset, backbone, partition, and L1/L2 setting, report three quantities:

[  
\Delta_{\mathrm{loss}}  
= A_{\mathrm{Full}}-A_{\mathrm{0hop}},  
]

[  
\Delta_{\mathrm{gain}}  
= A_{\mathrm{FedProp}}-A_{\mathrm{0hop}},  
]

[  
\mathrm{Recovery}%  
=100\frac{A_{\mathrm{FedProp}}-A_{\mathrm{0hop}}}  
{A_{\mathrm{Full}}-A_{\mathrm{0hop}}}.  
]

Call the final metric **gap recovery** or **degradation recovery**.

This directly answers the paper’s central question: how much of the performance lost by removing cross-client information is recovered without exchanging that information?

Important reporting rules:

- When (A_{\mathrm{Full}}-A_{\mathrm{0hop}}) is statistically indistinguishable from zero, report recovery as **N/A: no recoverable gap**, not as a large or unstable percentage.
    
- When zero-hop beats full-graph training, also report recovery as N/A. There is no degradation for FedProp to repair.
    
- Do not clip recovery at 100%. A value above 100% may occur, but should be interpreted as FedProp outperforming that particular full-graph baseline.
    
- Use paired seeds and confidence intervals for the three differences, not only separate confidence intervals for each accuracy.
    

Your main result figure should probably show, for each dataset:

**0-hop → L1 FedProp → L1+RPE → L2 FedProp → L2+RPE → Full**

A thin vertical bracket between 0-hop and Full can visually represent the recoverable gap, with the FedProp bars showing how much is recovered.

## 2. Treat Amazon and heterophilic results as scope diagnostics

Do not hide Amazon Computers/Photo because the improvement is small. Their small full-versus-zero-hop gap is itself an important result:

> FedProp cannot produce a large recovery when removing neighborhood information causes little degradation in the first place.

That is different from saying FedProp fails.

Similarly, the heterophilic datasets should not be forced into a positive-results narrative. Feature propagation is a low-pass, smoothness-promoting procedure. Prior feature-propagation work explicitly finds that its advantage decreases as homophily decreases and can approach the zero-feature baseline at very low homophily. The method is derived from Dirichlet-energy minimization, which promotes similarity between connected nodes.

A good dataset structure would be:

- **Core recovery benchmarks:** Cora, CiteSeer, PubMed, OGBN-Arxiv.
    
- **Non-citation diagnostic:** Amazon Computers or Amazon Photo.
    
- **Scope/negative control:** one or two heterophilic datasets, preferably in a compact subsection or appendix.
    

The conclusion should be that FedProp targets settings where graph aggregation is beneficial and partitioning removes useful, smooth cross-client signal. Avoid claiming that the missing-neighbor problem does not exist on all heterophilic graphs; the safer statement is that it is not manifested by your tested GCN/GAT setup when full-graph training does not outperform zero-hop training.

OGBN-Products is only necessary if you retain a strong scalability claim. The underlying feature-propagation method has been shown to scale to OGBN-Products, but that does not by itself establish that your federated neighborhood-expansion implementation scales to it. Either run a credible scalability experiment or soften that claim.

## 3. Turn the topology question into a testable theory

The most valuable additional analysis is not another large accuracy table. It is a connection between topology, feature smoothness, reconstruction error, and downstream recovery.

Partition the Laplacian according to known local nodes (K) and unknown remote nodes (U):

[  
L=  
\begin{bmatrix}  
L_{KK} & L_{KU}\  
L_{UK} & L_{UU}  
\end{bmatrix}.  
]

The harmonic reconstruction satisfies

[  
\widehat X_U=-L_{UU}^{-1}L_{UK}X_K.  
]

Therefore,

# [  
\widehat X_U-X_U

-L_{UU}^{-1}(LX)_U,  
]

and, when (L_{UU}) is invertible,

[  
|\widehat X_U-X_U|_F  
\leq  
\frac{1}{\lambda_{\min}(L_{UU})}  
|(LX)_U|_F.  
]

This gives you a clean explanation of two failure modes:

1. **Feature/topology incompatibility:** (|(LX)_U|_F) is large when features vary strongly across edges, as expected in less homophilic or high-frequency graph signals.
    
2. **Poor boundary anchoring:** (\lambda_{\min}(L_{UU})) is small when unknown nodes form weakly anchored regions, are far from known local nodes, or lie in poorly connected components.
    

Partitioning changes (K), (U), the graph cut, and (L_{UU}). It therefore changes reconstruction difficulty even when the dataset and propagation algorithm stay fixed.

This theoretical result would justify measuring:

- Cross-client edge ratio.
    
- Fraction of boundary nodes.
    
- Average remote-neighbor fraction per local node.
    
- Distance of reconstructed nodes to the nearest known node.
    
- (\lambda_{\min}(L_{UU})), or a scalable proxy.
    
- Feature Dirichlet energy or (|(LX)_U|_F).
    
- Label and feature homophily.
    

Then test whether the observed reconstruction error follows the theoretically motivated proxy

[  
\frac{|(LX)_U|_F}{\lambda_{\min}(L_{UU})}.  
]

That would be substantially stronger than a generic statement that “topology matters.”

## 4. Add reconstruction experiments, but keep them subordinate to the task result

Because the true remote features exist in the original centralized dataset, they can be hidden from the algorithm but retained for evaluation.

For each propagation iteration (t), evaluate only the masked cross-client nodes:

- Node-wise cosine similarity.
    
- Normalized RMSE or normalized Frobenius error.
    
- Relative error reduction against zero initialization.
    
- Dirichlet-energy ratio between reconstructed and true features.
    

For sparse bag-of-words datasets such as Cora and CiteSeer, raw MSE can be misleading because most entries are zero. Cosine similarity and support-recovery F1 are more informative. For OGBN-Arxiv’s dense features, cosine similarity and normalized RMSE are appropriate.

A useful normalized reconstruction-recovery metric is

# [  
\mathrm{FeatureRecovery}(t)

1-  
\frac{|\widehat X_U^{(t)}-X_U|_F}  
{|X_U^{(0)}-X_U|_F}.  
]

Then produce two plots:

1. Reconstruction recovery and downstream accuracy versus propagation iterations.
    
2. Downstream accuracy versus reconstruction similarity across all dataset-partition-client conditions.
    

Use Spearman correlation rather than claiming a linear relationship. Also acknowledge that exact feature reconstruction and task utility are not identical: prior work explicitly notes that downstream prediction can be more forgiving than recovering the original features exactly.

RPE should be kept separate in this analysis. RPE may improve classification without reconstructing the original semantic features, so do not use its downstream gain as evidence of better feature reconstruction.

## 5. Explain partitioning through realized graph statistics, not only (\beta)

The expectation that IID should always perform better is not valid in a partitioned graph.

A smaller Dirichlet (\beta) changes label skew, but it may also cluster connected or same-class nodes within clients, producing fewer cross-client edges. That can make zero-hop training better because less neighborhood information is removed. FedGCN reports exactly this phenomenon: its non-IID zero-hop setting can outperform IID zero-hop because the non-IID partition contains fewer cross-client edges.

Therefore, for every (\beta), report:

- Label-distribution divergence across clients.
    
- Cross-client edge ratio.
    
- Boundary-node fraction.
    
- Mean local-node remote-neighbor ratio.
    
- Per-client graph size and class coverage.
    

Do not write that FedProp is “immune” to partitioning. Use **robust across the evaluated partition regimes**.

Your proposed sweep (0.1,1,10,100,1000,10000) is reasonable, but the realized structural metrics are more informative than the nominal (\beta). If resources allow, add one experiment separating the two effects:

- Label-Dirichlet partitioning to alter label skew.
    
- Topology-aware partitioning, such as METIS/community partitioning, to alter edge cuts.
    

That lets you distinguish statistical heterogeneity from structural fragmentation.

## 6. Clarify L1 and L2 assumptions

This is a major presentation issue.

For **L1**, state exactly what is known locally:

- The client knows its own nodes and features.
    
- The client knows the existence or identity of incident cross-client edges.
    
- It does not know the remote feature vectors.
    

This is relatively natural and is also assumed in methods such as FedGCN and FedGAT, where cross-client edges are known while remote features are unavailable.

For **L2**, do not quietly treat two-hop structure as free. Either:

- Account for the setup communication required to discover it, or
    
- Label L2 as an **extended-structure**, **oracle-topology**, or **upper-bound** variant.
    

The primary contribution should be L1. L2 can demonstrate the potential benefit of richer topology, but should not carry the unqualified zero-communication claim unless two-hop structure is genuinely available before training.

The safest terminology throughout the paper is:

> zero additional node-feature, embedding, or reconstruction-model communication beyond standard FedAvg, given the stated neighborhood-structure assumption.

Avoid broad “privacy-preserving” claims unless you provide an attack model or formal privacy guarantee.

## 7. Separate controlled comparisons from literature positioning

Do not combine your results and copied literature values in one table as though they were obtained under the same protocol.

### Controlled main comparison

Run under your exact partition, split, backbone, and training protocol:

- Full/centralized.
    
- 0-hop federated.
    
- k-hop with zero-filled remote features.
    
- FedProp-L1.
    
- FedProp-L2.
    
- FedProp + RPE.
    
- FedGCN, where feasible.
    

FedGCN is the highest-priority external rerun because its code is available, it evaluates the same single-partitioned-graph problem, and it explicitly studies 0-, 1-, and 2-hop communication. It requires a one-time pretraining exchange rather than no graph-information exchange.

### Communication–accuracy positioning

Use a separate figure for methods evaluated under their own published protocols:

- FedProp: no additional graph-data exchange.
    
- FedGCN: one pretraining communication step.
    
- FedGAT: one pretraining communication step and an approximation mechanism for GAT.
    
- FedSage+: additional NeighGen training followed by federated GraphSAGE training; its algorithm exchanges generator information over multiple epochs before the classifier phase.
    
- Repeated-exchange methods: per-round feature/embedding communication.
    

Use different marker shapes for “rerun by us” and “reported by original paper,” and retain the protocol disclaimer you previously drafted.

I would **not prioritize modifying FedGAT’s code** unless a major claim is that FedProp is the strongest communication-efficient GAT method. Demonstrating FedProp with a GAT backbone is enough for backbone generality. The reconstruction/topology analysis is more likely to address reviewer criticism than another imperfect SOTA implementation.

Similarly, rerunning FedSage+ is low priority because its graph construction, model, and partition assumptions differ substantially. One well-controlled FedGCN comparison is more persuasive than three nominal SOTA comparisons under incompatible protocols.

## 8. Redraw Figure 2 around information flow

Figure 2 should make one fact unmistakable: **FedProp reconstructs missing features locally; it does not transmit them between clients.**

Use four horizontal stages:

1. **Partitioned global graph.**  
    Clients have differently colored node regions. Cross-client edges are dashed.
    
2. **Client-local structural context.**  
    Zoom into Client (k). Local nodes have known feature icons; remote boundary nodes are ghosted and marked “feature unavailable.” Show L1 normally and L2 as a small optional inset.
    
3. **Constrained feature propagation.**  
    Show diffusion arrows over the expanded local graph. Known local features are marked with locks/clamps; unknown remote features change from “?” to reconstructed feature vectors.
    
4. **Local GNN and FedAvg.**  
    The completed local graph enters either GCN or GAT. Only model parameters travel between the client and the server. Put a crossed-out arrow between clients labelled “no node-feature/embedding exchange.”
    

Do not show FedProp inventing edges unless your algorithm actually reconstructs topology. It uses an assumed structural context and reconstructs features over it.

**Figure 2: Overview of FedProp.** A global graph is partitioned across clients, creating cross-client neighbors whose features are unavailable locally. For each client, FedProp constructs the available (k)-hop structural context, initializes remote-node features as missing, and applies constrained feature propagation while clamping the observed local features. The reconstructed feature matrix is then used by a standard GNN backbone for local training. Clients exchange only the model updates required by FedAvg; no node features or intermediate node embeddings are exchanged during reconstruction or training.

Rossi et al.’s figure works because it clearly separates feature reconstruction from downstream GNN training; your figure should add the federated partition and FedAvg communication boundary around that same two-stage idea.

## 9. Recommended experimental priority

**Must complete before submission**

1. Redraw Figure 2 and qualify the communication claim.
    
2. Add full-to-zero-hop degradation and gap-recovery metrics.
    
3. Report realized structural statistics for every partition.
    
4. Add reconstruction-error analysis and its relationship to downstream accuracy.
    
5. Rerun FedGCN under your protocol if technically feasible.
    
6. Reframe Amazon and heterophilic datasets as scope diagnostics.
    

**Strong additions**

1. L1/L2 plus RPE ablation.
    
2. Number-of-clients robustness on Cora and OGBN-Arxiv.
    
3. Empirical validation of the Laplacian reconstruction-error bound.
    
4. One non-citation Amazon dataset in the main paper.
    

**Optional or future work**

1. OGBN-Products, unless needed to support a scalability claim.
    
2. Link prediction or other downstream tasks.
    
3. Full FedGAT reimplementation.
    
4. FedSage+ head-to-head rerun.
    
5. A broad survey of heterophilic architectures.
    

The final paper should answer four research questions in order: **Does partitioning create a recoverable loss? How much does FedProp recover? What does that recovery cost in communication? Which topological and feature conditions determine whether recovery is possible?**