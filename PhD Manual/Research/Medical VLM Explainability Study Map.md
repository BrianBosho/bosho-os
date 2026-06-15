---
type: domain-study-map
status: active
area: medical-vlm-explainability
updated: 2025-06
---

# Medical VLM Explainability — Study Map and Reading Plan

> Organized around the thesis anchor: **"Faithful, grounded, and clinically meaningful explanations for medical vision-language models."**

## Vault fit

This is a domain-track study map for the Portugal / FEUP / VCMI side of the thesis.

It connects:

- [[01_Research/VLM Grounding]]
- [[01_Research/Mechanistic Interpretability]]
- [[01_Research/Formal Research Questions]]
- [[01_Research/Reading Map]]
- [[03_People/Portuguese AI and Visual Computing Ecosystem]]
- [[04_Program_Admin/Program_Contacts/Jaime Cardoso]]

Use this as the medical-domain bridge between general VLM grounding and clinical explainability. Do not merge it into the general reading map until a specific medical-VLM project becomes active.

---

## Part 1 — Strategic Assessment: What This Document Is and Why It Matters

### What this document represents

This is the **Portugal-side thesis track taking shape**, anchored by the Jaime Cardoso / VCMI / iMIMIC community. The iMIMIC 2025 volume is edited by Mauricio Reyes, Pedro Henriques Abreu, and Jaime Cardoso, and it explicitly frames interpretability as central to clinical trust, deployment, legal frameworks, and AI safety in healthcare. This reading list is essentially a curated entry point into Cardoso's research community. Reading it before arriving in Porto is exactly the right move.

The dual-degree structure means the thesis needs to hold together across two research cultures:

| Side | Advisor anchor | Community | Vocabulary |
|---|---|---|---|
| CMU (Pittsburgh) | Virginia Smith + Aashiq | Mechanistic interpretability, SAEs, circuits | Faithful = causally accurate |
| Portugal (Porto) | Jaime Cardoso (+ Luis Teixeira) | Medical XAI, iMIMIC, clinical deployment | Faithful = clinically trustworthy |

Both sides use the word **faithful** about explanations. That is the conceptual bridge the thesis needs to build on. The distinctive thesis position is: bring mechanistic interpretability methods to medical VLM explainability, and show that the standard clinical XAI methods (Grad-CAM, attention rollout) do not produce *faithful* explanations in the deeper causal sense — while demonstrating what genuinely faithful explanations of medical VLMs would look like.

### The strongest version of the thesis arc

```
Standard clinical XAI (Grad-CAM, saliency maps, attention visualization)
        ↓ produces visually plausible but causally unreliable explanations
Medical VLMs lack faithful grounding between visual evidence and text outputs
        ↓ this is a safety and trust problem for clinical deployment
Mechanistic interpretability methods (causal tracing, probing, circuits, SAEs)
        ↓ can identify what visual evidence actually caused each clinical claim
Faithful, grounded, clinically meaningful explanations
        ↓ explanations that are both clinically relevant and mechanistically honest
```

### Key tensions to resolve before committing

**Tension 1: Depth vs. publishability.**
Circuit analysis and SAE methods applied to medical VLMs are high-novelty but high-risk. Standard medical XAI with better evaluation is lower novelty but more publishable in clinical venues. The thesis will need at least one paper that the MICCAI/iMIMIC community finds immediately relevant, and ideally one paper that the NeurIPS/ICML mech interp community finds novel.

**Tension 2: The attention trap.**
Most medical XAI papers use attention visualization as explanation. The *Sanity Checks* paper (which this document wisely includes) shows that many saliency methods are uninformative about what the model actually does. Be careful not to build the thesis on a method that has already been shown to be unreliable. The thesis should position itself *after* understanding this critique, not before.

**Tension 3: Radiology vs. pathology.**
Radiology (chest X-rays) is more accessible (MIMIC-CXR is public, X-ray models are well-understood, CLIP-based architectures are standard). Pathology (whole-slide images) is technically harder but connects to the CONCH/VLEER/PLIP ecosystem. Decide on domain before going deep on either.

**Recommendation for now:** Start with radiology. It is more tractable, the datasets are larger and more accessible, and the phrase-grounding benchmarks (MS-CXR) directly operationalize visual grounding in a way you can experiment with quickly.

---

## Part 2 — Conceptual Map of the Domain

### The landscape in one diagram

```
MEDICAL VLM EXPLAINABILITY
│
├── WHAT the model sees (visual grounding)
│       ├── Phrase grounding: text ↔ image region alignment
│       ├── Cross-modal projection: visual → language space
│       └── Attention: which patches the model "attends to"
│
├── HOW explanations are produced (method taxonomy)
│       ├── Gradient-based: Grad-CAM, Integrated Gradients
│       ├── Attention-based: rollout, raw attention, DINO attention
│       ├── Concept-based: TCAV, prototype methods
│       └── Causal/mechanistic: activation patching, probing, SAEs ← underexplored
│
├── WHETHER explanations are faithful (evaluation)
│       ├── Correlation with ground truth annotations
│       ├── Counterfactual perturbation tests
│       ├── Sanity checks (randomization tests)
│       └── Falsification frameworks (x2x / "Explained AI")
│
└── HOW to IMPROVE grounding (training methods)
        ├── Explanation-guided learning: constrain attention / attribution
        ├── Text-guided spatial priors: MATEX, GLoRIA
        └── Structured report alignment: D-MLM
```

### The key distinction the thesis must own

**Clinical XAI:** Does the explanation help a clinician trust or act on the model's output?
**Mechanistic faithfulness:** Does the explanation accurately describe what caused the model's output?

These can diverge badly. A Grad-CAM heatmap can look clinically reasonable (highlights the lung region) while being mechanistically uninformative (the heatmap barely changes if you randomize the model weights — Adebayo et al. 2018, the Sanity Checks paper). The thesis should own the claim that **clinical trust requires mechanistic faithfulness as a prerequisite**, not a nice-to-have.

---

## Part 3 — Full Phased Reading Plan

### Reading approach

- **Tier 1:** Must read carefully. These define the landscape. Take paper notes.
- **Tier 2:** Read when the relevant research question demands it. Skim and note key claims.
- **Tier 3:** Know they exist. Check when writing related work.

**Study artifact rule:** After each phase, produce one written artifact (comparison table, synthesis memo, or proposal sketch) before moving on.

---

### Phase 0 — Domain Reorientation (Weeks 1–2)
*Goal: understand the clinical deployment context and immediately problematize the standard explanation methods before building on them.*

**Read in this order:**

**0.1 — Attention survey from the FEUP/Cardoso orbit (Tier 1)**
> Gonçalves, Rio-Torto, Teixeira, Cardoso — "A Survey on Attention Mechanisms for Medical Applications: Are We Moving Towards Better Algorithms?" (arXiv 2204.12406)

Why first: This is Cardoso and Teixeira's community directly. It asks the right framing question: does attention improve medical models, and does it help interpretability? The paper reaches nuanced conclusions. Reading this before anything else signals you are entering Cardoso's intellectual territory, not just parachuting in with a generic VLM agenda. There is also a GitHub repo — clone it.

*Study note:* Pay attention to where the survey distinguishes between attention as a *performance mechanism* and attention as an *explanation*. This is the core tension you will be building your thesis on.

---

**0.2 — The calibration papers: understand what explanations cannot do (Tier 1)**

> Adebayo et al. 2018 — "Sanity Checks for Saliency Maps" (arXiv 1810.03292)

Why early: This paper shows that widely-used saliency methods (Grad-CAM, vanilla backpropagation, SmoothGrad) sometimes produce explanations that are independent of both the model parameters and the training labels. A method that does not change when you randomize model weights is not explaining the model — it is explaining something else (the data structure, the edge detector, etc.). This is not a minor caveat; it fundamentally challenges the use of these methods in clinical contexts. Read this before reading any paper that uses Grad-CAM or attention visualization as its explanation method.

> Jain & Wallace 2019 — "Attention is not Explanation" (ACL 2019) ← CRITICAL ADDITION NOT IN THE ORIGINAL LIST

Why: The companion paper to Sanity Checks for attention-based explanations specifically. Shows that attention weights are often not faithful explanations of model predictions — you can permute attention weights without changing the output significantly, and different attention patterns can produce the same prediction. This is essential before engaging with any paper that treats attention rollout or raw attention as a grounding signal.

*Study note:* Together, these two papers are the critical framing device. They do not say XAI is worthless — they say that most XAI methods are not yet held to a rigorous standard of faithfulness. Your thesis is positioned in the space they open up.

---

**0.3 — The "Explained AI" pivot paper (Tier 1)**
> Authors TBD — "From Explainable to Explained AI: Ideas for Falsifying and Quantifying Explanations" (arXiv 2508.09205)

Why: This paper (from the iMIMIC volume) argues for falsifiable explanations — moving from "here is a heatmap" to "here is a claim that can be tested and falsified." This is the intellectually rigorous version of what the thesis should be. The x2x code repo should be cloned and studied alongside the paper.

*Study note:* The x2x framework is potentially usable as an evaluation methodology in the thesis. Understand its implementation before the Portugal year starts.

---

**Phase 0 artifact:** Write a 1-page note answering: "What is the current standard for explanation faithfulness in medical AI, and what are its known failure modes?" This will become a section of the thesis introduction.

---

### Phase 1 — Medical VLM Foundations: Image-Text Pretraining (Weeks 3–5)
*Goal: understand the architectural lineage of medical VLMs, from CLIP to GLoRIA to BioViL to MedKLIP.*

**1.1 — CLIP (Tier 1, likely already read)**
> Radford et al. 2021 — "Learning Transferable Visual Models From Natural Language Supervision" (arXiv 2103.00020)

You should already have this from the general reading map. Read it again with the medical framing in mind: CLIP is trained on global image-caption pairs. The features it learns are aligned at the *whole-image* level, not at the *patch-region* level. This is a fundamental limitation for fine-grained medical grounding (e.g., "consolidation in the left lower lobe"). Keep this limitation in mind throughout Phase 1.

---

**1.2 — ConVIRT (Tier 1)**
> Zhang et al. 2022 — "Contrastive Learning of Medical Visual Representations from Paired Images and Text" (Proc. MLHC 2022 / arXiv 2010.00747)

Why: The foundational paper applying contrastive image-text learning to radiology. Trained on MIMIC-CXR image-report pairs. The baseline every subsequent medical VLM is measured against. Understand its training objective, what it optimizes, and what it cannot represent (sub-region grounding, fine-grained attributes).

---

**1.3 — GLoRIA (Tier 1)**
> Huang et al. 2021 — "GLoRIA: A Multimodal Global-Local Representation Learning Framework for Label-Efficient Medical Image Recognition" (ICCV 2021)

Why: Critical architectural step. GLoRIA aligns report *words* with image *subregions* — not just whole-image with whole-caption. This is the first step toward grounding in the medical domain. Understanding how GLoRIA does this (attention-based cross-modal alignment, word-level vs. sentence-level contrastive loss) is essential before reading MATEX or BioViL.

*Study note:* GLoRIA's attention maps are used as grounding evidence. After reading Sanity Checks, ask: are GLoRIA's attention-based alignments actually faithful? This is a research gap.

GitHub: https://github.com/marshuang80/gloria

---

**1.4 — BioViL (Tier 1)**
> Bannur et al. 2022 — "Making the Most of Text Semantics to Improve Biomedical Vision-Language Processing" (arXiv 2204.09817)

Why: BioViL is the cleanest architecture for understanding phrase grounding in radiology. Uses a RadBERT-based text encoder and phrase-level grounding objectives. MS-CXR (the grounding benchmark) was created alongside BioViL. If you work on phrase grounding in radiology, this is the baseline model.

HuggingFace: microsoft/BiomedVLP-BioViL-T

---

**1.5 — MedCLIP (Tier 2)**
> Wang et al. 2022 — "MedCLIP: Contrastive Learning from Unpaired Medical Images and Texts" (EMNLP 2022)

Why: Important because it relaxes the need for perfectly paired image-report data, using semantic similarity to construct pseudo-pairs. Relevant for understanding data efficiency in medical VLM training. GitHub: https://github.com/RyanWangZf/MedCLIP

---

**1.6 — MedKLIP (Tier 1)**
> Yang et al. 2023 — "MedKLIP: Medical Knowledge Enhanced Language-Image Pre-Training in Radiology" (arXiv 2301.02228)

Why: Injects structured medical knowledge (disease entities, anatomical structure, attributes) into the training objective. Important because it shows that better *structured* text supervision improves visual grounding. Directly relevant to the D-MLM paper in Phase 3.

GitHub: https://github.com/MediaBrain-SJTU/MedKLIP

---

**1.7 — PRIOR (Tier 2)**
> Cheng et al. 2023 — "PRIOR: Prototype Representation Joint Learning from Medical Images and Reports" (arXiv 2307.12577)

Why: Prototype-based alignment — instead of learning pairwise similarity, learns class-prototype representations. Relevant to concept-level interpretability (connects to TCAV in Phase 2).

---

**1.8 — CheXzero (Tier 2) ← IMPORTANT ADDITION NOT IN THE ORIGINAL LIST**
> Tiu et al. 2022 — "Expert-level detection of pathologies from unannotated chest X-ray images via self-supervised learning" (Nature Biomedical Engineering 2022)

Why: Shows that zero-shot CLIP-based models can match radiologist performance on chest X-ray classification without labeled data. Important for understanding the ceiling of what these models can do and what is still missing (grounding, faithfulness, not just accuracy).

---

**Phase 1 artifact:** Build an architecture comparison table:

| Model | Visual encoder | Text encoder | Projection/alignment | Grounding capability | Key limitation |
|---|---|---|---|---|---|
| ConVIRT | ResNet-50 | ClinicalBERT | Global contrastive | None — global only | No sub-region alignment |
| GLoRIA | ResNet-50 | BioBERT | Word-level attention | Word ↔ patch | Attention not causally validated |
| BioViL | ViT | RadBERT | Phrase grounding | Phrase ↔ region | — |
| MedKLIP | ViT | BERT+KG | Knowledge-enhanced | Entity ↔ region | Requires KG annotation |
| MedCLIP | ViT | PubMedBERT | Semantic similarity | None — global | Paired data not required |

---

### Phase 2 — Explanation Methods and Their Limits (Weeks 6–8)
*Goal: develop a precise, critical understanding of the XAI toolbox — not to master every method, but to know exactly what each method can and cannot faithfully say about model behavior.*

**2.1 — Grad-CAM (Tier 1 — but read critically)**
> Selvaraju et al. 2017 — "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization" (arXiv 1610.02391)

Why: The standard baseline in visual explanation. Must understand exactly how it works (gradient of class score w.r.t. feature maps) before critiquing it. Note what Grad-CAM can and cannot say: it identifies *which feature map regions* correlate with a class score, not which *image patches causally determined* the output.

---

**2.2 — Integrated Gradients (Tier 1)**
> Sundararajan et al. 2017 — "Axiomatic Attribution for Deep Networks" (arXiv 1703.01365)

Why: Grad-CAM's axiomatically-motivated competitor. Attributes output to input features using path integrals from a baseline. Satisfies completeness and sensitivity axioms that Grad-CAM does not. Important for understanding what "attribution" means precisely.

*Study note:* The choice of baseline (black image, blurred image, random noise) is a major underappreciated design choice that affects results substantially. Write a note on this.

---

**2.3 — TCAV (Tier 2)**
> Kim et al. 2018 — "Quantitative Testing with Concept Activation Vectors (TCAV)" (ICML 2018)

Why: Moves from pixel-level attribution to concept-level interpretation. Instead of asking "which pixels mattered," asks "how much did this human-defined concept influence the prediction?" In the medical context, concepts could be "consolidation," "ground-glass opacity," "pleural effusion." Relevant because concept-level explanations may be more clinically meaningful than heatmaps.

---

**2.4 — Right for the Right Reasons (Tier 1)**
> Ross et al. 2017 — "Right for the Right Reasons: Training Differentiable Models by Constraining their Explanations" (arXiv 1703.03717)

Why: Foundational paper for explanation-guided learning (EGL). Shows you can penalize models for attending to wrong regions (e.g., background pixels irrelevant to the classification) using gradient penalties. This directly connects to H-EGL (Phase 3) and establishes the training-time intervention idea.

---

**2.5 — XGL Survey (Tier 1)**
> Gao et al. 2022 — "Going Beyond XAI: A Systematic Survey for Explanation-Guided Learning" (arXiv 2212.03954)

Why: The comprehensive map of the explanation-guided learning (EGL) field. Read this before reading H-EGL. It will tell you what has been tried, what works, and what remains open.

---

**2.6 — Tell Me Where to Look (Tier 2)**
> Mnih et al. / relevant guided attention paper — "Tell Me Where to Look: Guided Attention Inference Network" (arXiv 1802.10171)

Background for attention guidance methods.

---

**2.7 — Attention is Not Explanation (Tier 1 — already mentioned in Phase 0)**
> Jain & Wallace 2019 — ACL. Read here in full if only skimmed in Phase 0.

---

**Phase 2 artifact:** Write a 1-page synthesis: "Why do standard XAI methods for medical VLMs fail the faithfulness test, and what would a faithful explanation require?" This becomes a key argument in the thesis introduction.

---

### Phase 3 — Medical VLM Explainability: The Core Papers (Weeks 9–11)
*Goal: engage deeply with the papers most directly relevant to the thesis. These are the ones to know well enough to extend.*

**3.1 — MATEX (Tier 1 — highest priority paper in the whole list)**
> "MATEX: Multi-scale Attention and Text-Guided Explainability of Medical Vision-Language Models" (arXiv 2601.11666)

Why: This paper is the closest existing work to the thesis direction. It uses multi-scale attention and text-guided spatial priors to produce clinically meaningful attribution maps for medical VLMs. Read the methodology in detail: how does it use text to guide visual attribution? What is the multi-scale architecture? What evaluation does it use, and does that evaluation test faithfulness in the Sanity Checks / Jain-Wallace sense?

*The thesis gap question:* MATEX produces text-guided attribution maps. But does it verify that these maps causally determine the model's output, or just that they correlate with it? Answering this question with causal intervention methods is a concrete thesis contribution.

---

**3.2 — H-EGL: Hybrid Explanation-Guided Learning (Tier 1)**
> "Hybrid Explanation-Guided Learning for Transformer-Based Chest X-Ray Diagnosis" (arXiv 2510.12704)

Why: Combines human-guided and self-supervised attention alignment. The "hybrid" refers to using human annotation (clinician-provided region labels) alongside self-supervised signal to guide where the model attends. Important for the training-side approach to grounding.

*Study note:* What happens when H-EGL is evaluated against the Sanity Checks criteria? Do the explanation maps change if the model is randomly re-initialized? This is worth checking.

---

**3.3 — D-MLM: Distribution-Based Masked Medical VLM (Tier 1)**
> "Distribution-Based Masked Medical Vision-Language Model Using Structured Reports" (arXiv 2507.21794)

Why: Uses structured clinical reports, uncertainty-aware image-text alignment, and disease "appearance" prompts to guide visual semantics. The structured report framing is important: instead of free-text radiology reports, uses ICD-coded or structured clinical findings. This connects to the MedKLIP direction and is important for the "clinically meaningful" part of the thesis title.

*Study note:* The word "distribution-based" in the title refers to modeling uncertainty in the image-text alignment — important for grounding calibration (your Q9 from the formal research questions).

---

**3.4 — Evaluating ViT Explainability in Medical Imaging (Tier 2)**
> "Evaluating the Explainability of Vision Transformers in Medical Imaging" (arXiv 2510.12021)

Why: Systematic comparison of explainability methods (Grad-CAM, attention rollout, DINO, Swin variants) on ViT architectures in the medical setting. Good reference for understanding the current empirical state of the field.

---

**3.5 — Prototype-Enhanced Confidence Modeling (Tier 2)**
> "Prototype-Enhanced Confidence Modeling for Cross-Modal Medical Image-Report Retrieval" (arXiv 2508.03494)

Why: Relevant if the thesis includes a confidence/calibration angle. Prototype-based confidence for retrieval is a cleaner version of the calibration problem.

---

**3.6 — Cardoso group: Intrinsic Explainability for Object Detection (Tier 2)**
> Fernandes et al. — "Intrinsic Explainability for End-to-End Object Detection" (IEEE Access 2024, with Jaime Cardoso)

Why: Directly from Cardoso's lab. Object detection is a clean grounding task where "why did the model localize this object here?" is precisely the question that transfers to medical VLM grounding. Read this before meeting Cardoso to show you have engaged with his group's specific output.

---

**Phase 3 artifact:** For each of the four main papers (MATEX, H-EGL, D-MLM, Evaluating ViTs), complete a paper note and add a row to a comparison table:

| Paper | What it explains | How it validates faithfulness | Missing: causal validation? | Connection to thesis |
|---|---|---|---|---|
| MATEX | Attention + text-guided attribution | Correlation w/ ground truth | Yes | Text-guided grounding → causal analysis |
| H-EGL | Attention + explanation-guided training | Accuracy improvement | Partially | Training-side grounding |
| D-MLM | Structured report alignment | Disease recognition metrics | Yes | Uncertainty + calibration angle |
| Evaluating ViTs | Comparison of methods | Per-method accuracy | Yes | Baseline evaluation framework |

---

### Phase 4 — Domain Deep-Dives: Datasets and Benchmarks (Weeks 12–13)
*Goal: hands-on familiarity with the datasets you will actually use. This phase is more practical than reading-based.*

**4.1 — MIMIC-CXR (Tier 1 — access, explore)**
> Johnson et al. — MIMIC-CXR Database v2.1.0 (PhysioNet)

Action: Request PhysioNet access if not already granted. Familiarize yourself with the structure: image metadata, free-text radiology reports, ICD codes. MIMIC-CXR is the backbone of almost all radiology VLM research.

URL: https://physionet.org/content/mimic-cxr/

---

**4.2 — MIMIC-CXR-JPG (Tier 1 — use this one)**
> MIMIC-CXR-JPG with structured labels (PhysioNet)

The processed version with 14-class labels extracted by CheXpert labeler. Easier to start with. 

URL: https://physionet.org/content/mimic-cxr-jpg/

---

**4.3 — MS-CXR (Tier 1 — most directly relevant to grounding)**
> Bannur et al. — "MS-CXR: Making the Most of Text Semantics to Improve Biomedical Vision-Language Processing" (PhysioNet)

This is the phrase-grounding benchmark: image-text pairs with bounding box annotations linking report phrases to image regions. This directly operationalizes visual grounding in radiology. This should be the primary evaluation benchmark for any grounding claims.

URL: https://physionet.org/content/ms-cxr/

---

**4.4 — CheXpert (Tier 2)**
> Irvin et al. 2019 — Stanford. Large chest X-ray dataset with uncertainty labels.

URL: https://aimi.stanford.edu/datasets/chexpert-chest-x-rays

---

**4.5 — NIH ChestX-ray14 (Tier 2)**
> Wang et al. 2017 — NIH. Classic benchmark for thoracic disease classification.

URL: https://www.kaggle.com/datasets/nih-chest-xrays/data

---

**4.6 — For pathology: CONCH, PLIP, Quilt-1M (Tier 2 — defer if staying in radiology)**
> CONCH: Lu et al. 2024 — Nature Medicine
> PLIP: Huang et al. 2023 — Nature Medicine
> Quilt-1M: Ikezogwo et al. 2023

If the thesis moves toward pathology, these three define the landscape. CONCH is currently the strongest pathology VLM. But pathology requires different compute (WSI processing is expensive) and different grounding tasks.

---

**4.7 — TCGA / The Cancer Genome Atlas (Tier 2 — use if pathology becomes relevant)**
> The Cancer Genome Atlas Program

Essential if the thesis moves toward whole-slide pathology, cancer subtype classification, or WSI explainability. Treat it as a pathology infrastructure resource rather than a first radiology-track dependency.

URL: https://www.cancer.gov/ccg/research/genome-sequencing/tcga

---

**4.8 — VLEER (Tier 2 — read if pathology becomes relevant)**
> "VLEER: Vision and Language Embeddings for Explainable Whole Slide Image Representation" (arXiv 2502.20850)

Pathology-specific explainability using text embeddings. Read in full only if you commit to pathology as a domain.

---

**Phase 4 artifact:** Set up a local environment with MIMIC-CXR-JPG loaded and a BioViL or MedKLIP model running. Produce one visualization of phrase-grounding on an X-ray. This is the first experimental artifact in the medical domain.

---

### Phase 5 — Mechanistic Connections: Bridging the Two Sides (Ongoing, Weeks 14+)
*Goal: identify exactly where and how the mechanistic interpretability methods from the CMU track apply to the medical VLM explainability from the Portugal track.*

This phase is ongoing and parallel to all other work. It is not a phase with a fixed reading list — it is a synthesis task.

**The key connection points:**

**Connection A: Causal tracing → faithful medical explanation**
ROME-style causal tracing (Meng et al. 2022) identifies which model components causally determine a specific output. Applied to medical VLMs: which image patches and model components causally determine the report phrase "consolidation in the lower lobe"? This is a stronger faithfulness guarantee than Grad-CAM correlation.

**Connection B: Probing → grounding state detection**
Linear probes trained on intermediate activations can detect whether a medical VLM is grounding in visual evidence vs. reporting language statistics. A VLM that says "consolidation" because "pneumonia" appeared in its training text is not grounded, even if the image shows consolidation.

**Connection C: SAEs → concept-level medical features**
SAEs applied to cross-modal representations in medical VLMs could recover interpretable medical concepts as monosemantic features. Connections: does a feature activate for "pleural effusion" across many different images? This would be a significant contribution.

**Connection D: Counterfactual interventions → diagnostic grounding tests**
For medical VLMs, counterfactual tests (modify the image while holding the clinical question constant) directly test whether the model is diagnosing from the image or from statistical priors. This is Q6 from the formal research questions, now operationalized in the clinical domain.

**Reading for this phase:**
- Connect back to Clusters 4–6 in the general [[Reading Map]] (mech interp foundations, SAEs, causal methods)
- Read: Geiger et al. "Causal Abstraction" — for verifying that mechanistic claims about medical VLMs are valid
- Read: Todd et al. "Function Vectors" — for understanding whether clinical concept representations are localizable

---

## Part 4 — Glossary Additions (Medical Domain)

*Add these terms to the main [[Glossary]] under a new Section 10: Medical VLM Domain.*

**Radiology Report:** A structured clinical document generated by a radiologist describing findings in a medical image. Contains findings, impressions, and clinical history. In medical VLMs, these are the text side of the image-text pair. Key challenge: reports are written for clinical communication, not for training ML models — they contain negations, uncertainty language, and abbreviations.

**Phrase Grounding (medical):** The task of linking a natural language phrase from a clinical report to the specific image region it describes. "Consolidation in the left lower lobe" should map to the corresponding lung region. MS-CXR is the benchmark. This is the medical instantiation of visual grounding.

**Structured Report:** A clinical report in a standardized format (e.g., using ICD codes or CheXpert labels) rather than free text. Structured reports are easier to align with image regions because they use controlled vocabulary. D-MLM uses structured reports.

**CheXpert Labeler:** A rule-based NLP system that extracts 14 disease labels (with uncertainty flags: positive, negative, uncertain) from free-text radiology reports. Used to create structured labels for MIMIC-CXR-JPG. Important because many medical VLMs are evaluated against CheXpert-labeled conditions.

**Contrastive Medical Pretraining:** Training a VLM on image-report pairs using contrastive objectives (pull matched pairs together, push mismatched pairs apart). ConVIRT, GLoRIA, BioViL, and MedKLIP all use variants of this paradigm.

**Explanation-Guided Learning (EGL):** Training a model using both task performance objectives and explanation constraints. For example, penalizing the model if its gradient attribution map focuses on background regions irrelevant to the diagnosis. Right for the Right Reasons is the foundational paper.

**Clinical Faithfulness:** An explanation is clinically faithful if it correctly identifies the image evidence that a clinical expert would use to make the same diagnosis. This is distinct from *mechanistic faithfulness* (the explanation matches what the model internally computed) and the two can diverge.

**Whole-Slide Image (WSI):** A high-resolution digital scan of a biopsy slide used in computational pathology. WSIs are gigapixel images — far too large to process with standard VLMs. Require multi-scale or tiled processing (multiple instance learning). CONCH, PLIP, and VLEER all work with WSIs.

**Multiple Instance Learning (MIL):** A weakly-supervised learning paradigm where a bag of instances (e.g., image tiles from a WSI) has a single bag-level label, and the goal is to identify which instances are responsible for the label. Standard approach for WSI classification.

**iMIMIC (Interpretability of Machine Intelligence in Medical Image Computing):** The most directly relevant workshop for this thesis direction. Organized annually alongside MICCAI. Co-edited by Cardoso. Follow every year.

**MIMIC-CXR:** A large publicly available dataset of chest X-ray images and associated radiology reports from Beth Israel Deaconess Medical Center (377,110 images, 227,835 studies). The primary training and evaluation dataset for radiology VLMs.

**MS-CXR:** A phrase-grounding benchmark (1,162 image-sentence pairs with bounding box annotations) created for testing whether medical VLMs can link report phrases to image regions. The most relevant benchmark for a grounding-focused thesis.

**PhysioNet:** The data repository where MIMIC-CXR, MS-CXR, and other clinical datasets are hosted. Requires credentialing and data use agreements to access.

---

## Part 5 — People and Labs Additions (Medical AI Community)

*Add these to the main [[People and Labs Map]] under a new Tier for the medical AI community.*

### Medical AI / iMIMIC orbit

**Mauricio Reyes** — University of Bern / iMIMIC co-editor
Contributions: Medical image analysis interpretability, fairness in medical AI. iMIMIC co-editor alongside Cardoso. Important person to know at MICCAI.

**Pedro Henriques Abreu** — University of Coimbra / iMIMIC co-editor
Contributions: Machine learning for healthcare, imbalanced data, medical AI. Co-edits iMIMIC. FEUP-adjacent Portuguese academic.

**Tiago Gonçalves** — VCMI / INESC TEC (FEUP group)
Contributions: Attention mechanisms for medical applications (the survey listed). Cardoso/Teixeira's PhD student or close collaborator. Early connection to make when in Porto.

**Luís Teixeira** — VCMI / INESC TEC (FEUP group)
Already in people map as mech interp anchor — now also relevant as attention/explainability collaborator for medical track.

---

### Medical VLM researchers

**Shruthi Bannur, Stephanie Hyland (Microsoft Research, Cambridge)**
Contributions: BioViL, BioViL-T, MS-CXR. The core team behind the best phrase-grounding models and benchmarks for radiology. Their work is the technical baseline for any MS-CXR experiments.

**Pranav Rajpurkar (Harvard)**
Contributions: CheXpert, CheXNet, chest X-ray AI benchmarking. Led the wave of radiology AI benchmarks. Important figure in the clinical AI deployment conversation.

**Fei-Fei Li / Percy Liang (Stanford HAI)**
Contributions: AI safety, reliability, and accountability in medical AI. HELM benchmark. Relevant if the thesis engages with the evaluation and deployment side.

**Faisal Mahmood Lab (Harvard, Brigham and Women's)**
Contributions: CONCH, CLAM, computational pathology at scale. The leading lab for pathology foundation models. If the thesis moves toward pathology, this is the group to follow.

**Ming Lu, Jinhong Wang (Stanford / Microsoft)**
Contributions: Medical VLM evaluation, grounding, and zero-shot disease recognition.

---

### Labs

**Microsoft Research Cambridge (Health Intelligence)**
Output: BioViL, BioViL-T, MS-CXR, CXR-BERT, RadBERT. The most productive lab for radiology VLM foundations. Their HuggingFace models are public and usable.

**Stanford AIMI (Center for Artificial Intelligence in Medicine and Imaging)**
Output: CheXpert, CheXZero, clinical AI benchmarks. Strong on evaluation and clinical validation. Their datasets are important baselines.

**Harvard Mahmood Lab**
Output: CONCH, PLIP backbone, Quilt-1M. Dominant in computational pathology.

**INESC TEC / VCMI (Porto)**
Output: Attention survey (Gonçalves et al.), object detection explainability (Fernandes et al.), other FEUP lab outputs. Your Portugal-side research home.

---

### Key venues for the medical track

| Venue | Type | Relevance |
|---|---|---|
| MICCAI | Conference (flagship) | Most important medical image computing venue |
| iMIMIC at MICCAI | Workshop | Most directly relevant workshop |
| Medical Image Analysis | Journal | Top journal for extended medical AI papers |
| Nature Medicine / Nature BME | Journal | For landmark results; high bar |
| NeurIPS / ICML / ICLR | Conference | For the mech interp / VLM side of the thesis |
| CVPR / ICCV | Conference | For vision + language grounding contributions |
| EMNLP / ACL | Conference | If the work is text-heavy (report generation) |

---

## Part 6 — Connection to Existing Formal Research Questions

*How the medical domain operationalizes each of the ten formal questions.*

| Q | General version | Medical instantiation |
|---|---|---|
| Q1 — Self-evaluation reliability | Can VLMs judge whether their outputs are grounded? | Can a radiology VLM detect when its report is not supported by the X-ray? |
| Q2 — Information through projection | How much visual information survives cross-modal projection? | Does the clinical finding (e.g., consolidation location) survive projection from ViT patch to language space? |
| Q3 — Grounding circuits | Are there circuits responsible for visual grounding? | Are there attention heads in BioViL/MedKLIP that are causally responsible for linking "consolidation" to lower-lobe patches? |
| Q4 — SAE visual features | Can SAEs recover interpretable visual features? | Can SAEs applied to medical VLM cross-modal representations recover monosemantic clinical concepts? |
| Q5 — DPI hallucination | Can hallucination be characterized as DPI violation? | Can radiology report hallucination (fabricated findings) be characterized as MI failure between image patches and report tokens? |
| Q6 — Counterfactual interventions | Counterfactual image → reveals grounding | Remove the consolidation from the image → does the report change? If not, the report was not grounded. |
| Q7 — Distributional robustness | How does grounding degrade under shift? | Does grounding degrade under scanner type shift, patient population shift, or disease prevalence shift? |
| Q8 — Probing for grounding state | Linear probe for "grounding mode" | Probe to detect whether medical VLM is in "visually grounded" vs. "prior-driven" generation mode during report generation |
| Q9 — Grounding calibration | Are VLMs calibrated about grounding confidence? | When a radiology VLM says "consolidation is present," is its confidence correlated with the actual quality of image evidence? |
| Q10 — Representation geometry | Does cross-modal geometry predict grounding? | Does GLoRIA/BioViL representation alignment geometry predict phrase-grounding quality on MS-CXR? |

---

## Part 7 — Suggested First Reading Order (Condensed)

This is the recommended linear sequence if starting from scratch, compressing Phases 0-3:

1. Gonçalves et al. attention survey (Cardoso group — domain orientation)
2. Sanity Checks for Saliency Maps (Adebayo et al. 2018)
3. Attention is Not Explanation (Jain & Wallace 2019)
4. ConVIRT → GLoRIA → BioViL (medical VLM lineage)
5. MedKLIP (structured grounding)
6. Right for the Right Reasons (Ross et al. 2017)
7. Going Beyond XAI survey (Gao et al. 2022)
8. MATEX (most thesis-relevant paper in the list)
9. H-EGL (training-side approach)
10. D-MLM (structured report alignment + uncertainty)
11. From Explainable to Explained AI (falsifiable explanations — pivot paper)

After these 11 papers, you will have a clear enough picture to write the first version of the thesis introduction and identify the specific gap you are filling.

---

## Part 8 — The First Experiment

When the reading is done and the domain is familiar, the first experiment should be:

**Take BioViL or MedKLIP. Run it on a subset of MS-CXR. Evaluate phrase grounding using the standard metrics. Then apply the Sanity Checks (randomize model parameters) and test whether the grounding maps are actually faithful.**

If the Sanity Checks fail (grounding maps do not change when the model is randomized), that is a finding: the standard medical VLM grounding evaluation is not measuring faithfulness. That finding motivates everything that comes next in the thesis.

This experiment is small, fast, and high-leverage. It directly connects the reading of Phase 0 to the empirical entry point of the thesis.

---

## Quick Reference Links

| Resource | URL |
|---|---|
| iMIMIC Workshop | https://imimic-workshop.com |
| Springer iMIMIC 2025 volume | https://link.springer.com/book/10.1007/978-3-032-17611-0 |
| MIMIC-CXR | https://physionet.org/content/mimic-cxr/ |
| MIMIC-CXR-JPG | https://physionet.org/content/mimic-cxr-jpg/ |
| MS-CXR | https://physionet.org/content/ms-cxr/ |
| CheXpert | https://aimi.stanford.edu/datasets/chexpert-chest-x-rays |
| NIH ChestX-ray14 | https://www.kaggle.com/datasets/nih-chest-xrays/data |
| TCGA | https://www.cancer.gov/ccg/research/genome-sequencing/tcga |
| x2x code | https://github.com/NKI-AI/x2x |
| MedCLIP code | https://github.com/RyanWangZf/MedCLIP |
| GLoRIA code | https://github.com/marshuang80/gloria |
| MedKLIP code | https://github.com/MediaBrain-SJTU/MedKLIP |
| PRIOR code | https://github.com/qtacierp/prior |
| BioViL (HuggingFace) | https://huggingface.co/microsoft/BiomedVLP-BioViL-T |
| CONCH | https://github.com/mahmoodlab/CONCH |
| PLIP | https://www.nature.com/articles/s41591-023-02504-3 |
| Quilt-1M | https://quilt1m.github.io/ |
| Awesome medical VLP | https://github.com/Liqq1/awesome-medical-vision-and-language-pretraining |
| Awesome multimodal medical imaging | https://github.com/richard-peng-xia/awesome-multimodal-in-medical-imaging |
