# Stage B/C/D Rigorous Ablation Results Analysis

> Auto-generated from `scripts/build_stage_bcd_ablation_report.py`.
> Sources: `stage_b_comparison/`, `stage_cd_sweep/`, and `stage_c_kernel_sweep/`.

## Scope

- Stage B spaces: `B2_S0_raw`, `B2_S1_all`, `B2_S1_bal`.
- Stage C kernels: `K0_cosine`, `K1_dot`, `K2_l2neg`, `K3_bilinear_drift`.
- Stage D state reductions now cover `var`, `std`, `max`, `range`, `kurtosis`, `pos_mass`, entropy/effective-rank, `l1`, and `l2` across all four kernels.
- Primary ranking targets: `hallucinated_yes` first, then `is_correct`. `within_yes` and `within_no` are secondary diagnostics.

## Executive Summary

- Across the full 12-way kernel-space matrix, the strongest `hallucinated_yes` result is **0.8871** from `dot + B2_S0_raw` using `dec_dp_x_cvar`.
- Across the full 12-way kernel-space matrix, the strongest `is_correct` result is **0.7762** from `l2neg + B2_S1_all` using `cau_logp_cf`.
- Raw wins the primary `hallucinated_yes` target in **4/4** kernels.
- Whitening never beats raw on the main hallucination target. Its gains show up on secondary targets (`within_yes`, `within_no`) and in one narrow `is_correct` case under `l2neg + S1_all`.
- Decision interactions dominate the strongest hallucination detectors under raw, while causal metrics dominate `is_correct` across most kernels and spaces.

## Stage B Space-Only Freeze

| Condition | HY Best Metric | HY Best AUC | HY Top-15 Mean | IC Best Metric | IC Best AUC | IC Top-15 Mean | WY Best Metric | WY Best AUC | WN Best Metric | WN Best AUC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B2_S0_raw | `dec_dp_x_cvar` | 0.8851 | 0.8137 | `cau_p_real` | 0.7738 | 0.6648 | `cau_logp_real` | 0.8241 | `dec_abs_delta_p` | 0.7179 |
| B2_S1_all | `cau_logp_real` | 0.7574 | 0.7173 | `cau_logp_real` | 0.7738 | 0.6809 | `cau_p_real` | 0.8241 | `cau_p_cf` | 0.7162 |
| B2_S1_bal | `cau_rd_x_pvar` | 0.8225 | 0.7922 | `cau_p_real` | 0.7738 | 0.6593 | `cau_logp_real` | 0.8241 | `dec_align_gen` | 0.8137 |

Interpretation:

- Stage B still freezes on `B2_S0_raw` because it wins the primary `hallucinated_yes` target (`0.8851`) and no whitening variant exceeds it.
- `B2_S1_bal` is the best whitening variant and is the only clear winner on `within_no` (`0.8137`).
- `B2_S1_all` improves some Top-15 means but does not convert that into a better primary-target best metric.

## End-to-End Kernel x Space Results

| Kernel | Condition | HY Metric | HY AUC | IC Metric | IC AUC | WY Metric | WY AUC | WN Metric | WN AUC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cosine | B2_S0_raw | `dec_dp_x_cvar` | 0.8851 | `cau_p_real` | 0.7738 | `cau_p_real` | 0.8241 | `dec_delta_p` | 0.7179 |
| cosine | B2_S1_all | `cau_logp_real` | 0.7574 | `cau_p_real` | 0.7738 | `cau_logp_real` | 0.8241 | `cau_p_cf` | 0.7162 |
| cosine | B2_S1_bal | `cau_rd_x_pvar` | 0.8225 | `cau_p_real` | 0.7738 | `cau_logp_real` | 0.8241 | `dec_align_gen` | 0.8137 |
| dot | B2_S0_raw | `dec_dp_x_cvar` | 0.8871 | `cau_logp_cf` | 0.7748 | `cau_logp_cf` | 0.8278 | `dec_abs_delta_p` | 0.7179 |
| dot | B2_S1_all | `cau_p_real` | 0.7574 | `cau_p_real` | 0.7738 | `cau_logp_cf` | 0.8251 | `cau_p_real` | 0.7145 |
| dot | B2_S1_bal | `cau_logp_real` | 0.7574 | `cau_logp_real` | 0.7738 | `cau_p_real` | 0.8241 | `dec_align_gen` | 0.7932 |
| l2neg | B2_S0_raw | `dec_dp_x_cvar` | 0.8774 | `cau_p_real` | 0.7738 | `cau_logp_real` | 0.8241 | `dec_delta_p` | 0.7179 |
| l2neg | B2_S1_all | `cau_logp_cf` | 0.7594 | `cau_logp_cf` | 0.7762 | `cau_logp_cf` | 0.8273 | `cau_p_real` | 0.7145 |
| l2neg | B2_S1_bal | `cau_p_real` | 0.7574 | `cau_p_real` | 0.7738 | `cau_p_real` | 0.8241 | `cau_p_real` | 0.7145 |
| bilinear_drift | B2_S0_raw | `dec_dp_x_align` | 0.8866 | `cau_p_real` | 0.7738 | `cau_p_real` | 0.8241 | `dec_abs_delta_p` | 0.7179 |
| bilinear_drift | B2_S1_all | `cau_delta_logp_yes` | 0.7577 | `cau_p_real` | 0.7738 | `cau_logp_cf` | 0.8439 | `cau_logp_real` | 0.7145 |
| bilinear_drift | B2_S1_bal | `cau_p_real` | 0.7574 | `cau_logp_real` | 0.7738 | `cau_p_real` | 0.8241 | `dec_align_gen` | 0.7821 |

## Winner By Kernel

| Kernel | HY Winner | HY Metric | HY AUC | IC Winner | IC Metric | IC AUC | WY Winner | WY AUC | WN Winner | WN AUC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cosine | B2_S0_raw | `dec_dp_x_cvar` | 0.8851 | B2_S0_raw | `cau_p_real` | 0.7738 | B2_S0_raw | 0.8241 | B2_S1_bal | 0.8137 |
| dot | B2_S0_raw | `dec_dp_x_cvar` | 0.8871 | B2_S0_raw | `cau_logp_cf` | 0.7748 | B2_S0_raw | 0.8278 | B2_S1_bal | 0.7932 |
| l2neg | B2_S0_raw | `dec_dp_x_cvar` | 0.8774 | B2_S1_all | `cau_logp_cf` | 0.7762 | B2_S1_all | 0.8273 | B2_S0_raw | 0.7179 |
| bilinear_drift | B2_S0_raw | `dec_dp_x_align` | 0.8866 | B2_S0_raw | `cau_p_real` | 0.7738 | B2_S1_all | 0.8439 | B2_S1_bal | 0.7821 |

## Overall Winners Across All 12 Variations

| Target | Kernel | Condition | Metric | AUC |
| --- | --- | --- | --- | --- |
| Hallucinated Yes | dot | B2_S0_raw | `dec_dp_x_cvar` | 0.8871 |
| Is Correct | l2neg | B2_S1_all | `cau_logp_cf` | 0.7762 |
| Within Yes | bilinear_drift | B2_S1_all | `cau_logp_cf` | 0.8439 |
| Within No | cosine | B2_S1_bal | `dec_align_gen` | 0.8137 |

## Cluster-Pruned Champion Set

The correlation-pruning step (`|rho| >= 0.95`) keeps a smaller orthogonal set of representatives.

### Raw Hallucinated Yes

| Cluster | Champion Metric | AUC | Track | Family | Operator |
| --- | --- | --- | --- | --- | --- |
| 5 | `dec_dp_x_cvar` | 0.8851 | Decision | mixed_decision | interaction |
| 70 | `x_dp_x_rd` | 0.8315 | Cross-track | mixed_tracks | cross_track |
| 69 | `x_dp_x_dlp` | 0.8067 | Cross-track | mixed_tracks | cross_track |
| 16 | `cau_rel_drop` | 0.7617 | Causal | cosine_support | ratio_margin |
| 26 | `dec_rank_null` | 0.7612 | Decision | logit_distribution | raw_probability |
| 22 | `cau_logp_real` | 0.7574 | Causal | cosine_support | raw_causal |
| 3 | `dec_jsd_max` | 0.7555 | Decision | cosine_footprint | divergence |
| 49 | `dec_p_null` | 0.7150 | Decision | logit_distribution | raw_probability |

### Raw Is Correct

| Cluster | Champion Metric | AUC | Track | Family | Operator |
| --- | --- | --- | --- | --- | --- |
| 22 | `cau_logp_real` | 0.7738 | Causal | cosine_support | raw_causal |
| 21 | `cau_logp_cf` | 0.6992 | Causal | cosine_support | raw_causal |
| 35 | `cau_abs_specificity` | 0.6700 | Causal | cosine_support | specificity |
| 70 | `x_dp_x_rd` | 0.6549 | Cross-track | mixed_tracks | cross_track |
| 5 | `dec_delta_p` | 0.6540 | Decision | logit_distribution | raw_probability |
| 16 | `cau_rel_drop` | 0.6380 | Causal | cosine_support | ratio_margin |
| 41 | `cau_delta_p_other_max` | 0.6319 | Causal | cosine_support | contrast |
| 69 | `x_dp_x_dlp` | 0.6170 | Cross-track | mixed_tracks | cross_track |

## Main Findings

1. **Raw remains the robust primary winner.** The best hallucination detector in every kernel is still a raw-space configuration.
2. **`dot` is the strongest kernel on the primary target.** `dot + raw` reaches `0.8871` on `hallucinated_yes`, slightly above cosine and bilinear-drift raw.
3. **`l2neg + S1_all` is the one narrow counterexample on `is_correct`.** It reaches `0.7762`, slightly above the usual `0.7738` plateau.
4. **Decision interactions explain the top hallucination detectors.** The strongest raw hallucination metrics are still `dec_dp_x_cvar` or `dec_dp_x_align`, not pure state reductions.
5. **Causal metrics explain most accuracy winners.** `cau_p_real`, `cau_logp_cf`, and `cau_logp_real` dominate `is_correct` and often `within_yes`.
6. **Whitening changes the secondary targets more than the primary one.** `S1_bal` helps `within_no` under cosine, and `S1_all` helps `within_yes` under bilinear-drift, but neither changes the main Stage B freeze decision.