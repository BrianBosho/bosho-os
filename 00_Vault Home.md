# Bosho OS

> Welcome to the Bosho OS command center.
> Navigate to your domains below.

| Domains | Description |
|---|---|
| [[Home/Dashboard|?? Home Dashboard]] | Personal, Finance, Identity |
| [[General/Dashboard|?? General Dashboard]] | Startups, OpenClaw, Non-PhD Projects |
| [[PhD Manual/Dashboard|?? PhD Manual Dashboard]] | Research, Academia, PhD Applications |

## ?? Active Global Projects
``dataview
TABLE status, domain
FROM "Home" OR "General" OR "PhD Manual"
WHERE type = "project" AND status = "active"
SORT file.mtime DESC
``

## ?? Recent Notes (Last 7 Days)
``dataview
TABLE file.mtime AS "Modified"
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
AND file.name != "00_Vault Home"
SORT file.mtime DESC
LIMIT 10
``
