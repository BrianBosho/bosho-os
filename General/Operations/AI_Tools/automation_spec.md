# Automation Spec — Bosho OS

> Agents reduce friction. Brian decides what matters.

This document defines every automation layer in Bosho OS: what it does, what triggers it, which tool runs it, and what it produces. It is the single reference for "I have X situation — what do I run?"

---

## System Overview

```
INPUTS                          PROCESSING LAYER                 VAULT OUTPUTS
──────────────────────────────────────────────────────────────────────────────
Gmail                 ──►  Claude Code MCP / OpenClaw  ──►  00_inbox/synthesis
Google Drive docs     ──►  OpenClaw (Workflow 7)        ──►  00_inbox/synthesis
Obsidian braindumps   ──►  OpenClaw (Workflow 6)        ──►  00_inbox/synthesis
                                      │
                                      ▼
Research repos        ──►  OpenClaw + Codex CLI         ──►  04_research_system/
                           (Workflows 1–5)                   experiment logs
                                                             results registry
                                                             paper audits
                                      │
                                      ▼
Weekly reflection     ──►  ChatGPT Planner               ──►  08_weekly_plans/
Planning / protocols  ──►  ChatGPT Planner               ──►  01_operating_system/
                                      │
                                      ▼
Vault task files      ──►  Obsidian: Dataview + Tasks    ──►  00_dashboard.md (live)
```

---

## Tool Registry

| Tool | Role | Access | Used For |
|------|------|--------|----------|
| **OpenClaw** | Agentic executor | Local files + repos | Research workflows, inbox synthesis, braindump processing |
| **Codex CLI** | Code agent | Local repos | Codebase inspection, scripts, debugging, experiment automation |
| **ChatGPT Planner** | Planning + reflection | Conversation | Weekly planning, protocol drafting, reflection, reviews |
| **Minimax M3** | Supporting model | Via OpenClaw | Supports OpenClaw on specific tasks (model-dependent) |
| **Claude Code MCP** | Integration agent | Gmail, Drive, Calendar | Email synthesis, Drive doc pull, Calendar event creation |
| **Obsidian Dataview** | Passive query engine | Vault frontmatter | Live project table on dashboard |
| **Obsidian Tasks** | Passive task engine | Vault checkboxes | Live task lists on dashboard |
| **Obsidian Templater** | Template engine | Vault templates | Auto-filled weekly plans, daily notes |

**Principle:** No single tool does everything. Each has a lane. Overlap is resolved by the table above — if a task fits multiple tools, use the most specific one.

---

## Automation Layers

### Layer 1 — Always-On (Obsidian Plugins)

These run passively inside Obsidian. No trigger needed.

| Automation | Plugin | What It Does |
|-----------|--------|-------------|
| Project overview table | Dataview | Queries frontmatter of all `02_projects/*.md` and renders live table on dashboard |
| Next actions list | Tasks | Filters all `🔺` tasks across `02_projects/` and renders on dashboard |
| All open tasks | Tasks | Groups all incomplete tasks by project file on dashboard |
| Completed this week | Tasks | Shows tasks marked `[x]` since Monday |

**Maintenance:** When you complete a task, change `[ ]` to `[x]` in the project file. Dashboard updates instantly. When a project changes epic, update `epic_active:` in the frontmatter.

---

### Layer 2 — On-Demand Research Automations (OpenClaw + Codex CLI)

Trigger these manually before or during research work blocks.

#### Before a TMLR work block

| Step | Tool | Workflow | Output |
|------|------|----------|--------|
| 1. Audit results vs tables | OpenClaw | Workflow 2 | `04_research_system/audit_tmlr_YYYY-MM-DD.md` |
| 2. Aggregate raw logs → CSV | Codex CLI | Workflow 3 | `04_research_system/results_registry.md` |
| 3. Check manuscript claims | OpenClaw | Workflow 4 | `04_research_system/paper_audit_tmlr.md` |
| 4. Log new experiment | OpenClaw | Experiment log template | `04_research_system/experiment_log_[name].md` |

#### Before a VLM work block

| Step | Tool | Workflow | Output |
|------|------|----------|--------|
| 1. Summarize VAUQ paper | OpenClaw | Literature Scout role | `04_research_system/summary_vauq.md` |
| 2. Scaffold LLaVA notebook | Codex CLI | Workflow 5 | `[llava_repo]/notebooks/demo.ipynb` |
| 3. Draft direction document | OpenClaw | Paper Assistant role | `00_inbox/vlm_direction_note.md` |

#### Onboarding a new repo

| Step | Tool | Workflow | Output |
|------|------|----------|--------|
| Generate README | OpenClaw | Workflow 1 | `[repo]/README.md` |
| Create AGENTS.md | Human (template) | AGENTS_template.md | `[repo]/AGENTS.md` |

**Prerequisite for any repo task:** `AGENTS.md` must exist at the repo root. See [openclaw_spec.md](openclaw_spec.md) for required fields.

---

### Layer 3 — On-Demand Inbox Automations (OpenClaw / Claude Code MCP)

Trigger at the start of a work week or when inputs accumulate.

#### Inbox synthesis

| Source | Tool | How |
|--------|------|-----|
| Obsidian braindumps in `00_inbox/` | OpenClaw | Workflow 7 — reads files automatically |
| Gmail | Claude Code MCP | Ask Claude Code: "Synthesize my last 48h of email into `00_inbox/synthesis_YYYY-MM-DD.md`" |
| Google Drive docs | Claude Code MCP | Ask Claude Code: "Read [doc name] from Drive and extract action items into `00_inbox/`" |
| Pasted email / Google Doc text | OpenClaw | Workflow 7 — paste into `[EMAIL INPUT]` / `[GDOC INPUT]` sections |

**Output of all routes:** `00_inbox/synthesis_YYYY-MM-DD.md` — Tasks plugin picks this up in the dashboard automatically.

**After synthesis:** Review the file. Promote accepted tasks to the relevant project file with the correct emoji. Delete or archive the synthesis note.

---

### Layer 4 — On-Demand Planning (ChatGPT Planner)

Trigger at the start/end of a work week, or during any planning session.

| Task | Prompt Pattern | Output |
|------|---------------|--------|
| Weekly plan | "Here is my priority stack and open loops. Draft a 4-day work block plan." | Paste into `08_weekly_plans/week_YYYY-MM-DD.md` |
| Weekly review | "Here is what I planned vs what happened. What should I adjust?" | Paste into `10_reviews/` |
| Protocol update | "I want to change my shutdown protocol to include X. Redraft it." | Update `03_protocols/` file |
| Yes/no decision | "Apply the yes/no boundary filter to this request: [X]" | Decision noted in context |

**Note:** ChatGPT Planner does not read vault files directly. Give it context by pasting relevant sections.

---

### Layer 5 — Scheduled Automations (Optional / Future)

These run automatically on a schedule via Claude Code's `/schedule` skill.

| Automation | Frequency | What It Does |
|-----------|-----------|-------------|
| Daily inbox synthesis | Every morning | Pulls Gmail → synthesizes → writes to `00_inbox/` |
| Weekly plan scaffold | Sunday evening | Reads open tasks → drafts next week's work blocks |
| Weekly review prompt | Friday evening | Summarizes completed tasks → sends review prompt |

**Status:** Not yet activated. Run `/schedule` in Claude Code to set these up when ready.

---

## Trigger Map

"I have this situation — what do I run?"

| Situation | Action | Tool |
|-----------|--------|------|
| Starting the work week | Inbox synthesis | OpenClaw Workflow 7 or Claude Code MCP |
| Starting a TMLR work block | Results audit | OpenClaw Workflow 2 |
| Starting a VLM work block | VAUQ summary | OpenClaw Literature Scout |
| New braindump written | Process braindump | OpenClaw Workflow 6 |
| New email with action items | Email synthesis | Claude Code MCP or paste into Workflow 7 |
| New Google Doc shared | Pull doc content | Claude Code MCP |
| New experiment run | Create experiment log | OpenClaw with experiment log template |
| Manuscript review needed | Claim audit | OpenClaw Workflow 4 |
| New intern / new repo | Repo onboarding | OpenClaw Workflow 1 + create AGENTS.md |
| Weekly review | Reflection + planning | ChatGPT Planner |
| New task in inbox synthesis | Promote to project | Human — edit project file, add emoji |
| Project status changed | Update frontmatter | Human — edit `status:` field in project file |

---

## Data Flow: Inbox → Vault

```
Raw Input                    Synthesis                    Vault
─────────────────────────────────────────────────────────────────
Gmail thread          ──►
Google Drive doc      ──►  00_inbox/synthesis_YYYY.md  ──►  Human reviews
00_inbox/*.md         ──►  (Tasks plugin reads this)        │
                                                            ├──► Accepted tasks
                                                            │    promoted to
                                                            │    02_projects/*.md
                                                            │
                                                            └──► Discarded / archived
```

---

## Data Flow: Research Repo → Vault

```
Repo                         OpenClaw / Codex              Vault
────────────────────────────────────────────────────────────────
results/                ──►  Experiment Auditor       ──►  04_research_system/results_registry.md
configs/                ──►  Research Engineer        ──►  04_research_system/experiment_log_*.md
paper/manuscript        ──►  Paper Assistant          ──►  04_research_system/paper_audit_*.md
(codebase)              ──►  Codex CLI                ──►  [repo]/scripts/, [repo]/notebooks/
```

---

## What Stays Manual

These are never automated because they require Brian's judgment:

| Decision | Why it stays manual |
|----------|-------------------|
| Accepting / rejecting synthesized tasks | Only Brian knows what actually matters |
| Setting task priority | Requires context that agents don't have |
| Research direction decisions | Intellectual ownership |
| Yes/no to new commitments | Values + constraints only Brian holds |
| Promoting tasks to project files | Intentional friction — prevents noise in project files |
| Marking results as verified | Scientific integrity |
| Sending emails / messages | Communication represents Brian, not an agent |

---

## File Reference

| Document | Purpose |
|----------|---------|
| [openclaw_spec.md](openclaw_spec.md) | Full OpenClaw operating model, permissions, AGENTS.md convention |
| [codex_openclaw_workflows.md](codex_openclaw_workflows.md) | Copy-pasteable prompts for all 7 workflows |
| [agent_roles.md](agent_roles.md) | Role definitions and prompt patterns |
| [external_integrations_guide.md](external_integrations_guide.md) | Gmail, Drive, Calendar API / MCP setup |
| [plugin_setup_guide.md](plugin_setup_guide.md) | Obsidian plugin installation and task emoji reference |
| [ai_tools_inventory.md](ai_tools_inventory.md) | Tool registry and principles |
