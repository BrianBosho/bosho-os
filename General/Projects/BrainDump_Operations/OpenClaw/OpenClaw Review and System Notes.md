---
title: OpenClaw Review and System Notes
type: operations-note
created: 2026-04-19
tags: [brain-dump, operations, openclaw, review]
---

# OpenClaw Review and System Notes

Source: [[../../00 Inbox/Workbook q2 wk1 - Raw Archive|Workbook q2 wk1 - Raw Archive]]

## OpenClaw review findings captured from the workbook

- Config drift from the original plan
- Subagent runs failing with model-switch errors
- Exec approvals effectively bypassed by a global wildcard
- POS agents partially configured and not fully operational
- Secrets exposed in config
- Weekly PhD deep digest not running
- MODEL-HEALTH documentation diverged from live config
- Telegram startup/connect error needs verification

## Recommendations embedded in the workbook review

- Fix subagent spawning first
- Reconcile live config with the architectural plan
- Remove the wildcard exec approval pattern
- Either complete POS agent setup or remove unused agents
- Rotate exposed tokens
- Verify Telegram connectivity
- Update docs to match reality

## Additional system notes from the workbook

- Need one central place to find cron runs and outputs
- Need a visible morning brief / run surface on the channels
- Need to review the cron jobs and ensure they run next time

## Research-workflow implications

- For each research project, there should be a page showing:
  - current status
  - last thing done
  - next thing to work on
- This should behave like a lab notebook with links to all project resources

## VLM project system notes mentioned alongside the OpenClaw material

- There is a paper-track doc for the current VLM grounding work
- There is a Drive folder for sanity checks, protocols, and results
- Those should be made explicit on a project homepage for day-to-day progress
- Progress updates and reports should be captured systematically

## Task snippets captured in this systems cluster

- Complete Stanchart transaction
- Follow up with Equity on transaction status
- Transfer credentials and logins from Comet to current Chrome
- Fix research setup issues with Claude on the Davout machine
- Fix OpenClaw crons
- Resolve Co-op Bank issues
- Check how to use Cursor, Copilot, and similar tools with OpenClaw
- Build a schedule that covers startup projects, lab work, and VLM grounding
- Explore exhaustion, exercise, and energy management
- Build an AI/LLM engineer profile from the Discord channel notes
- Ask the model to find a gym and maybe propose a schedule

## Concrete application mentioned in this part of the workbook

- Outpace Studios AI Builder role:
  - https://www.outpacestudios.com/careers/ai-builder

## Fix checklist

- [ ] Fix subagent model-switch failures.
- [ ] Reconcile live config with the intended architecture.
- [ ] Remove or tighten the wildcard exec approval pattern.
- [ ] Decide whether POS agents should be completed or removed.
- [ ] Rotate any exposed tokens or secrets.
- [ ] Verify Telegram startup and connectivity.
- [ ] Restore the weekly PhD deep digest.
- [ ] Update MODEL-HEALTH and related docs to match reality.
- [ ] Create one place for cron runs and outputs.
- [ ] Create a visible morning brief or run surface.

## Issue table

| Issue | Risk | Desired fix |
|---|---|---|
| Config drift | system behavior no longer matches design | align config and docs |
| Subagent failures | delegation path is unreliable | repair model-switch setup |
| Wildcard exec approval | unsafe command permissions | narrow the approval surface |
| Incomplete POS agents | dead or misleading system surface | finish or remove them |
| Exposed secrets | credential leakage | rotate and clean configs |
| Cron and digest failures | automation cannot be trusted | verify runs and logs |
| Telegram uncertainty | broken delivery surface | test and confirm end-to-end |

## Adjacent tasks captured here

| Task | Suggested home |
|---|---|
| Stanchart transaction | Admin |
| Equity follow-up | Admin |
| Transfer Comet credentials to current Chrome | Operations |
| Fix Davout machine research setup | Research operations |
| Resolve Co-op Bank issues | Admin |
| Check Cursor or Copilot workflows with OpenClaw | Operations |
| Build schedule across startup, lab, and VLM work | Planning |
| Explore exhaustion, exercise, and energy management | Planning or personal systems |
| Build AI engineer profile from Discord notes | Career |
| Gym search and schedule | Personal systems |

## Immediate next actions

| Order | Action | Outcome |
|---|---|---|
| 1 | fix subagent spawning and model switching | stable agent execution |
| 2 | audit approvals and secrets | safer runtime setup |
| 3 | verify crons, digest, and Telegram delivery | trusted automation surface |
