# Home Dashboard

[[00_Vault Home|Back to Vault Home]]

## Active life systems

| Area | Page | Current rule |
|---|---|---|
| Aliveness | [[Home/Operations/Life_OS/Aliveness Plan]] | Preserve non-work life while building the PhD. |
| Anti-burnout | [[Home/Operations/Life_OS/Anti-Burnout Protocol]] | Protect recovery before collapse. |
| Anti-isolation | [[Home/Operations/Life_OS/Anti-Isolation Protocol]] | Maintain social contact deliberately. |
| Health | [[Home/Knowledge/Health/recovery_health_dashboard]] | Track energy and recovery signals. |

## Active projects

```dataview
TABLE status
FROM "Home"
WHERE type = "project" AND status = "active"
SORT file.mtime DESC
```

## Open tasks

```tasks
not done
path includes Home
sort by priority
```

## Recent notes

```dataview
TABLE file.mtime AS "Modified"
FROM "Home"
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 10
```

