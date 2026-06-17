# POPE 1K Grounding Report

## Experiment Summary
- Dataset: POPE official adversarial 1K (1,000 questions)
- Run chunks: `pope_official_adv_1k_chunk01` ... `chunk05`
- Label balance: 500 `yes`, 500 `no`
- Aggregation unit for AUC: one row per sample (1,000 rows)

## Grounding Score Definition (Canonical)
- Target event for grounding confidence: `grounding_confidence = P(not hallucinated | s)`
- Raw score used for detection: `raw_grounding_score = causal_delta_logp_random`
- Since this metric is `lower=>yes` (more grounded), use oriented risk score: `risk_raw = +causal_delta_logp_random`
- Reporting rule: use one scalar per sample for ranking, thresholding, and coverage analyses.

## Model Classification Performance (POPE 1K)
- Token IDs observed: [1939, 3869]
- Inferred yes token ID: `3869`
- **Accuracy: 0.8300**
- Precision: 0.8300
- Recall: 0.8300
- F1: 0.8300
- Specificity: 0.8300
- Balanced Accuracy: 0.8300
- Confusion Matrix: TP=415 FP=85 TN=415 FN=85

## State Grounding: ROC-AUC by Metric
| metric | roc_auc | pr_auc | orientation |
| --- | --- | --- | --- |
| state_delta_max | 0.5151 | 0.5052 | lower=>yes |
| state_delta_mean | 0.5071 | 0.5016 | lower=>yes |
| state_delta_min | 0.5067 | 0.5114 | higher=>yes |
| state_delta_entropy_tau01 | 0.5064 | 0.5070 | higher=>yes |
| state_delta_std | 0.5031 | 0.5011 | lower=>yes |
| state_delta_var | 0.5031 | 0.5011 | lower=>yes |
| state_caption_score | 0.5000 | 0.5000 | higher=>yes |

## Decision Grounding: ROC-AUC by Metric
| metric | roc_auc | pr_auc | orientation |
| --- | --- | --- | --- |
| decision_p_real | 0.6516 | 0.6305 | higher=>yes |
| decision_rank_null | 0.6480 | 0.6693 | higher=>yes |
| decision_align_gen | 0.6463 | 0.6230 | higher=>yes |
| decision_p_null | 0.6319 | 0.6642 | higher=>yes |
| decision_jsd_tau01 | 0.5589 | 0.5507 | higher=>yes |
| decision_delta_p | 0.5531 | 0.5478 | lower=>yes |
| decision_rank_real | 0.5003 | 0.4824 | higher=>yes |

## Causal Grounding: ROC-AUC by Metric
| metric                    | roc_auc | pr_auc | orientation |
| ------------------------- | ------- | ------ | ----------- |
| causal_delta_logp_random  | 0.7667  | 0.6972 | lower=>yes  |
| causal_delta_logp         | 0.7322  | 0.6778 | lower=>yes  |
| causal_delta_p            | 0.7310  | 0.6763 | lower=>yes  |
| causal_p_cf               | 0.7215  | 0.7843 | higher=>yes |
| causal_logp_cf            | 0.7215  | 0.7843 | higher=>yes |
| causal_mask_size          | 0.6683  | 0.6786 | lower=>yes  |
| causal_rel_drop           | 0.6546  | 0.6304 | lower=>yes  |
| causal_p_real             | 0.6493  | 0.7201 | higher=>yes |
| causal_specificity_margin | 0.5833  | 0.5397 | higher=>yes |

## Composite Metric Exploration
- Family representatives: State `state_delta_max` (0.5151), Decision `decision_p_real` (0.6516), Causal `causal_delta_logp_random` (0.7667)

| model | auc | details |
| --- | --- | --- |
| best_single_causal | 0.7667 | causal_delta_logp_random |
| grid_weighted_3fam | 0.7667 | weights=[0.0, 0.0, 1.0] |
| logreg_3fam_in_sample | 0.7640 | 3-family logistic regression |
| logreg_3fam_cv5 | 0.7557 | cross-validated (most realistic) |
| best_single_decision | 0.6516 | decision_p_real |
| equal_weight_3fam | 0.6214 | mean(z_state,z_decision,z_causal) |
| best_single_state | 0.5151 | state_delta_max |

## Implemented Calibration (One Score Per Sample)
- Raw score: `grounding_score_raw = -causal_delta_logp_random` (higher = more grounded)
- Calibrated score: `grounding_confidence = P(not_hallucinated | grounding_score_raw)` using Platt scaling with 5-fold OOF calibration.
- OOF quality:
  - ROC-AUC: `0.7658`
  - PR-AUC: `0.6962`
  - Brier: `0.2171`
  - ECE (10-bin): `0.1841`
- Threshold metrics (`t*` selected by `max_f1` on OOF):
  - `t* = 0.5099`
  - Accuracy 0.7650, Precision 0.7440, Recall 0.8080, F1 0.7747, Specificity 0.7220
  - Confusion: TP=404 FP=139 TN=361 FN=96

## Interpretation
- Causal metrics dominate top single-metric AUC on this 1K set.
- Decision and state metrics are weaker individually, but can add signal in composites.
- `logreg_3fam_cv5` is the most realistic composite estimate (cross-validated).
- Best practical single-score choice on this run is still `causal_delta_logp_random`.

## Metrics To Publish (Final Package)
| category | metric(s) | purpose |
| --- | --- | --- |
| discrimination | ROC-AUC (primary), PR-AUC (secondary) | ranking quality of grounding signal |
| thresholded performance | Accuracy, Precision, Recall, F1, Specificity | operating-point quality |
| calibration | ECE, Brier, reliability diagram | probability correctness |
| selective prediction | coverage vs. performance at confidence thresholds | abstention/triage behavior |