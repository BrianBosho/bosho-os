---
title: Opportunities Pipeline
type: project-note
created: 2026-04-19
tags: [brain-dump, opportunities, phd, jobs, fellowships]
---

# Opportunities Pipeline

Source: [[../00 Inbox/Workbook q2 wk1|Workbook q2 wk1]]

## Opportunity categories

- PhD applications
- Job opportunities
- Fellowships
- Startup funding or startup-related support
- Immigration
- Remote jobs
- Kenya-related jobs
- Travel and events

## Input sources

- Email and subscriptions
- LinkedIn
- Twitter
- Internet sources and scraping
- Raindrop links/bookmarks

## Intended workflow

- Capture interests from Google Docs and related personal inputs.
- Decide which sources are important enough to monitor continuously.
- Ensure agents can read email safely and reliably.
- Create a Notion area dedicated to opportunities, with sub-pages by opportunity type.
- Create databases to track items and status.
- Use cron jobs to populate pages and databases automatically.
- Review the opportunity databases daily or every two days.
- Maintain a cadence of at least one application per week.

## Supporting systems

- Google Drive folders for essays, SOPs, resume/CV, and other application materials.
- Notion links pointing to those Drive folders and canonical documents.
- A task tracker for deadlines, execution, and application follow-through.

## Immediate gaps implied by the source doc

- Email access and ingestion need to be stable.
- Bookmark ingestion needs to be part of the pipeline.
- The opportunity system should be separated clearly from other planning and research material.

## Setup checklist

- [ ] Define the exact opportunity types to track in the database.
- [ ] Decide the canonical source of truth: Obsidian, Notion, or both with clear roles.
- [ ] Stabilize email access for opportunity capture.
- [ ] Add Raindrop or bookmark ingestion.
- [ ] Create one database or table per opportunity type.
- [ ] Define the minimum fields every opportunity record needs.
- [ ] Set the review cadence for new opportunities and deadlines.
- [ ] Define the rule for at least one application per week.

## Operating table

| Stage | What happens | Output |
|---|---|---|
| Capture | Pull items from email, LinkedIn, Twitter, scraping, and bookmarks | raw opportunity entries |
| Classify | Sort by PhD, job, fellowship, funding, immigration, remote, Kenya, travel | typed opportunity records |
| Enrich | Add deadline, fit, requirements, documents, and source link | usable application records |
| Decide | Mark pursue, defer, or discard | prioritized pipeline |
| Execute | Turn pursued records into tasks and document drafts | active application work |
| Review | Revisit the board daily or every two days | updated next actions |

## Minimum record fields

| Field | Purpose |
|---|---|
| Type | distinguish PhD, job, fellowship, and related paths |
| Title | identify the opportunity quickly |
| Organization | who is offering it |
| Deadline | enforce time awareness |
| Status | new, reviewing, ready, applied, deferred, rejected |
| Fit note | why it matters |
| Requirements | documents, links, or prerequisites |
| Source | where it came from |
| Next action | the next concrete move |
