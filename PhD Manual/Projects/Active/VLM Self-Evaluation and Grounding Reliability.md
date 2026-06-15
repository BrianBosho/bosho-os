---
type: project
status: active
domain: PhD Manual
tags: [project]
---

# VLM Self-Evaluation and Grounding Reliability

## Stage

Active Project.

This is the only active project unless explicitly changed in [[02_Projects/Project Pipeline]].

## One-sentence question

Can a vision-language model reliably evaluate the quality of its own visual grounding, and under what conditions does self-evaluation fail?

## Why it matters

If VLMs cannot reliably judge whether their answers are grounded in the image, then self-correction, hallucination detection, deployment safety, and model-based evaluation systems become fragile.

## Connection to thesis identity

This is the first concrete entry point into the broader thesis direction:

> How visual evidence is represented, transformed, lost, or misused inside multimodal models.

This project can become the publishable core from which deeper information-flow and mechanistic questions emerge.

## Possible contribution

- A benchmark or evaluation protocol for VLM self-evaluation of grounding.
- An empirical analysis of when self-evaluation succeeds/fails.
- A taxonomy of grounding/self-evaluation failures.
- A calibration or intervention method for improving grounding reliability.
- A bridge from output-level self-evaluation to representation-level evidence flow.

## Current uncertainty

Need to clarify whether the strongest claim is about:

- self-evaluation reliability
- visual grounding failure
- hallucination detection
- confidence calibration
- model-internal evidence versus output-level judgment

## Minimal project brief

### Problem

VLMs produce fluent answers, but fluency does not guarantee visual grounding. A model may answer correctly from priors, hallucinate unsupported content, or fail to notice that its own answer is not visually supported.

### Hypothesis

VLM self-evaluation is systematically unreliable in cases where the model's output is semantically plausible but weakly supported by visual evidence.

### Smallest possible experiment

1. Select a small set of images/questions with known grounding requirements.
2. Generate answers from one or more VLMs.
3. Ask the same or another model to evaluate whether the answer is grounded.
4. Compare self-evaluation to human/benchmark grounding labels.
5. Categorize failure modes.

### Initial experiment table

| Component | Options / notes |
|---|---|
| Models | GPT-4o-like API model, open VLMs if accessible, LLaVA/Qwen-style models as possible open baselines |
| Data | VQA-style, hallucination datasets, grounding datasets, custom curated examples |
| Ground truth | human labels, benchmark labels, object/region annotations if available |
| Self-evaluation prompts | binary grounded/not grounded, explanation-based, evidence-citation, uncertainty rating |
| Metrics | accuracy, calibration, false grounded rate, false ungrounded rate, agreement with human labels |
| Analysis | failure taxonomy, qualitative examples, prompt/model sensitivity |

## Next two weekly tasks

1. Write a two-page project brief with:
   - research question
   - related work
   - dataset/model setup
   - evaluation metric
   - expected claim
   - target venue/workshop

2. Build a concrete experiment table with:
   - models
   - datasets
   - grounding tasks
   - self-evaluation methods
   - success/failure metrics
   - qualitative examples

## Feedback plan

- Send brief to current supervisor/collaborator.
- Use [[03_People/Mentors/Aashiq]] for an altitude-check version if the safety/interp angle is unclear.
- Ask whether this is interesting, too benchmarky, too vague, or thesis-relevant.

## Research questions to refine

- Is self-evaluation better framed as hallucination detection, grounding calibration, or evidence attribution?
- Does self-evaluation fail because the model lacks visual evidence, cannot access its own evidence use, or is biased toward plausible language?
- Can we separate answer correctness from visual groundedness?
- Can we design adversarial cases where language priors and visual evidence conflict?
- Can representation-level signals predict self-evaluation failures?

## Target outputs

- Internal memo.
- Workshop submission candidate.
- Dataset/evaluation artifact.
- Potential first PhD paper seed.

## Weekly log

### Week of YYYY-MM-DD

- Artifact:
- Experiments:
- Reading:
- Feedback:
- Next action:

