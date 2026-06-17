# Grounding Methodology (State + Decision + Causal)

This is the canonical methodology document for intrinsic grounding in `vlm_grounding`.

## Scope

The intrinsic grounding stack has three stages:

1. **State grounding** — token-level image-evidence shift in hidden-state space.
2. **Decision grounding** — image-conditioned decision sensitivity per generated token.
3. **Causal grounding** — targeted patch ablation to test necessity of visual evidence.

All three stages are executed by the same pipeline and stored under one run root.

## Implementation Sources

- Pipeline orchestration: `vlm_grounding/pipeline/runner.py`
- Artifact contracts: `vlm_grounding/pipeline/artifact_store.py`
- Stage implementations:
  - `vlm_grounding/grounding/state.py`
  - `vlm_grounding/grounding/decision.py`
  - `vlm_grounding/grounding/causal.py`
- CLIs:
  - `scripts/run_pipeline.py`
  - `scripts/run_aggregate.py`

## Run Procedure

### Full intrinsic run

```bash
python scripts/run_pipeline.py configs/base.yaml
```

### Optional stage subset

```bash
python scripts/run_pipeline.py configs/base.yaml --stages extraction,state,decision,causal
```

### Aggregate outputs

```bash
python scripts/run_aggregate.py runs/<run_name>
```

## Stage 1: State Grounding

### Purpose

Measure whether generated tokens are supported by image evidence in Layer-32 representation space.

### Key per-sample outputs (`runs/<run_name>/samples/<sample_id>/`)

- `delta_l32.pt`
- `grounding_scores.csv`

### Aggregated outputs (`runs/<run_name>/results/`)

- `state_grounding_all.csv`

## Stage 2: Decision Grounding

### Purpose

Measure image-conditioned decision behavior for generated tokens and candidate-level effects.

### Key per-sample outputs

- `track_a.json`
- `track_b.json`
- `decision_matrix.csv`
- `decision_per_token.csv`

### Aggregated outputs

- `decision_grounding_all.csv`
- `decision_per_token_all.csv`

## Stage 3: Causal Grounding

### Purpose

Test whether selected visual support is causally necessary via targeted ablation.

### Key per-sample outputs

- `causal_result.csv`
- `causal_per_token.csv`
- `masks/t{step}_c{token_id}_mask.pt`

### Aggregated outputs

- `causal_grounding_all.csv`
- `causal_per_token_all.csv`

## Shared References

Under `runs/<run_name>/references/`:

- `null_patches_l32.pt`
- `null_patches_proj.pt`
- `lm_head_weight.pt`
- `rms_norm_weight.pt`

## Integration with GT-Free Judge Path

Intrinsic outputs are consumed by:

- `scripts/build_intrinsic_token_extended.py`
- `scripts/analyze_judge_alignment.py`
- `scripts/run_multimodal_judge_eval.py`

## Maintenance Rule

If artifact names, stage behavior, or entrypoints change, update this document together with:

- `vlm_grounding/pipeline/artifact_store.py`
- `scripts/run_pipeline.py`
- `scripts/run_aggregate.py`