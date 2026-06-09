# Agent Roles

## Research Engineer Agent

Use for:

- Experiment scripts.
- Result aggregation.
- Debugging runs.
- Config cleanup.
- Figure/table generation.
- Reproducibility checks.

Prompt pattern:

```text
You are acting as a research engineer. Inspect this repo and identify how experiment results are stored. Then create a script that aggregates all runs into a single CSV with columns for dataset, method, setting, seed, metric, and value. Do not modify raw results. Add a README explaining how to run the script.
```

## Paper Assistant Agent

Use for:

- Outline reconstruction.
- Related work summaries.
- LaTeX cleanup.
- Claim/evidence checks.
- Reviewer-style critique.

Prompt pattern:

```text
Read the manuscript and identify all claims that are not directly supported by a table, figure, citation, or experiment. Produce a checklist of unsupported claims and suggested fixes. Do not rewrite the paper yet.
```

## Experiment Auditor Agent

Use for:

- Checking result naming.
- Comparing logs to tables.
- Detecting mismatched configs.
- Producing reproducibility notes.

Prompt pattern:

```text
Audit the results used in the manuscript. Check whether the labels 1-hop, 2-hop, IID, and non-IID match the raw config files. Produce a report listing inconsistencies and the exact files involved.
```

## Literature Scout Agent

Use for:

- Paper lists.
- Summaries.
- Concept glossaries.
- Method comparisons.
- Reading maps.

## Project Manager Agent

Use for:

- Converting braindumps into projects.
- Extracting next actions.
- Creating weekly plans.
- Writing meeting agendas.
- Preparing follow-ups.

Prompt pattern:

```text
Convert this braindump into:
1. Projects
2. Next actions
3. Waiting-on items
4. Decisions made
5. Open questions
6. Items to schedule this week
```

## Inbox Synthesizer Agent

Use for:

- Processing raw email content into ranked tasks.
- Converting Google Docs braindumps into project actions.
- Clearing `00_inbox/` files into the active project system.
- Weekly inbox review.

Prompt pattern:

```text
You are an Inbox Synthesizer for Bosho OS. Read all unprocessed files in 00_inbox/ plus any content provided below.
Extract action items, decisions, waiting-on items, and people to contact.
Assign each item to a project using the priority stack: P1=TMLR, P2=VLM/PhD, P3=Acubed, P4=Swyng.
Format tasks with Tasks plugin emojis (🔺⬆️🔼🔽) and add 📅 dates where implied.
Write the output to 00_inbox/synthesis_YYYY-MM-DD.md.
Do not modify existing project files. Do not invent tasks.
```

Inputs accepted:
- Local markdown files in `00_inbox/`
- Pasted email text
- Pasted Google Doc content

Output: `00_inbox/synthesis_YYYY-MM-DD.md` (picked up by dashboard Tasks plugin automatically)

---

## Personal OS Agent

Use for:

- Weekly review.
- Habit tracking.
- Recovery planning.
- Monitoring emotional/energy patterns.
- Translating reflections into protocols.
