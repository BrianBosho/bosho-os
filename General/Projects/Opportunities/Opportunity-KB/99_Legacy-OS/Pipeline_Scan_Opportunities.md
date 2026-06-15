---
type: pipeline
layer: workflow
---

# Pipeline: Scan for New Opportunities

> Run weekly. Goal: keep the Inbox stocked with appraised opportunities across all types.

## Step 1 — Define This Week's Search Focus (5 min)
Decide which types to prioritize this week:
- [ ] PhD positions
- [ ] Fellowships
- [ ] EU jobs with visa
- [ ] Remote jobs
- [ ] Kenya jobs

Set volume targets per `06_Agents/Agent_Opportunity_Scout.md`.

## Step 2 — Run Scout Agent (20-30 min)
Provide Scout agent with:
- This week's search focus
- Countries to target (from `01_Profile/Preferences.md`)
- Any specific labs/companies to check (from `08_Reference/Target_Labs.md`)
- The application history file (to avoid duplicates)

Scout creates raw notes in `04_Opportunities/Inbox/`.

## Step 3 — Run Evaluator Agent (5-10 min per opportunity)
For each new note in Inbox:
- Run `07_Pipelines/Pipeline_Appraise_Opportunity.md`
- Score all 6 dimensions
- Apply decision rules from `05_Appraisals/Decision_Rules.md`
- Move to appropriate subfolder or Archive

## Step 4 — Update Weekly Queue (5 min)
Populate `00_Home/Weekly_Application_Queue.md` with:
- Must Apply items (sorted by deadline)
- Strong Apply items
- Conditional items for Brian's review

## Step 5 — Review with Brian (10 min)
Brian reviews the queue and:
- Confirms which Conditionals to pursue
- Reprioritizes if needed
- Confirms referee availability for any Must Apply items

## Step 6 — Initiate Drafting for Top Items
For each confirmed Must Apply or Strong Apply item:
- Run `07_Pipelines/Pipeline_Draft_Application.md`
- Start with highest urgency first

## Total Pipeline Time Target
- Scout: 30 min
- Evaluate (3-5 new items): 45-60 min
- Queue update + review: 20 min
- **Total: ~2 hours per week for a healthy pipeline**
