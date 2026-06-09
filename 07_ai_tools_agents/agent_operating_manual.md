# AI Agent Operating Manual

## Principle

Agents are not vague helpers. They are assigned bounded roles with explicit outputs.

## Agent roles

1. Research Engineer Agent
2. Paper Assistant Agent
3. Experiment Auditor Agent
4. Literature Scout Agent
5. Project Manager Agent
6. Personal OS Agent
7. Documentation Agent
8. Meeting Prep Agent

## Core rule

Every agent task must specify:

- Role
- Context
- Input files
- Exact output
- Constraints
- What not to change
- Review criteria

## Best uses

- Reduce setup friction.
- Audit results.
- Generate scripts.
- Create summaries.
- Refactor code.
- Draft documents.
- Process braindumps.
- Prepare agendas.
- Update project pages.

## Bad uses

- Avoiding hard decisions.
- Letting agents change raw results.
- Infinite tool tinkering.
- Replacing intellectual ownership.

## Standard agent task format

```text
Role: [Research Engineer / Paper Assistant / Experiment Auditor / etc.]
Context: [What project this belongs to]
Input: [Files, folders, manuscript sections, notes]
Task: [Exact action]
Output: [Report, script, markdown file, diff, checklist, etc.]
Constraints: [Do not delete raw results, do not overwrite files, etc.]
Review criteria: [How Brian will check the result]
```
