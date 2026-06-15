# Codex / OpenClaw Workflows

## Workflow 1: Repo onboarding

```text
Inspect this repository and create a concise README explaining:
1. project purpose,
2. directory structure,
3. setup,
4. how to run tests,
5. how to run a minimal experiment,
6. how results are stored,
7. unclear or missing documentation.
Do not modify code yet.
```

## Workflow 2: Results audit

```text
You are an experiment auditor. Check whether all manuscript tables are traceable to raw result files. Focus on 1-hop, 2-hop, IID, non-IID labels. Produce a report listing inconsistencies, missing files, suspicious labels, and suggested fixes. Do not change raw results.
```

## Workflow 3: Aggregate results

```text
Create a script that aggregates all experiment result files into one CSV with columns:
dataset, method, setting, split_type, hop_count, seed, metric, value, source_file.
Do not delete or overwrite raw result files.
```

## Workflow 4: Paper claim audit

```text
Read the manuscript and identify claims not directly supported by a citation, table, figure, or experiment. Produce a checklist with section, claim, issue, and suggested fix.
```

## Workflow 5: Notebook scaffold

```text
Create a clean notebook that demonstrates the current pipeline on one small example. Include setup, model loading, data loading, inference, output inspection, and next steps. Keep it simple and reproducible.
```

## Workflow 7: Inbox synthesis → prioritized task list

```text
Role: Personal OS Agent
Context: Bosho OS vault at [vault path]. Priority stack: P1 = TMLR FedProp, P2 = VLM Grounding / PhD Prep, P3 = Acubed, P4 = Swyng.

Input:
- All markdown files in 00_inbox/ that do not contain the tag #processed
- Any email text pasted below under [EMAIL INPUT]
- Any Google Docs content pasted below under [GDOC INPUT]

Task:
1. Read every input source.
2. Extract: action items, decisions needed, waiting-on items, people to contact, open questions.
3. Assign each item to a project: TMLR | VLM | PhD | Acubed | Swyng | Health | Other.
4. Rank by priority stack. Within same priority, sort time-sensitive items first.
5. Format tasks using Obsidian Tasks plugin emoji: 🔺 highest, ⬆️ high, 🔼 medium, 🔽 low.
   Add 📅 YYYY-MM-DD if a deadline is mentioned or implied.
6. Write output to 00_inbox/synthesis_YYYY-MM-DD.md using the format below.
7. Add #processed to the top of each input file that was fully consumed.

Output format:
# Inbox Synthesis — YYYY-MM-DD

## 🔺 Do Now
- [ ] Task 🔺 📅 YYYY-MM-DD
  > Source: [file or email subject]

## ⬆️ High
- [ ] Task ⬆️
  > Source: ...

## 🔼 Medium
- [ ] Task 🔼

## 👥 People to Contact
| Person | Reason | Project |
|--------|--------|---------|

## ❓ Open Questions / Decisions
- ...

## 🗃️ Waiting On
- ...

Constraints:
- Do not modify any existing project files.
- Do not invent tasks not implied by the source material.
- If an item is ambiguous, flag it under Open Questions rather than guessing.
```

[EMAIL INPUT]
(paste email text here before running)

[GDOC INPUT]
(paste Google Doc content here before running)

---

## Workflow 6: Braindump processing

```text
Convert this braindump into:
1. Projects,
2. next actions,
3. decisions,
4. open questions,
5. waiting-on items,
6. people to contact,
7. agent tasks,
8. items to schedule this week.
```
