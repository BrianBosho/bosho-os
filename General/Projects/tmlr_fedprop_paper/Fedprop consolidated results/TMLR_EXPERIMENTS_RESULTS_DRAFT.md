# Experiments and Results — TMLR Draft (v2)

Status: working draft (2026-06-13), aligned to "FedProp — Experiments & Results:
Organization Plan + Template.md" and to the current manuscript (`tmlr (1).pdf`, §6).
Numbering follows the manuscript (Section 6), not the plan's 7.x.
`‹status›` tags are working notes — delete before submission. Numbers come from
`paper_ready_results.csv` / the manuscript tables; [TODO] marks pending work.

**Plan amendments adopted** (vs. the organization plan as written):
1. Keep manuscript §6 numbering.
2. Minesweeper: accuracy is pinned at the 80% majority-class rate for every method —
   add ROC-AUC or drop from Table 8 (plan is silent; "neutral" framing is not safe).
3. Error-decomposition empirics (plan §7.8): qualitative in the Discussion until
   Term-1/2/3 instrumentation exists; not a submission blocker.
4. Amazon Computers/Photos: appendix-only until R7 hop-1 + width-matched PE runs land.

**Hard rules in force** (audit every table/caption):
- β=10,000 = IID; β=10 = non-IID (primary). Arxiv non-IID uses β=1 (state it).
- FedGCN/FedGAT non-IID numbers are β=1 → mismatch disclaimer in §6.3 caption.
- FedGCN numbers attributed to Ambekar et al. (FedGAT paper), not the original.
- PE variants never in main tables → Appendix F.
- FedSage+/FedDEP never in the main accuracy table → Appendix E + family disclaimer.
- GapClosed defined once (§6.3) with the selection-bias caveat; clip at 100%.

---

## 6 Experiments and Results

Core claims the section must establish:
**C1 Recovery** — local propagation recovers most of the missing-neighbor gap.
**C2 Efficiency** — at zero additional inter-client communication.
**C3 Backbone-agnosticism** — gains transfer GCN → GAT.
**C4 Honest failure mode** — degrades under heterophily as the irreducible-error term predicts.

### 6.1 Experimental Protocol  ‹condensed; exhaustive tables → Appendix B–C›

**Datasets.**

| Dataset | \|V\| | \|E\| | Feat | Classes | Regime | Role |
|---|---|---|---|---|---|---|
| Cora | 2,708 | 5,429 | 1,433 | 7 | Homophilic | Main |
| Citeseer | 3,327 | 4,732 | 3,703 | 6 | Homophilic | Main |
| Pubmed | 19,717 | 44,338 | 500 | 3 | Homophilic | Main |
| OGBN-Arxiv | 169,343 | 1,166,243 | 128 | 40 | Homophilic | Large-scale main |
| Texas | 183 | 295 | 1,703 | 5 | Heterophilic | Limitation study |
| Wisconsin | 251 | 466 | 1,703 | 5 | Heterophilic | Limitation study |
| Amazon-ratings | 24,492 | 93,050 | 300 | 5 | Heterophilic (partial) | Limitation study |

‹Amazon-ratings row: verify stats; Computers/Photos appear only in Appendix until R7.›

**Partitioning.** Label-Dirichlet over K=10 clients; β=10,000 (IID) and β=10
(primary non-IID); β=1 only for OGBN-Arxiv non-IID and the partition-severity ablation.
Transductive splits; boundary-node induction per §3.

**Information model.** Strict L=1: local nodes/features/edges + boundary incidence to
one-hop remote placeholders; no remote features, labels, or remote-remote edges.
L=2 is an accessibility ablation (Appendix).

**Variants and references.** FedProp-Adj (normalized adjacency), FedProp-Diff
(diffusion, h=0.1), Tprop=50 with boundary reset; FedProp-Zero (no imputation, lower
reference), FedProp-Full (oracle feature access), Centralized. Communication baselines:
FedGCN, FedGAT, DistGAT (same-protocol family where compatible); FedSage+/FedDEP only
in Appendix E.

**Reproducibility block** ‹main text — do not move›:
GCN 2-layer hidden 16 (Planetoid), hidden 32 (Texas/Wisconsin), 3-layer hidden 256
(OGBN-Arxiv); GAT 2-layer 8×8 heads. Dropout 0.5 (0.6 GAT). [TODO: optimizer/lr per
dataset group — verify against configs; Amazon reruns use Adam lr=0.01, wd=5e-4,
hidden 64.] One local epoch per round, synchronous FedAvg, early stopping patience 10.
10 seeds. Full tables Appendix B–C.

### 6.2 The Accuracy–Communication Tradeoff  ‹LEAD — C2›

[Figure 1: communication-regime positioning — x groups methods into {FedAvg-only,
one-time setup, per-round exchange}, y = accuracy; Cora (β=1) and OGBN-Arxiv (β=1)
panels. Already Figure 3 in the manuscript. ‹✅ written›]

[Table 2: per-round and total inter-client bytes per method + Recovery%.
‹✍️ TODO: numbers from `src/communication_cost_analysis.py` /
`notebooks/comm_vs_accuracy.ipynb`; FedGraph logs for baselines›]

Anchor numbers (manuscript §6.2): Cora — Centralized 80.69, FedProp-Adj 76.56
(FedAvg-only regime) vs BDS-GCN 75.98 (per-round), FedGCN 81.00 (one-time setup),
FedSage+ 80.26 (per-round). OGBN-Arxiv — FedProp-Adj 71.64 *beats* Centralized 70.00,
FedGCN 71.01, BDS-GCN 67.69, FedSage+ 70.53. Protocol-mismatch caveat stays
(positioning comparison, not controlled benchmark).

### 6.3 Main GCN Results: Accuracy and Gap Recovery  ‹C1›

Define once: GapClosed = (Acc_FedProp − Acc_Zero)/(Acc_Full − Acc_Zero) × 100%,
clipped at 100%; caveat: computed for the best no-PE variant per cell (selection bias).

**Table 1a — GCN, IID (β=10,000), no-PE, best accessible-hop. + Recovery% column.**

| Method | Cora | Citeseer | Pubmed | OGBN-Arxiv |
|---|---|---|---|---|
| Centralized GCN | 80.69 ± 0.65 | 69.14 ± 0.51 | 78.50 | 70.00 ± 0.82 |
| FedProp-Full | 80.96 ± 0.63 | 69.73 ± 0.47 | 77.94 ± 1.17 | 70.35 ± 0.81 |
| FedProp-Zero | 62.02 ± 1.70 | 58.78 ± 2.60 | 73.76 ± 1.15 | 59.38 ± 0.31 |
| FedProp-Adj | 74.77 ± 0.60 | 65.83 ± 0.55 | **80.20 ± 0.53** | **67.81 ± 0.60** |
| FedProp-Diff | **75.08 ± 0.81** | **66.90 ± 0.17** | 79.80 ± 0.87 | 67.52 ± 1.80 |
| FedGCN 1-hop | 80.09 ± 0.77 | 69.30 ± 0.69 | 77.40 ± 0.20 | 70.04 ± 0.31 |
| *Recovery%* | *69* | *74* | *100 (clipped)* | *85* |

**Table 1b — GCN, non-IID (β=10; Arxiv β=1), no-PE. + Recovery% column.**

| Method | Cora | Citeseer | Pubmed | OGBN-Arxiv |
|---|---|---|---|---|
| Centralized GCN | 80.69 ± 0.65 | 69.14 ± 0.51 | 78.50 | 70.00 ± 0.82 |
| FedProp-Full | 80.19 ± 0.67 | 69.77 ± 0.79 | 77.98 ± 0.92 | 71.14 ± 0.56 |
| FedProp-Zero | 61.73 ± 2.14 | 58.12 ± 1.93 | 74.47 ± 0.75 | 64.77 ± 0.15 |
| FedProp-Adj | **73.36 ± 1.29** | **63.44 ± 1.09** | **77.85 ± 1.38** | 71.64 ± 0.83 |
| FedProp-Diff | 71.29 ± 1.40 | 62.85 ± 1.43 | 75.97 ± 0.47 | **72.14 ± 0.52** |
| FedGCN 1-hop | 81.00 ± 0.66 | 70.06 ± 0.71 | 77.20 ± 0.30 | 71.01 ± 0.78 |
| *Recovery%* | *63* | *46* | *100 (clipped)* | *100 (clipped)* |

Caption disclaimers (mandatory): FedGCN non-IID numbers are reported at β=1 (β=10 not
available in the source) → communication-based reference, not a matched baseline;
FedGCN numbers from Ambekar et al.

**Narrative.** FedProp improves over Zero-hop in every cell (C1). Pubmed and Arxiv
non-IID exceed the oracle reference — interpret conservatively (finite-run variation +
propagation acting as regularization), never as "beats the upper bound." Recovery%
ranges 46–100; Citeseer non-IID (46%) is the honest low end (sparse graph). On Arxiv,
FedProp-Diff (72.14) beats FedProp-Full (71.14) and FedGCN (71.01) — state with the
same conservative framing.

### 6.4 Backbone-Agnosticity: GAT Results  ‹C3›

**Table 3 — GAT (2-layer, 8×8 heads), Planetoid, IID / non-IID, no-PE.**

| Method | Cora IID | Cora non-IID | Citeseer IID | Citeseer non-IID | Pubmed IID | Pubmed non-IID |
|---|---|---|---|---|---|---|
| Centralized GAT | 83.00 | 83.00 | 72.60 | 72.60 | 79.00 | 79.00 |
| FedProp-GAT-Full | 81.18 ± 0.81 | 81.03 ± 0.69 | 68.30 ± 0.94 | 69.23 ± 0.87 | 78.32 ± 0.45 | 71.19 ± 1.91 |
| FedProp-GAT-Zero | 61.30 ± 0.81 | 67.17 ± 0.76 | 57.10 ± 1.63 | 60.04 ± 0.86 | 64.35 ± 1.20 | 63.89 ± 2.27 |
| FedProp-GAT-Adj | **74.53 ± 2.36** | **80.18 ± 0.79** | **65.50 ± 1.78** | **68.00 ± 1.07** | **79.36 ± 0.63** | **71.94 ± 0.42** |
| FedProp-GAT-Diff | 70.42 ± 1.11 | 76.88 ± 1.17 | 61.78 ± 1.89 | 63.78 ± 1.88 | 75.59 ± 1.20 | 71.32 ± 2.56 |
| DistGAT | 64.50 ± 1.20 | 68.40 ± 1.30 | 63.50 ± 0.70 | 66.40 ± 1.40 | 74.50 ± 0.90 | 76.90 ± 1.00 |
| FedGAT | 80.20 ± 0.30 | 80.00 ± 0.50 | 69.40 ± 0.60 | 69.90 ± 0.40 | 78.70 ± 0.50 | 78.90 ± 0.40 |

**Narrative.** Same propagation step, attention backbone, same pattern: +13–15 points
over Zero (Cora), Cora non-IID essentially matches FedGAT (80.18 vs 80.00) at FedAvg
communication. Pubmed non-IID stays below FedGAT — say so plainly; the claim is
backbone-agnostic *recovery*, not raw-accuracy dominance.

### 6.5 Robustness: Partition Severity and Scale  ‹C1, C2 — plan §7.5›

[Figure 2: accuracy vs β (Planetoid sweep over β ∈ {1, 10, 100?, 10000}).
‹✅ per plan — locate/regenerate from `result_report_utils.py`›]
[Figure 3: gap-closed bars, fixed 3 conditions per dataset — β=10 non-IID L=1,
β=10,000 IID L=1, β=10,000 IID L=2; Arxiv substitutes β=1 non-IID L=1.
‹✅ data in `performance_gap_closed/`›]

**Narrative.** Gains persist across the severity sweep; the gap to Full widens as β
drops but FedProp's delta over Zero stays positive throughout (every homophilic
condition we ran). Scale: the Arxiv columns of Tables 1a/1b carry the scale story;
[optional ⏳: >20-client Amazon scale study — only if R7 supports it].

### 6.6 Failure Mode: Heterophilic Graphs  ‹C4›

No GapClosed here — under heterophily FedProp-Full is a *feature-access* reference,
not a performance upper bound (it loses to Zero-hop by 12–31 points on
Texas/Wisconsin/Roman-empire). Report ∆Zero = Acc(best FedProp) − Acc(Zero-hop).

**Table 4 — Heterophilic stress tests, GCN, strict L=1.**

| Dataset | Partition | Zero-hop | FedProp-Adj | FedProp-Diff | ∆Zero | Full |
|---|---|---|---|---|---|---|
| Amazon-ratings | IID | 37.51 ± 1.79 | 40.21 ± 0.35 | 40.06 ± 0.42 | +2.70 | 43.27 ± 0.48 |
| Amazon-ratings | non-IID | 35.85 ± 2.40 | 38.84 ± 0.36 | 38.66 ± 0.49 | +3.00 | 41.16 ± 0.46 |
| Roman-empire | IID | 55.71 ± 0.33 | 54.25 ± 0.34 | 54.93 ± 0.37 | −0.77 | 36.10 ± 0.60 |
| Roman-empire | non-IID | 54.81 ± 0.52 | 53.22 ± 0.44 | 53.92 ± 0.35 | −0.89 | 34.48 ± 0.33 |
| Texas | IID | 75.83 ± 0.64 | 72.97 ± 5.02 | 79.46 ± 2.22 | +3.63 | 64.30 ± 3.20 |
| Texas | non-IID | 72.43 ± 1.11 | 74.46 ± 2.05 | 74.86 ± 1.27 | +2.43 | 62.16 ± 3.51 |
| Wisconsin | IID | 70.00 ± 1.12 | 70.69 ± 1.19 | 72.75 ± 1.41 | +2.75 | 48.73 ± 2.32 |
| Wisconsin | non-IID | 75.88 ± 1.29 | 74.71 ± 2.00 | 77.84 ± 1.44 | +1.96 | 44.61 ± 2.28 |

‹Minesweeper REMOVED from this table pending ROC-AUC rerun: every method sits at the
80% majority-class rate, so accuracy carries no information. Re-add with AUC (Platonov
protocol) or leave out. The manuscript currently includes it as "neutral" — change this.›

**Narrative (keep the manuscript's framing — it is the right one).** Three regimes:
(i) partial heterophily (Amazon-ratings) — propagation still helps, modestly;
(ii) intermediate (Texas/Wisconsin) — FedProp-Diff helps even though Full is harmful:
the smoothing/interpolation effect is useful while raw neighbor access is not. Note
the operator asymmetry: Adj can dip below Zero (Texas IID −2.85) while Diff never
does — adjacency injects raw 1-hop dissimilar-neighbor noise, diffusion dampens it;
(iii) extreme heterophily (Roman-empire) — the explicit failure case, exactly where
the irreducible heterophily term predicts smooth propagation cannot help (Full itself
loses ~20 points to Zero). This is C4 evidence, not a result to hide.

### 6.7 Ablations and Extended Results  ‹support›

- **Convergence.** Dirichlet residual ‖LX‖²_F stabilizes by ~40 iterations
  (Figure 5 in manuscript ‹✅›); propagation <1% of training time → justifies Tprop=50.
- **Operator choice.** Adj vs Diff summary across regimes (homophilic: roughly tied,
  Adj better at hop-1/Pubmed; heterophilic: Diff strictly safer — cf. §6.6).
- **Propagation depth / L=1 vs L=2.** Pointer to Appendix (L=2 exposes richer
  topology, stronger setup assumption — never conflate with the L=1 claim).
- **PE.** One sentence: RFP encodings sometimes help but are high-variance →
  Appendix F. ‹Numbers exist: +3.2 Cora / +2.0 Pubmed / +1.8 Citeseer mean paired
  gain, but −3.6 on Arxiv where PE width (1088) is 8.5× the 128-dim features.›

### (Discussion §7 hook — plan §7.8, qualitative)  ‹amendment 3›
Tie the three regimes of Table 4 to the error decomposition (Term 1 shown small by the
convergence ablation; Term 2 boundary bias; Term 3 irreducible heterophily). Measured
Term-1/2/3 instrumentation is future work — do not promise numbers we don't log.

---

## Appendix plan (A–H, per the organization plan)

| § | Contents | Source | Status |
|---|---|---|---|
| A | Full proofs (convergence; error decomposition) | manuscript | ✅ |
| B | Full hyperparameters per dataset | configs + Table 3 of manuscript | ✍️ |
| C | Exact Dirichlet partition procedure (β, seeds, client counts, boundary induction) | configs / `partitioning.py` | ✍️ |
| D | Per-seed results and std-devs (incl. multi-seed centralized) | `raw_runs_index.csv` | ⏳ multi-seed centralized runs |
| E | Cross-protocol-family comparison (FedSage+/FedDEP, Louvain + inductive) + family disclaimer | literature + ⏳ FedSage+ run | ⏳ |
| F | Full operator ablation + PE variants (flag high variance; include Arxiv PE negative result + width explanation; width-matched retry pe_r=16, pe_P=7) | `table_pe_ablation_*.csv` | ✍️ (+⏳ retry) |
| G | Propagation overhead timing | run telemetry (`training_time_s`, `loader_timing_sink_sec`) | ✍️ |
| H | Imputation quality (MSE, cosine) | companion JSON instrumentation | ⏳ |
| — | Extended datasets: Amazon Computers/Photos | `results/R7` (hop-1 + PE pending) | ⏳ |
| — | L=2 accessibility ablation | hop-2 rows of `paper_ready_results.csv` | ✍️ |
| — | Minesweeper with ROC-AUC | ⏳ rerun (see PUBLICATION_REVIEW.md §6) | ⏳ |

## Pre-submission checklist (from the plan, amended)

- [ ] Tradeoff figure first, accuracy table second.
- [ ] Recovery% column in Tables 1a/1b and Table 2.
- [ ] Every β label audited (10,000=IID; 10=non-IID; Arxiv non-IID=1, stated).
- [ ] β-mismatch + FedGCN-attribution disclaimers in §6.3 captions.
- [ ] PE out of main; Appendix F includes the Arxiv negative result + explanation.
- [ ] FedSage+/FedDEP only in Appendix E with family disclaimer.
- [ ] Reproducibility block in §6.1 main text.
- [ ] GapClosed selection-bias caveat stated once.
- [ ] Minesweeper: AUC added or dataset removed from Table 4.
- [ ] All "Appendix ??" cross-references in the manuscript resolved (currently broken).
- [ ] Amazon Computers/Photos: appendix-only unless R7 changes the story.
