---
type: reference
layer: migration
created: 2026-04-21
---

# Migration Notes

## Source Folders Compared

- `Opportunity-KB` in the Obsidian vault: 32 Markdown files, about 3.3k words.
- `Opportunity-KB/99_Legacy-OS` from Downloads: 45 Markdown files, about 18k words.

## Decision

`Opportunity-KB/99_Legacy-OS` is the active system. It has fuller profile detail, opportunity tracking, appraisals, agents, pipelines, reusable assets, portfolio notes, and reference files.

`Opportunity-KB` should be treated as an earlier starter knowledge base and kept as an archive until the OS version is reviewed in practice.

## Superseded by Opportunity-KB/99_Legacy-OS

- `Opportunity-KB/01_Profile/Education.md` -> `01_Profile/Academic_Record.md`
- `Opportunity-KB/03_Skills-and-Fit/Fit Profile.md` -> `01_Profile/Fit_Profile.md`
- `Opportunity-KB/03_Skills-and-Fit/Skills Inventory.md` -> `01_Profile/Skills.md`
- `Opportunity-KB/04_Mobility-and-Preferences/*` -> `01_Profile/Immigration_and_Mobility.md` and `08_Reference/Country_Visa_Notes.md`
- `Opportunity-KB/05_Project-Evidence/*` -> `03_Portfolio/*`
- `Opportunity-KB/07_Appraisal-Rules/*` -> `05_Appraisals/*`
- `Opportunity-KB/08_Agent-Guides/*` -> `06_Agents/*` and `07_Pipelines/*`

## Preserved from Opportunity-KB

- `01_Profile/Positioning.md`
- `02_Assets/CV_Master_Blocks.md`
- `02_Assets/Paragraphs/Why_Me.md`
- `02_Assets/Paragraphs/Why_This_Lab.md`
- `08_Reference/Document_Purpose_Map.md`
- `08_Reference/Role_Taxonomy.md`

## Cleanup Notes

The downloaded `Opportunity-KB/99_Legacy-OS` folder contained malformed empty brace-named directories from a bad shell expansion. Those were not copied into the vault version.

