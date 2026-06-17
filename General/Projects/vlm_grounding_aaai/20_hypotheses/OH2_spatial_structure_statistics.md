---
title: OH2 - Spatial Structure Matters for Support Row Statistics
type: hypothesis
status: open
created: 2026-06-16
tags: [hypothesis, spatial, metrics]
---

# OH2: Spatial Structure Matters for Support Row Statistics

## Source Trace
- Absorbed from: `20_hypotheses/future_hypotheses.md` (H-B)

## Observation
The support row `s_t = {k(v_j, h_t)}` over 576 patches is currently summarized with scalar statistics (variance, entropy, max, etc.) that treat it as a flat 1D vector. But the 576 patches form a 24×24 grid.

## Problem
Three patches with similar values arranged **horizontally** (j, j+1, j+2) look "concentrated" under most 1D statistics. Three patches with the same values arranged **vertically** (j, j+24, j+48) look "dispersed" — even though the spatial concentration is identical.

Current metrics would report these as completely different distributions, but the underlying spatial pattern is the same.

## Hypothesis
Spatial structure in the support row is informative and current 1D statistics systematically mischaracterize it.

## Possible Compensations
- Compute 2D spatial statistics on the reshaped (24×24) support map instead of the flat (576,) vector.
- Use IoU-based or region-based metrics rather than scalar reductions.
- Check whether transformers disperse information along a "line" direction rather than a grid — if so, the 1D treatment may be structurally correct for what the model is doing, even if wrong for what the image contains.

## Status
- **Open**. Relevant to spatial localization test in `experiment_protocol_v3` (Step 3) and `SPATIAL_LOCALIZATION_PROTOCOL_v1`.
