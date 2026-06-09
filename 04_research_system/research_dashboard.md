# Research Dashboard

> OpenClaw reads this file before every research task. Keep it current.

---

## Active Research Directions

| Project | Status | Deadline | OpenClaw Role |
|---------|--------|----------|--------------|
| TMLR FedProp | Active — results audit needed | 2026-07-30 | Experiment Auditor, Paper Assistant |
| VLM Grounding / AAAI | Active — literature phase | 2026-07-21 | Literature Scout, Research Engineer |
| Subgraph topology | Paused — depends on M | — | None until momentum confirmed |

---

## Research Principles

- Every experiment needs a question.
- Every result needs provenance.
- Every table must map to raw logs and configs.
- Every claim needs evidence, citation, or removal.
- Every project needs a smallest publishable unit.

---

## System Components

### 📖 Reading List
*Populated by Literature Scout agent.*
- [ ] VAUQ paper (VLM self-evaluation baseline) — needed for VLM Epic 1
- [ ] FedProp original submission — review before final manuscript pass
- [ ] AI safety / multimodal grounding survey — PhD reading list seed

→ Add papers here. Ask OpenClaw (Literature Scout) to summarize on demand.

---

### 🧪 Experiment Logs
*One file per experiment. Template: [experiment_log_template.md](experiment_log_template.md)*

Active logs:
- *(none yet — create one before next TMLR work block)*

OpenClaw task to generate:
```text
Role: Research Engineer
Context: TMLR FedProp repo
Task: Inspect results directory and create one experiment_log file per distinct experimental configuration found.
Output: 04_research_system/experiment_log_[name].md per config
Constraints: Do not modify raw results.
```

---

### 📊 Results Registry
*Populated by Experiment Auditor. One row per manuscript result.*
→ [results_registry_template.md](results_registry_template.md)

Current state: **empty — needs population before TMLR manuscript pass.**

OpenClaw task to populate:
```text
Role: Experiment Auditor
Context: TMLR FedProp repo
Task: Read all result files and configs. Populate the results_registry.md with one row per result: project, dataset, method, setting, seed, metric, value, raw file, config file, table/figure reference, verified status.
Output: 04_research_system/results_registry.md
Constraints: Do not modify raw data. Mark any unverifiable result as Unverified.
```

---

### 📋 Paper Audit
*Populated by Paper Assistant.*

TMLR: **not yet run.**

OpenClaw task:
```text
Role: Paper Assistant
Context: TMLR FedProp manuscript
Task: Read the manuscript. Identify all claims not directly supported by a table, figure, citation, or experiment. Produce a checklist: section, claim, issue, suggested fix.
Output: 04_research_system/paper_audit_tmlr.md
Constraints: Do not rewrite the manuscript.
```

---

### 📝 Writing Fragments
*Short draft sections, argument sketches, or framing notes — saved here before insertion into manuscript.*

Active fragments:
- *(none)*

---

### 📅 Submission Calendar

| Venue | Deadline | Project | Status |
|-------|----------|---------|--------|
| AAAI 2026 | 2026-07-21 | VLM Grounding | In progress |
| TMLR (rolling) | 2026-07-30 target | FedProp | Near closure |

---

### 👥 Collaborator Notes
*Extracted from emails by Inbox Synthesizer. Key contacts per project.*

| Person | Project | Last Contact | Next Action |
|--------|---------|-------------|-------------|
| Carlee | TMLR + VLM | — | Questions on dataset inclusion + reconstruction errors |
| M | Subgraph topology | — | Check interest level before committing |
| VLM team | VLM Grounding | — | Share direction note after VAUQ review |

---

### 🤖 Agent Task Backlog

Tasks queued for OpenClaw — run when repo access is available:

- [ ] TMLR: Onboard repo (Workflow 1) — produce README
- [ ] TMLR: Audit results against manuscript tables (Workflow 2)
- [ ] TMLR: Aggregate raw logs into CSV (Workflow 3)
- [ ] TMLR: Run paper claim audit (Workflow 4)
- [ ] VLM: Scaffold LLaVA demo notebook (Workflow 5)
- [ ] VLM: Summarize VAUQ paper (Literature Scout)

---

## OpenClaw Reference

Full spec: [openclaw_spec.md](../07_ai_tools_agents/openclaw_spec.md)
Workflow prompts: [codex_openclaw_workflows.md](../07_ai_tools_agents/codex_openclaw_workflows.md)
Agent roles: [agent_roles.md](../07_ai_tools_agents/agent_roles.md)
