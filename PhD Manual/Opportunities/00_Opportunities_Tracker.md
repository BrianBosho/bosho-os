# ?? Opportunities Tracker

> Track all your fellowships, applications, and grants here.

``dataview
TABLE status AS "Status", deadline AS "Deadline", type AS "Type"
FROM "General/Projects/Opportunities/Opportunity-KB"
WHERE type = "opportunity" OR deadline != null
SORT deadline ASC
``
