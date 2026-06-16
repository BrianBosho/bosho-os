# General Dashboard

[[00_Vault Home|Back to Vault Home]]

## Active non-PhD work

| Area | Page | Current rule |
|---|---|---|
| Acubed / Colab | [[General/Projects/acubed_colab/acubed_colab]] - [[General/Projects/acubed_colab/execution|execution]] | Bounded weekly container only. |
| Hobby apps | [[General/Projects/hobby_apps/hobby_apps]] - [[General/Projects/hobby_apps/execution|execution]] | Parked this week. Capture only. |
| OpenClaw | [[General/Projects/openclaw/openclaw]] - [[General/Projects/openclaw/execution|execution]] | Parked unless needed for active research execution. |
| Swyng | [[General/Projects/Swyng/swyng]] - [[General/Projects/Swyng/execution|execution]] | Optional / delegated. |

## Active projects

```dataview
TABLE status
FROM "General/Projects"
WHERE type = "project" AND status = "active"
SORT file.mtime DESC
```

## Selected Action List

This dashboard intentionally shows the selected planning list, not raw project backlogs. Project state lives in each `execution.md`; selected tasks live in [[Planning/To-Do]].

```tasks
not done
path includes Planning/To-Do
sort by priority
```

## Recent notes

```dataview
TABLE file.mtime AS "Modified"
FROM "General"
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 10
```
