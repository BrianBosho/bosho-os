---
type: agent-instructions
agent: evaluator
---

# Agent: Opportunity Evaluator

## Purpose
Read each opportunity in `04_Opportunities/Inbox/`, score it using the rubric, and move it to the appropriate subfolder with a recommendation.

## Input Files to Read First
1. `01_Profile/Profile_Summary.md`
2. `01_Profile/Fit_Profile.md`
3. `01_Profile/Skills.md`
4. `01_Profile/Interests.md`
5. `01_Profile/Immigration_and_Mobility.md`
6. `01_Profile/Weak_Spots.md`
7. `05_Appraisals/Scoring_Rubric.md`

## Evaluation Process

### Step 1: Immediate Disqualification Check
Before scoring, check:
- Is visa/immigration feasible? If immigration_score = 0, mark DISQUALIFIED, archive.
- Is deadline already passed? If yes, archive.
- Is it unfunded PhD? Mark NOT VIABLE.
- Is it explicitly "no sponsorship" for non-EU? Mark NOT VIABLE.

### Step 2: Score Each Dimension
Using `05_Appraisals/Scoring_Rubric.md`, score:
- A. Interest Fit (0.25)
- B. Qualification Fit (0.20)
- C. Unique Fit (0.15)
- D. Immigration Feasibility (0.15)
- E. Strategic Value (0.15)
- F. Prestige / Upside (0.10)

Compute Overall Score with formula in rubric.

### Step 3: Estimate Effort
- Low: quick apply, <2 hours
- Medium: tailored letter + CV, 4-6 hours
- High: full SOP + references + transcripts, 10+ hours
- Very High: multi-stage, 20+ hours

### Step 4: Write Fit Analysis
Fill in the opportunity note:
- "Why Brian Fits" — 3-5 specific, concrete reasons
- "Why This Fits Brian" — what makes it attractive per his preferences
- "Risks and Gaps" — honest assessment per Weak_Spots.md
- "Tailoring Angle" — which Story Arcs to use, what to emphasize

### Step 5: Recommend Required Assets
Identify which CV version, which paragraph modules, and which portfolio items are most relevant.

### Step 6: Apply Decision Rule
| Score | Decision |
|---|---|
| ≥ 8.5 | Must apply |
| 7.0–8.4 | Strong apply |
| 5.5–6.9 | Conditional — flag for human review |
| < 5.5 | Skip |
| Immigration = 0 | Disqualify |

### Step 7: Move File
- Must apply / Strong apply → move to appropriate subfolder (`PhD_Positions/`, `Fellowships/`, etc.)
- Conditional → move to subfolder, add tag `needs-review`
- Skip → move to `09_Archive/`
- Disqualify → move to `09_Archive/` with reason noted

### Step 8: Update Opportunity Comparison Table
Add entry to `05_Appraisals/Opportunity_Comparison_Table.md` with scores and decision.

## Output
- Scored and annotated opportunity note in correct subfolder
- Updated comparison table
- Optional: brief summary message to user if running interactively

## Quality Checks
- Do not score based on title alone — read the full job description
- Do not assume visa sponsorship — check explicitly
- Do not inflate unique fit — be realistic per Weak_Spots.md
- If deadline is within 2 weeks, flag as URGENT regardless of score
