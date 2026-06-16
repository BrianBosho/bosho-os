# Bosho OS

> Welcome to the Bosho OS command center.
> Navigate to your domains below.

## Start Here

| Page | Use |
|---|---|
| [[Planning/Dashboard|Planning Dashboard]] | Active command center. |
| [[Planning/Today|Today]] | Current day's work blocks and first output. |
| [[Planning/This Week|This Week]] | Weekly commitments and parked items. |
| [[PhD Manual/Operations/Now|Now]] | Current season and priorities. |

## Domains

| Domain | Description |
|---|---|
| [[Home/Dashboard|Home Dashboard]] | Personal, finance, identity |
| [[General/Dashboard|General Dashboard]] | Startups, OpenClaw, non-PhD projects |
| [[PhD Manual/Dashboard|PhD Manual Dashboard]] | Research, academia, PhD administration |

## Active Global Projects

```dataview
TABLE status, domain
FROM "Home" OR "General" OR "PhD Manual"
WHERE type = "project" AND status = "active"
SORT file.mtime DESC
```

## Recent Notes

```dataview
TABLE file.mtime AS "Modified"
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
AND file.name != "00_Vault Home"
SORT file.mtime DESC
LIMIT 10
```

