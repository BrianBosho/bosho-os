Yes. My previous proposal **did increase the scope significantly**, especially by adding topology theory, reconstruction-error studies, heterophily analysis, multiple partition mechanisms, scalability, and several SOTA reruns. That would make the paper more comprehensive, but it risks turning one clear contribution into several partially developed research questions.

The paper should probably stay much narrower.

## A defensible minimal scope

The core paper only needs to establish:

1. **Partitioning harms GNN performance** because clients lose access to cross-client neighbor features.
    
2. **FedProp recovers a substantial portion of that lost performance.**
    
3. **This recovery requires no additional feature or embedding communication beyond standard FedAvg.**
    
4. **The method works with both GCN and GAT.**
    

Everything else should support those four claims rather than create a new claim.

### Essential experiments

Keep:

- Cora, CiteSeer, PubMed, and OGBN-Arxiv.
    
- Zero-hop, Full, FedProp-L1, and possibly FedProp-L2.
    
- GCN and GAT.
    
- Recovery percentage.
    
- Communication–accuracy comparison with FedGCN, FedGAT, and FedSage+, using literature results where protocols differ.
    
- A client-count robustness experiment on perhaps two datasets.
    
- One concise reconstruction-quality experiment, only if reviewers explicitly requested it.
    

That is already enough for a solid paper.

## What should be reduced or removed

### Topology analysis

Do not turn the paper into a full investigation of how graph topology controls federated GNN performance.

Instead, make a modest observation:

> FedProp provides the largest benefit when removing cross-client neighborhood information creates a substantial performance gap.

Amazon and heterophilic results can support this observation in the appendix. You do not need a new theoretical framework, spectral analysis, eigenvalue experiments, or an exhaustive topology study.

### Reconstruction analysis

Keep this small:

- One reconstruction metric, such as cosine similarity or normalized RMSE.
    
- One plot showing reconstruction quality against downstream accuracy.
    
- A comparison between IID and non-IID partitions.
    

You do not need to analyze many propagation algorithms, multiple missingness mechanisms, Dirichlet energy, and formal topology-dependent error bounds in the same paper.

### SOTA reruns

Prioritize only FedGCN if it can be run without major engineering work.

Do not spend substantial time modifying FedGAT or forcing a head-to-head FedSage+ comparison under incompatible protocols. Use a clearly labelled communication–accuracy positioning figure instead.

### Additional datasets

Amazon is useful only to show that FedProp has limited benefit when the full-to-zero-hop gap is already small. One Amazon dataset is enough, probably in the appendix.

Heterophilic datasets are optional. A small diagnostic table is sufficient. They should not become a major section.

OGBN-Products is unnecessary unless scalability is a central claim reviewers are challenging.

## A tighter experimental structure

The results section could be only:

1. **Performance degradation and recovery**  
    Full vs zero-hop vs FedProp, with recovery percentage.
    
2. **Communication–accuracy tradeoff**  
    Compare FedProp’s position against methods requiring setup or repeated communication.
    
3. **Ablations and robustness**  
    L1/L2, RPE, GCN/GAT, and number of clients.
    
4. **Reconstruction diagnostic**  
    A compact analysis connecting feature reconstruction to classification improvement.
    

The Amazon, heterophily, detailed partition sweeps, and extra reconstruction metrics can go into the appendix.

So the answer is: **yes, the scope was expanding, and it should be pulled back**. The topology questions are interesting future work, but they are not necessary to validate FedProp’s main contribution. The strongest revision is likely a more focused paper with a clearer recovery metric and communication claim, not a substantially larger experimental program.