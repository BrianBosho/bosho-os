---
type: pipeline
layer: workflow
---

# Pipeline: Appraise an Opportunity

> Run this pipeline on every new opportunity in `04_Opportunities/Inbox/` before any application work begins.

## Step 1 — Load Context (2 min)
Read these files:
- `01_Profile/Profile_Summary.md`
- `01_Profile/Fit_Profile.md`
- `01_Profile/Immigration_and_Mobility.md`
- `01_Profile/Weak_Spots.md`
- `05_Appraisals/Scoring_Rubric.md`

## Step 2 — Immediate Disqualification Check (1 min)
Ask:
- [ ] Does it require EU/EEA citizenship or have no visa sponsorship? → **DISQUALIFY**
- [ ] Is the deadline already passed? → **ARCHIVE**
- [ ] Is it an unfunded PhD? → **ARCHIVE** (unless exception applies)
- [ ] Is it clearly outside fit profile (pure software, non-ML)? → **SKIP**

If any box is checked → move file to `09_Archive/` with reason noted, stop.

## Step 3 — Score Each Dimension (5 min)
Using `05_Appraisals/Scoring_Rubric.md`, assign scores 1–10:
- A. Interest Fit (weight 0.25)
- B. Qualification Fit (weight 0.20)
- C. Unique Fit (weight 0.15)
- D. Immigration Feasibility (weight 0.15)
- E. Strategic Value (weight 0.15)
- F. Prestige / Upside (weight 0.10)

Compute: `Overall = 0.25A + 0.20B + 0.15C + 0.15D + 0.15E + 0.10F`

## Step 4 — Fit Analysis (5-10 min)
Write into the opportunity note:
- **Why Brian Fits:** 3-5 specific, concrete reasons (not generic)
- **Risks/Gaps:** What might work against him (check Weak_Spots.md)
- **Immigration Path:** How exactly would visa/permit work?
- **Tailoring Angle:** Which Story Arcs, which projects to feature

## Step 5 — Effort and Urgency (1 min)
- Effort: Low / Medium / High / Very High
- Days until deadline: [calculate]
- Flag as URGENT if deadline < 14 days

## Step 6 — Apply Decision Rule
| Score | Action |
|---|---|
| ≥ 8.5 | → Move to subfolder, tag `must-apply`, notify immediately |
| 7.0–8.4 | → Move to subfolder, tag `strong-apply` |
| 5.5–6.9 | → Move to subfolder, tag `needs-review`, flag for human decision |
| < 5.5 | → Move to `09_Archive/`, tag `skipped` |

## Step 7 — Update Comparison Table (2 min)
Add one row to `05_Appraisals/Opportunity_Comparison_Table.md`:
| Name | Type | Score | Decision | Deadline | Effort | Status |

## Step 8 — Notify (if interactive)
If running interactively, report:
"[Opportunity Name] scored [X]. Decision: [Must apply / Strong apply / Review / Skip].
Deadline in [N] days. Effort: [level]. Key fit: [1 line]. Key risk: [1 line]."

---

**Total time target: 15-20 minutes per opportunity**
