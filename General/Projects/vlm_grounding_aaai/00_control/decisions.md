---
title: Project Decisions Log
type: log
created: 2026-06-16
tags: [control, decisions, log]
---

# Project Decisions Log

This file is the immutable log of major scope changes, architectural decisions, and project pivots. 
Whenever scope changes or a major framing is selected/rejected, a short entry is added here.

## 2026-06-16 — Vault Reorganization & AAAI Track Selection

**Decision**: The vault was completely restructured into a Research Operating System (ROS) with strict 00-90 directories. The AAAI paper track (`10_paper/PAPER_TRACK_AAAI.md`) was promoted to the single canonical source of truth for the paper.

**Reason**: Sprawling "synthesis" documents and competing sources of truth (e.g., `PAPER_TRACK_FROZEN_v2.md` vs `AAAI.md`) created cognitive drag.

**Implications**:
- All active tasks live strictly in `00_control/execution.md` and `10_paper/PAPER_EXECUTION_TODO.md`.
- Hypotheses are isolated into atomic `OH*.md` files in `20_hypotheses/`.
- `PAPER_TRACK_FROZEN_v2.md` was archived to `90_archive/absorbed_sources/`.
