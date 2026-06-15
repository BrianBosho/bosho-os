---
type: pipeline
layer: workflow
---

# Pipeline: Draft an Application

> Run only after appraisal score ≥ 7.0. Never draft before scoring.

## Prerequisites
- [ ] Opportunity note is fully scored (all 6 dimensions)
- [ ] Score ≥ 7.0 overall
- [ ] Immigration feasibility confirmed (not 0)
- [ ] Deadline confirmed in future
- [ ] Required documents list complete in opportunity note

## Step 1 — Load Context (5 min)
Read:
- The opportunity note (all sections)
- `01_Profile/Story_Arcs.md` — identify which arcs to use per tailoring angle
- `01_Profile/Weak_Spots.md` — know what to handle carefully
- `01_Profile/Academic_Record.md` — exact credentials to use
- `03_Portfolio/` — the 2-3 most relevant project files

## Step 2 — Create Application Folder
Create: `04_Opportunities/[subfolder]/[opportunity-slug]/`

Files to create:
```
checklist.md          ← first, track everything
tailored_cv.md
cover_letter.md       (or motivation_letter.md for PhD)
research_statement.md (PhD and research fellowships only)
outreach_email.md     (PhD only — send before formal application)
notes.md              (decisions, sources, open questions)
```

## Step 3 — Draft Checklist First
In `checklist.md`, list every required document from the opportunity note.
Add submission instructions, portal URL, file format requirements.
This prevents missing documents at the last minute.

## Step 4 — Draft Outreach Email (PhD only, if applicable)
- Use `02_Assets/Email_Professor_Outreach.md` as base
- Customize: specific paper referenced, specific research question, specific ask
- Length: under 250 words
- **Send this BEFORE the formal application if timeline allows**
- Log send date in notes.md

## Step 5 — Draft CV
- Start from the most relevant base in `02_Assets/` (PhD Research / ML Engineer / Remote)
- Reorder: put most relevant experience first for this application
- Adjust summary: match to role/program
- Projects: include only the 3-4 most relevant, with relevant framing
- Length: 1 page (industry), 2 pages (academic)
- Verify all metrics and dates against portfolio files

## Step 6 — Draft Cover Letter or Motivation Letter
For industry (cover letter):
- Structure: Hook → Background fit → Why THIS role → What I bring → Close
- Length: max 1 page
- Use `02_Assets/Cover_Letter_Master_Template.md`

For PhD/fellowship (motivation letter):
- Structure: The problem → My approach → My preparation → Why here → Long-term goals
- Length: 1.5-2 pages
- Pull from paragraph modules in `02_Assets/Paragraphs/`
- Customize "Why here" per faculty and program

## Step 7 — Draft Research Statement (PhD only)
- Start from `02_Assets/Research_Statement_Master.md`
- Customize [LAB-SPECIFIC] section with faculty names, research threads, specific papers
- Length: 1-2 pages
- Must name specific people and their specific work — not generic

## Step 8 — Quality Check
Before finalizing any document:
- [ ] No forbidden phrases (see Agent_Application_Drafter.md)
- [ ] No claims contradicting Weak_Spots.md
- [ ] Correct names throughout (professor, institution, role title)
- [ ] Not copied from wrong application
- [ ] Active voice throughout
- [ ] Every paragraph earns its place — no filler
- [ ] Length within norms

## Step 9 — Update Status
In opportunity note: update `status` from `appraised` to `applied` (after submission)
In `08_Reference/Application_History.md`: add entry
In `00_Home/Home.md` pipeline table: update count

## Step 10 — Deadline Tracking
In `01_Profile/Timeline.md`: confirm deadline is tracked
Set reminder: 48 hours before deadline for final check
