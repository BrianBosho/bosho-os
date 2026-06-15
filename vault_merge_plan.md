# Vault Merge Plan
*Generated: 2026-06-15*

---

## Current State

Three vaults currently exist inside `Bosho OS/`:

| Vault | Purpose | Status |
|---|---|---|
| **Bosho OS** (root) | Summer 2026 operational system | Active, seasonal |
| **bosho-vault** | Master personal knowledge base | Older, most permanent content |
| **The Field Manual** | PhD-specific operating system | Most current PhD content |

**Core problem:** Three competing home pages, three dashboards, three operating systems, overlapping research notes, and three separate git repos nested inside each other.

---

## New Structure

One Obsidian vault at `Bosho OS/`. Everything below is a folder within that single vault. Numbered prefixes enforce display order; `_` prefix keeps utilities at the top.

```
Bosho OS/
│
├── _meta/                  ← vault conventions (from bosho-vault/_meta)
├── _templates/             ← all templates merged
├── _archive/               ← deprecated/inactive content from all three vaults
│
├── Home.md                 ← single master home (replaces three competing files)
├── Now.md                  ← current focus snapshot
├── Inbox.md                ← single capture point
│
├── 01_self/                ← permanent identity layer (timeless)
│   ├── Codex/
│   ├── Spiritual/
│   ├── Concepts/
│   └── Decisions/
│
├── 02_os/                  ← how you operate daily (recurring)
│   ├── [core OS docs]
│   └── protocols/
│
├── 03_phd/                 ← PhD domain (The Field Manual, relocated)
│   ├── [PhD Constitution, 5-YR Plan]
│   ├── research/
│   ├── projects/
│   ├── people/
│   ├── program_admin/
│   └── opportunities/
│
├── 04_projects/            ← active side/life projects
│
├── 05_people/              ← personal/family/social relationships
│
├── 06_health/              ← health & recovery tracking
│
├── 07_knowledge/           ← concepts, indexes, accumulated knowledge
│
├── 08_ai_tools/            ← agent setups, Cowork, OpenClaw workflows
│
├── 09_periodic/            ← time-stamped content
│   ├── daily/
│   ├── weekly/
│   ├── reviews/
│   └── journal/
│
└── 10_seasonal/            ← time-boxed working periods
    └── 2026_summer/        ← current Bosho OS seasonal content
```

---

## Content Mapping: What Goes Where

### `_meta/`
| Source | File | Action |
|---|---|---|
| bosho-vault/_meta/ | Agent_Instructions.md | Move here — becomes vault-wide |
| bosho-vault/_meta/ | Archival_Rules.md | Move here |
| bosho-vault/_meta/ | Frontmatter_Convention.md | Move here |
| bosho-vault/_meta/ | Tagging_Convention.md | Move here |

---

### `_templates/`
| Source | File | Action |
|---|---|---|
| Bosho OS/09_templates/ | daily_note_template.md | Move → rename `daily_note.md` |
| Bosho OS/09_templates/ | weekly_plan_template.md | Move → rename `weekly_plan.md` |
| Bosho OS/09_templates/ | project_template.md | Move → rename `project_brief.md` |
| Bosho OS/09_templates/ | braindump_processing_template.md | Move |
| Bosho OS/09_templates/ | daily_work_block_template.md | Move |
| Field Manual/07_Templates/ | Template - Paper Note.md | Move → rename `paper_note.md` |
| Field Manual/07_Templates/ | Template - Meeting Note.md | Move → rename `meeting_note.md` |
| Field Manual/07_Templates/ | Template - Altitude Check.md | Move → rename `altitude_check.md` |
| Field Manual/07_Templates/ | Template - Project Brief.md | Compare with Bosho OS version, keep best |
| Bosho OS/04_research_system/ | experiment_log_template.md | Move here |
| Bosho OS/04_research_system/ | results_registry_template.md | Move here |

---

### Root files: `Home.md`, `Now.md`, `Inbox.md`

**Home.md** — write new. Single entry point linking to:
- Now.md
- 03_phd/ dashboard
- 04_projects/ index
- 09_periodic/weekly/
- 06_health/ dashboard

**Now.md** — take from Field Manual/Now.md (most current).

**Inbox.md** — take from Field Manual/Inbox.md. Merge any open items from:
- Bosho OS/00_inbox/
- bosho-vault/BrainDump/00 Inbox/ (active items only)
- Field Manual/BrainDump.md

---

### `01_self/` — Permanent identity layer

All content from **bosho-vault** only. Nothing from Bosho OS or Field Manual overlaps this uniquely.

| Source | Destination |
|---|---|
| bosho-vault/01_Codex/ (11 files) | 01_self/Codex/ |
| bosho-vault/07_Spiritual/ (5 files + philosophy/) | 01_self/Spiritual/ |
| bosho-vault/08_Concepts/ | 01_self/Concepts/ |
| bosho-vault/09_Decisions/ | 01_self/Decisions/ |

---

### `02_os/` — Daily operating system

**Conflict:** Three vaults each have OS docs. Resolution:
- bosho-vault/04_Operating_System/ = general OS (best foundation for timeless rules)
- Field Manual/06_Life_OS/ = PhD-life-specific protocols (move to 02_os, not buried in 03_phd)
- Bosho OS/01_operating_system/ = summer-specific → goes to 10_seasonal/

| Source | Destination | Notes |
|---|---|---|
| bosho-vault/04_OS/Operating_Manual.md | 02_os/Operating_Manual.md | Primary version |
| bosho-vault/04_OS/Daily_System.md | 02_os/Daily_System.md | |
| bosho-vault/04_OS/Decision_Rules.md | 02_os/Decision_Rules.md | Compare with Bosho OS version |
| bosho-vault/04_OS/Deep_Work_System.md | 02_os/Deep_Work_System.md | |
| bosho-vault/04_OS/Recovery_System.md | 02_os/Recovery_System.md | |
| bosho-vault/04_OS/Recovery_System_Extended.md | 02_os/Recovery_System_Extended.md | |
| Field Manual/06_Life_OS/Aliveness_Plan.md | 02_os/Aliveness_Plan.md | |
| Field Manual/06_Life_OS/Anti_Burnout_Protocol.md | 02_os/Anti_Burnout_Protocol.md | |
| Field Manual/06_Life_OS/Anti_Isolation_Protocol.md | 02_os/Anti_Isolation_Protocol.md | |
| Field Manual/06_Life_OS/Anti_Regret_List.md | 02_os/Anti_Regret_List.md | |
| Bosho OS/03_protocols/ (7 files) | 02_os/protocols/ | Keep all — these are detailed and good |
| Bosho OS/01_os/decision_rules.md | **Review vs bosho-vault version** | Keep most current, archive other |

---

### `03_phd/` — The Field Manual, relocated

The Field Manual is the most current and best-structured PhD system. It moves largely intact. The key additions are absorbing relevant content from bosho-vault.

#### `03_phd/` root
| Source | Destination |
|---|---|
| Field Manual/00_Home/PhD_Constitution.md | 03_phd/PhD_Constitution.md |
| Field Manual/00_Home/Dashboard.md | 03_phd/PhD_Dashboard.md |
| Field Manual/PhDMaxxing OS.md | 03_phd/PhD_Map.md (rename) |
| Field Manual/5-YR Plan.md | 03_phd/5_YR_Plan.md |
| Field Manual/00_Home/Weekly Review Template.md | → _templates/ |
| Field Manual/00_Home/Monthly Review Template.md | → _templates/ |

#### `03_phd/research/`
| Source | Destination | Notes |
|---|---|---|
| Field Manual/01_Research/ (all 12 files) | 03_phd/research/ | Primary — most current |
| bosho-vault/05_Research/Research_Direction.md | Compare with Field Manual version | Archive if superseded |
| bosho-vault/05_Research/Research_Identity.md | Compare with Field Manual version | Archive if superseded |
| bosho-vault/05_Research/PhD_Strategy.md | 03_phd/research/PhD_Strategy.md | Likely unique — keep |
| bosho-vault/05_Research/Artifact_Pipeline.md | 03_phd/research/Artifact_Pipeline.md | |
| bosho-vault/05_Research/Collaboration_System.md | 03_phd/research/Collaboration_System.md | |
| bosho-vault/05_Research/Technical_Skill_Development.md | 03_phd/research/Technical_Skill_Dev.md | |
| bosho-vault/12_Research/ | 03_phd/research/ | Merge VLM_Grounding.md content into Field Manual's version |
| bosho-vault/BrainDump/02 Research/ | 03_phd/research/ | FedProp notes + VLM Phase 2 notes → keep |
| Bosho OS/04_research_system/research_dashboard.md | Compare with Field Manual Research Dashboard | Archive if superseded |

#### `03_phd/projects/`
| Source | Destination |
|---|---|
| Field Manual/02_Projects/ (all files, Active/, Candidates/, Sparks/) | 03_phd/projects/ |
| bosho-vault/11_Projects/VLM_Grounding/ | Merge into 03_phd/projects/Active/ |
| bosho-vault/11_Projects/FedProp/ | 03_phd/projects/FedProp/ |
| bosho-vault/BrainDump/02 Research/FedProp/ | Merge into 03_phd/projects/FedProp/ |
| Bosho OS/02_projects/vlm_grounding_aaai/ | Merge into 03_phd/projects/Active/ |
| Bosho OS/02_projects/tmlr_fedprop_paper/ | 03_phd/projects/FedProp/ |

#### `03_phd/people/`
**Conflict:** Virginia Smith appears in bosho-vault/06_People AND Field Manual/03_People/Target_Advisors/. Merge: Field Manual version is PhD-context; bosho-vault version may have personal/relationship notes. Read both and combine.

| Source | Destination |
|---|---|
| Field Manual/03_People/ (all) | 03_phd/people/ |
| bosho-vault/06_People/Bhiksha_Raj.md | 03_phd/people/Mentors/ |
| bosho-vault/06_People/Virginia_Smith.md | Merge with Field Manual/03_People/Target_Advisors/Virginia_Smith.md |

#### `03_phd/program_admin/`
| Source | Destination |
|---|---|
| Field Manual/04_Program_Admin/ (all) | 03_phd/program_admin/ |

#### `03_phd/opportunities/`
**Decision:** bosho-vault/Opportunity-KB/99_Legacy-OS is the v2 (more sophisticated) version; General/Projects/Opportunities/Opportunity-KB is v1 (older). Field Manual/05_Opportunities/ has forward-looking plans.

| Source | Destination | Notes |
|---|---|---|
| bosho-vault/Opportunity-KB/99_Legacy-OS/ (all) | 03_phd/opportunities/ | Primary — most complete |
| Field Manual/05_Opportunities/Opportunity_Calendar.md | 03_phd/opportunities/ | |
| Field Manual/05_Opportunities/May_2027_Industry_Plan.md | 03_phd/opportunities/ | |
| Field Manual/05_Opportunities/Application_Materials_Bank.md | Merge with Opportunity-KB/99_Legacy-OS/02_Assets/ | |
| General/Projects/Opportunities/Opportunity-KB/ | → _archive/opportunity-kb-v1/ | Superseded by Opportunity-KB/99_Legacy-OS |

---

### `04_projects/` — Active side/life projects

| Source | Destination |
|---|---|
| Bosho OS/02_projects/openclaw/ | 04_projects/openclaw/ |
| Bosho OS/02_projects/swyng/ | 04_projects/swyng/ |
| Bosho OS/02_projects/acubed_colab/ | 04_projects/acubed_colab/ |
| Bosho OS/02_projects/hobby_apps/ | 04_projects/hobby_apps/ |
| Bosho OS/02_projects/admin_systems/ | 04_projects/admin_systems/ |
| Bosho OS/02_projects/subgraph_topology/ | 04_projects/subgraph_topology/ |
| Bosho OS/02_projects/phd_preparation/ | → _archive/ (preparation phase is done) |
| bosho-vault/BrainDump/03 Projects/College_App/ | 04_projects/college_app/ |
| bosho-vault/BrainDump/04 Operations/OpenClaw/ | Merge into 04_projects/openclaw/ |
| Bosho OS/02_projects/active_projects_index.md | 04_projects/index.md |
| bosho-vault/11_Projects/Swyng/ | Merge into 04_projects/swyng/ |
| bosho-vault/11_Projects/CMU_Portugal_PhD/ | → _archive/ or merge into 03_phd/program_admin/ |

---

### `05_people/` — Personal/family/social relationships

| Source | Destination |
|---|---|
| Bosho OS/05_people_network/ | 05_people/ |
| (PhD-specific people go in 03_phd/people/, not here) | |

---

### `06_health/` — Health & recovery

| Source | Destination |
|---|---|
| Bosho OS/06_health_recovery/ (all) | 06_health/ |

---

### `07_knowledge/` — Accumulated concepts and indexes

| Source | Destination |
|---|---|
| bosho-vault/10_Indexes/Open_Questions_Index.md | 07_knowledge/ |
| bosho-vault/10_Indexes/Topic_Index.md | 07_knowledge/ |

*Note: Individual concept notes live in 01_self/Concepts/. This folder is for cross-domain indexes and maps.*

---

### `08_ai_tools/` — Agent tools and workflows

| Source | Destination |
|---|---|
| Bosho OS/07_ai_tools_agents/ (all) | 08_ai_tools/ |
| Bosho OS/copilot/ | 08_ai_tools/copilot/ |
| bosho-vault/BrainDump/04 Operations/OpenClaw/ | Merge into 04_projects/openclaw/ (not here) |
| bosho-vault/Opportunity-KB/99_Legacy-OS/06_Agents/ | Stays in 03_phd/opportunities/agents/ — they're domain-specific |

---

### `09_periodic/` — Time-stamped content

| Source | Destination |
|---|---|
| bosho-vault/02_Daily/ (10 daily notes, May 2026) | 09_periodic/daily/ |
| Field Manual/2026-06-09.md | 09_periodic/daily/ |
| Bosho OS/08_weekly_plans/ | 09_periodic/weekly/ |
| Bosho OS/10_reviews/ | 09_periodic/reviews/ |
| Bosho OS/11_journal/ | 09_periodic/journal/ |

---

### `10_seasonal/2026_summer/` — Current season

| Source | Destination |
|---|---|
| Bosho OS/01_operating_system/summer_2026_operating_plan.md | 10_seasonal/2026_summer/ |
| Bosho OS/01_operating_system/vault_usage_rules.md | 10_seasonal/2026_summer/ |
| Bosho OS/01_operating_system/weekly_rhythm_4_work_3_rest.md | 10_seasonal/2026_summer/ |
| bosho-vault/BrainDump/06 Planning/ | 10_seasonal/2026_summer/planning/ |
| bosho-vault/BrainDump/00 Inbox/ (Workbook q2 wk1) | 10_seasonal/2026_summer/workbooks/ |

*When summer ends: move entire 2026_summer/ to _archive/.*

---

### `_archive/` — What gets retired

| Content | Archive path | Reason |
|---|---|---|
| bosho-vault/phd-knowledge-base/ | _archive/phd-application-era/ | Pre-enrollment content (SOPs, application status, motivation letters) |
| General/Projects/Opportunities/Opportunity-KB/ | _archive/opportunity-kb-v1/ | Superseded by Opportunity-KB/99_Legacy-OS |
| bosho-vault/BrainDump/ (processed content) | _archive/braindump-legacy/ | Already processed |
| bosho-vault/processed/ | _archive/ | By definition done |
| bosho-vault/_gdrive_raw/ | _archive/ | Raw imports |
| bosho-vault/_synthesis/ | Review — if active, keep; if stale, archive | |
| Bosho OS/02_projects/phd_preparation/ | _archive/ | Preparation phase is over |
| Field Manual/09_Archive/ | _archive/field-manual-archive/ | |
| bosho-vault/11_Projects/CMU_Portugal_PhD/ | _archive/ | Now enrolled — was tracking the application |

---

## Conflict Resolution Notes

### Decision Rules (three versions exist)
- Bosho OS: `01_operating_system/decision_rules.md`
- bosho-vault: `04_Operating_System/Decision_Rules.md`
- Field Manual: doesn't have one (deferred to PhD Constitution)

**Action:** Read both Bosho OS and bosho-vault versions. They likely evolved from each other. Create one merged `02_os/Decision_Rules.md` with the most current logic. Archive the others.

### Research Dashboard (two versions)
- Bosho OS: `04_research_system/research_dashboard.md`
- Field Manual: `01_Research/Research_Dashboard.md`

**Action:** Field Manual version wins (more current, better structured). Archive Bosho OS version.

### Virginia Smith (two notes)
- bosho-vault/06_People/Virginia_Smith.md
- Field Manual/03_People/Target_Advisors/Virginia_Smith.md

**Action:** Read both. Merge into single note at `03_phd/people/Target_Advisors/Virginia_Smith.md`. One person, one note.

### Operating Manual (two versions)
- bosho-vault: `04_Operating_System/Operating_Manual.md`
- Field Manual: PhD Constitution covers the PhD-specific rules

**Action:** bosho-vault version → `02_os/Operating_Manual.md` (general life OS). Field Manual PhD Constitution stays at `03_phd/PhD_Constitution.md`. These serve different purposes — no conflict.

---

## Git Strategy

Currently: three separate `.git` repos nested inside one folder. This causes problems if you ever run git commands at the root level.

**Recommendation:**
1. After the merge, initialize one git repo at the `Bosho OS/` root (if you want version control).
2. Remove `.git` from `bosho-vault/` and `The Field Manual/` subdirectories (they'll no longer be standalone repos — their history is preserved in their remote if needed).
3. Or: keep all three separate git remotes and just don't track them from the root. Obsidian doesn't care about git — only your backup workflow does.

If you're using Obsidian Sync instead of git, this is a non-issue.

---

## Execution Order

Do this in phases. Each phase is safe to stop after.

### Phase 0: Backup (before anything)
- Copy entire `Bosho OS/` folder to a backup location or push all three git repos to their remotes.

### Phase 1: Scaffold the new structure
Create the empty folder skeleton: `_meta/`, `_templates/`, `_archive/`, `01_self/` through `10_seasonal/`. No files moved yet.

### Phase 2: Move non-overlapping content (easy wins)
In order:
1. `_meta/` ← bosho-vault/_meta/ (4 files, no conflicts)
2. `01_self/` ← bosho-vault/Codex, Spiritual, Concepts, Decisions
3. `06_health/` ← Bosho OS/06_health_recovery/ (no conflicts)
4. `09_periodic/` ← daily notes, weekly plans, reviews, journal
5. `08_ai_tools/` ← Bosho OS/07_ai_tools_agents/ + copilot/
6. `10_seasonal/2026_summer/` ← Bosho OS seasonal operating content
7. `07_knowledge/` ← bosho-vault/10_Indexes/

### Phase 3: Migrate The Field Manual → 03_phd/
Move Field Manual content into the new `03_phd/` folder structure. This is the cleanest migration — almost no conflicts with its own content.

### Phase 4: Absorb bosho-vault into 03_phd/ (overlapping content)
This is where you read and compare:
- Research notes: bosho-vault/05_Research/ and /12_Research/ vs Field Manual/01_Research/
- People notes: bosho-vault/06_People/ vs Field Manual/03_People/
- Opportunity-KB/99_Legacy-OS into 03_phd/opportunities/

### Phase 5: Migrate side projects → 04_projects/
Move Bosho OS/02_projects/ non-PhD projects. Merge any bosho-vault BrainDump project notes.

### Phase 6: Templates
Merge all templates into _templates/. Compare duplicates, keep the better version.

### Phase 7: Archive
Move everything that was decided for archival. This cleans up the root.

### Phase 8: Build the new Home.md
Write a single master Home.md that links out to all domains.

### Phase 9: Update internal links
Obsidian's built-in link updater handles most renames automatically if you move files within an open vault. Do all moves from within Obsidian (drag in the file explorer), not from your OS file manager, so links update automatically.

---

## What the Vault Looks Like When Done

```
Bosho OS/
├── _meta/                    (4 files: conventions, archival rules, frontmatter, tagging)
├── _templates/               (~10 files: all templates unified)
├── _archive/                 (retired content, untouched)
│
├── Home.md                   ← open this every day
├── Now.md                    ← what you're focused on right now
├── Inbox.md                  ← capture everything here
│
├── 01_self/                  (Codex 11 files, Spiritual 5, Concepts 2, Decisions 3)
├── 02_os/                    (OS docs + 7 protocols)
├── 03_phd/                   (research, projects, people, program admin, opportunities)
├── 04_projects/              (OpenClaw, Swyng, Acubed, hobby apps, etc.)
├── 05_people/                (personal network)
├── 06_health/                (recovery dashboard, psychiatric, meditation, media)
├── 07_knowledge/             (open questions index, topic index)
├── 08_ai_tools/              (agent manual, roles, tools, OpenClaw spec, copilot)
├── 09_periodic/              (daily notes, weekly plans, reviews, journal)
└── 10_seasonal/
    └── 2026_summer/          (summer plan, workbooks, weekly rhythm)
```

Total: one vault, one Obsidian config, one sync setup, one plugin install.

