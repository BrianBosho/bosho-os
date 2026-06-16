---
type: index
status: active
tags: [projects, structure]
---

# Projects Structure

This folder is the execution home for all projects.

## Folder Pattern

Each real project should use this structure:

```text
General/Projects/<project>/
  <project>.md       # stable project brief, context, strategy, links
  execution.md       # current state, deliverables, work areas, blockers, log
  archive.md         # old migrated tasks or historical material, if needed
  supporting files   # only for real artifacts such as experiment plans or packets
```

## Page Roles

| Page | Role | Should contain |
|---|---|---|
| `<project>.md` | Project brief | Objective, why it matters, strategy, milestones, people, links. No live checkbox backlog. |
| `execution.md` | Project control surface | Current state, active deliverables, pending work areas, completed artifacts, blockers, activity log, source links. Not a giant backlog. |
| `Planning/To-Do.md` | Short-term pull list | Only the tasks selected for the current week or next few days. This is where checkboxes belong. |
| `Planning/Today.md` | Daily action subset | Only today's selected tasks and blocks. |

## Task Rule

Project briefs define direction. Execution pages define state. Planning pages define action.

`execution.md` should synthesize the project into deliverables and work areas. It should not contain every possible task. Pull only the next few executable actions into [[Planning/To-Do]].

Kanban files were retired on 2026-06-16 and preserved in [[General/Projects/_retired_kanban/README|_retired_kanban]].

## Dashboard Rule

Dashboards should surface selected planning tasks, not raw project backlogs. Supporting notes may contain old checklists, review checklists, or templates, but those should not drive dashboards directly.
