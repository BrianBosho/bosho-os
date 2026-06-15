# External Integrations Guide

## Overview
This document outlines the architecture for syncing Bosho OS (your local markdown vault) with your active cloud tools: Google Drive, Google Docs, Google Calendar, and task managers (Linear/Todoist).

---

## 🛠️ Integration Architecture

We use lightweight Python scripts located in `07_ai_tools_agents/scripts/` to connect local Markdown files with cloud APIs.

```mermaid
graph LR
    A[Google Docs/Drive] <── Python Script ──> B[00_inbox/]
    C[Google Calendar] <── Python Script ──> D[08_weekly_plans/]
    E[Linear / Todoist] <── Python Script ──> F[02_projects/]
```

---

## 📂 1. Google Drive & Docs Integration
**Goal:** Pull raw text from Google Docs (e.g., your master `SummerMaxxing` doc) and save it directly to `00_inbox/` for agent processing.

### Setup Instructions
1. Enable the Google Docs API in the Google Cloud Console and download the `credentials.json` file.
2. Put the `credentials.json` file in `07_ai_tools_agents/credentials/`.
3. Install required libraries:
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

### Python Sync Script Template
Create `07_ai_tools_agents/scripts/sync_gdocs.py`:
```python
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
DOCUMENT_ID = 'YOUR_GOOGLE_DOC_ID_HERE'
OUTPUT_PATH = 'c:/Users/Bosho/Desktop/Bosho OS/00_inbox/summermaxxing_gdoc_sync.md'

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '07_ai_tools_agents/credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    
    # Process doc content and write markdown to OUTPUT_PATH
    print(f"Document title: {document.get('title')}")
    # ... markdown translation logic ...

if __name__ == '__main__':
    main()
```

---

## 📅 2. Google Calendar Integration
**Goal:** Sync work blocks and restoration blocks from [week_2026_06_08_starter.md](../08_weekly_plans/week_2026_06_08_starter.md) into Google Calendar events.

### Mechanism
* **Write Sync:** Parse the Monday/Tuesday/Thursday/Friday work block structures in your weekly plan markdown file.
* **API Action:** Create or update calendar events matching those slots (e.g., "Block 1: TMLR Results Audit").
* **Constraint:** Protect sleep hours by raising warnings if calendar events are placed before 7:30 AM or after 10:30 PM.

---

## 📈 3. Linear / Todoist Integration
**Goal:** Map tasks in [active_projects_index.md](../02_projects/active_projects_index.md) directly to your project boards.

### Linear CLI / API Sync
Using the Linear API, tasks under project headers in your markdown files can be bidirectionally synced:
* **Creation:** A new line like `- [ ] Task Name` creates a Linear issue under the respective team.
* **ID Mapping:** The script appends the Linear ID to the markdown line, e.g., `- [ ] Task Name [ENG-102]`.
* **State Sync:** If you mark the task complete locally (`- [x]`), the script calls the Linear GraphQL mutation to set the issue status to `Done`.

---

## 🤖 How the Agent Can Assist
* Call the agent to **run sync scripts** before starting a deep work session to ensure local markdown state is up-to-date.
* Ask the agent to **audit calendar events** against your [yes_no_boundary_filter.md](../03_protocols/yes_no_boundary_filter.md) to detect conflicts with your rest days or sleep boundaries.
