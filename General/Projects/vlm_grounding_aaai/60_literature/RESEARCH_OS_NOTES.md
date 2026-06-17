# Research Operating System Notes

*Source: VLM Grounding Ideas doc (Tab 2). Captured 2026-06-16. These are workflow and infrastructure design notes — not directly about experiments.*

---

## Core Concept

Research theme: **VLM reliability and faithfulness.**

Within the theme: multiple ideas, methodologies, problems, papers. This space is the home of all unresolved problems/areas. Each one eventually resolves into a **paper track** (a candidate problem with a defined scope).

---

## Paper Track Structure

Each paper track should have a living document with:

- **Core claims** (what the paper asserts)
- **Core literature** (problem framing, adjacent work, datasets, benchmarks, techniques)
- **Hypotheses, experiments, findings** (one block per hypothesis)
- **Next things to check**

The document evolves over time as evidence accumulates. The decision of when to consolidate into a paper is separate from tracking the track itself.

---

## Literature Organization

Two Google Docs per track:

1. **Exploratory papers** — general overview, not core. Papers that help orient the space but won't be cited directly.
2. **Core papers** — papers to understand well, reread, and reference. These are:
   - Directly adjacent work (may work / builds on their contributions)
   - Datasets, baselines, benchmarks I adopt
   - Core techniques I use (e.g., spectral analysis, linear probes)

A literature manager agent accesses these docs and feeds content into NotebookLM for synthesis.

---

## Hypothesis Lifecycle

1. **Raw brainstorming docs** → dump of unfiltered ideas
2. **Formalization** → a clean, single hypothesis or research question
3. **Resolution** → either:
   - Look for answers in literature / adjacent work
   - Design an experiment
4. **Record** → hypothesis + literature answer + experiment + findings in one doc

**Key principle:** The hypothesis (or micro research question) is the **atomic unit** of the research workflow. Speed of iteration through this loop = research progress.

**Scope management:** Some hypotheses lead to further questions and experiments. Need to determine:
- What goes in the appendix
- What counts as a core question/experiment
- What counts as supporting material
- What becomes a separate track

---

## Codebase Integration

Each hypothesis ends up in the codebase as a `.md` file with:
- Description of the question
- The experiment design
- A folder for the experiment (notebook + report)

The Google Drive folder mirrors this: hypothesis markdown files, one per question, plus their results.

---

## Tooling Stack

| Tool | Role |
|---|---|
| Google Docs/Drive | Primary document repository |
| Notion | Overview layer, links to docs, DB tracking |
| NotebookLM | Literature synthesis |
| Markdown files (codebase) | Source of truth for agents |
| Openclaw agent setup | Multi-agent execution |

**Important:** Markdown files are the source of truth for agents. Google Docs is where most reading, writing, and file creation happens.

---

## Agent Roles (Planned)

- **Orchestrator agent** — creates and manages research track folders and documents
- **Literature manager agent** — manages exploratory + core paper docs, feeds NotebookLM
- **Hypothesis agent** — formalizes raw ideas into clean hypotheses; tracks what's been tested
- **Execution agents** — handle actual implementation (separate from the core workflow)
- **Manager/clerk agent** — the core workflow agent: understands overall research state, keeps a source of truth, manages feedback loops

**Key distinction:** The manager agent is a record-keeper and loop manager, not an executor. Execution is outside its scope.

---

## Inspiration

- Neel Nanda's research philosophy: tight feedback loops, hypothesis-driven iteration
- [Research process post (LessWrong)](https://www.lesswrong.com/posts/Ldrss6o3tiKT6NdMm/my-research-process-understanding-and-cultivating-research)
- [Mechanistic interpretability researcher guide (Alignment Forum)](https://www.alignmentforum.org/posts/jP9KDyMkchuv6tHwm/how-to-become-a-mechanistic-interpretability-researcher)
