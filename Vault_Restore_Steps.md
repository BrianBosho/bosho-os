# Vault Content Restoration — Steps for Implementing Agent

> **Goal:** Restore ~107 notes that were never placed during the merge. They exist only in `PreMerge_Backup.zip` (vault root). Three destination folders currently hold only stub files:
> - `General/Projects/Opportunities/Opportunity-KB/` — has README only; **32 notes** to restore
> - `General/Projects/Opportunities/Opportunity-KB/99_Legacy-OS/` — has README only; **52 notes** to restore
> - `PhD Manual/Knowledge/phd-knowledge-base/` — has Todo only; **23 notes** to restore
>
> All paths are relative to the vault root: `C:\Users\Bosho\Desktop\Bosho OS\`.
> The backup zip stores Windows-style paths; `unzip` on Linux/macOS expands the backslashes into proper nested folders (verified).

---

## Pre-flight

1. Confirm `PreMerge_Backup.zip` exists at the vault root and is intact (`unzip -t PreMerge_Backup.zip`).
2. Make a fresh safety copy first: `cp PreMerge_Backup.zip PreMerge_Backup.bak.zip` (or commit current state to git).
3. Do **not** delete `PreMerge_Backup.zip` or the `bosho-vault/` and `The Field Manual/` shells until the verification checklist passes.

---

## Step 1 — Extract the backup to a temp location

```bash
mkdir -p /tmp/vault_restore
unzip -q "PreMerge_Backup.zip" -d /tmp/vault_restore
# source roots inside the extracted tree:
#   /tmp/vault_restore/General/Projects/Opportunities/Opportunity-KB
#   /tmp/vault_restore/bosho-vault/Opportunity-KB/99_Legacy-OS
#   /tmp/vault_restore/bosho-vault/phd-knowledge-base
```
(Windows PowerShell equivalent: `Expand-Archive -Path 'PreMerge_Backup.zip' -DestinationPath "$env:TEMP\vault_restore" -Force`.)

## Step 2 — Restore the three folders (merge, preserve subfolder structure)

Copy **contents into** the existing destination skeletons so the numbered subfolders (`00_Index`, `01_Profile`, …) line up. Do not overwrite newer files blindly — if a destination note already exists, keep the richer version.

```bash
cd "C:/Users/Bosho/Desktop/Bosho OS"   # adjust for your shell
cp -rn /tmp/vault_restore/General/Projects/Opportunities/Opportunity-KB/.      "General/Projects/Opportunities/Opportunity-KB/"
cp -rn /tmp/vault_restore/bosho-vault/Opportunity-KB/99_Legacy-OS/.      "General/Projects/Opportunities/Opportunity-KB/99_Legacy-OS/"
cp -rn /tmp/vault_restore/bosho-vault/phd-knowledge-base/.  "PhD Manual/Knowledge/phd-knowledge-base/"
```
(`-n` = no-clobber. Windows: `robocopy "<src>" "<dst>" /E /XC /XN /XO` or `Copy-Item -Recurse`.)

Expected note counts **after** restore:
- `Opportunity-KB/` → **32** `.md`
- `Opportunity-KB/99_Legacy-OS/` → **52** `.md`
- `phd-knowledge-base/` → **23** `.md`

## Step 3 — Verify the restore

```bash
for p in "General/Projects/Opportunities/Opportunity-KB" \
         "General/Projects/Opportunities/Opportunity-KB/99_Legacy-OS" \
         "PhD Manual/Knowledge/phd-knowledge-base"; do
  echo "$(find "$p" -name '*.md' | wc -l)  $p"
done
```
Spot-check that these specific notes now open and have real content (they were confirmed missing before): `Apply Rules.md`, `Skills Inventory.md`, `SOP Draft.md`, `Fellowship Profile.md`, `CV.md`, `Motivation Letters.md`, `Scholarships.md`, `Positioning Statement.md`.

## Step 4 — Minor cleanup (safe deletions)

Remove empty leftover folders from the merge and the junk dirs:

```bash
# empty double-nested leftovers (confirmed 0 notes each)
rmdir "PhD Manual/People/People" "PhD Manual/People/People_dup" \
      "PhD Manual/Projects/Projects" "PhD Manual/Opportunities/Opportunities" \
      "_Inbox/BrainDump/BrainDump" "General/Operations/OS" \
      "General/Projects/Bosho_OS_Projects" 2>/dev/null
# remove all remaining empty directories under the domains
find Home General "PhD Manual" -type d -empty -delete
# delete Windows temp artifacts
rm -rf "PhD Manual/Projects/phd_preparation/~BROMIUM" "PhD Manual/Visa/Docs/~BROMIUM"
```
Note: `find -type d -empty -delete` will also remove intentional empty placeholders (e.g. `Archive/Dead_Projects`, `Projects/Active|Candidates|Sparks`). If you want to keep those as a deliberate skeleton, drop the bulk `find` line and remove only the named folders above.

## Step 5 — Post-restore de-duplication (review, do NOT auto-delete)

`Opportunity-KB` and `Opportunity-KB/99_Legacy-OS` are **two parallel generations of the same career system** (KB = TitleCase + numbered; OS = snake_case). Restoring both reintroduces duplicate concepts, e.g.:

- `CV Master Blocks.md` (KB) vs `CV_Master_Blocks.md` (OS)
- `Fit Profile.md` (KB) vs `Fit_Profile.md` (OS)
- `Why Me.md` / `Why This Lab.md` (KB) vs `Why_Me.md` / `Why_This_Lab.md` (OS)
- `Cryo-ET Pipeline.md` / `Urban Mobility VFMs.md` / `FedProp.md` appear in KB, OS, **and** project folders

**Decision needed from Brian:** keep both systems, or consolidate into one (recommend keeping `Opportunity-KB` as canonical and folding any unique OS notes into it, then archiving `Opportunity-KB/99_Legacy-OS`). Flag the pairs above; merge the richer of each into one note and repoint wikilinks. Do not delete the second copy until its unique content is confirmed merged.

## Step 6 — Finalize

1. Open the vault in Obsidian; let the link index rebuild.
2. Run a broken-link / orphan check (Dataview or the Obsidian "unresolved links" pane); repoint links broken by the move.
3. Commit: `git add -A && git commit -m "Restore Opportunity-KB / Opportunity-KB/99_Legacy-OS / phd-knowledge-base; cleanup leftovers"`.

---

## Verification checklist

1. `Opportunity-KB` = 32, `Opportunity-KB/99_Legacy-OS` = 52, `phd-knowledge-base` = 23 notes.
2. The eight spot-check notes (Step 3) open with real content.
3. No empty double-nested folders remain (Step 4).
4. `~BROMIUM` folders gone.
5. Duplicate pairs from Step 5 reviewed and either kept intentionally or merged — not silently overwritten.
6. No new unresolved wikilinks beyond what existed pre-restore.
7. `PreMerge_Backup.zip` retained until 1–6 pass; then it (and the source shells) can be archived.

