# OpenClaw Spec: Role, Interface, and Vault Integration

## What OpenClaw Is

OpenClaw is the AI agent used for bounded, executable tasks in Bosho OS. It operates on local files and repositories — reading context, producing outputs, and writing results back to the vault. It does not plan, decide priorities, or manage the OS. Those are human responsibilities. OpenClaw executes.

**Core principle:** Every OpenClaw task has a defined input, a defined output, and a defined constraint. If any of these is missing, the task should not start.

---

## Operating Model

```
HUMAN defines task
    │
    ▼
Prompt from Workflow Library (codex_openclaw_workflows.md)
    │
    ├── Reads: vault files, repo files, pasted content
    │
    ▼
OpenClaw executes
    │
    ├── Writes: output to designated vault path
    ├── Never: modifies raw results, overwrites without instruction, invents data
    │
    ▼
Human reviews output in vault
    │
    ▼
If accepted → tasks promoted to project files
If rejected → discard or revise prompt
```

---

## Input Sources

| Source | Path / Location | Used For |
|--------|----------------|----------|
| Vault project files | `02_projects/*.md` | Context for task scope and priority |
| Research dashboard | `04_research_system/research_dashboard.md` | Current research state |
| Experiment logs | `04_research_system/experiment_log_*.md` | Experiment context |
| Results registry | `04_research_system/results_registry.md` | Verified result tracking |
| Inbox files | `00_inbox/*.md` | Braindumps awaiting processing |
| Repo AGENTS.md | `[repo root]/AGENTS.md` | Per-project agent context |
| Repo results | `[repo]/results/`, `[repo]/configs/` | Raw experiment data |
| Repo manuscript | `[repo]/paper/` | Draft LaTeX/markdown |
| Pasted email/doc content | Provided inline in prompt | Inbox synthesis |

---

## Output Locations

| Output Type | Write To | Never Write To |
|-------------|----------|----------------|
| Inbox synthesis | `00_inbox/synthesis_YYYY-MM-DD.md` | Project files directly |
| Experiment audit report | `04_research_system/audit_[project]_YYYY-MM-DD.md` | Raw result files |
| Results registry | `04_research_system/results_registry.md` | Config or log files |
| Paper audit | `04_research_system/paper_audit_[project].md` | Manuscript directly |
| Notebook scaffold | `[repo]/notebooks/[name].ipynb` | Existing notebooks |
| Aggregation script | `[repo]/scripts/aggregate_results.py` | Result data |
| Agent task update | Append to `## Agent Notes` in experiment log | Experiment data |
| Synthesis tasks | `00_inbox/synthesis_YYYY-MM-DD.md` | Project task lists |

---

## Task Categories and Trigger Conditions

### 1. Research Tasks (repo-level)

**Trigger:** You are about to start a deep work block on TMLR or VLM.

| Task | Workflow | Output |
|------|----------|--------|
| Audit results against manuscript tables | Workflow 2 | `audit_tmlr_YYYY-MM-DD.md` |
| Aggregate raw logs into CSV | Workflow 3 | `results_registry.md` update |
| Check manuscript for unsupported claims | Workflow 4 | `paper_audit_tmlr.md` |
| Scaffold a demo notebook | Workflow 5 | `notebooks/demo.ipynb` |
| Onboard a new repo | Workflow 1 | `README.md` update |

**Always give OpenClaw:**
- Path to the repo root
- Path to AGENTS.md
- Which specific tables/figures to audit
- Constraint: do not modify raw results

---

### 2. Inbox Synthesis (vault-level)

**Trigger:** New emails, new braindumps, or beginning of a work week.

| Task | Workflow | Output |
|------|----------|--------|
| Process inbox + emails | Workflow 7 | `00_inbox/synthesis_YYYY-MM-DD.md` |
| Convert braindump to actions | Workflow 6 | `00_inbox/synthesis_YYYY-MM-DD.md` |

**Always give OpenClaw:**
- Path to `00_inbox/`
- Pasted email/doc content in `[EMAIL INPUT]` / `[GDOC INPUT]` sections
- The priority stack: P1=TMLR, P2=VLM/PhD, P3=Acubed, P4=Swyng

---

### 3. Documentation Tasks (repo or vault)

**Trigger:** New intern joining, new experiment started, repo hasn't been touched in a while.

| Task | Workflow | Output |
|------|----------|--------|
| Repo README | Workflow 1 | `README.md` |
| Experiment log | Experiment log template | `04_research_system/experiment_log_[name].md` |
| Meeting agenda | Agent manual | `00_inbox/agenda_YYYY-MM-DD.md` |
| Follow-up summary | Agent manual | `00_inbox/followup_YYYY-MM-DD.md` |

---

### 4. Literature and Reading (research system)

**Trigger:** Starting a new research direction or preparing a team document.

| Task | Agent Role | Output |
|------|-----------|--------|
| Summarize a paper | Literature Scout | Paper summary note in `04_research_system/` |
| Build reading list | Literature Scout | Reading list markdown |
| Compare methods | Literature Scout | Comparison table markdown |
| Draft concept glossary | Literature Scout | Glossary markdown for PhD prep |

---

## Research Dashboard Integration

The `04_research_system/research_dashboard.md` is OpenClaw's **research context anchor**. Before any research task, OpenClaw should read this file to understand:
- Which research directions are active
- What the current priorities are
- What experiments are in progress

The dashboard's components and their OpenClaw mapping:

| Dashboard Component | How OpenClaw Populates It |
|--------------------|--------------------------|
| Reading list | Literature Scout → outputs reading list markdown |
| Paper summaries | Literature Scout / Paper Assistant → summary notes |
| Experiment logs | Research Engineer fills experiment log template |
| Results registry | Experiment Auditor → populates `results_registry.md` |
| Figures/tables | Research Engineer → generates scripts; human runs them |
| Writing fragments | Paper Assistant → drafts saved to `04_research_system/` |
| Submission calendar | Paper Assistant extracts deadlines from CFPs |
| Collaborator notes | Inbox Synthesizer extracts from emails |
| Agent task backlog | Human writes; OpenClaw reads and executes |

**Rule:** OpenClaw writes *to* the research system files. It does not *define* research direction. That remains human.

---

## AGENTS.md Convention

Every research repository must have an `AGENTS.md` at its root. This is what OpenClaw reads before doing anything in that repo.

Minimum required fields:

```markdown
## Project Purpose
[One paragraph: what this repo is for, what paper it supports]

## Important Directories
- results/: raw output files — DO NOT DELETE OR MODIFY
- configs/: experiment config files
- scripts/: runnable scripts
- paper/: manuscript and figures

## Common Commands
- Run experiment: python scripts/run_experiment.py --config configs/X.yaml
- Aggregate results: python scripts/aggregate_results.py
- Run tests: pytest

## Known Issues
[List any known naming inconsistencies, missing files, broken configs]

## Rules for Agents
- Do not delete raw results
- Do not overwrite existing result files
- Produce a diagnostic report instead of guessing

## Agent Task Backlog
- [ ] [Next task for OpenClaw]
```

**Current repos needing AGENTS.md:**
- TMLR FedProp repo → add before next results audit
- LLaVA/VLM codebase → add before notebook scaffold

---

## Vault-Wide Rules for OpenClaw

**Always allowed:**
- Reading any vault file
- Writing to `00_inbox/` (synthesis notes only)
- Writing to `04_research_system/` (audit reports, summaries, registry)
- Writing to `[repo]/scripts/` and `[repo]/notebooks/`
- Appending to `## Agent Notes` sections in experiment logs

**Never allowed without explicit instruction:**
- Modifying any file in `02_projects/`
- Modifying `00_dashboard.md`
- Modifying any file in `03_protocols/`
- Deleting any file
- Overwriting raw result data in any repo
- Marking tasks complete in project files

**On ambiguity:**
- Write findings to a diagnostic report
- Flag the ambiguity explicitly
- Do not guess or infer results

---

## Workflow Library Reference

All copy-pasteable OpenClaw prompts live in:
→ [codex_openclaw_workflows.md](codex_openclaw_workflows.md)

| Workflow | Purpose |
|----------|---------|
| 1 | Repo onboarding / README |
| 2 | Results audit (TMLR-focused) |
| 3 | Aggregate raw logs → CSV |
| 4 | Manuscript claim audit |
| 5 | Notebook scaffold |
| 6 | Braindump → tasks |
| 7 | Inbox synthesis → prioritized task list |

Agent role templates:
→ [agent_roles.md](agent_roles.md)

---

## Standard Task Format (required for every OpenClaw task)

```text
Role: [from agent_roles.md]
Context: [project name, vault path, repo path]
Input: [exact files or pasted content]
Task: [exact action — one sentence]
Output: [exact file path and format]
Constraints: [what not to touch]
Review criteria: [how you will verify the result]
```

Incomplete tasks get incomplete results. Define scope before running.
