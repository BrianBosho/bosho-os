---
title: FedProp Revision Checklist v4
type: writing-checklist
source: google-drive
drive-id: 14AfH7Diku00hLM3ERVsGu139JM96G5NMaqSPcez_Lb0
created: 2026-04-21
tags: [fedprop, tmlr, revision, writing]
project: tmlr_fedprop_paper
---

**FedProp — TMLR Revision Checklist**

*Version 4 (final)  |  Updated April 2026  |  Target: Transactions on Machine Learning Research*

**26 items across 4 phases**

**14 Must-have**  |  **4 Important**  |  **4 Polish**  |  **3 Admin**

**Experimental status**

**Done and in paper:**  Cora, Citeseer, Pubmed, OGBN-Arxiv

**Done, needs write-up:**  Amazon Computers, Amazon Photos (item 7)

**Still to run:**  One heterophilic result — Texas/Wisconsin or synthetic fallback (item 9)

**Still to decide:**  FedSage+ / FedDEP reproduction or positioning fallback (item 8)

> ⚡ **Do now, in parallel with everything else**
> **Item 23 — arXiv upload.** Post the current version to arXiv immediately to establish timestamp. Do not treat arXiv as a Phase 4 item.

> **Scope freeze:** No new datasets beyond the 6 already locked. No new theoretical directions beyond sharpening existing claims. No new baselines unless an existing item fails and its fallback activates.

## Phase 1 — Paper design

*Do this before touching experiments or prose. Lock identity and assumption model first.*

| # | Action required | Type | Priority | Status |
|---|---|---|---|---|
| **1** | Rewrite abstract, intro, and contributions as a coordinated reframing. FedProp's identity is: a communication-free federated GNN with local imputation, zero inter-client overhead, and a theory-backed tradeoff analysis. Remove language implying formal privacy guarantees, universal SOTA accuracy, or broad graph generality. | writing | **Must-have** | [ ] To do |
| **2** | Create a formal information model subsection. Use a table specifying what each client and the server knows under L=1 (strict) and L=2 (relaxed): local nodes, local edges, boundary incidence, remote features, remote-remote edges. | writing | **Must-have** | [ ] To do |
| **3** | Specify the graph used at each stage: (a) propagation graph; (b) training graph; (c) normalization. | writing | **Must-have** | [ ] To do |
| **4** | Reframe L=2 communication cost. Clarify that topology setup for L=2 is a one-time setup cost. | writing | **Must-have** | [ ] To do |
| **5** | Lock the 11-section paper structure before writing. | structure | **Must-have** | [ ] To do |
| **6** | Lock results table architecture before writing. | structure | **Must-have** | [ ] To do |

## Phase 2 — Experimental closure

| # | Action required | Type | Priority | Status |
|---|---|---|---|---|
| **7** | Write up Amazon Computers and Amazon Photos results into the main paper. | experiment | **Must-have** | [ ] To do |
| **8** | Add at least one strong missing-neighbor / generative baseline (FedSage+ preferred). *Fallback: strengthen same-protocol comparisons if reproduction fails.* | experiment | **Must-have** | [ ] To do |
| **9** | Run one heterophilic dataset experiment. Primary: Texas or Wisconsin. *Cutoff: 2 weeks. Fallback: synthetic heterophily stress test.* | experiment | **Must-have** | [ ] To do |
| **10** | Create a direct FedProp-GAT vs FedGAT comparison table in the main paper. | experiment | **Must-have** | [ ] To do |
| **11** | Address FedCog (arXiv 2301.11099) as a novelty positioning concern. Dedicated comparison paragraph or table. | writing | **Must-have** | [ ] To do |
| **12** | Add citations for arXiv 2401.04336 and arXiv 2408.16288. | new refs | **Important** | [ ] To do |

## Phase 3 — Paper revision

| # | Action required | Type | Priority | Status |
|---|---|---|---|---|
| **13** | Rewrite method section with cleaner assumption model. Formally introduce FedProp (Adj) and FedProp (Diff). Include Taylor series approximation for diffusion kernel. | writing | **Must-have** | [ ] To do |
| **14** | Tighten theory claims. Separate convergence from optimality. State exactly when fixed point equals Dirichlet solution. | writing | **Must-have** | [ ] To do |
| **15** | Write Discussion section built around three-part error decomposition: convergence error, boundary bias, irreducible heterophily error. | writing | **Must-have** | [ ] To do |
| **16** | Write reproducibility detail block in main paper. | writing | **Must-have** | [ ] To do |
| **17** | Rebuild results section around tradeoffs, not accuracy rankings. | writing | **Must-have** | [ ] To do |
| **18** | Write serious Limitations section. | writing | **Must-have** | [ ] To do |
| **19** | Replace 'strong privacy' language with precise terms: 'zero additional inter-client communication'. | writing | Polish | [ ] To do |
| **20** | Moderate abstract accuracy claim. '97–99% of centralized' is only true for IID. | writing | Polish | [ ] To do |
| **21** | Add sentence clarifying goal of imputation: task-useful reconstruction, not perfect recovery. | writing | Polish | [ ] To do |
| **22** | Remove unnecessary bold formatting. Fix reference citation style. | formatting | Polish | [ ] To do |

## Phase 4 — Release

| # | Action required | Type | Priority | Status |
|---|---|---|---|---|
| **23** | Upload full paper + appendix to arXiv. Start immediately. | admin | Admin | [ ] To do |
| **24** | Complete the TMLR reproducibility checklist on OpenReview. Release code. | admin | Admin | [ ] To do |
| **25** | Prepare 4–6 page workshop paper for FL@NeurIPS or graph learning workshop. | admin | Admin | [ ] To do |

## Minimum viable submission threshold

**Must-have before submitting:**
- Items 1–6: framing, information model, and table architecture locked
- Item 7: Amazon Computers and Photos written up
- Item 8: at least one generative baseline (or fallback activated)
- Item 9: heterophilic result or synthetic stress test
- Item 10: FedProp-GAT vs FedGAT comparison in main paper
- Item 11: FedCog novelty positioning resolved
- Items 13–18: method, theory, discussion, reproducibility, and limitations written
- Item 23: arXiv upload complete

> **Emergency submission rule:** If everything in the must-have list is complete *except* item 8, and the paper is otherwise strong, **do not delay indefinitely.** Submit with strengthened positioning and explicit statement that direct same-codebase comparison is future work.