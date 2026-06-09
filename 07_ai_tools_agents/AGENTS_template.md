# AGENTS.md

## Project Purpose

This repository supports [project name].

## Important Directories

- `src/`: core implementation
- `configs/`: experiment configs
- `scripts/`: runnable scripts
- `results/`: raw outputs
- `notebooks/`: analysis notebooks
- `paper/`: manuscript, figures, tables

## Common Commands

- Run tests: `pytest`
- Run linting: `ruff check .`
- Format: `ruff format .`
- Run experiment: `python scripts/run_experiment.py --config configs/example.yaml`
- Aggregate results: `python scripts/aggregate_results.py`

## Rules for Agents

- Do not delete raw results.
- Do not overwrite existing result files unless explicitly told.
- Prefer small, reviewable changes.
- Always explain what changed.
- Always run relevant tests/checks when possible.
- If results are ambiguous, create a diagnostic report instead of guessing.

## Paper-Specific Context

The main manuscript is about [brief description].

Key baselines:

- [Baseline 1]
- [Baseline 2]

Known issues:

- [Issue 1]
- [Issue 2]

## Agent Task Backlog

- [ ] Inspect result file structure.
- [ ] Create result aggregation script.
- [ ] Verify table values against raw logs.
- [ ] Generate reproducibility README.
