# Bosho OS: Central Dashboard

> **Mantra:** Hard days hard. Rest days real. Work bounded. Sleep protected. Old loops closed. Future direction built.

> [!info] Requires **Dataview** + **Tasks** plugins → [Plugin Setup Guide](07_ai_tools_agents/plugin_setup_guide.md)

---

## 🗂️ Active Projects

```dataview
TABLE WITHOUT ID
  link(file.link, title) as "Project",
  priority as "P",
  epic_active as "Active Epic",
  deadline as "Deadline",
  time_budget_weekly as "hrs/wk"
FROM "02_projects"
WHERE status = "active"
SORT priority ASC
```

---

## 🎯 Next Actions

```tasks
not done
path includes 02_projects
priority is highest
sort by path
```

---

## 📋 All Open Tasks

```tasks
not done
path includes 02_projects
group by filename
sort by priority
sort by due
```

---

## ✅ Completed This Week

```tasks
done after 2026-06-07
path includes 02_projects
group by filename
```

---

## ⚡ Protocols & Routines

- 🌅 **Startup:** [workday_protocol.md](03_protocols/workday_protocol.md)
- 🧠 **Deep Work:** [deep_work_block_protocol.md](03_protocols/deep_work_block_protocol.md)
- 📴 **Shutdown:** [shutdown_protocol.md](03_protocols/shutdown_protocol.md)
- 🔋 **Rest & Restore:** [rest_day_protocol.md](03_protocols/rest_day_protocol.md)
- 🔍 **Boundary Filter:** [yes_no_boundary_filter.md](03_protocols/yes_no_boundary_filter.md)
- 📥 **Inbox Synthesis:** [inbox_synthesis_protocol.md](03_protocols/inbox_synthesis_protocol.md)

---

## 🏥 Health & Recovery

- **Dashboard:** [recovery_health_dashboard.md](06_health_recovery/recovery_health_dashboard.md)
- **Psychiatric:** [psychiatric_monitoring.md](06_health_recovery/psychiatric_monitoring.md)
- **Meditation:** [meditation_and_psychology.md](06_health_recovery/meditation_and_psychology.md)
- **Media Queue:** [recreation_media_tracker.md](06_health_recovery/recreation_media_tracker.md)

---

## 🤝 Key Connections

| Person | Action Needed |
|--------|---------------|
| Carlee | Draft questions on dataset inclusion and reconstruction errors |
| M | Weekly call check-in — subgraph topology interest |
| B2 | Recruit for Swyng business/social operations |
| Pivotal | Check email and respond 🔺 |

[People Index →](05_people_network/people_index.md) | [Email Templates →](05_people_network/email_templates.md)

---

## 📅 This Week

[Week 2026-06-08 →](08_weekly_plans/week_2026_06_08_starter.md) | [Research Dashboard →](04_research_system/research_dashboard.md)

---

## 🗺️ Resource Map

```
Bosho OS (Vault Root)
│
├── 00_dashboard.md ← YOU ARE HERE
│
├── 00_inbox/ ───────────── Raw inputs, braindumps, email synthesis
├── 01_operating_system/ ── Master plan, decision rules, weekly rhythm
├── 02_projects/ ─────────── Active project logs (Dataview-indexed)
│   ├── tmlr_fedprop_paper.md      [P1]
│   ├── vlm_grounding_aaai.md      [P2] ← deadline Jul 21
│   ├── phd_preparation.md         [P2]
│   ├── acubed_colab.md            [P3] ← 10h/wk cap
│   └── swyng.md                   [P4] ← 5h/wk cap
├── 03_protocols/ ─────────── Execution guides (workday, shutdown, rest)
├── 04_research_system/ ───── Experiment logs, results registry
├── 05_people_network/ ────── CRM, contacts, email templates
├── 06_health_recovery/ ───── Health, psychiatric, media queue
├── 07_ai_tools_agents/ ───── AI workflows, MCP integrations
│   ├── automation_spec.md     ← full automation map
│   ├── openclaw_spec.md       ← OpenClaw operating model
│   └── plugin_setup_guide.md  ← Obsidian plugin install
├── 08_weekly_plans/ ──────── Current & past week plans
├── 09_templates/ ─────────── Reusable templates
└── 10_reviews/ ───────────── Weekly reviews
```
