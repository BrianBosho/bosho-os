---
title: VLM Ideas — Developed
type: ideas
created: 2026-06-16
tags: [research, vlm, grounding, ideas]
---

# VLM Ideas — Developed

This document articulates and develops the ideas from `unprocessed/VLM Ideas.md`. No implementation status, no experiment tracking — just the ideas themselves, sharpened and connected.

---

## The central question

The VLM pipeline takes an image and a question and produces an answer. The central question running through all the ideas below is:

> At each stage of the pipeline, how much of the original visual information is present, and how much of it is actually used to produce the answer?

These are two distinct sub-questions. Information can be *present* at a stage without being *used* downstream. And downstream stages may *use* information that is no longer spatially localized the way it was when it entered the pipeline. Keeping these two sub-questions separate is important for designing experiments and interpreting results.

---

## Idea 1: Information flow through the pipeline

### The basic observation

A VLM processes an image through at least three distinct stages before generating an answer:

1. **CLIP encoder** — takes raw image patches and produces patch-level embeddings in CLIP space
2. **Projector** — maps CLIP embeddings into the LLM's token space
3. **LLM layers** — process the projected image tokens alongside text tokens to generate an answer

At each stage, the visual information is transformed. The question is whether these transformations preserve, attenuate, or redistribute the semantic content of the image.

### What does "visual information" mean at each stage?

This is worth being precise about. "Information" here is not information in the Shannon sense (which would require a probability distribution over inputs). A more tractable framing is:

**Does the representation at this stage allow an observer to distinguish images that differ in semantically relevant ways?**

For example:
- Can you tell from CLIP patch embeddings alone whether the image contains a dog or a cat?
- Can you still tell after the projector?
- Can you still tell from the LLM's hidden states at Layer 32?

If the answer degrades across stages, visual information is being lost or diffused. If it is preserved but restructured, the model is transforming rather than losing it.

### The smearing hypothesis

A specific sub-hypothesis is that spatial localization degrades as you move through the pipeline. In CLIP space, the embedding for a patch in the upper-left corner of the image is meaningfully distinct from the embedding for a patch in the lower-right. After multiple LLM transformer layers with full attention, information from one patch position may spread across many hidden states. By Layer 32, the correspondence between hidden state positions and original image regions may be weak.

This would mean:
- Support patches identified at Layer 32 may not correspond to the spatially meaningful regions in the image
- Bounding box patches (defined in image space) may be less informative at Layer 32 than at earlier stages
- The most informative stage for spatial localization may be the projector output, not the final LLM layer

### The pipeline as a localization ladder

A natural way to study this is to ablate the same semantic region at each stage and measure the effect on the model's output. Removing the dog-region patches at pixel level, CLIP level, projector level, and LLM Layer 32 level should all reduce the model's confidence in dog-related tokens — but by how much? The stage where the ablation effect is largest is the stage where the visual information is most concentrated and most causally necessary.

This gives a *localization ladder*: a profile of how information dependency shifts across the pipeline.

### The broader framing

This idea is ultimately about whether a VLM's visual grounding can be understood as a single thing or whether it decomposes into multiple stages, each with its own grounding behavior. A model could be strongly grounded at the CLIP encoder stage (correct patch representations) but weakly grounded at the LLM stage (not using those representations). Or vice versa: a model could have noisy CLIP representations but still generate correct answers by using aggregate signals effectively.

Understanding which stage is the bottleneck for grounding is a prerequisite for designing interventions (training objectives, architectural changes, inference-time corrections) that actually improve faithfulness.

---

## Idea 2: LLM dependence on visual input

### Representational similarity between generated tokens and image patches

When the LLM generates a token (say, "dog"), its hidden state at that position encodes information that was used to produce that prediction. A natural question is: how similar is that hidden state to the patch embeddings that represent the dog in the image?

If the hidden state at a generated token is strongly aligned with the relevant patch embeddings, that is evidence the model is using image evidence to produce that token. If it is weakly aligned, the model may be generating based on language priors — the word "dog" follows naturally in the context of the question regardless of what is in the image.

This similarity is not binary. It is a continuous signal, and measuring it across many tokens and many images gives a distributional picture of how much the LLM's generation depends on visual input.

### The counterfactual framing

A cleaner version of the same idea is counterfactual: what changes about the hidden state (and the output probability) when you replace the real image with a null image?

This addresses a confound in the raw similarity approach: even for a purely text-driven token, the hidden state may have non-trivial inner products with patch embeddings just due to the geometry of the embedding space (anisotropy). A counterfactual subtraction removes this background signal.

So the question becomes: how much does the hidden state *change* when the image is removed? And does that change align with specific image patches — or is it diffuse?

A token whose hidden state shifts strongly and in a spatially concentrated direction when the image is replaced is a token that genuinely depended on specific visual evidence. A token whose hidden state barely shifts, or shifts diffusely, depended mostly on text context.

### Earlier layers

The hidden-state analysis can be done at any LLM layer. Layer 32 (the final layer) is a natural choice because it directly drives the output. But it is possible that visual information is *used* at earlier layers — integrated into intermediate representations — and then the final layer state reflects a mixture of visual and text evidence that is harder to attribute.

An earlier-layer analysis would ask: at which layer does the visual-evidence alignment peak? If it peaks at L8 and decays by L32, that suggests the model integrates visual evidence early and then processes it further in ways that make it harder to trace back. If it peaks at L32, the final-layer analysis is sufficient.

This would also reveal whether different kinds of information (object identity vs. spatial relationships vs. attributes) are grounded at different depths in the network.

### Support patches and the causal question

Identifying which patches support a given generated token is a more ambitious version of the representational similarity idea. Rather than asking "does the hidden state align with image patches?", it asks "which specific patches are necessary for this particular prediction?"

This is a causal question, not a correlational one. Correlation (hidden state aligns with patch) is compatible with a scenario where the patch is just statistically typical of the scene, not specifically needed for the token. Causality requires showing that removing the patch changes the prediction.

The "can we change the support patches?" question takes this further: if you identified the support patches and then altered them (masked, replaced, or perturbed), does the model's prediction change accordingly? And do predictions that seemed correct but were visually unsupported degrade when the putatively supporting patches are removed?

This is the key empirical test of what "grounded" means: a grounded prediction depends on specific visual evidence, and removing that evidence should change the prediction.

---

## Idea 3: Measurement design

### Can we measure semantic information quantitatively?

The practical version of this question is: can the grounding instrument tell the difference between an image with a dog and an image with a cat? Not in the sense of answering the question correctly — in the sense of assigning higher grounding scores to tokens that describe what is actually in the image.

One way to operationalize this is through token-class ordering: the instrument should score visual nouns (naming objects present in the image) higher than visual attributes (describing properties), which in turn should score higher than function words (which have no direct visual referent). If this ordering does not hold, the instrument is not measuring semantic content — it is measuring something else (token frequency, syntactic position, language model confidence).

A stronger test is concept-specific: does the instrument score the token "dog" more highly in images that contain dogs than in images that do not? This tests whether the instrument is sensitive to the specific semantic content of the image, not just to a generic "visual relevance" signal.

### Basis construction from the dataset

To measure whether a hidden state aligns with "visual semantic directions," you need a basis for that space. One approach is to use a dataset of image-text pairs to identify directions that correspond to specific semantic concepts.

For CLIP embeddings, the dataset-mean approach offers a neutral null: the mean patch embedding across many images is a point in embedding space that carries no specific semantic content (or carries average/generic visual content). Subtracting this null removes the baseline similarity that all patches share, leaving only the image-specific variation.

An alternative approach would project into a semantic basis — for example, the directions in LLM embedding space that correspond to specific object concepts. This would allow asking "how much of the hidden state change aligns with the dog-concept direction?" — a more interpretable measure than raw cosine similarity.

The tension between these approaches is between interpretability and stability. Semantic basis directions can be noisy and may not generalize across models. Dataset-mean nulls are stable and model-agnostic, but tell you less about which concepts are represented.

### The null baseline problem

Any similarity-based grounding measure needs a null: what does the similarity look like when the image provides no relevant evidence? Without a good null, you cannot separate genuine grounding from embedding geometry artifacts.

The null baseline design choices are:
- **Dataset-mean patch** — average CLIP embedding across many images; generic but not content-free
- **Per-image-mean** — average across patches within the same image; removes spatial variation but preserves scene-level information
- **Random noise** — maximally content-free, but outside the learned distribution of CLIP embeddings
- **Patch shuffle** — randomly permutes patches; preserves the marginal distribution but destroys spatial structure

Each of these preserves different aspects of the original image and is therefore measuring something slightly different when used as a null. The choice of null determines what "visual grounding" means operationally.

### The patch logit lens idea

A complementary approach is to decode patch embeddings directly: project each patch's embedding through the LM head and ask what tokens decode most strongly. A patch containing a dog should decode to dog-adjacent tokens. This provides a direct sanity check on whether the embedding space being measured contains interpretable semantic content — and gives a richer picture of what "semantic information in the patch embedding" actually means.

This also provides a way to identify support patches interpretably: rather than selecting the top-k patches by a scalar grounding score, you could select patches whose decoded tokens match the generated token. This would be a content-matched localization method rather than a similarity-matched one.

---

## Connecting the three ideas

The three idea groups are not independent — they form a layered question about what visual grounding is and how to measure it:

- **Idea 1** (pipeline flow) asks where visual information lives across the pipeline.
- **Idea 2** (LLM dependence) asks how much of that information the LLM uses when generating a specific token.
- **Idea 3** (measurement) asks how to reliably quantify that use.

They converge on a single core question: **is a VLM's generated token genuinely supported by visual evidence, and can we tell?**

The pipeline framing (Idea 1) is about *information availability*. The LLM dependence framing (Idea 2) is about *information use*. The measurement framing (Idea 3) is about *signal validity* — whether the instrument is actually measuring what it claims to measure.

A complete answer requires all three:
1. The visual information must be present and accessible at the stage being measured.
2. The LLM must be using that information (not just co-occurring language patterns).
3. The measurement must isolate that use from confounds (anisotropy, baseline similarity, non-specific signals).

Each idea group is also a potential failure mode for the others: information may not survive the projector (Idea 1 failure), the LLM may ignore present information (Idea 2 failure), or the metric may not detect genuine use (Idea 3 failure).

---

## Open questions worth developing

The ideas above leave several questions open that are worth formalizing into hypotheses:

**On information flow:**
- Does CLIP spatial structure (the 24×24 grid of patches) survive the projector? Does the LLM treat the projected tokens as a spatial structure or as an unordered set?
- At which pipeline stage does the best spatial localization of support patches occur?

**On LLM dependence:**
- Do different token types (object names vs. attributes vs. relational terms like prepositions) depend on visual evidence at different layers?
- Can a trajectory through hidden-state space, rather than a single-layer snapshot, give a better account of how visual evidence is integrated during generation?

**On measurement:**
- Is cosine similarity the right metric for comparing hidden states with patch embeddings, or do the geometry properties of these spaces (dimensionality, anisotropy, alignment) require a different comparison function?
- How sensitive are grounding scores to the choice of aggregation (max, mean, variance) across patches?
- Can a content-matched patch selection (patch logit lens) outperform a similarity-matched selection for causal validation?
