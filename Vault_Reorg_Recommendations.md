# Vault Reorganization Recommendations

> Hand-off spec for an implementing agent. Based on a structural audit of the merged vault (2026-06-15). The three-domain merge (Home / General / PhD Manual) is in place; this document lists the cleanup needed to make it coherent. **Recovery source for any missing content: `PreMerge_Backup.zip` at the vault root (contains all original source notes).**

---

## Guiding principles

1. **One canonical location per note.** No note or project folder should exist in two domains.
2. **Strict domain separation:** Home = personal/identity/health; General = day-to-day ops + general projects; PhD Manual = all PhD/research.
3. **Identical skeleton per domain:** `Dashboard / Projects / Knowledge / People / Operations / Archive`. Each domain owns its own `Projects/` (no pooled projects).
4. **One naming convention:** TitleCase folder names; keep numeric prefixes only for intentionally-ordered sets (e.g. templates, Codex chapters).
5. **Non-destructive:** keep `PreMerge_Backup.zip` and the empty `bosho-vault/` and `The Field Manual/` shells until counts are verified.

---

## A. Flatten double-nested folders

Each of these is a folder nested inside an identically-named parent (a move-onto-existing artifact). Move children up one level, then delete the empty inner folder:

- `PhD Manual/Archive/Archive/*` → `PhD Manual/Archive/`
- `PhD Manual/Opportunities/Opportunities/*` → `PhD Manual/Opportunities/`
- `PhD Manual/People/People/*` → `PhD Manual/People/`
- `PhD Manual/Projects/Projects/*` → `PhD Manual/Projects/`
- `_Inbox/BrainDump/BrainDump/*` → `_Inbox/BrainDump/`

## B. Merge duplicate folders

- **`General/Operations/OS/` + `General/Operations/Operating_System/`** → one `General/Operations/Operating_System/`. Resolve duplicate notes (e.g. `Decision_Rules.md`) by keeping the richer version.
- **`PhD Manual/People/People_dup/`** → merge into `PhD Manual/People/`, preserving its subfolders (`Mentors`, `Target_Advisors`, `Students_Postdocs`, `Collaborators`, `Meeting_Notes`). Delete `People_dup`.
- **`_Templates/{Bosho_OS, Field_Manual, bosho-vault}/`** → one merged `_Templates/` set; de-duplicate near-identical templates (meeting note, paper note, project brief, weekly/monthly review).

## C. De-duplicate projects & fix cross-domain leakage

This is the biggest deviation from the domain model — the same projects exist in multiple places.

1. **Pick one project layout in General:** each project a single folder directly under `General/Projects/` (recommended). Eliminate the `Bosho_OS_Projects/` wrapper by moving its children up, then delete it.
2. **Move all research/PhD projects into `PhD Manual/Projects/` only** and remove their General copies: `FedProp` (`tmlr_fedprop_paper`), `VLM_Grounding` (`vlm_grounding_aaai`), `phd_preparation`, `subgraph_topology` (if research). De-duplicate against the copies already under `PhD Manual/Projects/`.
3. **Keep in `General/Projects/` only non-PhD work:** `Swyng`, `College App`, `OpenClaw`, `admin_systems`, `hobby_apps`, `acubed_colab` (verify each).
4. **End state:** no project name appears under two domains.

## D. Restore content that appears not to have landed

These destination skeletons exist but their subfolders read as **empty**, while the backup holds substantial content. Verify against `PreMerge_Backup.zip` and restore if confirmed missing:

| Folder | Notes in backup | Restore to |
|--------|----------------:|-----------|
| `Opportunity-KB` | ~30 (Apply/Skip/Stretch Rules, Fit Profile, Skills Inventory, CV Master Blocks, Positioning, Visa Strategy, Country Tiers, Why Me / Why This Lab, Professor Outreach…) | `General/Projects/Opportunities/Opportunity-KB/` |
| `Opportunity-KB/99_Legacy-OS` | ~20 (Agent + Pipeline files, Application queue, Scoring rubric) | `General/Projects/Opportunities/Opportunity-KB/99_Legacy-OS/` |
| `phd-knowledge-base` | ~40 (CV, PhD/Fellowship/Research-Engineer Profiles, SOP Draft, Motivation Letters, Scholarships, Target Programs/Professors) | `PhD Manual/Knowledge/phd-knowledge-base/` |

Also confirm Field Manual people/admin landed (Virginia Smith, Luis Teixeira, Blessed Guda, Carlee Joe-Wong, Jaime Cardoso, CMU Ecosystem, ECE Milestones, FCT Scholarship, Visa Guide).

## E. Merge duplicate files (content-level)

bosho-vault carried both snake_case and TitleCase copies of the same notes. Merge each pair (keep the richer, repoint wikilinks):

- `CV.md` ↔ `CV_Master_Blocks.md` / `CV Master Blocks.md`
- `Fit Profile.md` ↔ `Fit_Profile.md`
- `Why Me.md` ↔ `Why_Me.md`; `Why This Lab.md` ↔ `Why_This_Lab.md`
- `Cryo-ET Pipeline.md` ↔ `Cryo_ET_Pipeline.md`
- `Urban Mobility VFMs.md` ↔ `Urban_Mobility_VFMs.md`
- `Document Purpose Map.md` ↔ `Document_Purpose_Map.md`
- `Role Taxonomy.md` ↔ `Role_Taxonomy.md`
- `Positioning.md` ↔ `Positioning Statement.md`
- `People and Labs Map.md` (appears under both `Research/` and `People/` — keep one, link the other)

## F. Remove junk & decide on empty scaffolding

- Delete: `PhD Manual/Visa/Docs/~BROMIUM/` (Windows temp artifact), `General/Operations/Copilot/copilot-conversations/` and `copilot-custom-prompts/` (plugin chatter).
- Review the 2 files in `_Attic/` (looks like the old `00_dashboard.md`); keep, re-file, or move out of the vault.
- Decide on empty placeholder folders (e.g. `Archive/{Completed_Admin, Dead_Projects, Old_Plans…}`): keep as intentional skeleton or remove until needed. Recommend removing empties to reduce noise.

## G. Dashboards / entry points

- Create one canonical `00_Vault Home.md` at the root linking to the three domain dashboards.
- Give each domain a `Dashboard.md`.
- Archive the competing dashboards into `_Attic` or the relevant domain Archive: `00_dashboard.md`, `bosho-vault/00_Home`, `The Field Manual/00_Home/Home`, `PhDMaxxing OS.md`.
- Decide placement of the Field Manual planning notes (`5-YR Plan.md`, `Now.md`, `PhDMaxxing OS.md`): root entry points or `PhD Manual` / `General` Operations.

## H. Obsidian config

- Port the **Tasks** and **Templater** plugins into the main vault's `.obsidian/plugins/` (only The Field Manual had them); add both to `community-plugins.json`; point Templater at `_Templates/`. Dataview is already installed.
- Drop the leftover `.git` / `.obsidian` inside the `bosho-vault/` and `The Field Manual/` shells.

---

## Verification checklist (for the implementing agent)

1. Note count reconciles to backup minus intentional dedup; nothing orphaned.
2. No folder nested inside an identically-named folder (Section A clear).
3. No project folder present in two domains (Section C clear).
4. `Opportunity-KB`, `Opportunity-KB/99_Legacy-OS`, `phd-knowledge-base` subfolders are populated — compare counts to backup (Section D).
5. Duplicate-file pairs from Section E resolved; wikilinks updated, no new unresolved links.
6. Junk removed (Section F); naming convention applied consistently (Section F/principle 4).
7. Plugins load; each domain Dashboard and the root home note render.
8. `PreMerge_Backup.zip` and the source shells retained until 1–7 pass; then decommission.

