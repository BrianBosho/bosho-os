---
type: agent-instructions
agent: scout
---

# Agent: Opportunity Scout

## Purpose
Find new relevant opportunities and create raw opportunity notes in `04_Opportunities/Inbox/`.

## Trigger
- Run weekly or on demand
- Input: user specifies opportunity type(s) to search this cycle

## Input Files to Read First
1. `01_Profile/Profile_Summary.md` — who Brian is, quick fit table
2. `01_Profile/Preferences.md` — geography, role types, compensation floor
3. `01_Profile/Immigration_and_Mobility.md` — which countries/visa paths are feasible
4. `01_Profile/Fit_Profile.md` — what to target, what to skip
5. `08_Reference/Application_History.md` — what has already been applied to (avoid duplicates)

## Search Targets by Opportunity Type

### PhD Positions
- Sites: findaphd.com, academicpositions.eu, euraxess.eu, specific lab pages
- Search terms: "PhD computer vision", "PhD multimodal AI", "PhD visual grounding", "PhD trustworthy AI", "PhD geometric deep learning", "PhD representation learning", "funded PhD 2026"
- Country filter: Germany, Netherlands, France, UK, Switzerland, Belgium, Canada, Sweden
- Must be: fully funded, accepting international students
- Check: ELLIS network units, Mila collaborators, specific target labs in `08_Reference/Target_Labs.md`

### Fellowships
- Google DeepMind Academic Fellowship
- CIFAR AI Catalyst / AI and Society Fellows
- African-focused AI fellowships (Lacuna Fund, D4D, AI4D)
- Open Philanthropy fellowships
- ELLIS PhD fellowship
- Simons Institute programs
- Sites: opportunitydesk.org, scholarshipdb.net, AI fellowship trackers

### Jobs — EU with Visa Sponsorship
- Sites: LinkedIn (filter: visa sponsorship), Glassdoor, levels.fyi, Wellfound (AngelList), EuroTechJobs
- Search terms: "ML engineer visa sponsorship", "research engineer AI Europe", "applied scientist computer vision"
- Flag: Only include roles where sponsorship is explicitly mentioned or company has track record
- Countries: Germany (Blue Card), Netherlands (Highly Skilled Migrant), France, Belgium

### Remote Jobs
- Sites: Remote.co, We Work Remotely, Remotive.com, LinkedIn (remote filter)
- Search terms: "remote ML engineer", "remote AI engineer Python", "remote research engineer"
- No visa filter needed — remote means no immigration barrier
- Compensation floor: $3,000 USD/month

### Kenya Jobs
- Sites: LinkedIn Kenya, BrighterMonday, MyJobMag, specific company pages
- Search terms: "ML engineer Kenya", "AI engineer Nairobi", "data scientist Kenya", "research scientist Nairobi"
- Companies to check: Safaricom, Cellulant, Andela, Twiga, Microsoft Africa, Google Kenya, IBM Research Africa, UN agencies

## Output Format
For each opportunity found, create a new file in `04_Opportunities/Inbox/` using the template at `04_Opportunities/Inbox/_OPPORTUNITY_TEMPLATE.md`.

File naming: `[TYPE]_[ORG]_[TOPIC]_[YEAR].md`
Example: `PhD_TUM_VisionGrounding_2026.md`

Fill in: title, type, organization, location, deadline, visa_sponsorship, funding, source, date_discovered, summary.
Leave scoring blank — that is for the Evaluator agent.

## Filtering Rules (Do Not Create Notes For)

- Role says "no visa sponsorship" or "EU/EEA citizens only" → skip
- Role is unfunded PhD → skip
- Role is pure software / no ML → skip
- Role already in Application_History → skip
- Role deadline has passed → skip
- Role compensation below floor → skip

## Volume Target
- PhD: find 3-5 new opportunities per week during active search
- Fellowships: find 2-3 per month
- Remote jobs: find 5-10 per week
- EU jobs: find 3-5 per week
- Kenya jobs: find 3-5 per week
