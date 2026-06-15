---
project: College Agent
type: applied-ai
status: completed
year: 2025
tags: [LLM, FastAPI, PostgreSQL, RAG, tool-calling, full-stack, production-AI]
---

# College Agent: AI-Powered Admissions Guidance System

## One-Line Summary
Production-ready Kenya college admissions guidance platform combining deterministic educational scoring, database-backed eligibility intelligence, and an LLM-powered multi-turn chat assistant with grounded tool-calling.

## Two-Line Summary (for CVs)
Built a full-stack AI admissions guidance platform for Kenya using FastAPI, PostgreSQL, Next.js, and LangGraph. Implemented structured retrieval over relational admissions data, tool-calling workflows for eligibility checking, and grounded LLM response generation with grade parsing and multi-turn state management.

## Problem
Kenyan high school students navigating college admissions face a complex system (KCSE grades → cluster points → programme cutoffs → eligibility) that's hard to understand without expert guidance. Most students lack access to counselors who know the full system.

## Brian's Role
- Full system design and implementation
- Backend: FastAPI + PostgreSQL database of programmes, cutoffs, clusters, offerings
- LLM integration: LangGraph multi-turn chat, tool-calling for eligibility queries
- Frontend: Next.js + React chat interface
- Deployment: Railway (backend) + Vercel (frontend)

## Tech Stack
FastAPI, Pydantic, PostgreSQL, Prisma, Next.js, React, Tailwind CSS, LangGraph, Tavily, Railway, Vercel

## Key Features
- Deterministic KCSE grade → cluster point calculation
- Database-backed eligibility checking across programmes and institutions
- LLM-powered chat with grounded responses (tool-calling over real data)
- Grade parsing, state normalization, multi-turn conversation management
- Recommendation, search, and report generation tools

## Why It Matters
Demonstrates Brian can build production AI systems — not just research prototypes. Real data, real users, real deployment. Shows FastAPI + PostgreSQL + LLM integration in a complete product.

## Variants for Different Applications

### ML/AI engineer framing (primary)
"Production full-stack AI application: LLM chat assistant with structured retrieval over relational databases, tool-calling workflows, and multi-turn state management. FastAPI backend + Next.js frontend, deployed on Railway/Vercel."

### Applied AI framing
"AI system combining deterministic logic with LLM reasoning: grade calculations are deterministic; eligibility reasoning is LLM-assisted with grounded retrieval. Shows understanding of when to use rules vs. models."

## Links
- Code: [GitHub — confirm public]
- Live demo: [if available]
