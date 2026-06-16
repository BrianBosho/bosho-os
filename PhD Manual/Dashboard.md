# PhD Manual Dashboard

[[00_Vault Home|Back to Vault Home]]

## Open first

| Page | Use |
|---|---|
| [[PhD Manual/Operations/Now|Now]] | Current PhD season and priorities. |
| [[tmlr_fedprop_paper\|FedProp Paper]] | This week's paper closure priority (now in General/Projects). |
| [[vlm_grounding_aaai\|VLM Grounding / AAAI]] | This week's VLM team-unblocking priority (now in General/Projects). |
| [[PhD Manual/Operations/Program_Admin/PhD Logistics Board|PhD Logistics Board]] | Portugal/US, visa, Andrew ID, and program admin. |

## Active projects

```dataview
TABLE status, domain
FROM "General/Projects" or "PhD Manual"
WHERE (type = "project" OR type = "project-board") AND status = "active"
SORT file.mtime DESC
```

## Open tasks

```tasks
not done
(path includes General/Projects) OR (path includes PhD Manual)
sort by priority
```

## Recent notes

```dataview
TABLE file.mtime AS "Modified"
FROM "PhD Manual"
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 10
```

