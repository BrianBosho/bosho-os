---
type: project-execution
status: active
project: tmlr_fedprop_paper
tags: [project, execution, fedprop]
---

# TMLR FedProp Paper Execution

Project brief: [[tmlr_fedprop_paper]]

## Purpose

Current execution control surface for FedProp. This page tracks active deliverables and priority sequencing only. It is not the full backlog, and it should not duplicate the raw notes in [[Unprocessed]].

## Current State

| Field               | Status                                                                                                   |
| ------------------- | -------------------------------------------------------------------------------------------------------- |
| Stage               | P1 manuscript revision                                                                                   |
| Scope decision      | P1 only: reorganize and rewrite using existing evidence; no new experiments                              |
| Project status      | Active                                                                                                   |
| Priority            | Manuscript coherence before result expansion                                                             |
| Deadline            | None fixed; TMLR resubmission when P1 is complete and reviewed                                           |
| Current focus       | Reorganize and rewrite Section 6 around the P1 recovery-results spine                                    |
| Current next action | Revise Section 6 first: start from [[writing/Section 6]] and build the core GCN recovery table/narrative |

## Scope Boundary: P1 Core Claims

The paper must establish exactly four things. Everything else either supports these or moves to appendix, P2, or P3.

1. Partitioning harms GNN performance because clients lose cross-client neighbor features.
2. FedProp recovers a substantial portion of that lost performance.
3. This recovery requires no additional node-feature or embedding communication beyond FedAvg.
4. The method works with both GCN and GAT.

## Stage Files

| File | Role | Status |
|---|---|---|
| [[execution/P1-current-evidence-manuscript]] | Active P1 checklist and scope boundary | Active |
| [[execution/P2-tmlr-improvement-plan]] | Parked bounded additions for the same TMLR paper | Parked |
| [[execution/P3-topology-reconstructability-paper]] | Parked separate follow-up paper | Parked |
| [[execution/P1-to-P2-gap-assessment]] | Claim-evidence matrix to fill after P1 | Not started |

## Active Deliverables - P1

| Deliverable | Status | Target | Notes / link |
|---|---|---|---|
| Section 6 revision | Active - next task | Now | Reorganize and rewrite the results section around the P1 recovery spine. Start from [[writing/Section 6]]. |
| Revision map | Active | This week | Section-by-section audit: weak, missing, stale, inconsistent, or unsupported material. Output: [[writing/revision_map]]. |
| Processed results-note map | Complete | This week | Raw [[Unprocessed/Result section Notes]] concerns mapped into P1/P2/P3. Output: [[writing/result_section_notes_processed]]. |
| Section 6 rewrite plan | Active | Now | Reorganized P1 results-section blueprint. Output: [[writing/Section 6]]. |
| Figure 2 redraw spec | Pending | This week | Four-stage information-flow figure. Output: [[writing/figure_2_redraw_spec]]. |
| Recovery metrics rewrite | Pending | This week | Results should report loss, gain, and Recovery% where meaningful. Output: [[analysis/recovery_metrics]]. |
| L1/L2 and communication claim pass | Pending | This week | Qualify assumptions and replace broad "communication-free" language. Outputs: [[analysis/l1_l2_assumptions]], [[analysis/communication_accounting]]. |
| Amazon / heterophilic reframe | Pending | This week | Treat as scope diagnostics or appendix material, not core positive-results narrative. |
| Weak-claims inventory | Pending | After P1 edits | Unsupported claims after P1 become input to [[execution/P1-to-P2-gap-assessment]]. |
| Review packet | Pending | After revision map | Manuscript, open questions, result status, and feedback request for Carlee/Joao. Output: [[writing/review_packet]]. |

## Pending Work Areas

| Work area | Status | Output |
|---|---|---|
| Draft audit | Active | Section-level revision map. |
| Feedback merge | Pending | One combined issue list from prior ICC/AAAI/TMLR feedback. |
| Results validation | Pending | P1 result inventory: keep, exclude, appendix, or P2. |
| Writing integration | Active | Section 6 rewrite first; then assumptions, limitations, and review packet. |
| Collaborator review | Pending | Review packet and targeted questions. |

## Parked Work - Not P1

| Work | Destination | Reason parked |
|---|---|---|
| New reconstruction diagnostics | [[execution/P2-tmlr-improvement-plan]] | Useful but not needed to make the current-evidence manuscript coherent. |
| Realized graph statistics for every partition | [[execution/P2-tmlr-improvement-plan]] | Strong addition, but can wait until P1 gap assessment. |
| Controlled FedGCN rerun | [[execution/P2-tmlr-improvement-plan]] | High-value comparison, but not part of current no-new-experiments P1. |
| Topology/reconstructability theory and broad empirical study | [[execution/P3-topology-reconstructability-paper]] | Separate research question. |

## Selected Actions

Next task: revise Section 6. Start with the core GCN recovery table and narrative, then handle GAT, communication positioning, ablations, and scope diagnostics in that order.

Pull only 3-5 FedProp tasks at a time from the active P1 deliverables above.

## Completed

| Date | Completed | Output / link |
|---|---|---|
| 2026-06-16 | Consolidated project task sources into execution model | Initial [[execution]] page |
| 2026-06-16 | Split planning into P1/P2/P3 execution files without deleting raw Unprocessed notes | P1 active; P2/P3 parked |
| 2026-06-16 | Processed Result section Notes into a concern-resolution map | [[writing/result_section_notes_processed]] created | Use it to fill revision map |
| 2026-06-16 | Reorganized Section 6 plan around recovery-first P1 results structure | [[writing/Section 6]] rewritten | Build core GCN recovery table and narrative |

## Blocked / Waiting

| Item | Blocker | Unblock action |
|---|---|---|
| Latest manuscript state | Need full section-by-section audit of current PDF/manuscript | Create [[writing/revision_map]]. |
| Figure 2 | Requires illustration or LaTeX work | Start from [[writing/figure_2_redraw_spec]]. |
| P2/P3 temptation | Interesting open questions can expand scope | Park them in stage files; do not start until P1 is complete. |

## Activity Log

| Date | Activity | Result | Next |
|---|---|---|---|
| 2026-06-16 | Consolidated project task sources into execution model | FedProp has current-state execution page | Start revision map |
| 2026-06-16 | Split planning into P1/P2/P3 execution files without deleting raw Unprocessed notes | P1 active; P2/P3 parked | Fill revision map |

## Source Material

- [[FedProp Publication Push]]
- [[Unprocessed/3 Step Approach]]
- [[Unprocessed/Minimal scope]]
- [[Unprocessed/Result section Notes]]
- [[writing/result_section_notes_processed]]
- [[writing/Section 6]]
- [[Unprocessed/Review 1]]
- [[writing/revision_checklist_v4]]
- [[archive]]
