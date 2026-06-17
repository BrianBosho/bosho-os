---
title: Vault Reorganization & Redundancy Proposal
type: control-proposal
created: 2026-06-17
status: proposal-awaiting-approval
tags: [control, reorg, redundancy, vault]
---

# Vault Reorganization & Redundancy Proposal

Audit of the full vault with a focus on the three named archive folders
(`old_methods`, `old_direction_notes`, `old_paper_tracks`) and whether the same
information (records, ideas, concepts, methodology, plans) lives in more than one
place. Nothing here has been executed yet — this is the plan for approval.

---

## Headline findings

1. **The archives are mostly already absorbed.** The direction notes live on in
   `70_ideas/synthesis.md`, `70_ideas/developed.md`, and
   `20_hypotheses/future_hypotheses.md`; the methods live on in
   `30_methods/canonical_method.md` and `10_paper/PAPER_TRACK_FROZEN_v2.md`.
   Only **three fragments** carry unique content that was never migrated (see §3).

2. **The active redundancy is worse than the archive redundancy.** Three
   overlapping paper specs sit in `10_paper/` at once, and two files each *claim*
   to be "canonical" for the method. This is the main thing to fix.

3. **Two "canonical" labels conflict.** Archived
   `old_methods/GROUNDING_METHODOLOGY.md` still says "This is the canonical
   methodology document," directly contradicting the active
   `30_methods/canonical_method.md`.

4. **A referenced control file is missing.** `70_ideas/README.md` says ideas are
   promoted "by a formal decision in `00_control/decisions.md`" — that file does
   not exist.

5. **Earlier reframe edits were lost in the migration.** The
   "object we measure / candidate measures (exploratory)" reframe previously
   applied to a root `PAPER_TRACK_AAAI.md` is **not** present in the current
   `10_paper/PAPER_TRACK_AAAI.md` (that file is the pre-edit version).

6. **Mechanical debris.** `\_` escaping breaks markdown in three files;
   `migration_map.md` has line-break-corrupted rows; `result_index.md` status
   columns are empty.

---

## 1. Redundancy map (same information, multiple files)

| Topic | Files holding it | Verdict |
|---|---|---|
| **Paper spec** | `10_paper/PAPER_TRACK_FROZEN_v2.md` (declares itself authoritative); `10_paper/PAPER_TRACK_AAAI.md` ("based on" v2; migration_map marks it *deprecated→archive* yet it's still active); `90_archive/old_paper_tracks/method_paper_blueprint.md` (older 5-claim blueprint, self-marked superseded) | **One active conflict.** Pick FROZEN_v2 as the single frozen spec; resolve AAAI track (merge or archive); blueprint stays archived but donate its unique sections (§3). |
| **Method / three-track formulation** | `30_methods/canonical_method.md` (V2, what runs); `30_methods/implementation_report.md` (math spec); `90_archive/old_methods/GROUNDING_METHODOLOGY.md` (claims canonical; run/artifact procedure); `90_archive/old_methods/METHODOLOGY.md` (46k, deprecated); `90_archive/old_methods/groundingv3c.md` (unimplemented V3C design) | Keep canonical_method + implementation_report active. Strip the stale "canonical" claim from the archived file. Migrate two unique fragments (§3). |
| **Idea development** | `70_ideas/inbox.md` (raw); `70_ideas/developed.md` (articulated); `70_ideas/synthesis.md` (mapped to vault); `90_archive/old_direction_notes/VLM Grounding Synthesis.md` (older Directions A–E synthesis) | Keep the inbox→developed→synthesis chain (distinct roles, light overlap). Archive synthesis is superseded — fix the *active* links that still point to it (§2). |
| **Hypotheses / open questions** | `20_hypotheses/future_hypotheses.md` (H-A…H-D); `70_ideas/synthesis.md` (references H-A, H2, H3); `70_ideas/developed.md` ("open questions") | Inconsistent numbering (H-A vs H2/H3) across files. Unify into one hypothesis register. |
| **Pipeline / station framing** | `70_ideas` Idea 1; `90_archive/separate_project_spectral_vlm/*` (F/T/z three-station) | Different project, correctly separated. Add one cross-link, no merge. |

---

## 2. Proposed target structure (single source of truth per layer)

Adopt one canonical file per concern; everything else links to it rather than
restating it.

| Layer | Canonical file | Rule |
|---|---|---|
| Project control | `00_control/project_index.md` | Context/strategy only; no restated ideas. |
| Decisions | **`00_control/decisions.md` (NEW)** | Append-only log; the only place that promotes an idea into the paper. |
| Paper spec | `10_paper/PAPER_TRACK_FROZEN_v2.md` | The single frozen spec. |
| Hypotheses | `20_hypotheses/future_hypotheses.md` | One register, one numbering scheme. |
| Method (runs) | `30_methods/canonical_method.md` | What the code actually does. |
| Method (math) | `30_methods/implementation_report.md` | Formal spec. |
| Candidate signals | **`30_methods/signal_catalog.md` (NEW)** | One table of every grounding signal explored + status (see §4). |
| Ideas | `70_ideas/{inbox,developed,synthesis}.md` | Raw → articulated → mapped. |
| Results | `50_results/result_index.md` | Index with filled status columns. |

Link-only rule: a fact lives in exactly one canonical file; other files reference
it with `[[wikilink]]`, never re-paste it.

---

## 3. The only archive content not yet absorbed (migrate these)

1. **`old_methods/groundingv3c.md` → `30_methods/signal_catalog.md` (new).**
   V3C is a concrete, not-yet-implemented state-grounding formulation
   (evidence-weighted delta-residual). Under the "signals are still exploratory"
   reframe it is a *candidate signal*, not dead — capture it as one catalog entry
   with status "designed, not implemented."

2. **`old_methods/GROUNDING_METHODOLOGY.md` run/artifact procedure →
   `30_methods/canonical_method.md`.** The pipeline run commands, stage→output
   file contracts, and reference-tensor list are operational details not fully in
   canonical_method. Migrate that section, then leave the file archived with a
   deprecation banner.

3. **`old_paper_tracks/method_paper_blueprint.md` differentiation table + venue
   fit → `10_paper/` (positioning section of the paper track).** FROZEN_v2 has no
   competitor-differentiation table or venue analysis; the blueprint's are still
   useful. Donate those two sections; the rest stays archived.

Everything else in the three folders is genuinely superseded history — keep
archived, do not migrate.

---

## 4. New documents to create

- **`00_control/decisions.md`** — decision log (date, decision, rationale, affected
  files). Resolves the dangling reference in `70_ideas/README.md` and gives a
  single gate for promoting ideas into the frozen paper.
- **`30_methods/signal_catalog.md`** — one table of every candidate grounding
  signal (state_v2 / projection R²; `dec_dp_x_cvar`; `causal_delta_logp_random`;
  V3C; patch-logit-lens; layer-traversal `state_delta_var`) with columns: status,
  where defined, evidence/AUC, keep-for-paper?. This directly serves "systematize
  the ideas" and the exploratory-signal framing — it replaces scattered signal
  definitions across method/idea/hypothesis files with one register.

---

## 5. Cleanups (mechanical, low-risk)

- Run `encoding_fixer.py` on `30_methods/canonical_method.md`,
  `30_methods/implementation_report.md`, `90_archive/old_methods/METHODOLOGY.md`
  (broken `\_` escaping).
- Repair the corrupted line-broken rows at the bottom of
  `00_control/migration_map.md`.
- Repoint active links in `00_control/project_index.md` and
  `00_control/execution.md` from `90_archive/old_direction_notes/VLM Grounding
  Synthesis.md` to the live `70_ideas/synthesis.md`.
- Add a deprecation banner to `90_archive/old_methods/GROUNDING_METHODOLOGY.md`
  (remove its "canonical" self-claim).
- Fill the empty status columns in `50_results/result_index.md`.

---

## 6. Open decision for you

The one item I can't resolve unilaterally: the **AAAI track vs FROZEN_v2**
relationship. Options:
- (a) Treat FROZEN_v2 as the only paper spec; archive `PAPER_TRACK_AAAI.md`
  (as the migration_map already intended).
- (b) Keep `PAPER_TRACK_AAAI.md` as the active AAAI-facing view and demote
  FROZEN_v2 to a frozen appendix.
- (c) Merge the earlier "object/exploratory-signals" reframe into FROZEN_v2's
  framing and retire the separate AAAI file.

My recommendation: **(a) or (c)** — one paper spec, not two.
