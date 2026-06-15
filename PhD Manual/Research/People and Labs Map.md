---
type: people-labs-map
status: seed
tags: [research, people, labs, vlm, interp, safety]
---

# People and Labs Map

This note tracks people, labs, and research ecosystems relevant to the PhD direction.

Purpose:

- know who is shaping the field
- identify papers to read
- identify possible collaborators/mentors
- identify fellowship/internship targets
- avoid discovering important communities too late

Rule:

> Add people/labs when they connect to a real paper, project, opportunity, or conversation.

---

## 1. CMU / Pittsburgh Ecosystem

### CMU MultiComp Lab / Multimodal ML

Why relevant:

- multimodal learning
- language/vision/audio grounding
- representation and evaluation of multimodal systems
- strong local ecosystem for multimodal AI

Possible connection:

- seminars
- reading groups
- students working on multimodal models
- possible feedback on VLM grounding direction

Next action:

- identify 3 recent papers from the lab that overlap with VLM grounding/reliability.

---

### CMU Machine Learning / AI Safety / Interpretability-adjacent People

Why relevant:

- possible altitude checks
- technical direction calibration
- collaborators outside ECE

Current known contacts:

- [[03_People/Mentors/Aashiq]]
- [[03_People/Target_Advisors/Virginia Smith]]

Next action:

- use Aashiq conversation to identify 3-5 CMU people/students who understand mechanistic interpretability or AI safety.

---

## 2. FEUP / Portugal Ecosystem

### Jaime Cardoso / Visual Computing / Explainability

Why relevant:

- FEUP anchor
- visual computing
- explainability
- possible medical AI / trustworthy AI connection

Current note:

- [[04_Program_Admin/Program_Contacts/Jaime Cardoso]]

Possible framing:

> VLM grounding and interpretability as an extension of visual explainability: not only what the model predicts, but whether its language output is visually supported.

Next action:

- prepare a concise research direction brief to discuss fit with FEUP work.

---

## 3. VLM / Multimodal Model Labs

### Salesforce AI Research

Why relevant:

- BLIP and InstructBLIP line of work
- strong history in vision-language model pretraining and instruction tuning

Research connection:

- architecture and training background for VLMs
- grounding and hallucination evaluation in instruction-tuned VLMs

What to read:

- BLIP
- InstructBLIP
- related VLM evaluation/hallucination papers

---

### Google DeepMind / Flamingo and Multimodal Models

Why relevant:

- Flamingo and later multimodal foundation model work
- few-shot multimodal learning
- large-scale VLM architecture and evaluation

Research connection:

- understanding architecture families and scaling behavior
- multimodal grounding and reasoning benchmarks

---

### OpenAI / Multimodal Models

Why relevant:

- frontier multimodal models
- practical safety and deployment questions
- grounding, reliability, and evaluation in production-scale systems

Research connection:

- safety cases
- evaluation of multimodal reliability
- eventual internship/fellowship interest

---

### Anthropic / Interpretability and AI Safety

Why relevant:

- mechanistic interpretability
- sparse autoencoders
- circuit tracing
- AI safety research ecosystem

Research connection:

- tools and conceptual framing for internal mechanisms
- possible bridge from VLM grounding to safety/interp

Next action:

- track whether multimodal interpretability work emerges or whether language-model methods transfer to VLMs.

---

## 4. Mechanistic Interpretability Ecosystem

### Transformer Circuits / Anthropic Interpretability

Why relevant:

- core mechanistic interpretability concepts
- activation/circuit analysis
- sparse features
- causal tracing/circuit tracing direction

Possible connection to VLMs:

- adapt language-model interpretability tools to multimodal models
- study whether visual evidence is routed through identifiable pathways

---

### MATS / AI Safety Mentorship Ecosystem

Why relevant:

- structured mentorship
- connects students to frontier safety researchers
- possible path into mechanistic interpretability and safety community

Related note:

- [[05_Opportunities/Opportunity Calendar]]

---

## 5. Research Figure Categories to Track

Instead of overfilling this note with names too early, track categories:

### VLM Architecture People

People/labs behind CLIP, BLIP, InstructBLIP, Flamingo, LLaVA, Qwen-VL, etc.

Use for:

- understanding model families
- finding open models
- choosing experiment targets

### VLM Hallucination / Grounding Benchmark People

People/labs working on:

- POPE
- CHAIR
- HallusionBench
- MMHal-Bench
- MME-style evaluation
- object hallucination
- claim-level hallucination

Use for:

- active project related work
- benchmark selection

### Multimodal Interpretability People

People/labs working on:

- VLM attribution
- activation patching in multimodal models
- visual token analysis
- cross-modal feature analysis
- multimodal circuits

Use for:

- Project 3 and altitude checks

### Information Theory / Representation Learning People

People/labs working on:

- information bottleneck
- representation learning theory
- mutual information estimation
- rate-distortion
- causal representation learning

Use for:

- long-term theoretical layer

---

## 6. Relationship Pipeline

For each person/lab worth tracking, eventually create a short note with:

- why relevant
- papers to read
- relationship status
- possible question to ask
- next action

Do not create a separate people note unless there is a real next action.
