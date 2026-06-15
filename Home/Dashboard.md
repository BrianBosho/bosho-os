# ?? Home Dashboard

[[00_Vault Home|? Back to Vault Home]]

## ?? Active Projects
``dataview
TABLE status
FROM "Home"
WHERE type = "project" AND status = "active"
SORT file.mtime DESC
``

## ? Open Tasks
``tasks
not done
path includes Home
sort by priority
``

## ?? Recent Notes
``dataview
TABLE file.mtime AS "Modified"
FROM "Home"
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 10
``
