---
title: Method Decisions & Autopsies
type: methods-history
created: 2026-06-16
---

# Method Decisions & Autopsies

## Source Trace
- Absorbed from: 30_methods/canonical_method.md (Prior V2 notes)
- Absorbed from: 90_archive/old_methods/METHODOLOGY.md

## V2 SVD Formulation (Rejected)

# Grounding V2 Implementation Notes  
  
This document describes the Grounding V2 implementation that currently exists in the repository under `vlm\_grounding\_v2/`.  
  
It is intentionally about the code we run now, not the idealized formulation. Where the current implementation differs from the conceptual design, this document says so explicitly.  
  
## 1. Scope  
  
Current V2 coverage:  
  
\- State grounding: implemented  
\- Decision grounding: implemented  
\- Causal grounding: not implemented as a live intervention path yet  
  
Current entrypoints:  
  
\- `scripts/run\_grounding\_v2\_replay.py`  
\- `vlm\_grounding\_v2/projection.py`  
\- `vlm\_grounding\_v2/state.py`  
\- `vlm\_grounding\_v2/decision.py`  
\- `vlm\_grounding\_v2/reader.py`  
  
## 2. Inputs  
  
For one sample, the replay path loads:  
  
\- `H\_real` from `states\_real.pt`  
\- `H\_null` from `states\_null.pt`  
\- `V\_real` from `patches\_l32.pt`  
\- `V\_null` from either:  
 \- `sample\_null\_l32.pt` when present and `null\_policy=sample\_then\_shared`  
 \- shared `null\_patches\_l32.pt` otherwise  
\- `W\_u` from `lm\_head\_weight.pt` for decision replay  
\- `rms\_norm\_weight` from `rms\_norm\_weight.pt` for decision replay  
  
Shapes used by the implementation:  
  
\- `H\_real, H\_null in R^{T x d}`  
\- `V\_real, V\_null in R^{M x d}`  
\- with `T = number of answer tokens`, `M = 576`, `d = 4096`  
  
## 3. Core State Formulation  
  
### 3.1 Token-state and patch-difference matrices  
  
The implementation first computes:  
  
```  
DeltaH = H\_real \- H\_null  
DeltaV = V\_real \- V\_null  
```  
  
For SVD, the code uses `D\_V = DeltaV^T` so `D\_V in R^{d x M}`.  
  
### 3.2 SVD basis  
  
The code computes `D\_V = U Sigma V^T` with:  
  
\- `U = u\_full`  
\- `Sigma = singular\_values`  
\- `V^T = vh\_full`  
  
The numerical rank is `rank = count(sigma\_i > svd\_eps)`.  
  
Then the rank\-trimmed basis is:  
  
```  
U\_r = U\[:, :rank\]  
Sigma\_r = Sigma\[:rank\]  
V\_r^T = V^T\[:rank, :\]  
```  
  
### 3.3 How `k\_selected` is chosen  
  
The replay code supports an explicit `full\_rank` mode. When `full\_rank=True`:  
  
```  
k\_selected = rank  
```  
  
and the truncated\-basis machinery is bypassed.  
  
If `k` is provided explicitly:  
  
```  
k\_selected = min(max(k, 0), rank)  
```  
  
If `k` is not provided, the code selects the smallest `k\_selected` such that:  
  
```  
sum\_{i=1..k\_selected} sigma\_i^2 / sum\_{i=1..rank} sigma\_i^2 >= energy\_threshold  
```  
  
then clips with `k\_max` if provided.  
  
The selected basis is `U\_k = U\_r\[:, :k\_selected\]`.  
  
## 4. Exact State V2 Quantities  
  
For token `t`, let `DeltaH\_t` be the `t`th row of `DeltaH`.  
  
### 4.1 Total token energy  
  
`delta\_h\_energy\[t\] = ||DeltaH\_t||\_2^2`  
  
### 4.2 Response amplitude  
  
`delta\_h\_l2\[t\] = ||DeltaH\_t||\_2 = sqrt(delta\_h\_energy\[t\])`  
  
### 4.3 Projected coefficients  
  
`c\_t = DeltaH\_t U\_k`  
  
### 4.4 Projected component  
  
`DeltaH\_parallel\_t = c\_t U\_k^T`  
  
### 4.5 Projected energy  
  
Because `U\_k` is orthonormal:  
  
`projected\_energy\[t\] = ||DeltaH\_parallel\_t||\_2^2 = ||c\_t||\_2^2`  
  
### 4.6 Residual component  
  
`DeltaH\_residual\_t = DeltaH\_t \- DeltaH\_parallel\_t`  
  
### 4.7 Residual energy  
  
`residual\_energy\[t\] = ||DeltaH\_residual\_t||\_2^2`  
  
### 4.8 State V2 score  
  
`state\_v2\_score\[t\] = projected\_energy\[t\] / delta\_h\_energy\[t\]`  
  
with safeguard: `state\_v2\_score\[t\] = 0` when `delta\_h\_energy\[t\] <= eps`.  
  
So: `state\_v2\_score = projected\_energy / (projected\_energy + residual\_energy)` up to floating\-point roundoff.  
  
## 5. Spectral Diagnostics  
  
The code also stores a mode\-wise profile:  
  
`spectral\_profile\[t, l\] = c\_{t,l\}^2 / delta\_h\_energy\[t\]`  
  
Its row sum is exactly `state\_v2\_score\[t\]`.  
  
Derived quantities:  
  
\- `spectral\_entropy`: entropy of the selected\-mode distribution after renormalizing by row sum  
\- `spectral\_effective\_rank = exp(spectral\_entropy)`  
\- `spectral\_top1\_mass`: largest selected\-mode mass  
\- `spectral\_top3\_mass`: sum of top 3 selected\-mode masses  
  
## 6. Patch Attribution `alpha`  
  
The implementation also saves a patch\-attribution matrix:  
  
`alpha = DeltaH D\_V^+`  
  
expressed using the compact SVD as:  
  
`alpha = DeltaH U\_r Sigma\_r^{-1} V\_r^T`  
  
**Important:** this uses the full numerical rank `r`, not `k\_selected`.  
  
That means:  
  
\- `state\_v2\_score`, `projected\_energy`, and `residual\_energy` are based on the truncated selected subspace `U\_k`  
\- `alpha` is based on the full pseudoinverse over `U\_r`  
  
## 7. Decision V2 Quantities  
  
For each teacher\-forced emitted token `y\_t`, let `w\_t = W\_u\[y\_t\]`.  
  
The code computes:  
  
```  
delta\_logit\_linear\[t\] = <DeltaH\_t, w\_t>  
delta\_logit\_projected\[t\] = <DeltaH\_parallel\_t, w\_t>  
delta\_logit\_residual\[t\] = <DeltaH\_residual\_t, w\_t>  
```  
  
Then:  
  
```  
decision\_v2\_fraction\[t\] =  
 0 if |delta\_logit\_linear\[t\]| <= eps  
 0 if delta\_logit\_projected\[t\] == 0  
 0 if delta\_logit\_projected\[t\] and delta\_logit\_linear\[t\] have opposite sign  
 delta\_logit\_projected\[t\] / delta\_logit\_linear\[t\] otherwise  
```  
  
The concept\-direction alignment is:  
  
`concept\_subspace\_alignment\[t\] = ||P\_k w\_t||\_2^2 / ||w\_t||\_2^2`  
  
## 8. State CSV Columns  
  
\- `delta\_h\_l2 = ||DeltaH\_t||\_2`  
\- `delta\_h\_energy = ||DeltaH\_t||\_2^2`  
\- `projected\_energy = ||DeltaH\_parallel\_t||\_2^2`  
\- `residual\_energy = ||DeltaH\_residual\_t||\_2^2`  
\- `state\_v2\_score = projected\_energy / delta\_h\_energy`  
\- `spectral\_entropy = entropy of selected\-mode mass after renormalization`  
\- `spectral\_effective\_rank = exp(spectral\_entropy)`  
\- `spectral\_top1\_mass = max\_l spectral\_profile\[t, l\]`  
\- `spectral\_top3\_mass = sum of top 3 spectral\_profile\[t, l\]`  
\- `basis\_rank = numerical rank of D\_V`  
\- `k\_selected = selected truncation rank`  
\- `k\_energy\_fraction = sum\_{i<=k\_selected} sigma\_i^2 / sum\_i sigma\_i^2`  
  
## 9. Current Review Findings  
  
### Finding 1: `alpha` and `state\_v2\_score` are not based on the same subspace  
  
Severity: medium  
  
`state\_v2\_score` uses the truncated selected basis `U\_k`, but `alpha` uses the full\-rank pseudoinverse over `U\_r`. So the alpha heatmap is not strictly an attribution of the same truncated component that defines `state\_v2\_score`. When `full\_rank=True`, this mismatch disappears.  
  
### Finding 2: decision linearization omits the final RMSNorm map  
  
Severity: medium  
  
`delta\_logit\_linear = <H\_real \- H\_null, w\_t>` is a simpler surrogate, not a Jacobian\-consistent first\-order approximation of the actual final logit map. `linear\_vs\_model\_gap` therefore includes both true modeling error and the omitted RMSNorm linearization term.  
  
### Finding 3: caption\-level score is a convenience heuristic  
  
Severity: low  
  
`caption\_score` is a mean over mention or token scores — convenient but not part of the formal V2 derivation.  
  
### Finding 4: test coverage is still narrow  
  
Severity: low  
  
Current tests do not verify energy conservation, CSV formula consistency, the alpha/truncated\-subspace distinction, or decision behavior with RMSNorm\-aware linearization.  
  
## 10. Practical Reading Guide  
  
When looking at notebook outputs today:  
  
1. Read `delta\_h\_l2` as response magnitude.  
2. Read `state\_v2\_score` as the fraction of that response that lies in the selected patch\-difference subspace.  
3. Read `projected\_energy` and `residual\_energy` as the explained vs unexplained energy split under that selected subspace.  
4. Read `decision\_v2\_fraction` as a surrogate decision\-side fraction, not a full RMSNorm\-aware local Jacobian decomposition.  
5. Read alpha heatmaps as full\-rank pseudoinverse patch reconstructions, not exact visualizations of the truncated `state\_v2\_score`.  
  
## 11. Recommended Next Corrections  
  
1. Decide whether `alpha` should be full\-rank pseudoinverse attribution or truncated `k\_selected` attribution aligned with `state\_v2\_score`.  
2. Make decision replay explicitly RMSNorm\-aware if we want `delta\_logit\_linear` to be a closer local\-linear explanation of `model\_logit\_shift\_rms`.  
3. Add tests for energy conservation, CSV formula consistency, and alpha behavior under truncated vs full\-rank definitions.

## 14. Current Issues (Autopsy Findings — 2026-02-17)  
  
This section records current known failures and risks from the latest review run.  
  
### 14.1 What is working (integrity and separability)  
  
1\. Stage 4 matrix mechanics and identities pass:  
- row sums of `P_real` / `P_null` are \~1  
- `A_delta = P_real - P_null`  
- `g_state = sum(A_pos) = 0.5*L1(P_real,P_null)` within float tolerance  
  
2\. Tri-scenario state separation is strong for real-vs-null:  
- source: `tables/stage4_state_separability_tri_scenario.json`  
- dataset means:  
 - `d_free_real_mean = 0.00118257`  
 - `d_free_null_mean = 0.50412493`  
 - `d_real_null_mean = 0.50412866`  
 - `c_free_real_mean = 0.99999897`  
 - `c_free_null_mean = 0.85007003`  
 - `c_real_null_mean = 0.85006747`  
  
Interpretation: the model state changes materially under null conditioning; this is not a no-signal failure.  
  
### 14.2 What is failing (semantic discrimination at token level)  
  
1\. Baseline token-level score is in the wrong direction:  
- source: `tables/stage4_discrimination_diagnostics.json`  
- `mean_mention = 0.04856148`  
- `mean_nonmention = 0.05048453`  
- `mean_diff = -0.00192305`  
- `auc_like_p_mention_gt_nonmention = 0.44033690` (\< 0.5)  
  
2\. Alternative scalar metrics tested so far also fail directional discrimination:  
- source: `tables/stage4_distribution_metric_benchmark.csv`  
- best observed AUC-like among tested metrics: `g_com_shift = 0.47423611` (\< 0.5)  
- all tested metrics remain below `0.5`  
  
3\. Visual interpretability remains weak:  
- overlays are numerically distinct, but semantic interpretability is still low for many tokens.  
  
### 14.3 Current diagnosis  
  
At present, this is best interpreted as a **metric-objective mismatch**, not a pure implementation bug:  
  
- the pipeline is sensitive to real-vs-null state changes,  
- but token-level scalarization does not align with mention-token semantic grounding.  
  
### 14.4 Decision status (effective immediately)  
  
Until a metric passes discrimination gates:  
  
1\. Treat token-level scores as **diagnostic only**.  
2\. Do not make semantic hallucination claims from token-level rankings.  
3\. Keep semantic evaluation anchored at mention/caption levels.  
4\. Continue critical review in:  
- `artifacts/experiments/experiment1/stage4_critical_review.ipynb`  
- `artifacts/experiments/experiment1/STAGE4_CRITICAL_REVIEW_PROTOCOL.md`  
  
### 14.5 Open remediation work  
  
1\. Expand score families beyond current distribution-shift metrics.  
2\. Audit mention-token alignment/subword aggregation effects.  
3\. Add logit-space and similarity-space semantic discrimination tests.  
4\. Reassess token-level objective before any Stage 5+ interpretation claims depend on it.  