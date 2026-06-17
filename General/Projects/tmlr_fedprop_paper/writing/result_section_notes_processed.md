---
type: processed-note
status: draft
project: tmlr_fedprop_paper
source: Unprocessed/Result section Notes.md
tags: [fedprop, writing, results, scope-map]
---

# Result Section Notes - Processed Scope Map

## Purpose

This note processes the raw ideas, issues, and concerns in [[../Unprocessed/Result section Notes]] into an execution map. The raw note stays unchanged. This file records what each concern means for P1, P2, or P3.

## Scope Decision Summary

| Theme | Decision |
|---|---|
| P1 | Make the current manuscript coherent using existing evidence. Rewrite claims, fix Figure 2, clarify assumptions, foreground recovery, and park unsupported expansion. |
| P2 | Strengthen the same TMLR paper with bounded analysis or reruns only after P1 gap assessment. |
| P3 | Preserve topology, reconstructability, and broad heterophily questions as a separate paper. |

## Processed Concern Map

| Raw concern | Stage | Resolution / implementation | Destination |
|---|---|---|---|
| Figure 2 does not clearly show the FedProp process. | P1 | Redraw as a four-stage information-flow diagram: partitioned graph, client-local structural context, constrained propagation, local GNN plus FedAvg. Emphasize no node-feature or embedding exchange. | [[figure_2_redraw_spec]] |
| Primary contribution is currently described as "communication-free." | P1 | Replace broad phrasing with the precise claim: zero additional node-feature, embedding, or reconstruction-model communication beyond standard FedAvg, given the stated neighborhood-structure assumption. | [[claims_and_language_pass]], [[../analysis/communication_accounting]] |
| Results should show improvement without added communication cost. | P1 | Make recovery from Full-to-Zero-hop degradation the main results spine. Pair it with communication accounting instead of relying only on raw accuracy. | [[results_rewrite_notes]], [[../analysis/recovery_metrics]], [[../analysis/communication_accounting]] |
| Show recovery percentage for L1 and L2. | P1 if values already exist; otherwise P2 | Compute/report loss, gain, and Recovery% from existing result tables. L1 carries the main claim; L2 must be labeled as extended-structure/oracle-topology unless setup cost is accounted for. | [[../analysis/recovery_metrics]], [[../analysis/l1_l2_assumptions]] |
| RPE can improve recovery. | P1 if existing ablation is already paper-ready; otherwise P2 | Present RPE as an ablation that may improve task performance. Do not imply RPE necessarily improves semantic feature reconstruction. | [[results_rewrite_notes]], [[../execution/P2-tmlr-improvement-plan]] |
| Amazon datasets may show little Full-to-Zero-hop degradation. | P1 framing; P2 if rerun needed | Treat Amazon as a scope diagnostic: when there is little recoverable gap, FedProp has limited room to help. Do not force it into a positive-results narrative. | [[results_rewrite_notes]], [[../execution/P1-current-evidence-manuscript]] |
| Amazon/topology issue raises broader questions about graph topology. | P3 | Park as a separate topology and reconstructability research question. Do not let it expand P1. | [[../analysis/topology_reconstructability_notes]], [[../execution/P3-topology-reconstructability-paper]] |
| Compare FedProp to SOTA methods: FedGCN, FedGAT, FedSage/FedSage+. | P1 positioning; P2 controlled rerun | In P1, separate same-protocol results from literature positioning. In P2, consider controlled FedGCN rerun first. FedGAT modification and FedSage+ head-to-head are lower priority because protocols differ. | [[results_rewrite_notes]], [[../execution/P2-tmlr-improvement-plan]] |
| Raw SOTA accuracy comparison drew criticism. | P1 | Avoid mixing literature values and rerun values as though protocols match. Use a communication-accuracy positioning figure/table with explicit protocol labels. | [[results_rewrite_notes]], [[../analysis/communication_accounting]] |
| Reconstruction errors may address reviewer concerns about generated/recovered features. | P2 | Add a small diagnostic only after P1: cosine similarity or normalized RMSE, reconstruction quality vs downstream accuracy, IID vs non-IID comparison. Keep subordinate to task performance. | [[../execution/P2-tmlr-improvement-plan]] |
| Link reconstruction error to topology or theoretical formulation. | P3, maybe small P2 bridge | The broad theory question belongs to P3. P2 may include a small diagnostic if the P1-to-P2 gap assessment says it is required for the TMLR claim. | [[../analysis/topology_reconstructability_notes]], [[../execution/P3-topology-reconstructability-paper]], [[../execution/P1-to-P2-gap-assessment]] |
| Model-agnostic framework should show GCN and GAT. | P1 | Keep GCN and GAT evidence as one of the four core claims. Avoid turning this into a demand for every backbone. | [[../execution/P1-current-evidence-manuscript]] |
| Robustness to number of clients. | P2 unless already paper-ready | Include existing client-count results only if clean and directly useful. New or expanded robustness belongs after P1. | [[../execution/P2-tmlr-improvement-plan]] |
| Partition-regime robustness across beta values. | P2 | Do not claim immunity to partition changes. Use "robust across evaluated partition regimes." Deeper beta sweeps and structural metrics are P2. | [[claims_and_language_pass]], [[../execution/P2-tmlr-improvement-plan]] |
| What does changing partition regime do to graph structure? | P2/P3 | P2 can report realized graph statistics. P3 can study partition-induced missingness systematically. | [[../execution/P2-tmlr-improvement-plan]], [[../execution/P3-topology-reconstructability-paper]] |
| Solid results exist for Planetoid and OGBN-Arxiv. | P1 | Use Cora, CiteSeer, PubMed, and OGBN-Arxiv as core recovery benchmarks if already paper-ready. | [[results_rewrite_notes]], [[../execution/P1-current-evidence-manuscript]] |
| OGBN-Products may be too big and only useful for scalability. | P3 or optional P2 | Exclude unless scalability becomes a central claim. Do not block P1 on it. | [[../execution/P2-tmlr-improvement-plan]], [[../execution/P3-topology-reconstructability-paper]] |
| Amazon Computers/Photo are non-citation homophilic datasets but have thin recovery gap. | P1 framing if valid; otherwise P2 rerun | Include only if results are valid. If included, frame as "limited recoverable gap." If current hyperparameters are invalid, park rerun to P2. | [[results_rewrite_notes]], [[../execution/P2-tmlr-improvement-plan]] |
| Heterophilic datasets show Zero-hop can match or beat Full. | P1 framing | Treat as a scope diagnostic: under the tested setup there may be no degradation to recover, and smoothness assumptions may be broken. | [[results_rewrite_notes]], [[../execution/P1-current-evidence-manuscript]] |
| Avoid saying the missing-neighbor problem does not exist in heterophilic settings. | P1 | Use the safer wording: the tested GCN/GAT setup does not show a recoverable Full-to-Zero-hop degradation on those datasets. | [[claims_and_language_pass]], [[results_rewrite_notes]] |
| L1 is the most natural assumption. | P1 | Make L1 the main contribution. State exactly what clients know and do not know. | [[../analysis/l1_l2_assumptions]] |
| L2 improves performance but may require extra topology knowledge. | P1 | Label L2 as extended-structure/oracle-topology unless setup communication is explicitly counted. Do not let L2 carry the unqualified communication claim. | [[../analysis/l1_l2_assumptions]], [[../analysis/communication_accounting]] |
| IID vs non-IID behavior is not always intuitive. | P2 | Explain that label skew and graph cut structure differ. In P2, report realized structural statistics rather than relying only on beta. | [[../execution/P2-tmlr-improvement-plan]] |
| PubMed beta choice differs because beta=1 harmed Full. | P1 disclosure; P2 analysis if needed | Document the chosen beta setting if it remains in the manuscript. Do not overgeneralize partition conclusions from it. | [[../writing/revision_map]], [[../execution/P1-current-evidence-manuscript]] |
| Should we rerun SOTA experiments or use literature? | P1/P2 decision | P1 uses careful literature positioning. P2 prioritizes FedGCN controlled rerun if feasible. FedGAT modification and FedSage+ rerun are not first-order. | [[../execution/P2-tmlr-improvement-plan]] |
| FedSage/FedSage+ partitioning differs from ours. | P1 | Do not present as same-protocol head-to-head. Use explicit protocol disclaimer or separate positioning table. | [[results_rewrite_notes]] |
| Possible next step 1: complete paper from current evidence only. | P1 | This is the active track. | [[../execution/P1-current-evidence-manuscript]], [[../execution]] |
| Possible next step 2: identify gaps and next scopes. | P1 exit / P2 entry | Fill the claim-evidence matrix after P1. | [[../execution/P1-to-P2-gap-assessment]] |
| Possible next step 3: decide what belongs to TMLR vs separate paper. | P1/P2/P3 | P1 and P2 are TMLR stages; P3 is the separate follow-up paper. | [[../execution/P2-tmlr-improvement-plan]], [[../execution/P3-topology-reconstructability-paper]] |

## P1 Action List from This Note

| Action | Output |
|---|---|
| Rewrite results around degradation recovery. | Updated results narrative and tables. |
| Qualify all communication claims. | Claims/language pass. |
| Clarify L1 and L2 assumptions. | Information-model edits. |
| Redraw Figure 2. | New process diagram. |
| Reframe Amazon and heterophilic results. | Scope-diagnostic subsection or appendix text. |
| Separate controlled results from literature positioning. | Cleaner comparison table/figure. |

## Parked for P2

- Focused reconstruction diagnostic.
- Realized partition graph statistics.
- Controlled FedGCN rerun if feasible.
- Client-count robustness if needed.
- Additional recovery/ablation analysis beyond existing results.

## Parked for P3

- Topology-driven theory of reconstructability.
- Broad heterophily/topology study.
- OGBN-Products or large-scale scalability if it becomes a separate contribution.
- Systematic partition sweeps and graph-structure explanations.
