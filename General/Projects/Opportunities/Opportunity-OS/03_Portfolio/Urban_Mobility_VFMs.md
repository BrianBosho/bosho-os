---
project: Urban Mobility VFMs
type: research
status: active
year: 2025-present
tags: [computer-vision, VLM, foundation-models, urban-mobility, low-resource, Africa, distribution-shift]
---

# Vision Foundation Models for Urban Mobility (Kigali)

## One-Line Summary
Research program evaluating and improving vision foundation models for traffic scene understanding in low-resource African urban environments, where standard sensor suites are too expensive and distribution shift is severe.

## Two-Line Summary (for CVs)
Building and curating an urban mobility dataset for Kigali to evaluate vision foundation models under real-world distribution shift. Developing benchmarking workflows and experimental pipelines for robust visual data mining in data-scarce, sensor-poor environments.

## Problem
Urban mobility analysis in African cities typically cannot rely on expensive LiDAR, depth cameras, or radar. Only monocular cameras are financially viable. Yet traffic scenes in cities like Kigali are highly unstructured — different vehicle types, informal rules, dense pedestrian-vehicle mixing — and severely underrepresented in existing training data. Current VLMs fail frequently: hallucinating objects, misreading scene dynamics, and producing confident wrong answers under distribution shift.

## Brian's Role
- Curating a purpose-built Kigali traffic scene dataset
- Designing benchmarking workflows to evaluate VFM robustness under distribution shift
- Building experimental pipelines for dataset preparation, model testing, and comparative analysis
- Working with diffusion models for dataset augmentation and visual grounding
- Analyzing failure modes of current VLMs in non-standard traffic scenarios

## Methods and Tools
- Vision Foundation Models (evaluation and probing)
- Diffusion models (for dataset augmentation)
- Monocular camera processing pipelines
- Dataset curation and benchmark design
- Python, PyTorch, computer vision toolkits

## Key Results
- [In progress — update as results emerge]
- Dataset covering Kigali traffic scenes (in development)
- Benchmarking framework for VFM robustness in low-resource settings

## Why It Matters
AI for urban mobility in Africa cannot simply import Western datasets and pretrained models — the distribution gap is too large and the sensor constraints too different. Building infrastructure for evaluation and adaptation in these contexts is a prerequisite for AI that works where it is most needed.

## Core Lesson Brian Draws From This
"Every day in this role I see VLMs be confidently wrong — hallucinating objects, misreading interactions, ignoring the visual evidence in front of them. These are not edge cases; they are systematic. This daily exposure to failure modes is what turned my research question from abstract to urgent: how do we build systems that actually use what they see?"

## Variants for Different Applications

### Research framing (PhD apps — primary use)
"My current work on urban mobility in Kigali is the empirical grounding for my research questions. The failure modes I document daily — confident hallucinations, brittleness under distribution shift, performance collapse on non-Western scenes — are exactly the pathologies my Visual Groundedness Toolkit aims to diagnose and prevent."

### Africa / low-resource framing
"Building AI infrastructure for urban mobility in resource-constrained African cities — dataset curation, model evaluation, and robustness analysis under the realistic constraint that only monocular cameras are available."

### Applied research framing
"Active research on applying and evaluating vision foundation models in real-world, data-scarce environments, including dataset construction and systematic benchmarking of VFM failure modes."

## Links
- Supervisor: [Name, CMU-Africa — UPDATE]
- Code: [GitHub — confirm status]
- Dataset: [Not yet public — update when available]

## Note for Agents
This is an active project — update results and links as the research progresses. When drafting applications, always present this as current, active research (not past experience).
