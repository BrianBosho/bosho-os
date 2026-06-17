Clinical decision support?

Link: https://docs.google.com/spreadsheets/d/1uPBbqx8NvinGqx1YTVsxrnSUfNA3szWV/edit?gid=55841821#gid=55841821 

 https://drive.google.com/drive/folders/1MBTmrl-I5pVHt-vXWRRuaJc8nC7ZP3F0 
**Inputs:**
- Data from the transcripts & the image - C2 not now!

Kinyarwanda Speech -> Kinywarwanda text -> English text:
- English text ->DSS -> Diagnosis (Based on the input symptoms, A patient has the following issues, recommend a tests)
- Based on test input recommend other tests or make a final decision -> 
- Recommending interventions: Drugs, advice, and other adjustments... 

DSS Components:
- Knowledge base
- LLM

Q/A- 

Conversation: 
- D/P: Do we have info
	- No: Ask more questions ->Which Questions?
	- Yes: Recommend test or make a diagnosis
RAG:
- Pass the info to an LLM: 
	- NLP Task: Capture relevant clinical information, and then it has to 
		-  How?
	- determine when the information it has is exhaustive. 
		- How?
- The LLM will use a RAG to:
	- 

**Outputs:**
- What questions to ask? 
	- narrow down on symptoms
	- Rule out conditions
- Recommending tests
- Make a diagnosis
- Recommend intervention. 

How 

**Design document**
- Inputs/Outputs
- Modules: LLM/RAG
- System requirements
- Functional requirements
- User requirements. 

**Implementation phases**
- LLM
- 