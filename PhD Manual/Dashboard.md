# ?? PhD Manual Dashboard

[[00_Vault Home|? Back to Vault Home]]

## ?? Active Projects
``dataview
TABLE status
FROM "PhD Manual"
WHERE type = "project" AND status = "active"
SORT file.mtime DESC
``

## ? Open Tasks
``tasks
not done
path includes PhD Manual
sort by priority
``

## ?? Recent Notes
``dataview
TABLE file.mtime AS "Modified"
FROM "PhD Manual"
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 10
``
