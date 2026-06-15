---

## type: master-plan status: active created: 2026-06-10 tags: [phd, master-plan, cmu-portugal, mech-interp, vlm]

# PhD Master Plan: 2026–2031

## Becoming a Top Researcher in Mechanistic Interpretability of Multimodal Models

> **North star (5–10 years):** Be one of the best researchers in the world at the intersection of multimodal models, mechanistic interpretability, AI safety, and explainability — recognized through a coherent body of work, a defensible dissertation, and a position at a frontier lab or top-tier faculty role.

> **Constraint stack (explicit priority order):**
> 
> 1. Become a top global mech interp researcher (5–10 yr horizon)
> 2. Graduate as fast as possible (4-year target, 5-year ceiling)
> 3. Maximize earnings along the way

---

## 0. The One-Paragraph Plan

Enter CMU ECE (Fall 2026, Pittsburgh) and immediately compress: finish all coursework and the qualifying exam inside Year 1, while converting the existing VLM self-evaluation project into a first published paper. Use Years 1–2 at CMU to embed in the mech interp ecosystem (Aashiq → Smith cluster, Raghunathan, Xie) and produce the _mechanistic core_ of the thesis — causal/circuit-level analysis of how visual grounding succeeds and fails inside VLMs. Take the highest-value industry internship in Summer 2027 and/or 2028 _before_ the FCT contract activates (this is the earnings + reputation window). Transfer to FEUP/Porto for Years 3–4(–5), anchored in Cardoso's VCMI group, where the work extends to interventions, reliability guarantees, and (optionally) a medical-imaging application that makes the Portugal side substantive rather than decorative. Prospectus end of Year 3; defend in Year 4 if everything compresses, Year 5 realistically. Emerge with 4–6 strong papers forming a single arc: **behavioral evaluation → mechanistic explanation → intervention/theory** of visual grounding in multimodal models.

---

## 1. Research Identity & Thesis Arc

### 1.1 Thesis statement (working)

> **"Mechanistic Foundations of Visual Grounding in Vision-Language Models: How Visual Evidence Is Represented, Transformed, Lost, and Recovered."**

This sits exactly at your declared intersection:

- **Multimodal models** — the object of study (VLMs)
- **Mech interp** — the method (circuits, SAEs, causal interventions, information flow)
- **AI safety** — the motivation (hallucination, self-evaluation reliability, scalable oversight of multimodal systems)
- **Explainability** — the FEUP/VCMI bridge (Cardoso's group identity)
- **Possible domain** — medical imaging (VCMI's applied strength; optional Chapter 5)

### 1.2 The three-layer stack (unchanged, now scheduled)

|Layer|Content|When it dominates|
|---|---|---|
|**L1: Publishable core**|VLM grounding, self-evaluation, hallucination, benchmarks, failure taxonomies|Year 0–1|
|**L2: Scientific abstraction**|Mechanistic/causal analysis, cross-modal information flow, SAEs on multimodal representations, evidence loss|Years 1–3 (the thesis spine)|
|**L3: Audacious vision**|Information-theoretic account of learned perception; training objectives with grounding guarantees|Years 3–4+ (final chapter + post-PhD agenda)|

### 1.3 The paper arc (dissertation = 4–5 chapters = 4–6 papers)

|#|Paper (working title)|Layer|Target window|Target venues|Role in thesis|
|---|---|---|---|---|---|
|P1|_When VLMs Misjudge Themselves: A Systematic Study of Self-Evaluation of Visual Grounding_|L1|Submit Summer–Fall 2026|CVPR/ICCV workshop → ACL/EMNLP findings → NeurIPS D&B|Ch. 2 — establishes the phenomenon|
|P2|_Where Grounding Lives: Causal Localization of Visual Evidence Use in VLMs_ (activation patching, cross-modal attention knockouts, layer-wise evidence tracing)|L2|Year 1 → submit early Year 2|NeurIPS / ICLR / ICML|Ch. 3 — the mechanistic core; **this is the paper that makes your name in interp**|
|P3|_Sparse Features of Visual Grounding: SAE Analysis of Multimodal Representations_ (or equivalent feature-level study; natural collaboration surface with Aashiq)|L2|Year 2|ICLR / NeurIPS / interp workshops (BlackboxNLP, ATTRIB, NeurIPS Interp)|Ch. 3b or merged into Ch. 3|
|P4|_Steering Grounded Behavior: Interventions That Repair Grounding Failures_ (steering vectors, representation surgery, or training-time fixes)|L2→L3|Year 3 (Portugal)|NeurIPS / ICML|Ch. 4 — from explanation to control|
|P5|_Grounding Under Stakes: Mechanistic Reliability of Medical VLMs_ (optional, with VCMI) — or — _An Information-Theoretic Account of Grounding Failure_|L3 / domain|Years 3–4|MICCAI/TMI (domain) or theory venue|Ch. 5 — the Portugal-anchored chapter|
|P6|Survey/position paper: _Mechanistic Interpretability for Multimodal Models: Open Problems_|—|Year 2–3, opportunistic|TMLR / survey venues|Field-shaping; cheap citations; establishes you as a reference point|

**Rule:** every paper must be a chapter or get killed. No orphan papers (the Anti-Diffusion Protocol applies at the thesis level too).

### 1.4 Why this arc wins on Priority 1 (top researcher)

Top interp researchers are known for a _named problem_, not a pile of papers. Your named problem: **"multimodal grounding, mechanistically."** Almost all of mech interp's center of mass is text-only LLMs; multimodal interp is visibly under-populated relative to its safety importance (VLMs are deployed in robotics, medicine, autonomous systems). You are positioning in the gap _adjacent to_ the established field, where the established people (Anthropic interp team, the SAE literature, the Smith/Aashiq cluster) will cite you rather than compete with you. P2 and P3 are the reputation engines; P1 is the on-ramp; P4–P5 prove it matters.

---

## 2. Advisor & Committee Architecture

### 2.1 Current honest state (from the vault)

|Person|Status|Fit|Role in plan|
|---|---|---|---|
|**Carlee Joe-Wong** (CMU)|Established program contact, relationship confidence HIGH, research fit UNCERTAIN|Networks/resource allocation/federated learning — bridge via _trustworthy & reliable ML_, possibly federated/distributed multimodal systems|CMU anchor & likely official CMU advisor; flexibility for fellowships/internships is a major asset for Priorities 2–3|
|**Jaime Cardoso** (FEUP)|Initial contact, relationship confidence SOLID, research fit GOOD|Visual computing + explainability + medical AI (VCMI)|Portugal-side advisor; Ch. 5 anchor; explainability framing|
|**Virginia Smith** (CMU)|Not yet established; approach after peer rapport via Aashiq|Direct mech interp cluster (Aashiq, Xiangchen Song)|Target: committee member or informal co-advisor; ecosystem entry|
|**Aashiq Muhamed**|Outreach email finalized, pending send/reply|SAEs, circuits, safety; Anthropic Fellow / MATS alum|Peer mentor → collaborator on P3; bridge to Smith|
|**Aditi Raghunathan**|Not contacted|Reliable AI|Committee candidate|
|**Shaoan Xie**|Not contacted|Causal identifiability in vision-language (SmartCLIP)|Committee candidate / Ch. 4 theory input|
|**Luis Teixeira** (FEUP/VCMI)|Not contacted|Portugal-side mech interp continuity|Second Portugal reader; mitigates continuity risk when CMU cluster is remote|

### 2.2 The configuration to build (target by end of Semester 2)

```
Official co-advisors:   Carlee Joe-Wong (CMU)  +  Jaime Cardoso (FEUP)
Intellectual engine:    Smith cluster (via Aashiq) + VCMI explainability group
Committee (4–5):        Joe-Wong, Cardoso, Smith or Raghunathan, + 1 interp-credible external
                        (dream external: someone from Anthropic interp / DeepMind interp / David Bau's group)
```

**The Joe-Wong bridge, made concrete.** Don't force her profile onto interp; build a real intersection she can own:

- _Reliable multimodal ML in distributed/resource-constrained settings_ — grounding reliability as a deployment-reliability problem.
- _Federated or on-device VLMs_ — does grounding degrade under compression/personalization? (One workshop paper here cheaply cements the advising relationship and is honest, not decorative.)
- Frame your memo to her as: "Core thesis = mechanistic grounding reliability; one thrust examines reliability under the system constraints you study."

**The Smith approach (sequenced, per your locked preference):**

1. Send the finalized Aashiq email (this month — it is done; the bottleneck is the send button).
2. 2–4 exchanges → natural call → small collaboration surface (e.g., SAEs on a VLM, which is P3's seed).
3. Only then: short note to Smith referencing the concrete artifact, asking for 30 minutes — ideally with Aashiq's awareness.
4. Goal is _committee membership + group meeting access_, not displacing Joe-Wong. Co-advisor relationships at CMU are normal; an awkward advisor swap is not worth the political cost in a 4-year plan.

### 2.3 Annual Work Plan (program requirement, strategic tool)

The CMU–Portugal program requires a yearly Work Plan signed by you and both advisors, sent to FCT and the National Directors. Treat it as your _alignment forcing function_: it is the document where the Joe-Wong/Cardoso division of labor, the residency schedule, and the internship windows get made explicit and signed. Draft it yourself every year; never let it be boilerplate.

---

## 3. Program Mechanics (the rails you must run on)

### 3.1 Fixed requirements (ECE PhD, entering with external M.S.)

- **Coursework:** 4 ECE/related courses (48 units), ≥3 graduate-level, all B− or better; + 1-unit Intro to Graduate Studies (Semester 1). QPA ≥ 3.0.
- **Breadth:** graduate courses in 3 of 7 ECE areas. Primary fit: _Signal Processing & Communications_; pair with _AI/Robotics/Control_ and one more (_Algorithms/PL_ or _Software Systems_). Petition to count one M.S. course toward a breadth area → potentially only 2 new breadth courses.
- **Qualifying exam:** target Semester 2 (Spring 2027) — the typical latest point, and your compression plan demands it.
- **Research:** 18-990 every semester (section A in Pittsburgh, PP in Portugal). 37 units first Pittsburgh semester; 36 every semester thereafter.
- **Teaching Internships:** two — one at CMU, one in Portugal. Plan: TI-1 in Fall 2027 (CMU), TI-2 in Year 3 (FEUP). Aim for Deep Learning / Mathematics courses (your stated TA aspiration).
- **Prospectus:** typically ~Semester 7; your target = end of Year 3 (Spring 2029).
- **Thesis + Defense:** final milestone.
- **Residency:** ~3 years in Portugal, up to 2 at CMU (see §3.2 — this is the central tension with the 4-year target).
- **CITI RCR training** before research starts; FCT acknowledgment text on every publication once the fellowship is active.

### 3.2 The 4-year problem, stated honestly

The program's stated structure (3 years Portugal + up to 2 years CMU) naturally sums to **5 years**. A 4-year graduation therefore requires one of:

- **(a) 1 year CMU + 3 years Portugal** — feasible only if all coursework, the qual, and TI-1 compress into Year 1, and the CMU research relationships are strong enough to run remotely. High execution risk; weakens the Smith-cluster embedding that Priority 1 depends on.
- **(b) ~1.5–2 years CMU + ~2.5 years Portugal with an early defense** — requires confirming with Silvia Castro / National Directors how strictly the 3-year Portugal residency is enforced when the dissertation is done (some dual-degree students defend within the Portugal period without serving the full final year).
- **(c) Accept 4.5–5 years** but make Year 5 _cheap_: dissertation already written, final year mostly defense logistics + a frontier-lab internship or fellowship that serves Priority 1 and 3 simultaneously.

**Decision protocol:** Ask Greta Ruperto + Silvia Castro in **Month 1 (Sept 2026)**: (i) is the Portugal residency strictly 3 calendar years on FCT contract, (ii) can CMU time be 1 year, (iii) earliest permissible defense date. Put the answer in the first Work Plan. _Until answered, plan for option (b) with option (c) as the accepted fallback._ The plan below shows the 4-year aggressive track with the Year-5 buffer marked.

### 3.3 Funding & the FCT constraint map

|Period|Funding|Internship/earnings implications|
|---|---|---|
|CMU years|CMU stipend ($43,800/yr)|Summer internships possible via F-1 CPT with advisor + OIE approval. **This is the open earnings window.**|
|Portugal years|FCT fellowship (€1,359.64/mo)|**Exclusive dedication** — paid external work generally requires FCT suspension. Suspension/reactivation rules exist (Student Guide §12) but burn time.|
|While in Portugal|+ research-visit support: up to 6 months at CMU with up to €750/mo allowance|Use this in Year 3–4 to refresh CMU collaborations cheaply.|

**Strategic consequences:**

1. **Front-load industry internships into Summer 2027 and Summer 2028** (Anthropic, GDM interp, Amazon AGI/safety). They serve all three priorities at once: reputation (P1), speed (industry-scale experiments for P2/P3), earnings (P3-priority but frontier internships pay $10–15k+/mo).
2. **MATS:** verify compatibility with FCT _before_ the contract is signed (an Admin Question already in the vault). If incompatible during Portugal years, do MATS-equivalent work via the internships or the Anthropic Fellows route during CMU years instead.
3. **Earnings reality check:** the PhD years are reputation-accumulation years; the earnings payoff is the post-PhD offer (frontier-lab research scientist comp is the real Priority-3 instrument). Optimize internship _selection_ for the post-PhD offer, not the internship paycheck.

---

## 4. Year-by-Year Plan

### Year 0 — Pre-Arrival (June–August 2026, Kigali)

**Theme: arrive with a paper under review and the ecosystem doors already opening.**

Research

- [ ] **Send the Aashiq email** (finalized; send within 7 days of reading this).
- [ ] Execute the P1 minimal experiment (models × datasets × self-eval protocols table already exists). Target: workshop or findings-track submission by **August–October 2026**.
- [ ] Write the 1-page **PhD Research Vision Statement** (the planned doc) + two tailored variants: Joe-Wong memo (reliability framing) and Cardoso memo (explainability/visual-computing framing).
- [ ] Read deeply, narrowly: the SAE canon, activation patching / causal tracing methods, the 5–10 key VLM-hallucination papers, Pando, SmartCLIP. Maintain the Reading Map; everything feeds P2's related-work section.

Admin & logistics

- [ ] Visa (F-1/J-1 via OIE), enrollment, CITI RCR training.
- [ ] Confirm first-year location = Pittsburgh (per assumption; verify with Carlee/Greta).
- [ ] Contact **Blessed Guda** and **Rufimelo** for lived-experience guidance (housing, first-year traps, transfer timing).
- [ ] Pittsburgh housing secured by July.

Exit criteria for Year 0: P1 submitted or submission-ready; Aashiq thread alive; both advisor memos sent; visa in hand.

---

### Year 1 — CMU, Pittsburgh (Fall 2026 – Summer 2027)

**Theme: compress all program obligations into one year; ship the mechanistic core's first results; embed in the interp cluster.**

**Fall 2026 (Semester 1) — 37 units**

- Courses: 2 technical (one breadth, one directly useful — e.g., a deep learning / probabilistic ML graduate course) + Intro to Grad Studies (1 unit) + 18-990A.
- Sign Work Plan #1 (Joe-Wong + Cardoso) — encode the residency/qual/internship plan from §3.2's answers.
- **Month 1 admin sprint:** Greta + Silvia questions (§3.2 decision protocol); qual declaration timeline; TI scheduling; petition one M.S. course toward breadth.
- Attend Smith group meetings if/when invited (the Aashiq path); attend Raghunathan's and relevant SCS/MLD interp-adjacent reading groups regardless.
- P1: handle reviews/resubmission; P2: design experiments (model internals access — pick 1–2 open VLMs, e.g., LLaVA/Qwen-VL class, and build the patching/tracing infra once, reusably).
- December: NeurIPS attendance if P1 lands a workshop there — go regardless if budget allows; conference presence is ecosystem-entry.

**Spring 2027 (Semester 2) — 36 units**

- Courses: final 2 technical courses → **coursework complete**.
- **Qualifying exam: pass.**
- P2 experiments run; target submission to NeurIPS 2027 (May deadline) or ICLR 2028 (Sept) as fallback.
- Smith introduction happens this semester at the latest (with a concrete artifact in hand).
- Apply for Summer 2027 internships (applications run Oct 2026–Feb 2027 — calendar this in _Fall_): Anthropic interp/safety internship or Fellows program, GDM interp, Ai2, Amazon. CPT paperwork with OIE + advisor sign-off.

**Summer 2027**

- **Internship #1** (frontier lab, interp-adjacent) — or, if no offer, a focused research summer finishing P2 and seeding P3 with Aashiq.
- Keep P3 (SAE study) warm either way; internship learnings often legally feed methods (not artifacts) back into it.

Exit criteria for Year 1: coursework done, qual passed, P1 published, P2 submitted, Smith-cluster access real, internship #1 completed or P2/P3 advanced equivalently.

---

### Year 2 — CMU, Pittsburgh (Fall 2027 – Summer 2028)

**Theme: the reputation year. Two strong interp papers in flight; teaching done; Portugal transition engineered.**

**Fall 2027 (Semester 3)**

- **Teaching Internship #1** (CMU — target Deep Learning or a math-for-ML course).
- P2 camera-ready / resubmission; P3 in full execution (this is the natural Aashiq/Smith collaboration paper).
- Begin the **survey/position paper** (P6) as a low-intensity background thread — it forces the literature mastery the prospectus needs anyway.
- Draft thesis skeleton v0.1 (chapter map = paper map).
- Cardoso engagement intensifies: monthly calls; co-design Ch. 5 (the VCMI-anchored paper P5); identify the FEUP-side committee and Teixeira's role. **The Portugal years must be planned from Pittsburgh, not improvised on arrival.**

**Spring 2028 (Semester 4)**

- P3 submitted. P4 (interventions) designed.
- Work Plan #3 signed: encodes the **transfer to Portugal (Aug/Sept 2028)**, FCT contract activation, FEUP enrollment, residence-permit process (start visa paperwork ~4 months out; Student Guide §10–12 process).
- Apply for Summer 2028 **Internship #2** — the most strategically chosen one (ideally Anthropic interp if not already done; this is the last clean window before FCT exclusive dedication).
- FCT formalities: contract docs, scholarship reference, acknowledgment text into your paper templates.

**Summer 2028**

- Internship #2, ending in time for Portugal arrival (Portuguese academic year starts late Aug–mid Sept).

Exit criteria for Year 2: P2 + P3 accepted or in strong revision; both internships done; TI-1 done; transfer executed; thesis skeleton v1 agreed by both advisors.

---

### Year 3 — FEUP / Porto (Fall 2028 – Summer 2029)

**Theme: the Portugal years are not exile from interp — they are where the thesis consolidates and the intervention/application work lands.**

- FCT contract active; 18-990 section PP; arrival reporting to CMU Portugal office (and every address change within 10 days).
- Embed in **VCMI**: weekly group presence, co-supervise a master's student if offered (cheap leadership signal), engage Teixeira as the local interp interlocutor.
- **P4 (interventions/steering)** executed and submitted — compute via FEUP/INESC TEC clusters + EuroHPC applications + any frontier-lab API credits from internship relationships.
- **P5 (VCMI-anchored)** launched: mechanistic reliability of medical VLMs _or_ the information-theoretic account — choose by what P2/P3 revealed and what Cardoso can champion.
- **Teaching Internship #2** at FEUP.
- Remote rhythm with CMU: biweekly Joe-Wong calls, monthly Smith-cluster check-ins, the periodic three-way advisor calls the program expects.
- **Prospectus: written Fall 2028–Spring 2029, defended by end of Spring 2029** (this is the 4-year track's hinge; the standard track would put it Fall 2029).
- Use the **CMU research-visit support** (up to 6 months, €750/mo allowance) to plan a Spring/Summer 2029 Pittsburgh visit — synchronize with P4's submission cycle and committee formation.
- FCT renewal paperwork 90 days before the deadline (calendar it on arrival).

Exit criteria for Year 3: prospectus defended; P4 submitted; P5 underway; committee fully formed; FCT renewed.

---

### Year 4 — FEUP / Porto (Fall 2029 – Summer 2030)

**Theme: write the dissertation while the last papers land.**

- **Fall 2029:** P5 submitted. Dissertation writing sprint — chapters 2–4 are largely assembled from P1–P4; the real writing is the introduction, the unifying framework, and the synthesis chapter. Target: full draft by **February 2030**.
- **Spring 2030:** committee review cycle; **defense target: May–July 2030** (4-year track), satisfying both CMU ECE and FEUP defense requirements (run both checklists in parallel from January — dual-degree paperwork is slow).
- Post-PhD positioning runs _concurrently_: frontier-lab research scientist applications open ~6–9 months before start dates; faculty applications (if desired) are due Nov–Dec 2029 for Fall 2030 starts. Decide the lab-vs-faculty question by **Summer 2029** so Year 4 applications are aimed.
- If §3.2 answers force the 5-year shape: defense moves to late 2030–Spring 2031, and Year 5 becomes a low-cost year — dissertation done, possibly an FCT-compatible research visit or (post-fellowship-end) a pre-start industry period.

### Year 5 — Buffer (Fall 2030 – Spring 2031) — _only if required by residency rules or paper delays_

- Defense, dual-degree certification (CMU ECE PhD + U. Porto PhD), $0.00 tuition balance, paperwork.
- Bridge employment: if FCT has ended, a research-engineer/scientist contract or extended internship at the destination lab converts dead time into Priority-3 income and a warm start.

---

## 5. Milestone Tracker (single view)

|Milestone|Standard timing|This plan|Status|
|---|---|---|---|
|P1 submitted|—|Aug–Oct 2026|☐|
|Coursework + breadth complete|by ~S4|**Spring 2027**|☐|
|Qualifying exam|by S2|**Spring 2027**|☐|
|Internship #1|—|Summer 2027|☐|
|P2 submitted (mechanistic core)|—|Spring–Fall 2027|☐|
|TI #1 (CMU)|F2|Fall 2027|☐|
|P3 submitted (SAE/features)|—|Spring 2028|☐|
|Internship #2|—|Summer 2028|☐|
|Transfer to Portugal + FCT active|varies|Aug–Sept 2028|☐|
|TI #2 (FEUP)|S3 era|2028–29|☐|
|Prospectus|~S7|**Spring 2029**|☐|
|P4 submitted (interventions)|—|2029|☐|
|P5 submitted (domain/theory)|—|Fall 2029|☐|
|Dissertation draft|—|Feb 2030|☐|
|**Defense**|S5 era|**May–Jul 2030** (buffer: 2031)|☐|

---

## 6. Ecosystem & Visibility Strategy (Priority 1 engine)

Being "top" is one-third papers, one-third problem ownership, one-third network legibility. Schedule all three:

1. **Problem ownership.** By Year 2, your name should be the answer to "who works on multimodal mech interp at CMU?" Instruments: P2, P3, the P6 survey, a well-maintained open-source patching/SAE-for-VLMs toolkit released with P2 (toolkits generate citations and collaborators disproportionately to effort).
2. **Community presence.** One major conference per year minimum (NeurIPS or ICLR), plus interp-specific venues/workshops. Volunteer to review early (NeurIPS/ICLR reviewer by Year 2 — ask Smith/Raghunathan to nominate). Post readable research threads/blog posts per paper; interp as a field rewards legible public communication unusually highly (Distill/Anthropic-circuits culture).
3. **Strategic collaborations.** One paper with the Smith cluster (P3), one with VCMI (P5), one industry-internship paper if the lab permits. Three distinct collaboration surfaces = three independent reference networks at job-market time.
4. **Fellowship layer** (prestige + Priority 3): Anthropic AI Safety Fellows, Open Phil early-career funding, Vitalik/LTFF-style safety grants, CMU Presidential fellowships, Fulbright-adjacent CMU-Portugal awards. One application cycle per Fall, every Fall, from the Opportunity Calendar.

---

## 7. Risk Register

|#|Risk|Likelihood|Impact|Mitigation|
|---|---|---|---|---|
|R1|**Advisor-fit gap with Joe-Wong** strains the official advising line|Med|High|The reliability-framing memo + one honest shared-interest workshop paper (federated/efficient VLM reliability); clarify her preferred role explicitly in Sem 1; Smith as intellectual co-engine without political displacement|
|R2|**Smith cluster doesn't open** (Aashiq unresponsive / group full)|Low–Med|High|Parallel paths: Raghunathan, Xie, SCS interp reading groups, external collaborators (internships, MATS network); P2 is executable solo with open models|
|R3|**4-year target collides with 3-year Portugal residency**|Med–High|Med|§3.2 decision protocol in Month 1; pre-accept the 5-year shape with a cheap Year 5; everything else in the plan is unchanged either way|
|R4|**FCT exclusive dedication blocks MATS/internships in Years 3–5**|High|Med|Front-load both internships into 2027/2028; verify MATS compatibility before signing; use suspension rules only if the opportunity is exceptional|
|R5|**Portugal-period isolation from interp community**|Med|High|Teixeira as local anchor; CMU research-visit mechanism (6 mo, funded); standing remote rhythms; European interp community (EleutherAI, Apollo, UK AISI orbit, ELLIS) is timezone-adjacent to Porto — a feature, not a bug|
|R6|**P2 mechanistic results are messy/negative**|Med|Med|Negative/nuanced mechanistic findings publish well in interp if rigorous (the field rewards careful falsification); design P2 with a taxonomy fallback claim|
|R7|**Compute scarcity for internals work in Portugal**|Med|Med|INESC TEC/EuroHPC allocations applied for in Year 2; choose open models sized to available compute; internship-era relationships for API/compute credits|
|R8|**Burnout from the compression schedule**|Med|High|The vault's Aliveness Plan / Anti-Burnout Protocol are load-bearing, not decorative: weekly review, one non-work block per week, the "what artifact by Friday?" cadence prevents both drift and grind|
|R9|**Visa/immigration delays at either transition**|Low–Med|Med|Start each visa process 4+ months early; OIE + Silvia Castro on speed dial; keep document pack (transcripts, FCT letters, funding proofs) perpetually current|
|R10|**Field shift: interp paradigm moves (e.g., away from SAEs)**|Med|Med|Thesis is framed around _grounding_ (the problem), not SAEs (a tool); tools are swappable, the question is durable|

---

## 8. Operating Rhythm (how the plan executes weekly)

- **Daily:** open `00_dashboard.md`; one deep-work block on the active project before anything reactive.
- **Weekly:** Weekly Review (already templated). The forcing question stands: _What artifact will exist by Friday?_
- **Monthly:** Pipeline review (max 1 active, 2 candidates); Opportunity Calendar check; advisor-relationship next-actions updated.
- **Per semester:** milestone tracker (§5) reviewed against reality; Work Plan deltas logged; one explicit go/no-go on the 4-vs-5-year track.
- **Per year:** Work Plan signed; IDP updated; thesis skeleton revised; "would a top interp researcher recognize this trajectory?" gut check with one senior person.

---

## 9. Immediate Next Actions (next 30 days)

1. **Send the Aashiq email.** (Done > perfect; it is already final.)
2. Run the P1 minimal experiment; lock the strongest claim (self-evaluation reliability vs. grounding failure — decide via pilot data, not deliberation).
3. Draft the 1-page Research Vision Statement + the Joe-Wong and Cardoso memo variants.
4. Email Greta Ruperto / Silvia Castro the §3.2 residency questions (they answer faster pre-arrival than you'd expect).
5. Message Blessed Guda and Rufimelo.
6. Calendar the Fall 2026 internship-application season (Anthropic/GDM/Ai2 postings open Sept–Oct).
7. File this document in the vault as `00_Home/PhD Master Plan.md` and link it from `Now.md` and the Dashboard.

---

_Plan version 1.0 — 2026-06-10. Review and revise at each semester boundary. The plan is a hypothesis; the weekly artifacts are the experiment._