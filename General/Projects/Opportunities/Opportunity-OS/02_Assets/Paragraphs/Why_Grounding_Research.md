---
type: asset
asset-type: paragraph-module
topic: Why visual grounding / the research problem
use-for: PhD motivation letters, fellowship statements, research summaries
---

# Paragraph Module: Why Visual Grounding

## Version A — Full problem statement (for motivation letters)
Vision-language models exhibit two distinct failure modes that emerge from the same root cause. In some cases, they are right for the wrong reason — exploiting statistical shortcuts and language priors to produce correct answers without processing the visual evidence. In others, they fail catastrophically — hallucinating objects, misreading dynamics, generating confident responses unconstrained by what the image shows. Both failures share a common feature: the model's internal representations have become decoupled from the visual input. My research aims to make this decoupling measurable and preventable.

## Version B — Mechanism-focused (for research-oriented readers)
The core challenge is that current evaluation methods are external: they measure whether outputs are correct, not whether the process that produced them was genuinely visual. What is needed are intrinsic diagnostic tools — methods that can examine internal model states and determine, without ground-truth labels, whether representations are grounded in visual input or floating on language priors. This is the gap my Visual Groundedness Toolkit is designed to close.

## Version C — Concise (for shorter letters)
Current VLMs can be simultaneously accurate and perceptually groundless — the benchmark measures the output, not the mechanism. My research develops intrinsic tools to measure visual grounding from internal model states, localize where the visual signal is lost or overwritten, and build faithfulness-aware training objectives that push models toward genuine perception.
