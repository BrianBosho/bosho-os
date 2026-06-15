# Unified Vault Merge Strategy — Domain Model

> Status: **Strategy / planning only — nothing has been moved.** Reflects the vaults as they actually exist on disk (verified 2026-06-15) and the domain-first architecture you specified.

---

## 1. Organizing principle

The vault is split into **three top-level domains**, each self-contained and following the **same internal skeleton**. Projects are **not** pooled into one folder — every domain owns its own `Projects/`, and projects may nest sub-projects.

| Domain | Holds |
|--------|-------|
| **Home** | Personal information, identity, "about me as a human," health, spiritual, personal projects. |
| **General** | Day-to-day operations, schedules, life-OS, career/opportunities, general projects. The **default launchpad for new projects.** |
| **PhD Manual** | Everything PhD: research, projects, advisors/people, program admin, fellowships. |

**Project promotion lifecycle:** a new project starts as a folder in `General/Projects/`. When it matures, it branches out — first into its parent domain's `Projects/`, and eventually it can be promoted to its **own top-level domain** (a 4th, 5th… sibling of Home/General/PhD Manual). The folder layout is designed so promotion is a single move, not a restructure.

### Decisions locked from earlier
1. **Source subfolders during import** — imported folders land in labeled per-vault subfolders so nothing overwrites; cleanup/flattening happens after.
2. **Keep originals untouched until verified** — `bosho-vault/` and `The Field Manual/` stay in place until the merged vault is confirmed working.
3. **Port plugins** — install Tasks + Templater into the main vault.

---

## 2. Current state (ground truth)

All three are git repos; `bosho-vault/` and `The Field Manual/` currently sit *inside* the `Bosho OS` folder as nested repos.

| Vault | Notes | `.obsidian` | Maps mostly to |
|-------|------:|-------------|----------------|
| `Bosho OS/` (main) | 95 | Yes (copilot, dataview, calendar, kanban, git…) | **General** + Home |
| `bosho-vault/` | 310 | No | **Home** (Codex/Spiritual) + **PhD** (Research) + General |
| `The Field Manual/` | 59 | Yes (dataview, **tasks**, **templater**) | **PhD Manual** |

**Total to reconcile: 464 notes.** Convenient alignment: The Field Manual ≈ the PhD Manual domain already; bosho-vault's Codex/Spiritual ≈ Home; the main vault ≈ General.

---

## 3. Target architecture

```
Vault root/
├── 00_Vault Home.md            ← master map, links to the 3 domain dashboards
├── _Inbox/                     ← single frictionless capture point; triaged into domains
├── _Templates/                 ← shared templates (incl. ported Templater templates)
├── _Attic/                     ← raw data/automation not part of any domain (scripts, dumps)
│
├── Home/
│   ├── Dashboard.md
│   ├── Projects/               → Project/ → Sub-project/
│   ├── Knowledge/              (Codex, identity, spiritual, reference)
│   ├── People/
│   ├── Operations/             (journal, reviews, personal routines)
│   └── Archive/
│
├── General/
│   ├── Dashboard.md
│   ├── Projects/               ← default home for new/immature projects
│   ├── Knowledge/
│   ├── People/                 (network, contacts)
│   ├── Operations/             (life-OS, protocols, schedules, weekly plans, AI tools)
│   └── Archive/
│
└── PhD Manual/
    ├── Dashboard.md
    ├── Projects/               (Active, Candidates, Sparks)
    ├── Knowledge/              (research notes, concepts, reading, phd-knowledge-base)
    ├── People/                 (advisors, mentors, students)
    ├── Operations/             (program admin, milestones, research system)
    ├── Opportunities/          (fellowships, industry plans)
    └── Archive/
```

The skeleton is deliberately identical across domains (`Dashboard / Projects / Knowledge / People / Operations / Archive`) so each domain feels the same and a project can be lifted out cleanly when promoted.

---

## 4. Domain mapping (every source folder)

Imports keep their `_from_bosho-vault/` or `_from_field-manual/` source-subfolder label inside the destination until the post-merge cleanup pass.

### → HOME
| Source | Destination |
|--------|-------------|
| `bosho-vault/01_Codex/` | `Home/Knowledge/Codex/` |
| `bosho-vault/07_Spiritual/` | `Home/Knowledge/Spiritual/` |
| `bosho-vault/09_Decisions/` | `Home/Knowledge/Decisions/` |
| `Bosho OS/06_health_recovery/` | `Home/Knowledge/Health/` |
| `Bosho OS/11_journal/`, `10_reviews/` | `Home/Operations/` (journal, reviews) |
| `bosho-vault/02_Daily/` | `Home/Operations/Daily/` |
| `The Field Manual/06_Life_OS/` | `Home/Operations/` (wellbeing protocols) |
| `bosho-vault/00_Home.md`, `Welcome.md` | `Home/Dashboard.md` candidates |

### → GENERAL
| Source | Destination |
|--------|-------------|
| `Bosho OS/02_projects/` | `General/Projects/` |
| `bosho-vault/11_Projects/Swyng/` | `General/Projects/Swyng/` |
| `bosho-vault/BrainDump/03 Projects/`, `04 Operations/` (College App, OpenClaw) | `General/Projects/` |
| `Bosho OS/01_operating_system/`, `03_protocols/` | `General/Operations/` |
| `bosho-vault/04_Operating_System/`, `10_Indexes/`, `_meta/`, `_synthesis/` | `General/Operations/` |
| `Bosho OS/08_weekly_plans/` | `General/Operations/Weekly Plans/` |
| `Bosho OS/07_ai_tools_agents/`, `copilot/` | `General/Operations/AI Tools/` |
| `Bosho OS/05_people_network/` | `General/People/` |
| `bosho-vault/Opportunity-KB/`, `Opportunity-OS/` | `General/Projects/Opportunities/` (career/job hunt) |

### → PhD MANUAL
| Source | Destination |
|--------|-------------|
| `The Field Manual/02_Projects/` (Active/Candidates/Sparks) | `PhD Manual/Projects/` |
| `bosho-vault/11_Projects/` (CMU_Portugal_PhD, FedProp, VLM_Grounding) | `PhD Manual/Projects/` |
| `The Field Manual/01_Research/` | `PhD Manual/Knowledge/` |
| `bosho-vault/05_Research/`, `12_Research/`, `08_Concepts/`, `phd-knowledge-base/` | `PhD Manual/Knowledge/` |
| `The Field Manual/03_People/` | `PhD Manual/People/` |
| `bosho-vault/06_People/` (Bhiksha Raj, Virginia Smith) | `PhD Manual/People/` |
| `The Field Manual/04_Program_Admin/` | `PhD Manual/Operations/Program Admin/` |
| `Bosho OS/04_research_system/`, `bosho-vault/05_Research/*System*` | `PhD Manual/Operations/Research System/` |
| `The Field Manual/05_Opportunities/` | `PhD Manual/Opportunities/` |
| `The Field Manual/09_Archive/` | `PhD Manual/Archive/` |

### → ROOT SCAFFOLDING
| Source | Destination |
|--------|-------------|
| `Bosho OS/00_inbox/`, `Unprocessed/`; `bosho-vault/BrainDump/`, `braindump-readme.md`; `The Field Manual/{BrainDump, Inbox, 2026-06-09}.md` | `_Inbox/` |
| `Bosho OS/09_templates/`, `bosho-vault/_templates/`, `The Field Manual/07_Templates/`, `The Field Manual/00_Home/*Template*` | `_Templates/` |
| `bosho-vault/scripts/`, `processed/`, `_gdrive_raw/`, `Tasks-Archive/`, `_archive/` | `_Attic/` (data/automation/old dumps) |
| `Bosho OS/00_dashboard.md`; `The Field Manual/{5-YR Plan, Now, PhDMaxxing OS}.md` | `00_Vault Home.md` + per-domain dashboards (see Judgment Calls) |
| redundant `README.md` from the two sources | `_Attic/` or discard; keep main README |

---

## 5. Plugins, git & backup

**Plugins:** keep the main `Bosho OS/.obsidian` as the single config. Copy `obsidian-tasks-plugin` and `templater-obsidian` from The Field Manual into `Bosho OS/.obsidian/plugins/`, add both to `community-plugins.json`, and point Templater's template folder at `_Templates/`. Dataview is already installed.

**Git/backup:** the main `Bosho OS` repo is the one we keep. On import, drop the nested `.git`/`.obsidian` of the sources (originals retain their own history in place as backup, per decision #2). Commit before Phase 1 and after each phase. Optional: zip both sources before starting.

---

## 6. Execution sequence (for later — not now)

- **Phase 0 — Backup:** commit/tag all three repos; optional zip of the two sources.
- **Phase 1 — Scaffold:** create root (`00_Vault Home`, `_Inbox`, `_Templates`, `_Attic`) and the three domains with the common skeleton; port Tasks + Templater.
- **Phase 2 — Populate Home** from the mapping (source-subfolders).
- **Phase 3 — Populate General.**
- **Phase 4 — Populate PhD Manual.**
- **Phase 5 — Root reconcile:** dashboards, planning files, inbox.
- **Phase 6 — Open in Obsidian**, rebuild index, spot-check links, confirm Dataview/Tasks/Templater work.
- **Phase 7 — (optional) cleanup:** dedup the 8 colliding filenames, flatten `_from_*` subfolders within each domain.
- **Phase 8 — Decommission originals** only after verification.

---

## 7. Verification plan

1. **Count reconciliation:** 464 notes accounted for, nothing orphaned.
2. **No unmapped items:** every source top-level folder and root file lands somewhere.
3. **Domain integrity:** each domain has the full skeleton and its own `Projects/`; no project pooled across domains.
4. **Link integrity:** no new unresolved links beyond the known 8 collisions.
5. **Plugins load:** Dataview, Tasks, Templater initialize; sample queries/templates render.
6. **Originals intact** until all of the above pass.

---

## 8. Judgment calls — tell me to flip any of these

These are reasonable defaults I chose where content could sit in more than one domain:

1. **Daily notes / journal / reviews → Home/Operations.** (Could instead be General if you consider them operational rather than personal.)
2. **Career & job-hunt (`Opportunity-KB/OS`) → General/Projects/Opportunities.** (PhD fellowships from The Field Manual stay in `PhD Manual/Opportunities`. You may prefer all opportunities in one place.)
3. **`Life_OS` wellbeing protocols (Anti-Burnout, Aliveness…) → Home/Operations.** (They live in the PhD field manual today; could stay under PhD Manual.)
4. **`research_system` → PhD Manual/Operations.** (Could be General if it's a generic research workflow.)
5. **AI tools / copilot / scripts → General/Operations + `_Attic`.** (Could be their own top-level "Tools" domain.)
6. **Project splits:** Swyng + College App + OpenClaw → General; CMU Portugal PhD / FedProp / VLM Grounding → PhD Manual. Confirm these land in the right domain.
7. **Inbox & Templates: shared at root** vs. one per domain.

---

## 9. Still open (carried over)

- **Canonical dashboards:** pick the entry note for each domain from the competing candidates (`00_dashboard`, `bosho-vault/00_Home`, `Field Manual/00_Home/Home`, `PhDMaxxing OS`).
- **Non-note data** (`scripts`, `processed`, `_gdrive_raw`): keep in `_Attic` inside the vault, or move out of the vault entirely?
