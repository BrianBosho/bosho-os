---
project: RoboCRAM / RoboCHAT
type: capstone
status: completed
year: 2025
tags: [robotics, LLM, human-robot-interaction, RAG, symbolic-planning, NLP]
---

# RoboCRAM: LLM-Powered Human-Robot Interaction

## One-Line Summary
Middleware layer enabling natural language control of a PR2 robot by bridging an LLM-powered chat agent with PyCRAM symbolic task planning, achieving 89% command and 85% parameter resolution accuracy.

## Two-Line Summary (for CVs)
Developed RoboCRAM, a middleware connecting LLM-based chat agents to symbolic robot task planning (PyCRAM), enabling users to issue high-level natural language commands executed as robot actions. Integrated a FAISS-based RAG pipeline for contextual understanding; achieved 89% command and 85% parameter resolution accuracy across 172 test cases.

## Problem
Robots using symbolic planning (like PyCRAM) require precise, structured commands. Natural language is ambiguous and unstructured. Bridging the gap — allowing humans to speak naturally while robots execute precisely — requires a translation layer that understands context, resolves ambiguity, and maps language to symbolic actions.

## Brian's Role
- Designed the RoboCRAM middleware architecture
- Built the LLM-based chat agent as the natural language interface
- Implemented FAISS-based RAG pipeline for contextual grounding
- Designed command parsing and parameter resolution pipeline
- Evaluated across 172 structured test cases

## Methods and Tools
- LLM integration (chat agent design)
- Retrieval-Augmented Generation (FAISS vector store)
- PyCRAM (symbolic task planning for robotics)
- PR2 robot platform
- Python

## Key Results
- 89% command resolution accuracy
- 85% parameter resolution accuracy
- 172 test cases evaluated
- Demonstrated natural language → symbolic plan → robot execution pipeline

## Framing Note
This is a capstone project, not deep robotics research. Present as systems/integration work, not as core research contribution. Best used to demonstrate LLM systems ability, RAG implementation, and end-to-end AI application building.

## Variants for Different Applications

### LLM systems / AI engineer framing
"Built an LLM-powered robot control system with RAG-based contextual understanding, achieving 89% command and 85% parameter accuracy across 172 test cases. Demonstrates end-to-end AI system design from natural language to physical robot action."

### Research framing (use sparingly)
"Capstone project exploring natural language grounding for symbolic robot planning — relevant to embodied AI questions about language-action alignment."

## Links
- Demo: [if available]
- Code: [GitHub — confirm status]
