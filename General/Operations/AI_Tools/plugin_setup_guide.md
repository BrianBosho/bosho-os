# Plugin Setup Guide

Three plugins activate the dynamic features of this vault. Each takes under 2 minutes to install.

---

## Step 1: Open Community Plugins

In Obsidian:
1. **Settings** (gear icon) → **Community Plugins**
2. Disable **Safe Mode** if prompted
3. Click **Browse**

---

## Step 2: Install These Three Plugins

### 1. Dataview
- Search: `Dataview` — Author: `blacksmithgu`
- Powers the **Active Projects table** in the dashboard
- Queries frontmatter fields (priority, deadline, epic_active, etc.) across all project files

### 2. Tasks
- Search: `Tasks` — Author: `obsidian-tasks-group`
- Powers **Next Actions**, **All Open Tasks**, and **Completed This Week** in the dashboard
- Reads checkbox tasks with emoji metadata from all project files

### 3. Templater
- Search: `Templater` — Author: `SilentVoid13`
- Powers smart weekly plan and daily note templates
- After install: **Settings → Templater** → set Template folder to `09_templates`

---

## Step 3: Verify It Works

Open `00_dashboard.md`. You should see:
- A live **project table** (not a code block) — Dataview working
- A filtered list of **🔺 next actions** — Tasks working
- A full **task list grouped by project** — Tasks working

If you still see raw code blocks, go to **Settings → Community Plugins → Installed Plugins** and confirm all three are toggled on.

---

## Task Emoji Reference

Add these at the end of any task line to control filtering and sorting:

| Emoji | Priority |
|-------|----------|
| 🔺 | Highest — do this now |
| ⬆️ | High |
| 🔼 | Medium |
| 🔽 | Low |
| ⬇️ | Lowest |

Due dates: append `📅 YYYY-MM-DD` after the task text.

**Examples:**
```
- [ ] Audit results labels 🔺 📅 2026-06-11
- [ ] Draft cold email to Andrea Zanette ⬆️ 📅 2026-06-20
- [ ] Explore Zeraki relationship 🔼
```

Mark complete: change `[ ]` to `[x]`. Tasks plugin records the completion date automatically.

---

## Gmail / Drive Inbox Synthesis (Claude Code MCP)

Your Claude Code session already has Gmail and Google Drive MCP tools connected. No scripts to write or maintain.

To synthesize your inbox, paste this into a Claude Code chat:

```
Role: Personal OS Agent
Task: Search my Gmail for the last 48 hours of messages. Extract:
  1. Action items I need to take
  2. Project-relevant updates (TMLR, VLM, PhD, Acubed, Swyng)
  3. People I need to follow up with
Output: A markdown inbox note saved to 00_inbox/email_synthesis_YYYY-MM-DD.md
Constraints: Do not modify any existing vault files.
```

---

## Google Calendar Sync (Claude Code MCP)

To push this week's work blocks to Google Calendar:

```
Role: Personal OS Agent
Task: Read 08_weekly_plans/week_2026_06_08_starter.md.
Create Google Calendar events for each work block on the correct day.
Event format: "[Block N] — [Project]" with 3-hour duration starting 9am.
Do not schedule events before 7:30am or after 10:30pm.
```

---

## Todoist Integration (Optional)

If you want tasks mirrored in Todoist for mobile access:
1. Install the **Todoist** community plugin in Obsidian
2. Connect your Todoist account via API token
3. Tasks marked `🔺` in the vault can be synced to a Todoist "Bosho OS" project

This is optional — the vault is fully functional without Todoist.
