---
type: formal-research-questions
status: active
layer: 2-formal
tags: [research, questions, formal]
---

# Formal Research Questions

These are promoted, scoped versions of the curiosities in [[01_Research/Research Questions Map]].

Each question should be answerable, scoped, and connected to both concepts and papers.

## Q1: VLM Self-Evaluation Reliability

**Question:** To what extent can vision-language models reliably judge whether their own outputs are causally supported by visual evidence in the input image, and what failure modes characterize self-evaluation breakdowns?

**Why it matters:** If VLMs cannot reliably judge whether their answers are grounded, then self-correction, hallucination detection, and model-based evaluation systems are fragile.

**Possible contribution:** A benchmark or evaluation protocol for VLM self-evaluation of grounding; a taxonomy of failure modes; a calibration method for improving grounding reliability.

**Current uncertainty:** Whether self-evaluation should be operationalized as asking the model to judge its own output, asking a second model to judge, or using likelihood/internal-state measures.

**Status:** Active project: [[02_Projects/Active/VLM Self-Evaluation and Grounding Reliability]].

## Q2: Information Preservation Through Cross-Modal Projection

**Question:** How much semantic visual information is preserved versus systematically lost when a VLM converts patch-level visual features into language-aligned representations, and can this be quantified using mutual information estimation or practical proxies?

**Why it matters:** If grounding failures are caused by information loss at the projection layer, interventions should target architecture and representation alignment. If not, the failure may be downstream.

**Possible contribution:** A mutual information or proxy audit of the cross-modal projection step across VLM families; a characterization of which visual features are compressed away.

**Current uncertainty:** Mutual information estimation in high-dimensional continuous spaces is noisy and may require proxy measures.

**Status:** Candidate: [[02_Projects/Candidates/Information-Theoretic Framework for Visual Grounding]].

## Q3: Circuit Identification For Grounding In VLMs

**Question:** Are there identifiable internal circuits in open-weight VLMs that are causally responsible for visual grounding, and can these circuits be distinguished from those responsible for fluent text generation?

**Why it matters:** Identifying grounding circuits would connect VLM grounding to mechanistic interpretability and enable targeted interventions such as ablation, patching, and steering.

**Possible contribution:** A circuit map for one open VLM; evidence for or against modularity of grounding; activation patching experiments on grounded versus ungrounded generation.

**Current uncertainty:** Multimodal circuit methods are much less mature than language-only mech interp methods.

**Status:** Spark: [[02_Projects/Sparks/Mechanistic Interpretability of Visual Circuits in VLMs]].

## Q4: SAE-Based Visual Feature Discovery In VLMs

**Question:** Can sparse autoencoders applied to cross-modal representations in open VLMs recover interpretable visual features, and do those feature activations predict grounding success or failure?

**Why it matters:** If SAEs recover useful multimodal features, they could provide a dictionary of visual concepts used by the model.

**Possible contribution:** A VLM-specific SAE training pipeline; a feature dictionary for a cross-modal layer; correlation between feature activations and grounding quality.

**Current uncertainty:** It is unclear whether cross-modal representations have the same sparse structure that makes SAEs successful in LLMs.

**Status:** Spark / possible extension of Aashiq-adjacent work.

## Q5: Hallucination As A Data Processing Inequality Failure

**Question:** Can visual hallucination in VLMs be characterized as a failure to preserve sufficient task-relevant mutual information between image representations and output tokens?

**Why it matters:** This could give hallucination a more precise information-theoretic definition and suggest objectives that preserve visual evidence.

**Possible contribution:** A formal definition; an empirical test linking hallucination to information loss; a sketch of a training objective.

**Current uncertainty:** The difficult piece is defining semantic visual information in a way that can be measured.

**Status:** Candidate/theory: [[01_Research/Information-Theoretic Vision]].

## Q6: Counterfactual Visual Interventions For Grounding Attribution

**Question:** Can counterfactual image interventions, while holding the question constant, reveal whether a VLM answer is caused by visual evidence or by language priors?

**Why it matters:** Many VQA examples can be answered without the image. Counterfactual tests can expose this.

**Possible contribution:** A counterfactual grounding protocol; a dataset of controlled image edits; analysis of image-independent answer behavior.

**Status:** Seed / promising wedge for the active project.

## Q7: Distributional Robustness Of Grounding Under Visual Shift

**Question:** How does visual grounding reliability degrade under background, lighting, viewpoint, texture, style, or domain shift, and are different VLM architectures vulnerable to different shifts?

**Why it matters:** Grounding robustness is central to reliable deployment and may reveal which visual signals models actually use.

**Possible contribution:** A controlled robustness benchmark for grounding under visual distribution shift.

**Status:** Seed.

## Q8: Linear Probing For Grounding State During Generation

**Question:** Can linear probes trained on VLM intermediate representations distinguish grounded generation from prior-driven generation during inference?

**Why it matters:** A successful probe could become a lightweight grounding monitor.

**Possible contribution:** A probing framework and evidence for whether groundedness is linearly represented.

**Status:** Seed.

## Q9: Grounding Calibration In VLMs

**Question:** Are VLMs calibrated in their expressed confidence about visually grounded claims, and can calibration be improved?

**Why it matters:** A trustworthy VLM should know when visual evidence is weak, ambiguous, or absent.

**Possible contribution:** A grounding calibration benchmark and calibration improvement method.

**Status:** Seed / natural extension of Q1.

## Q10: Cross-Modal Representation Geometry And Grounding Quality

**Question:** Does the geometry of cross-modal representation space predict grounding quality, and can representation-level interventions improve grounding?

**Why it matters:** If grounding is predictable from representation geometry, projection-layer training objectives could directly improve it.

**Possible contribution:** A geometric analysis of cross-modal representations across VLMs, connected to grounding metrics.

**Status:** Seed / possible SmartCLIP-adjacent collaboration direction.

## Priority Matrix

| Question | Tractability | Novelty | Status | First artifact |
|---|---|---|---|---|
| Q1 Self-evaluation reliability | High | Medium-high | Active | Benchmark protocol |
| Q2 Information through projection | Medium | High | Candidate | MI/proxy audit |
| Q3 Grounding circuits | Medium | High | Spark | Tool/model map |
| Q4 SAE visual features | Medium-high | High | Spark | SAE feasibility note |
| Q5 DPI hallucination | Low-medium | High | Candidate | One-page formalization |
| Q6 Counterfactual interventions | High | Medium | Seed | Image intervention dataset |
| Q7 Distributional robustness | High | Medium | Seed | Robustness benchmark design |
| Q8 Grounding state probes | Medium | Medium-high | Seed | Probe experiment |
| Q9 Grounding calibration | High | Medium | Seed | Calibration evaluation |
| Q10 Representation geometry | Medium | High | Seed | Geometry notebook |

## Connections Across Questions

- Q1 and Q9: self-evaluation and calibration.
- Q1 and Q6: robust grounding evaluation.
- Q2 and Q5: information loss and hallucination theory.
- Q3 and Q4: circuits and SAE feature discovery.
- Q3 and Q8: interventional versus observational grounding.
- Q7 and Q10: visual shift and representation structure.
- Q5 and Q10: information theory and representation geometry.
