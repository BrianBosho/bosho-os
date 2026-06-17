---
type: analysis-note
status: draft
project: tmlr_fedprop_paper
tags: [fedprop, analysis, results]
---

# Recovery Metrics

## Purpose

Make performance recovery the primary result, not a secondary interpretation of raw accuracy.

## Metrics

For each dataset, backbone, partition, and L setting:

```text
loss = Full - Zero-hop
gain = FedProp - Zero-hop
Recovery% = 100 * gain / loss
```

## Reporting Rules

- If `Full - Zero-hop` is statistically indistinguishable from zero, report recovery as `N/A: no recoverable gap`.
- If Zero-hop beats Full, report recovery as `N/A`; there is no degradation for FedProp to repair.
- Do not clip recovery at 100%.
- Prefer paired seed differences and confidence intervals when available.

## Figure Idea

For each core dataset, show:

```text
Zero-hop -> L1 FedProp -> L1 + RPE -> L2 FedProp -> L2 + RPE -> Full
```

Use a bracket between Zero-hop and Full to show the recoverable gap.
