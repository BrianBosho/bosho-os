**

======= ICC Review 1 =======

  

> *** Relevance and timeliness: Rate the importance and timeliness of the topic addressed in the paper within its area of research.

Good (4)

  

> *** Technical content and scientific rigour: Rate the technical content of the paper (e.g.: completeness of the analysis or simulation study, thoroughness of the treatise, accuracy of the models, etc.), its soundness and scientific rigour.

Valid work but limited contribution. (3)

  

> *** Quality of presentation: Rate the paper organization, the clearness of text and figures, the completeness and accuracy of references.

Well written. (4)

  

> *** Strong aspects: Comments to the author: what are the strong aspects of the paper

  

- The paper introduces a compelling solution to the missing neighbor problem in Subgraph Federated Learning by recasting it as a local feature imputation task. Unlike transmission-based methods (e.g., FedGCN) or generative methods (e.g., FedSage+), FedProp requires no inter-client communication during the feature propagation phase, effectively minimizing bandwidth usage.

- The results demonstrate that FedProp recovers a massive portion of the performance lost due to data partitioning. For example, on the Cora dataset (Non-IID), the method recovers 100% of the performance gap compared to the centralized oracle, which is a striking result. The trade-off analysis between accuracy and communication efficiency (Fig. 3) clearly positions the proposed method in the "ideal" quadrant compared to baselines.

  

> *** Weak aspects: Comments to the author: what are the weak aspects of the paper?

  

- The proposed method relies heavily on feature smoothness (Dirichlet energy minimization), which assumes that connected nodes share similar features (homophily). As admitted in the conclusion, this approach may underperform or fail on heterophilic graphs where neighbors have dissimilar features. The paper lacks experimental validation on heterophilic datasets (e.g., Texas, Wisconsin) to quantify this limitation.

- For the 2-hop scenario (L=2), the paper assumes a “centrally known topology” where a server provides the topology, including edges between remote nodes. While the training phase is zero-communication, this setup phase entails significant leakage of topological information to the server or among clients, which might contradict strict privacy requirements in some FL scenarios. Furthermore, the cost/privacy trade-off of this initial setup is not fully analyzed.

- While Fig. 3 plots a comparison against FedGCN and FedGAT regarding efficiency, the main numerical results (Table I) primarily compare FedProp against its own variants (1-hop vs 2-hop) and the zero and full baselines . A direct tabular comparison of accuracy against state-of-the-art methods like FedSage+ or FedNI in Table I is missing.

- The paper claims computational efficiency based on sparse matrix multiplication. However, feature propagation is an iterative process (typically 30-50 iterations). On very large, dense subgraphs, this local pre-processing step could become a computational bottleneck for resource-constrained edge devices.

  

> *** Novelty and originality: Rate the novelty and originality of the ideas or results presented in the paper.

Minor variations on a well-investigated subject. (2)

  

> *** Recommended changes: Please indicate any changes that should be made to the paper if accepted.

  

- Should include at least one experiment on a heterophilic dataset

- Should compare directly to SOTA in terms of raw accuracy, not just communication efficiency.

-Should revise the claim of "Strong Privacy" to explicitly discuss the implications of the L=2 setting. If the server "provides the complete 2-hop topology", the paper needs to clarify if this reveals sensitive link information and if this setup cost is included in the communication efficiency calculations.

Minor:

- A brief discussion or citation regarding the privacy implications of successfully reconstructing neighbor features would strengthen the security analysis.

  

> *** Submission Policy: Does the paper list the same author(s), title and abstract (minor wording differences in the abstract are okay) in its PDF file and EDAS registration? (yes/no)

  

yes

  

======= ICC Review 2 =======

  

> *** Relevance and timeliness: Rate the importance and timeliness of the topic addressed in the paper within its area of research.

Excellent (5)

  

> *** Technical content and scientific rigour: Rate the technical content of the paper (e.g.: completeness of the analysis or simulation study, thoroughness of the treatise, accuracy of the models, etc.), its soundness and scientific rigour.

Solid work of notable importance. (4)

  

> *** Quality of presentation: Rate the paper organization, the clearness of text and figures, the completeness and accuracy of references.

Excellent. (5)

  

> *** Strong aspects: Comments to the author: what are the strong aspects of the paper

  

This paper is well written overall. This author addresses a key challenge in federated graph neural networks—the loss of neighborhood information caused by cross-client edges—by proposing a novel solution with strong theoretical foundations and practical feasibility. By reformulating the problem as a local feature imputation task guided by Dirichlet energy minimization, the authors introduce a model-agnostic framework, FedProp, which efficiently reconstructs missing neighborhood information without requiring any additional inter-client communication.

  

> *** Weak aspects: Comments to the author: what are the weak aspects of the paper?

  

1. The manuscript contains a substantial amount of unnecessary bold formatting, particularly in the Results and Conclusion sections. It is recommended that these boldface elements be removed to improve readability and maintain a consistent academic style.

2. The reference citation format is not consistent with standard conventions. The authors are advised to revise the references according to the IEEE citation style.

  

> *** Novelty and originality: Rate the novelty and originality of the ideas or results presented in the paper.

Significant original work and novel results. (4)

  

> *** Recommended changes: Please indicate any changes that should be made to the paper if accepted.

  

1. The manuscript contains a substantial amount of unnecessary bold formatting, particularly in the Results and Conclusion sections. It is recommended that these boldface elements be removed to improve readability and maintain a consistent academic style.

2. The reference citation format is not consistent with standard conventions. The authors are advised to revise the references according to the IEEE citation style.

  

> *** Submission Policy: Does the paper list the same author(s), title and abstract (minor wording differences in the abstract are okay) in its PDF file and EDAS registration? (yes/no)

  

Yes

  

======= ICC Review 3 =======

  

> *** Relevance and timeliness: Rate the importance and timeliness of the topic addressed in the paper within its area of research.

Good (4)

  

> *** Technical content and scientific rigour: Rate the technical content of the paper (e.g.: completeness of the analysis or simulation study, thoroughness of the treatise, accuracy of the models, etc.), its soundness and scientific rigour.

Valid work but limited contribution. (3)

  

> *** Quality of presentation: Rate the paper organization, the clearness of text and figures, the completeness and accuracy of references.

Readable, but revision is needed in some parts. (3)

  

> *** Strong aspects: Comments to the author: what are the strong aspects of the paper

  

The problem addressed in this paper is important, though several advancements have been made in recent years.

  

> *** Weak aspects: Comments to the author: what are the weak aspects of the paper?

  

The main contribution of the paper is the authors’ claim that they are the first to minimize the DE for each client by adding nodes to each client’s local subgraph. However, it is not clear from the manuscript how this node addition is performed, nor how many nodes are created at each client.

  

Furthermore, the paper does not clearly describe how the GNN training is conducted, or how the trained model generalizes when a new client is added to the federated learning setup.

  

According to the manuscript, many important details are deferred to the supplementary material, but I was unable to locate it. In particular, while the convergence of DE is well established in the literature, it would be more appropriate to include an analysis of the convergence of the GNN training in the specific setting considered in this paper.

  

> *** Novelty and originality: Rate the novelty and originality of the ideas or results presented in the paper.

Some interesting ideas and results on a subject well investigated. (3)

  

> *** Recommended changes: Please indicate any changes that should be made to the paper if accepted.

  

See weak aspects.

  

> *** Submission Policy: Does the paper list the same author(s), title and abstract (minor wording differences in the abstract are okay) in its PDF file and EDAS registration? (yes/no)

  

yes

**