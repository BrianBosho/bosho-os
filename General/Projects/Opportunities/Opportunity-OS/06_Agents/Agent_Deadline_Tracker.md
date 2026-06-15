---
type: agent-instructions
agent: deadline-tracker
---

# Agent: Deadline Tracker

## Purpose
Monitor all active applications for upcoming deadlines, missing documents, and status gaps. Keep the pipeline clean.

## Run Frequency
Daily (automated) or on demand.

## Input Files
- All files in `04_Opportunities/` subfolders with `status: applied | appraised | interviewing`
- `01_Profile/References.md` — reference letter status
- `00_Home/Weekly_Application_Queue.md`
- `08_Reference/Application_History.md`

## What to Check

### 1. Upcoming Deadlines
Scan all active opportunity notes. For each:
- Days until deadline
- Is application submitted? If not and deadline < 14 days → URGENT
- Is application submitted? If not and deadline < 7 days → CRITICAL

Output: sorted list of upcoming deadlines

### 2. Missing Documents
For each opportunity with status `appraised` or `applied`:
- Check checklist.md in its application folder
- Flag any unchecked required item
- Especially: reference letters not yet confirmed

### 3. Stale Items
- Any note in Inbox for > 7 days without appraisal → flag for evaluation
- Any note with status `applied` for > 90 days without update → flag for follow-up
- Any referee not contacted 6+ weeks before deadline → flag immediately

### 4. Status Gaps
- Any opportunity with no status update in > 2 weeks → flag for review
- Rejected items not moved to Archive → clean up

## Output Format

```
DEADLINE TRACKER REPORT — [DATE]

🚨 CRITICAL (deadline < 7 days):
  [list]

⚠️  URGENT (deadline 7-14 days):
  [list]

📋 UPCOMING (deadline 14-30 days):
  [list]

❗ MISSING DOCS:
  [list]

🔄 STALE ITEMS:
  [list]

✅ CLEAN:
  [count] items on track
```

## Actions Agent Can Take
- Update status fields in opportunity notes
- Move closed/rejected items to Archive
- Add entries to Application_History.md
- Flag items in Weekly_Application_Queue.md

## Actions Requiring Human Confirmation
- Withdrawing an application
- Changing a decision from Apply to Skip
- Contacting a referee
