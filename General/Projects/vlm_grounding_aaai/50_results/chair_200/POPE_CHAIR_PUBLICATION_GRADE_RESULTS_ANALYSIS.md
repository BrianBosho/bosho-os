# POPE + CHAIR Results and Analysis (Camera-Ready Draft)

**Date:** 2026-03-03  
**Companion documents:** `docs/GROUNDING_METHODOLOGY.md`, `docs/TECHNICAL_IMPLEMENTATION_REPORT.md`

This report is intentionally critical. Primary evidence is restricted to **POPE official 1K** and **CHAIR-200**. All other analyses are supplementary.

## 1. Primary Scope

- **Primary benchmark A:** POPE official adversarial 1K (binary object-presence QA)
- **Primary benchmark B:** CHAIR-200 (caption hallucination analysis)
- **Primary objective:** evaluate intrinsic grounding signals for discrimination quality, operating-point behavior, and reliability.

## 2. Key Claims and Evidence

| Claim | Evidence |
|---|---|
| C1. Causal intrinsic metrics are strongest on POPE-1K. | `causal_delta_logp_random` ROC-AUC 0.7667 (best single metric), with causal family occupying top ranks. |
| C2. POPE direct task performance is solid but not sufficient for confidence-critical use. | Task accuracy/F1 = 0.8300, but calibrated ECE = 0.1841 (moderate miscalibration). |
| C3. CHAIR headline hallucination rates overestimate true fabrication. | Manual audit: only 13/80 CHAIR flags (16.3%) are TRUE-HALL. |
| C4. CHAIR-aligned intrinsic detection is high-recall/low-precision. | Best operating point (`decision_jsd_tau0.1`): Recall 0.8689, Precision 0.1677, F1 0.2812. |
| C5. CHAIR should be used as diagnostic context, not sole hallucination ground truth. | 83.7% of CHAIR flags fall into GT-GAP/INFERENCE/MISID/SYNONYM categories. |

## 3. Primary Dataset Characterization

### 3.1 POPE official adversarial 1K

- N = 1000
- Label balance = 500 yes / 500 no
- Unique queried objects = 73
- Unique images = 167
- Canonical question template usage = 1000/1000

Critical caveat: repeated image reuse and fixed yes/no template reduce linguistic variance; external transfer to free-form generation remains unproven.

### 3.2 CHAIR-200

- N = 200 images
- Mentions = 419, CHAIR-flagged mentions = 88
- Sentences = 701, hallucinated sentences = 99

Critical caveat: CHAIR is sensitive to COCO annotation gaps and taxonomy boundary effects.

## 4. Primary Results A: POPE Official 1K

### 4.1 Direct yes/no classification

| Metric | Value |
|---|---:|
| Accuracy | 0.8300 |
| Precision | 0.8300 |
| Recall | 0.8300 |
| F1 | 0.8300 |
| Specificity | 0.8300 |
| Balanced Accuracy | 0.8300 |
| FPR / FNR | 0.1700 / 0.1700 |
| NPV | 0.8300 |
| MCC | 0.6600 |
| TP / FP / TN / FN | 415 / 85 / 415 / 85 |

### 4.2 Unified POPE-1K Score Table (Single Metrics + Composite + Calibration)

All rows below are sample-level POPE-1K scores.  
`Op-threshold` is the operating threshold used for the thresholded columns.

| Score | ROC-AUC | PR-AUC | Op-threshold | Accuracy | Precision | Recall | F1 | Specificity | MCC | TP/FP/TN/FN |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Direct model yes/no classifier | 0.8300* | 0.8300* | token mapping | 0.8300 | 0.8300 | 0.8300 | 0.8300 | 0.8300 | 0.6600 | 415/85/415/85 |
| Calibrated grounding confidence (OOF Platt) | 0.7658 | 0.6962 | `t*=0.5099` | 0.7650 | 0.7440 | 0.8080 | 0.7747 | 0.7220 | 0.5320 | 404/139/361/96 |
| `causal_delta_logp_random` (best single causal) | 0.7667 | 0.6972 | -0.0739 (BestF1) | 0.7640 | 0.7426 | 0.8080 | 0.7739 | 0.7200 | 0.5301 | 404/140/360/96 |
| `causal_delta_logp` | 0.7322 | 0.6778 | -0.0634 (BestF1) | 0.7300 | 0.7083 | 0.7820 | 0.7433 | 0.6780 | 0.4625 | 391/161/339/109 |
| `causal_delta_p` | 0.7310 | 0.6763 | -0.0497 (BestF1) | 0.7270 | 0.7098 | 0.7680 | 0.7378 | 0.6860 | 0.4555 | 384/157/343/116 |
| `causal_logp_cf` | 0.7215 | 0.7843 | -0.6403 (BestF1) | 0.5350 | 0.5193 | 0.9400 | 0.6690 | 0.1300 | 0.1194 | 470/435/65/30 |
| `causal_p_cf` | 0.7215 | 0.7843 | 0.5271 (BestF1) | 0.5350 | 0.5193 | 0.9400 | 0.6690 | 0.1300 | 0.1194 | 470/435/65/30 |
| `grid_weighted_3fam` (weights=[0,0,1]) | 0.7667 | — | — | — | — | — | — | — | — | — |
| `logreg_3fam_in_sample` | 0.7640 | — | — | — | — | — | — | — | — | — |
| `logreg_3fam_cv5` | 0.7557 | — | — | — | — | — | — | — | — | — |
| `equal_weight_3fam` | 0.6214 | — | — | — | — | — | — | — | — | — |
| `best_single_decision` (`decision_p_real`) | 0.6516 | 0.6305 | — | — | — | — | — | — | — | — |
| `best_single_state` (`state_delta_max`) | 0.5151 | 0.5052 | — | — | — | — | — | — | — | — |

\*For the direct yes/no classifier row, ROC-AUC/PR-AUC are shown as point-performance references from the balanced binary decision output, not threshold-sweep score AUCs.

Critical interpretation:
- Causal metrics still carry most discriminative signal among single intrinsic scores.
- `causal_logp_cf`/`causal_p_cf` achieve high recall but with very poor specificity at BestF1.
- Composite rows currently preserve archived AUC results; full threshold metrics for those composites are not stored in current artifacts.
- Calibration remains operationally useful but moderate in reliability (ECE 0.1841, Brier 0.2171).

### 4.3 Full Unified Threshold Table Artifact (All Requested POPE Scores)

To provide one table with thresholded metrics (accuracy/precision/recall/F1/etc.) for single and composite scores, we generated:

- `runs/pope_official_adversarial_1k_grounding/results_1k_eval/unified_score_threshold_metrics_1k.csv`
- `runs/pope_official_adversarial_1k_grounding/results_1k_eval/unified_score_threshold_metrics_1k.md`

## 5. Primary Results B: CHAIR-200

### 5.1 Corpus-level summary

| Metric | Value |
|---|---:|
| CHAIR_i | 0.2100 |
| CHAIR_s | 0.1412 |
| Cover | 0.5737 |
| Hallucinated mentions | 88 / 419 |
| Hallucinated sentences | 99 / 701 |

### 5.2 Intrinsic-to-CHAIR detection (top operating points)

| Metric | ROC-AUC | AP | Precision | Recall | F1 | TP | FP | FN | TN |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| decision_jsd_tau0.1 | 0.7482 | 0.2618 | 0.1677 | 0.8689 | 0.2812 | 53 | 263 | 8 | 328 |
| decision_concept_var | 0.7237 | 0.2496 | 0.1568 | 0.8689 | 0.2657 | 53 | 285 | 8 | 306 |
| causal_patch_var | 0.7146 | 0.2036 | 0.1564 | 0.8361 | 0.2636 | 51 | 275 | 10 | 316 |

Interpretation: excellent recall, poor precision; suitable for triage but not standalone adjudication.

### 5.3 Manual audit validity correction

Audit distribution over 80 CHAIR-flagged mentions:
- GT-GAP 22 (27.5%)
- INFERENCE 17 (21.3%)
- MISID 16 (20.0%)
- SYNONYM 12 (15.0%)
- TRUE-HALL 13 (16.3%)

Critical implication: raw CHAIR flags are mostly not pure fabrications; CHAIR must be paired with audit or alternative judges for valid prevalence claims.

## 6. Metric Semantics (Operational)

### 6.1 Confusion-matrix terms

- `TP`, `FP`, `TN`, `FN` as standard binary classification counts.

### 6.2 Core formulas

| Metric | Formula |
|---|---|
| Precision | `TP / (TP + FP)` |
| Recall | `TP / (TP + FN)` |
| Specificity | `TN / (TN + FP)` |
| F1 | `2PR / (P + R)` |
| Accuracy | `(TP + TN) / N` |
| Balanced Accuracy | `(Recall + Specificity) / 2` |
| FPR | `FP / (FP + TN)` |
| FNR | `FN / (FN + TP)` |
| NPV | `TN / (TN + FN)` |
| MCC | `(TP*TN - FP*FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN))` |

## 7. Primary Conclusions (Strict)

1. POPE-1K supports a defensible claim that causal intrinsic metrics are the strongest single-family grounding signals in this setup.
2. CHAIR headline hallucination rates are not valid direct estimates of true fabrication without audit correction.
3. Current calibrated score quality is moderate (ECE 0.1841), not yet high-calibration.
4. Best current practice: use intrinsic metrics for ranking/triage, combine CHAIR with audit-aware interpretation.

---

## Supplementary A: Secondary POPE-like Splits

| Benchmark | N | Positive rate | Precision | Recall | F1 | Accuracy | TP | FP | FN | TN |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| POPE-like Balanced 400 | 400 | 0.5000 | 0.9479 | 0.9100 | 0.9286 | 0.9300 | 182 | 10 | 18 | 190 |
| POPE-like More-Adv 800 | 800 | 0.2500 | 0.9010 | 0.9100 | 0.9055 | 0.9525 | 182 | 20 | 18 | 580 |

## Supplementary B: CHAIR + LLM Judge Experiments

### B.1 GPT-4o noun-judge benchmark

| Metric | Oriented AUC | AP | Direction |
|---|---:|---:|---|
| decision_jsd_tau0.1 | 0.6746 | 0.4502 | lower_absent |
| causal_patch_var | 0.6738 | 0.4570 | lower_absent |
| decision_align_gen | 0.6139 | 0.4099 | lower_absent |
| causal_delta_logp | 0.5865 | 0.3413 | lower_absent |

### B.2 Threshold example (`decision_jsd_tau0.1`, BestF1)

- Precision = 0.403
- Recall = 0.823
- F1 = 0.541
- TP/FP/TN/FN = 1477/2187/1876/317

## Supplementary C: Improvement Backlog (Prioritized)

1. Bootstrap CIs for all primary metrics.
2. Reliability diagrams and calibration tables.
3. Full PR/ROC curves with threshold sweeps.
4. Cost-sensitive decision analysis (FP/FN utility weights).
5. Per-object/per-frequency error slices on POPE.
6. Formal CHAIR uncertainty decomposition (annotation vs model).
7. Dual-annotator audit and agreement metrics.
8. Statistical tests for AUC gaps (e.g., DeLong).
9. Prompt/decoding robustness checks.
10. Failure-case atlas with metric-linked exemplars.
11. Cross-split calibration transfer tests.
12. Confidence-based abstention/coverage analysis.
13. Mention-pooling ablations (mean/max/quantile).
14. CHAIR vs LLM-judge disagreement matrix.
15. External benchmark triangulation beyond COCO/POPE.