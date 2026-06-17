# Experiment 1: From Image to Heatmap — Full Methodology  
  
> **Updated 2026-02-20** — This document now covers the full clean pipeline including  
> Stage 4B (drift analysis) and Stage 6 (raw L32 delta grounding), reflecting the  
> resolution of the projector/Layer-32 space contamination bug.  
  
This document walks through every step, from first principles, of how data flows  
through the Vision–Language Model (VLM) and our staged pipeline to produce the  
final grounding analysis results.  
  
---  
  
## Table of Contents  
  
1\. [High-Level Research Question](#1-high-level-research-question)  
2\. [The VLM Architecture (LLaVA-1.5)](#2-the-vlm-architecture-llava-15)  
3\. [Pipeline Overview (Flowchart)](#3-pipeline-overview-flowchart)  
4\. [Stage 0 — Scaffold & Directory Layout](#4-stage-0--scaffold--directory-layout)  
5\. [Stage 1 — Dataset Indexing](#5-stage-1--dataset-indexing)  
6\. [Stage 1.5 — Null Reference Construction](#6-stage-15--null-reference-construction)  
7\. [Stage 2 — Caption Generation & Mention Extraction](#7-stage-2--caption-generation--mention-extraction)  
8\. [Stage 3 — Teacher-Forced Real/Null State Extraction](#8-stage-3--teacher-forced-realnull-state-extraction)  
9\. [Stage 4 — Whitened Distributional State Grounding](#9-stage-4--whitened-distributional-state-grounding) *[DEPRECATED — see Section 15]*  
10\. [Stage 4B — Hidden State Drift Analysis](#10-stage-4b--hidden-state-drift-analysis)  
11\. [Stage 6 — Raw L32 Delta Grounding (Clean Pipeline)](#11-stage-6--raw-l32-delta-grounding-clean-pipeline)  
12\. [Visualization — How the Heatmaps Are Drawn](#12-visualization--how-the-heatmaps-are-drawn)  
13\. [Files & Artifacts Reference](#13-files--artifacts-reference)  
14\. [Mathematical Summary](#14-mathematical-summary)  
15\. [Critical Bug: Projector/Layer-32 Space Contamination](#15-critical-bug-projectorlayer-32-space-contamination)  
16\. [Current Status & Next Steps](#16-current-status--next-steps)  
  
---  
  
## 1. High-Level Research Question  
  
**Current focus (post-bug-fix):**  
  
> Does LLaVA-1.5-7B encode visual grounding in its final transformer layer (Layer-32)?  
> Specifically: when the model generates a visually-descriptive token (e.g. `▁black`, `▁cabinet`),  
> does its Layer-32 hidden state show stronger and more spatially-specific alignment with  
> image patch representations than a structurally required but non-visual token (e.g. the period `.`)?  
  
**Original motivation (hallucination detection):**  
  
> When a VLM produces a caption mentioning objects **not present** in the image  
> (hallucination), do those object mentions exhibit **weaker state grounding** —  
> i.e., less positive evidence above a null baseline in the token×patch support matrix?  
  
**Status:** After discovering and fixing the projector/Layer-32 space contamination bug,  
we have validated that the grounding signal exists and is robust. The primary metric is  
now **delta_var** (spatial variance of raw L32 cosine delta), which shows 35.7× median  
ratio (content vs period tokens) in raw space and 10.3× in whitened space.  
  
---  
  
## 2. The VLM Architecture (LLaVA-1.5)  
  
LLaVA-1.5 is a two-tower vision–language model:  
  
```  
 ┌──────────────────┐  
 Image I ────────▶│ CLIP ViT-L/14 │──── patch embeddings (576 × 1024)  
 │ (Vision Encoder) │  
 └────────┬─────────┘  
 │  
 ▼  
 ┌──────────────────┐  
 │ Linear Projector │──── projected visual tokens V(I) ∈ ℝ^{M×d}  
 │ (1024 → 4096) │ M = 576 patches, d = 4096  
 └────────┬─────────┘  
 │  
 ▼  
 ┌────────────────────────────────┐  
 │ │  
 │ Vicuna-7B LLM │  
 │ (autoregressive transformer) │  
 │ │  
 │ Input sequence: │  
 │ [system] [v₁..v₅₇₆] [Q] [y*] │  
 │ │  
 │ At each step t: │  
 │ h_t = final-layer hidden state │  
 │ z_t = logit vector │  
 │ ŷ_t = argmax(z_t) or sample │  
 │ │  
 └────────────────────────────────┘  
```  
  
### Key representations we extract:  
  
| Symbol | Shape | Description |  
|--------|-------|-------------|  
| $V^{\text{real}}(I)$ | $(M, d)$ = $(576, 4096)$ | Projected visual tokens from the **real** image |  
| $h_t^{\text{real}}$ | $(d,)$ = $(4096,)$ | Decision state at step $t$ under the **real** image |  
| $h_t^{\text{null}}$ | $(d,)$ = $(4096,)$ | Decision state at step $t$ under the **null** image |  
  
The **projected visual tokens** are the bridge between vision and language.  
They live in the same $d$-dimensional space as the LLM's hidden states,  
which is why we can measure cosine similarity between them.  
  
---  
  
## 3. Pipeline Overview (Flowchart)  
  
```  
 ┌──────────────────────────────────────────────────────────────────────────┐  
 │ EXPERIMENT 1 PIPELINE │  
 │ │  
 │ ┌───────────┐ ┌─────────────┐ ┌─────────────┐ │  
 │ │ Stage 0 │────▶│ Stage 1 │────▶│ Stage 1.5 │ │  
 │ │ Scaffold │ │ Dataset │ │ Null Ref │ │  
 │ │ & Config │ │ Indexing │ │ Builder │ │  
 │ └───────────┘ └──────┬──────┘ └──────┬──────┘ │  
 │ │ │ │  
 │ ▼ ▼ │  
 │ ┌─────────────┐ ┌─────────────┐ │  
 │ │ Stage 2 │ │ Null tiled │ │  
 │ │ Generate │ │ matrix I_∅ │ │  
 │ │ Y* + find │ │ (576×1024) │ │  
 │ │ mentions │ └──────┬──────┘ │  
 │ └──────┬──────┘ │ │  
 │ │ │ │  
 │ ▼ ▼ │  
 │ ┌──────────────────────────────────┐ │  
 │ │ Stage 3 │ │  
 │ │ Teacher-forced extraction: │ │  
 │ │ • Real image → h_t^real, V^real│ │  
 │ │ • Null image → h_t^null │ │  
 │ └───────────────┬──────────────────┘ │  
 │ │ │  
 │ ▼ │  
 │ ┌──────────────────────────────────┐ │  
 │ │ Stage 3.5 │ │  
 │ │ PCA whitening basis: │ │  
 │ │ μ, U, Λ from all R^4096 vecs │ │  
 │ └───────────────┬──────────────────┘ │  
 │ │ │  
 │ ▼ │  
 │ ┌──────────────────────────────────┐ │  
 │ │ Stage 4 │ │  
 │ │ Whiten: ĥ = (h-μ)UΛ^{-1/2} │ │  
 │ │ Logits = cos(ĥ, v̂)/τ │ │  
 │ │ P = Softmax(Logits) │ │  
 │ │ A_Δ = P_real − P_null │ │  
 │ │ A⁺ = max(0, A_Δ) │ │  
 │ │ G^state_t = Σ A⁺_t,: │ │  
 │ └───────────────┬──────────────────┘ │  
 │ │ │  
 │ ▼ │  
 │ ┌──────────────────────────────────┐ │  
 │ │ Visualization │ │  
 │ │ Heatmap of P_real, P_null, │ │  
 │ │ A_Δ, A⁺ as (T × M) matrices │ │  
 │ └──────────────────────────────────┘ │  
 └──────────────────────────────────────────────────────────────────────────┘  
```  
  
---  
  
## 4. Stage 0 — Scaffold & Directory Layout  
  
**What happens:** Parse and validate the YAML config. Create the output directory tree.  
Initialize or resume the checkpoint file.  
  
**Source file:** `vlm_spectral_analysis/experiments/exp1_runner.py` → `run_stage0()`  
  
**Config file:** `configs/experiments/experiment1.yaml`  
  
**Directories created:**  
  
```  
artifacts/experiments/experiment1/  
├── checkpoints/ # Checkpoint JSON (resume support)  
├── matrices/  
│ ├── raw/ # Stage 3 raw tensors (states, patches)  
│ └── derived/ # Stage 4 derived matrices (A_real, A_null, A_delta, A_pos)  
├── plots/ # Visualization outputs  
├── records/ # JSONL/Parquet tabular data  
├── references/ # Null reference tensors  
└── tables/ # Summary tables  
```  
  
**Key config values:**  
  
| Parameter | Value | Purpose |  
|-----------|-------|---------|  
| `model.model_id` | `llava-hf/llava-1.5-7b-hf` | LLaVA-1.5 checkpoint |  
| `experiment.prompt` | *"Describe the image in one sentence."* | Fixed question for all images |  
| `nulls.primary` | `dataset_mean_patch` | Null construction method |  
| `grounding.temperature` | `0.1` | Softmax temperature for Stage 4 logits |  
| `grounding.whitening.epsilon` | `1e-5` | Whitening regularization in $\Lambda^{-1/2}$ |  
| `decoding.policy` | `greedy` | Deterministic caption generation |  
| `null_reference.expected_patch_count` | `576` | CLIP ViT-L/14 patch grid: $24 \times 24 = 576$ |  
| `null_reference.expected_clip_dim` | `1024` | CLIP hidden dimension |  
  
---  
  
## 5. Stage 1 — Dataset Indexing  
  
**What happens:** Build a structured inventory of all image/question pairs from the COCO-based toy dataset.  
  
**Source file:** `vlm_spectral_analysis/experiments/exp1_dataset.py` → `Experiment1DatasetBuilder.build()`  
  
**Input:**  
- COCO images organized into 4 complexity slices:  
 `single_object`, `multi_object`, `text_heavy`, `texture_rich`  
- Image list files (`.txt`) — one per slice, listing image filenames  
- COCO annotations: `instances_val2017.json` (object labels), `captions_val2017.json` (GT captions)  
  
**Processing:**  
1\. Read image lists from each slice directory  
2\. Cross-reference with COCO instance annotations to get ground-truth object categories $O(I)$ per image  
3\. Cross-reference with COCO caption annotations to get ground-truth captions  
4\. Build a flat index with one row per (image, slice, question) tuple  
  
**Data produced per image:**  
  
| Field | Example |  
|-------|---------|  
| `image_id` | `130599` |  
| `slice` | `single_object` |  
| `image_path` | `datasets/coco/val2017/000000130599.jpg` |  
| `question` | `"Describe the image in one sentence."` |  
| `objects_present` | `["person", "giraffe"]` |  
| `ground_truth_captions` | `["A man standing next to a giraffe...", ...]` |  
  
**Output artifacts:**  
  
| File | Format | Description |  
|------|--------|-------------|  
| `records/image_index.parquet` | Parquet | Full image index |  
| `records/image_index.jsonl` | JSONL | Fallback if no Parquet library |  
| `records/stage1_image_question_gt.jsonl` | JSONL | Readable QA rows |  
| `records/stage1_image_question_gt.csv` | CSV | Spreadsheet-friendly format |  
| `records/stage1_image_index_summary.json` | JSON | Build summary & paths |  
  
---  
  
## 6. Stage 1.5 — Null Reference Construction  
  
**What happens:** Compute a **content-free null image** $I_\varnothing$ that preserves the  
architectural layout (same patch count, same dimensionality) while removing all  
image-specific visual content.  
  
**Source file:** `vlm_spectral_analysis/experiments/exp1_null_reference.py` → `Experiment1NullReferenceBuilder.build()`  
  
### Why do we need a null?  
  
When we measure cosine similarity between a decision state $h_t$ and visual patches $v_j$,  
we get a non-zero baseline even for tokens with **no visual grounding at all**. This is due to:  
- **Anisotropy** in the embedding space (representations cluster in a cone)  
- **Positional artifacts** from the projector  
- **Projector biases** that create background alignment  
  
The null condition removes these confounds by providing a "what would the model attend to  
if the image were content-free?" baseline.  
  
### Construction: Dataset-Mean Patch  
  
1\. **Load the CLIP vision encoder** from the LLaVA model  
2\. **For each image** in the dataset:  
 - Pass through CLIP ViT-L/14 → obtain patch embeddings $P_i \in \mathbb{R}^{576 \times 1024}$  
3\. **Compute the global mean patch vector:**  
  
$$\bar{p} = \frac{1}{N} \sum_{i=1}^{N} \left( \frac{1}{M} \sum_{j=1}^{M} P_{i,j} \right) \in \mathbb{R}^{1024}$$  
  
4\. **Tile to full patch count:**  
  
$$P_\varnothing = \text{tile}(\bar{p}, M) \in \mathbb{R}^{576 \times 1024}$$  
  
This gives us a null image representation where every patch is identical — the dataset average.  
It preserves the correct tensor shape (576 patches × 1024 dims) so the projector and  
LLM still receive the expected input layout.  
  
**Output artifacts:**  
  
| File | Format | Description |  
|------|--------|-------------|  
| `references/mean_patch_vector.pt` | PyTorch tensor | $\bar{p} \in \mathbb{R}^{1024}$ |  
| `references/mean_patch_tiled_576x1024.pt` | PyTorch tensor | $P_\varnothing \in \mathbb{R}^{576 \times 1024}$ |  
| `references/stage1_5_mean_patch_metadata.json` | JSON | Processor settings, image counts |  
| `references/stage1_5_mean_patch_summary.json` | JSON | Build summary & paths |  
  
---  
  
## 7. Stage 2 — Caption Generation & Mention Extraction  
  
**What happens:** For each image, generate a caption $Y^*$ using greedy decoding,  
extract hidden states, and find object mentions in the text.  
  
**Source file:** `vlm_spectral_analysis/experiments/exp1_mentions.py` → `Experiment1Stage2Builder.build()`  
  
### Step 2a: Generate the Reference Caption  
  
For each image $I$:  
  
1\. **Format the prompt:**  
 ```  
 USER: \<image>  
 Describe the image in one sentence.  
 ASSISTANT:  
 ```  
  
2\. **Run greedy decoding** (temperature=0, no sampling):  
$$Y^*(I) = (y^*_1, y^*_2, \ldots, y^*_T) = \arg\max_{y_t} \prod_{t=1}^{T} P(y_t \mid y^*_{\<t}, I, Q)$$  
  
3\. **Capture at each generation step:**  
 - The generated token id $y^*_t$  
 - The final-layer hidden state $h_t \in \mathbb{R}^{4096}$  
 - The token piece (subword string, e.g., `"▁man"`, `"▁gir"`, `"affe"`)  
  
4\. **Filter out special tokens** (EOS, BOS, padding)  
  
5\. **Compute character→token offset mappings** using the tokenizer  
  
**Example output:**  
  
| Field | Value |  
|-------|-------|  
| `caption` | `"A man is making a funny face while standing next to a giraffe statue."` |  
| `token_ids` | `[319, 767, 338, 3907, 263, 2090, 1460, 3700, ...]` |  
| `token_pieces` | `["▁A", "▁man", "▁is", "▁making", "▁a", "▁fun", "ny", "▁face", ...]` |  
  
### Step 2b: Extract Object Mentions  
  
Parse the generated caption to find spans that map to COCO's 80 object categories.  
  
1\. **Build an alias table** mapping surface forms to canonical categories:  
 ```  
 "man" → person, "woman" → person, "people" → person  
 "bike" → bicycle, "motorbike" → motorcycle  
 "sofa" → couch, "tv" → tv, "fridge" → refrigerator  
 ```  
 Plus automatic plural forms (`"giraffe"` → `"giraffes"`).  
  
2\. **Scan the caption** for each alias using regex (longest-match-first to avoid ambiguity):  
 - Find character spans: `"man"` at chars 2–5, `"giraffe"` at chars 54–61  
 - Map character spans to token spans using offset mappings  
  
3\. **Produce mention records:**  
  
| mention_id | surface_text | mapped_category | char_span | token_span |  
|-----------|--------------|-----------------|-----------|------------|  
| `m0000` | `man` | `person` | `[2, 5)` | `[1, 1]` |  
| `m0001` | `giraffe` | `giraffe` | `[54, 61)` | `[13, 15]` |  
  
### Step 2c: Save Hidden States  
  
The per-step hidden states from generation are saved as a tensor for potential later use:  
  
$$H^{\text{stage2}} \in \mathbb{R}^{T \times d}$$  
  
**Output artifacts:**  
  
| File | Format | Description |  
|------|--------|-------------|  
| `records/stage2_generated_captions.jsonl` | JSONL | Caption text + token ids per image |  
| `records/stage2_mentions.jsonl` | JSONL | Extracted mentions per image |  
| `records/captions_mentions.parquet` | Parquet | Joined captions + mentions + metadata |  
| `records/stage2_caption_objects.csv` | CSV | Flat mention table |  
| `records/stage2_manifest.json` | JSON | Build summary |  
| `matrices/raw/{record_id}_stage2_hidden_real.pt` | Tensor | Hidden states $H \in \mathbb{R}^{T \times 4096}$ |  
  
---  
  
## 8. Stage 3 — Teacher-Forced Real/Null State Extraction  
  
**What happens:** Re-run the model under **teacher forcing** on the frozen token  
sequence $Y^*$ from Stage 2, extracting decision states under two conditions:  
real image and null image. Also extract the real image's projected visual patches.  
  
**Source file:** `vlm_spectral_analysis/experiments/exp1_teacher_forcing.py` → `Experiment1Stage3Builder.build()`  
  
### Why teacher forcing?  
  
In Stage 2, we generated $Y^*$ freely. Now we need to compare the model's internal  
state at each step $t$ under two visual conditions **for the same token sequence**.  
Teacher forcing ensures:  
- Both conditions decode the exact same tokens $y^*_1, \ldots, y^*_T$  
- There is no generation drift between conditions  
- The only variable is the visual input (real vs. null)  
  
### Step 3a: Real-Image Condition  
  
Feed the model: $(I, Q, y^*_{\<t})$ at each step.  
  
```  
Input: [system_tokens] [v₁^real ... v₅₇₆^real] [question_tokens] [y*₁ ... y*_T]  
 └── real image patches ──┘ └── frozen tokens ─┘  
```  
  
**Forward pass (no generation, just compute):**  
  
$$\text{outputs}^{\text{real}} = \text{LLaVA}(\text{input\_ids}, \text{pixel\_values}^{\text{real}}, \text{output\_hidden\_states=True})$$  
  
**Extract from the output:**  
  
- $h_t^{\text{real}}$ — final-layer hidden state at position corresponding to token $y^*_t$:  
  
$$h_t^{\text{real}} = \text{outputs.hidden\_states}[-1][0][\text{prompt\_len} - 1 + t, :]$$  
  
 Specifically, we take positions $[\text{prompt\_len}-1 \ldots \text{prompt\_len}-1+T)$  
 because position $p-1$ is the state that *predicts* token $y^*_1$.  
  
- $V^{\text{real}}$ — the projected visual patches (image hidden states from the model):  
  
$$V^{\text{real}} \in \mathbb{R}^{576 \times 4096}$$  
  
These are the CLIP patches after passing through LLaVA's linear projector.  
  
### Step 3b: Null-Image Condition  
  
Feed the model: $(I_\varnothing, Q, y^*_{\<t})$ at each step.  
  
The null patches are injected by:  
1\. Loading the tiled null reference $P_\varnothing \in \mathbb{R}^{576 \times 1024}$  
2\. Passing it through the LLaVA multi-modal projector:  
  
$$V^{\text{null}} = \text{Projector}(P_\varnothing) \in \mathbb{R}^{576 \times 4096}$$  
  
3\. **Replacing** the real image tokens in the input embeddings with $V^{\text{null}}$  
 using a masked scatter operation on the `\<image>` placeholder positions  
  
4\. Running a forward pass with the modified embeddings:  
  
$$\text{outputs}^{\text{null}} = \text{LLaVA}(\text{inputs\_embeds}^{\text{null}}, \text{output\_hidden\_states=True})$$  
  
5\. Extracting the null decision states the same way:  
  
$$h_t^{\text{null}} = \text{outputs.hidden\_states}[-1][0][\text{prompt\_len} - 1 + t, :]$$  
  
### Critical design choice  
  
> The patch basis used in Stage 4 is always $V^{\text{real}}$ — the projected patches  
> from the **real** image. Both $h_t^{\text{real}}$ and $h_t^{\text{null}}$ are measured  
> against the same visual coordinate system. This isolates the effect: "given the real  
> image's visual content, does the decision state align with it more when the model  
> actually sees the real image?"  
  
### Data flow diagram for one image  
  
```  
 Image I ──────► CLIP ──► Projector ──► V^real (576×4096) ◄─── saved as patches_real  
 │  
 ▼  
 ┌─────────────────────────────────────┐  
 │ LLaVA forward pass │  
 │ input: [system][V^real][Q][y*₁..T] │  
 │ output: hidden_states[-1] │  
 └──────────────┬──────────────────────┘  
 │  
 ▼  
 h₁^real ... h_T^real ◄─── saved as states_real  
 (T × 4096)  
  
  
 Null P_∅ ─────► Projector ──► V^null (576×4096)  
 │  
 ▼  
 ┌─────────────────────────────────────┐  
 │ LLaVA forward pass │  
 │ input: [system][V^null][Q][y*₁..T] │  
 │ output: hidden_states[-1] │  
 └──────────────┬──────────────────────┘  
 │  
 ▼  
 h₁^null ... h_T^null ◄─── saved as states_null  
 (T × 4096)  
```  
  
**Output artifacts per image:**  
  
| File | Shape | Description |  
|------|-------|-------------|  
| `matrices/raw/{id}_states_real.pt` | $(T, 4096)$ | Real-condition decision states |  
| `matrices/raw/{id}_states_null.pt` | $(T, 4096)$ | Null-condition decision states |  
| `matrices/raw/{id}_patches_real.pt` | $(576, 4096)$ | Real image projected visual tokens |  
| `matrices/raw/{id}_stage3_meta.json` | — | Metadata (shapes, checksums, paths) |  
  
**Aggregate output:**  
  
| File | Description |  
|------|-------------|  
| `records/stage3_manifest.json` | Index of all Stage 3 records with paths |  
  
---  
  
## 9. Stage 4 — Whitened Distributional State Grounding  
  
**What happens:** Apply the whitening transform from Stage 3.5, compute temperature-scaled  
cosine logits, convert to probability distributions via softmax, derive contrastive  
distributions, and extract per-token / per-mention / per-caption grounding scores.  
  
**Source file:** `vlm_spectral_analysis/experiments/exp1_grounding.py` → `Experiment1Stage4Builder.build()`  
  
### Step 4a: Whitening Transform  
  
Load the whitening basis ($\mu$, $U$, $\Lambda$) from `references/whitening/` and apply  
independently to all three input matrices:  
  
$$\hat{x} = (x - \mu) \, U \, \Lambda^{-1/2}$$  
  
where $\Lambda^{-1/2}_{ii} = 1/\sqrt{\lambda_i + \varepsilon}$ with $\varepsilon = 10^{-5}$.  
  
Apply to:  
- $\hat{H}^{\text{real}} = \text{Whiten}(H^{\text{real}})$  
- $\hat{H}^{\text{null}} = \text{Whiten}(H^{\text{null}})$  
- $\hat{V}^{\text{real}} = \text{Whiten}(V^{\text{real}})$  
  
**Crucial:** Both real and null states are compared against the real patches  
$\hat{V}^{\text{real}}$, measuring state shift relative to the actual image content.  
  
### Step 4b: Cosine Logits with Temperature Scaling  
  
Compute cosine similarity between every whitened token state and every whitened patch,  
then sharpen with temperature $\tau$ (default 0.1):  
  
$$\text{Logits}^{\text{real}}_{t,j} = \frac{\langle \hat{h}_t^{\text{real}}, \hat{v}_j^{\text{real}} \rangle}{\|\hat{h}_t^{\text{real}}\| \cdot \|\hat{v}_j^{\text{real}}\|} \cdot \frac{1}{\tau}$$  
  
In code:  
```python  
states_norm = F.normalize(h_real_w, p=2, dim=1) # (T, d)  
patches_norm = F.normalize(v_real_w, p=2, dim=1) # (M, d)  
logits = (states_norm @ patches_norm.T) / tau # (T, M)  
```  
  
### Step 4c: Softmax Probability Distributions  
  
Convert logits into probability distributions over patches:  
  
$$P^{\text{real}}_{t,:} = \text{Softmax}(\text{Logits}^{\text{real}}_{t,:})$$  
$$P^{\text{null}}_{t,:} = \text{Softmax}(\text{Logits}^{\text{null}}_{t,:})$$  
  
Each row $t$ is now a proper probability distribution summing to 1.0.  
  
### Step 4d: Contrastive Derivation  
  
**Distributional delta** — isolate the shift in probability mass caused by the image:  
  
$$A^{\Delta}_{t,j} = P^{\text{real}}_{t,j} - P^{\text{null}}_{t,j}$$  
  
**Rectification (ReLU)** — keep only positive shifts:  
  
$$A^{+}_{t,j} = \max(0,\; A^{\Delta}_{t,j})$$  
  
$A^+$ captures where the image *increased* attention to specific patches.  
Negative shifts (distractions or suppressed priors) are discarded.  
  
### Step 4e: Per-Token Grounding Score  
  
Sum the positive mass shift per token:  
  
$$G^{\text{state}}_t = \sum_{j} A^{+}_{t,j}$$  
  
This score represents the total "attention mass" that moved to specific patches  
because of the image. It ranges from 0 (no image-driven shift) to a theoretical  
maximum of 1 (all probability mass shifted).  
  
### Important interpretation caveat (why punctuation can score high)  
  
Because each row is a probability distribution, we always have:  
  
$$\sum_j P^{\text{real}}_{t,j} = \sum_j P^{\text{null}}_{t,j} = 1 \;\Rightarrow\; \sum_j A^\Delta_{t,j} = 0.$$  
  
Therefore the positive and negative mass are equal in total magnitude, and:  
  
$$G^{\text{state}}_t = \sum_j \max(0, A^\Delta_{t,j}) = \frac{1}{2}\|P^{\text{real}}_{t,:} - P^{\text{null}}_{t,:}\|_1.$$  
  
So `g_state` is fundamentally a **distribution-shift magnitude** metric, not a direct  
"object-word relevance" metric. A token like `"."` can be high if the image strongly  
changes end-of-sentence / continuation dynamics at that step, even if the token itself  
is not a visual noun.  
  
Practical implication:  
- Use token-level `g_state` for diagnostics and flow analysis.  
- Use mention-level / caption-level metrics (`g_mention`, `g_mention_mean`) for semantic  
 hallucination evaluation.  
- Interpret punctuation or stopword token spikes as image-conditioned language control,  
 not necessarily object grounding.  
  
Recommended Stage 4 diagnostics (to avoid misinterpretation):  
- `tables/stage4_token_class_diagnostics.json`:  
 compare punctuation/stopword/content token score distributions.  
- `tables/stage4_position_diagnostics.json`:  
 check whether sequence-position effects dominate token-level `g_state`.  
- Per-record case study (e.g., `tables/stage4_case_study_\<record_id>.json`):  
 report `g_state`, `0.5*L1`, KL, and top patch shifts for selected tokens.  
- Full integrity protocol (output → formula → inputs):  
 `artifacts/experiments/experiment1/STAGE4_CRITICAL_REVIEW_PROTOCOL.md`  
 (includes tri-scenario state audit: `H_free`, `H_tf_real`, `H_tf_null`).  
 The protocol also includes discrimination-first metric benchmarking  
 (entropy/spread/divergence alternatives to baseline `g_state`) and  
 intermediate token-vector tracing (`S -> z -> P -> A_delta -> A_pos`).  
  
**⚠️ DEPRECATION NOTICE:** Stage 4's original whitening-based `g_state` metric has been  
superseded by Stage 6's raw L32 delta pipeline due to the discovery of projector/Layer-32  
space contamination. See Section 15 for details.  
  
Generate these with:  
```bash  
python scripts/experiments/run_stage4_diagnostics.py  
```  
  
Notebook-first critical review workflow:  
- `artifacts/experiments/experiment1/stage4_critical_review.ipynb`  
  
If punctuation tokens outrank nouns at token level, treat that as expected behavior for  
this metric family and confirm semantic discrimination at mention/caption level.  
  
### Step 4f: Per-Mention and Per-Caption Grounding  
  
**Per-mention grounding** (for mention $m$ spanning tokens $S_m$):  
  
$$G_{\text{mention}}(m) = \frac{1}{|S_m|} \sum_{t \in S_m} G^{\text{state}}_t$$  
  
**Caption-level mean mention grounding:**  
  
$$\bar{G}_{\text{mention}}(I) = \frac{1}{|M(I)|} \sum_{m \in M(I)} G_{\text{mention}}(m)$$  
  
### Interpretation of the four matrices  
  
| Matrix | Colormap | What it shows |  
|--------|----------|---------------|  
| $P^{\text{real}}$ | `viridis` | Probability distribution over patches under the **real image** |  
| $P^{\text{null}}$ | `viridis` | Probability distribution over patches under the **null image** (baseline) |  
| $A^{\Delta}$ | `coolwarm` (diverging) | Shift in probability mass: positive = image moved attention here |  
| $A^{+}$ | `hot` (sequential) | Only **positive** shifts — the image-driven grounding signal |  
  
### What to look for in the heatmaps  
  
- **Peaked rows in $P^{\text{real}}$:** tokens whose attention concentrates on specific patches  
- **Flat rows in $P^{\text{null}}$:** null condition distributes attention uniformly (as expected)  
- **Bright rows in $A^+$:** tokens with strong visual grounding (image shifted attention mass)  
- **Dark rows in $A^+$:** tokens with no visual grounding (language-prior driven)  
- **Localized columns in $A^+$:** specific patches receiving more attention due to the image  
  
**Output artifacts per image:**  
  
| File | Shape | Description |  
|------|-------|-------------|  
| `matrices/derived/{id}_A_real.pt` | $(T, 576)$ | Real softmax probability matrix $P^{\text{real}}$ |  
| `matrices/derived/{id}_A_null.pt` | $(T, 576)$ | Null softmax probability matrix $P^{\text{null}}$ |  
| `matrices/derived/{id}_A_delta.pt` | $(T, 576)$ | Distributional delta $A^{\Delta}$ |  
| `matrices/derived/{id}_A_pos.pt` | $(T, 576)$ | Rectified positive evidence $A^{+}$ |  
  
**Aggregate output tables:**  
  
| File | Granularity | Key columns |  
|------|-------------|-------------|  
| `records/grounding_token.parquet` | per token | `record_id`, `token_index`, `token_id`, `g_state` |  
| `records/grounding_mention.parquet` | per mention | `record_id`, `mention_id`, `surface_text`, `mapped_category`, `g_mention` |  
| `records/grounding_caption.parquet` | per caption | `record_id`, `caption`, `n_mentions`, `g_mention_mean` |  
| `records/stage4_manifest.json` | — | Build summary, methodology params |  
  
---  
  
## 10. Visualization — How the Heatmaps Are Drawn  
  
**Source file:** `vlm_spectral_analysis/experiments/exp1_visualization.py` → `Stage4MatrixVisualizer.plot_record()`  
  
When you call:  
```python  
fig, rec = viz.plot_record(sample="1/200", mode="quad", scale_mode="adaptive_quantile")  
```  
  
The following happens:  
  
1\. **Resolve the record:** Parse `"1/200"` → index 0 (1st of 200 records)  
2\. **Load metadata:** question, caption, mentions, token pieces from Stage 2/3 files  
3\. **Load all four matrices** from `matrices/derived/`:  
 - `A_real`, `A_null` from `.pt` files (these store $P^{\text{real}}$, $P^{\text{null}}$)  
 - `A_delta` from file (or compute $P^{\text{real}} - P^{\text{null}}$)  
 - `A_pos` from file (or compute $\max(0, A^{\Delta})$)  
4\. **Create the figure layout:**  
 - **Pair mode:** 1×2 grid for $P^{\text{real}}$, $P^{\text{null}}$  
 - **Quad mode:** 2×2 grid with a text header:  
 - Top-left: $P^{\text{real}}$ (`viridis`)  
 - Top-right: $P^{\text{null}}$ (`viridis`)  
 - Bottom-left: $A^{\Delta}$ (`coolwarm`)  
 - Bottom-right: $A^{+}$ (`hot`)  
 - **Scale modes** (configurable in `plot_record(..., scale_mode=...)` and CLI):  
 - `fixed`: absolute ranges (`P_*:[0,1]`, `A_Δ:[-1,1]`, `A^+:[0,1]`) for strict comparability  
 - `adaptive_minmax`: per-record min/max ranges  
 - `adaptive_quantile` (default): per-record robust quantile ranges (default $q=[0.01, 0.99]$)  
 - `global_quantile`: dataset-wide robust quantile ranges for report-friendly comparability  
5\. **Add annotations:**  
 - Title: record ID, image ID, slice  
 - Question and caption text  
 - Mention summary (e.g., `man→person, giraffe→giraffe`)  
 - Token piece labels on the y-axis (if ≤ 40 tokens)  
6\. **Render with matplotlib** using `imshow` with `aspect="auto"`  
  
Each pixel in the heatmap is one entry from $P^{\text{real}}$, $P^{\text{null}}$, $A^{\Delta}$, or $A^{+}$:  
- **Y-axis** = token step $t$ (0 at top, $T-1$ at bottom)  
- **X-axis** = patch index $j$ (0 to 575, corresponding to spatial positions in the 24×24 CLIP grid)  
- **Color** = probability mass or probability-mass shift  
  
### Word-level overlay on the actual image  
  
For sample-level debugging and interpretability, use:  
  
```bash  
python scripts/experiments/visualize_stage4_word_heatmaps.py \  
 --record-id 000000130599_single_object_0000 \  
 --words man,face,giraffe,statue \  
 --matrix a_pos \  
 --output artifacts/experiments/experiment1/plots/000000130599_word_heatmaps_a_pos.png \  
 --scores-json artifacts/experiments/experiment1/tables/000000130599_word_scores.json  
```  
  
This script:  
- maps selected words to token spans  
- overlays each word's 24×24 patch heatmap on the real image  
- writes per-word grounding scores (span-mean of `g_state`) to JSON  
  
To inspect punctuation or exact subword tokens, select token indices directly:  
  
```bash  
python scripts/experiments/visualize_stage4_word_heatmaps.py \  
 --record-id 000000130599_single_object_0000 \  
 --token-indices 1,7,17 \  
 --matrix a_pos \  
 --output artifacts/experiments/experiment1/plots/000000130599_man_face_period_a_pos.png \  
 --scores-json artifacts/experiments/experiment1/tables/000000130599_man_face_period_scores.json  
```  
  
---  
  
## 11. Files & Artifacts Reference  
  
### Complete output tree  
  
```  
artifacts/experiments/experiment1/  
│  
├── checkpoints/  
│ └── experiment1_checkpoint.json ← Resume state  
│  
├── references/  
│ ├── mean_patch_vector.pt ← p̄ ∈ ℝ^1024  
│ ├── mean_patch_tiled_576x1024.pt ← P_∅ ∈ ℝ^{576×1024}  
│ ├── stage1_5_mean_patch_metadata.json  
│ └── stage1_5_mean_patch_summary.json  
│  
├── records/  
│ ├── image_index.parquet ← Stage 1 dataset index  
│ ├── stage1_image_question_gt.jsonl ← QA rows  
│ ├── stage1_image_index_summary.json  
│ ├── stage2_generated_captions.jsonl ← Generated captions + token ids  
│ ├── stage2_mentions.jsonl ← Extracted mentions  
│ ├── stage2_caption_objects.csv ← Flat mention table  
│ ├── captions_mentions.parquet ← Joined Stage 2 data  
│ ├── stage2_manifest.json  
│ ├── stage3_manifest.json ← Stage 3 record index with paths  
│ ├── grounding_token.parquet ← Per-token G^state scores  
│ ├── grounding_mention.parquet ← Per-mention G_mention scores  
│ ├── grounding_caption.parquet ← Per-caption summary scores  
│ └── stage4_manifest.json  
│  
├── matrices/  
│ ├── raw/ ← Stage 3 tensors (per image)  
│ │ ├── {record_id}_states_real.pt ← h^real ∈ ℝ^{T×4096}  
│ │ ├── {record_id}_states_null.pt ← h^null ∈ ℝ^{T×4096}  
│ │ ├── {record_id}_patches_real.pt ← V^real ∈ ℝ^{576×4096}  
│ │ ├── {record_id}_stage3_meta.json  
│ │ ├── {record_id}_stage2_hidden_real.pt  
│ │ └── {record_id}_stage2_hidden_real_meta.json  
│ │  
│ └── derived/ ← Stage 4 matrices (per image)  
│ ├── {record_id}_A_real.pt ← A^real ∈ ℝ^{T×576}  
│ ├── {record_id}_A_null.pt ← A^null ∈ ℝ^{T×576}  
│ ├── {record_id}_A_delta.pt ← A^Δ ∈ ℝ^{T×576}  
│ └── {record_id}_A_pos.pt ← A^+ ∈ ℝ^{T×576}  
│  
├── plots/ ← Saved visualizations  
└── tables/ ← Summary tables  
```  
  
### Source code files  
  
| File | Stage | Responsibility |  
|------|-------|----------------|  
| `configs/experiments/experiment1.yaml` | — | All experiment hyperparameters |  
| `vlm_spectral_analysis/experiments/exp1_config.py` | — | Config dataclasses & YAML parser |  
| `vlm_spectral_analysis/experiments/exp1_runner.py` | 0–4 | Orchestrator: runs stages in order |  
| `vlm_spectral_analysis/experiments/exp1_dataset.py` | 1 | COCO dataset indexing |  
| `vlm_spectral_analysis/experiments/exp1_null_reference.py` | 1.5 | Dataset-mean null construction |  
| `vlm_spectral_analysis/experiments/exp1_mentions.py` | 2 | Caption generation + mention extraction |  
| `vlm_spectral_analysis/experiments/exp1_teacher_forcing.py` | 3 | Teacher-forced real/null extraction |  
| `vlm_spectral_analysis/experiments/exp1_whitening.py` | 3.5 | Global PCA whitening basis |  
| `vlm_spectral_analysis/experiments/exp1_grounding.py` | 4 | Whitened distributional grounding |  
| `vlm_spectral_analysis/experiments/exp1_visualization.py` | Viz | Heatmap plotting (pair / quad modes) |  
| `scripts/experiments/visualize_stage4_matrices.py` | Viz | CLI wrapper |  
  
---  
  
## 12. Mathematical Summary  
  
### The complete chain from image to grounding score  
  
Given image $I$ and fixed question $Q$:  
  
**1. Generate caption (greedy):**  
  
$$Y^* = (y^*_1, \ldots, y^*_T) = \arg\max \prod_t P(y_t \mid y^*_{\<t}, I, Q)$$  
  
**2. Extract visual patches (real image):**  
  
$$V^{\text{real}} = \text{Projector}(\text{CLIP}(I)) \in \mathbb{R}^{M \times d}$$  
  
where $M = 576$, $d = 4096$.  
  
**3. Construct null reference:**  
  
$$\bar{p} = \frac{1}{NM} \sum_{i,j} P_{i,j} \in \mathbb{R}^{1024}, \quad P_\varnothing = \text{tile}(\bar{p}, M)$$  
  
**4. Teacher-forced forward passes:**  
  
$$h_t^{\text{real}} = \text{LLM}^{(L)}_t(V^{\text{real}}, Q, y^*_{\<t})$$  
$$h_t^{\text{null}} = \text{LLM}^{(L)}_t(\text{Proj}(P_\varnothing), Q, y^*_{\<t})$$  
  
**5. Whitening (Stage 3.5 basis, applied in Stage 4):**  
  
$$\hat{x} = (x - \mu) \, U \, \Lambda^{-1/2}, \quad \Lambda^{-1/2}_{ii} = 1/\sqrt{\lambda_i + \varepsilon}$$  
  
Applied to $H^{\text{real}}$, $H^{\text{null}}$, and $V^{\text{real}}$.  
  
**6. Temperature-scaled cosine logits:**  
  
$$\text{Logits}^{\text{real}}_{t,j} = \frac{1}{\tau} \cdot \frac{\langle \hat{h}_t^{\text{real}}, \hat{v}_j^{\text{real}} \rangle}{\|\hat{h}_t^{\text{real}}\| \cdot \|\hat{v}_j^{\text{real}}\|}$$  
  
**7. Softmax probability distributions:**  
  
$$P^{\text{real}}_{t,:} = \text{Softmax}(\text{Logits}^{\text{real}}_{t,:}), \quad P^{\text{null}}_{t,:} = \text{Softmax}(\text{Logits}^{\text{null}}_{t,:})$$  
  
**8. Contrastive derivation:**  
  
$$A^{\Delta} = P^{\text{real}} - P^{\text{null}}, \quad A^{+}_{t,j} = \max(0, A^{\Delta}_{t,j})$$  
  
**9. Per-token grounding (sum of positive mass):**  
  
$$G^{\text{state}}_t = \sum_{j} A^{+}_{t,j}$$  
  
Equivalent form (because rows of $P^{\text{real}}$ and $P^{\text{null}}$ both sum to 1):  
  
$$G^{\text{state}}_t = \frac{1}{2}\|P^{\text{real}}_{t,:} - P^{\text{null}}_{t,:}\|_1.$$  
  
**10. Per-mention grounding (for mention $m$ with token span $S_m$):**  
  
$$G_{\text{mention}}(m) = \frac{1}{|S_m|} \sum_{t \in S_m} G^{\text{state}}_t$$  
  
**11. Caption-level grounding:**  
  
$$\bar{G}_{\text{mention}}(I) = \frac{1}{|M(I)|} \sum_{m \in M(I)} G_{\text{mention}}(m)$$  
  
**12. The hypotheses to test:**  
- $\text{H1: } \rho(\bar{G}_{\text{mention}}, H) \< 0$ — higher grounding → less hallucination  
- $\text{H2: } \mathbb{E}[G_{\text{mention}} \mid \text{present}] > \mathbb{E}[G_{\text{mention}} \mid \text{hallucinated}]$  
  
---  
  
## 13. Complete Metric Walkthrough (Dimensions + Equations)  
  
This section lists all currently used and reviewed metrics with explicit tensor dimensions.  
  
### 13.1 Indices and core dimensions  
  
- token index: $t \in \{1,\dots,T\}$  
- patch index: $j \in \{1,\dots,M\}$, with $M=576=24\times 24$  
- embedding index: $k \in \{1,\dots,d\}$, with $d=4096$  
  
Core tensors:  
  
- $H^{\text{free}} \in \mathbb{R}^{T\times d}$ (free-running Stage 2 hidden states)  
- $H^{\text{real}} \in \mathbb{R}^{T\times d}$ (teacher-forced, real image)  
- $H^{\text{null}} \in \mathbb{R}^{T\times d}$ (teacher-forced, null image)  
- $V^{\text{real}} \in \mathbb{R}^{M\times d}$ (projected real-image patch vectors)  
  
### 13.2 State-space tri-scenario metrics  
  
Per-token normalized distances:  
  
$$d_{\text{free,real}}(t)=\frac{\|h_t^{\text{free}}-h_t^{\text{real}}\|_2}{\|h_t^{\text{real}}\|_2+\epsilon}$$  
$$d_{\text{free,null}}(t)=\frac{\|h_t^{\text{free}}-h_t^{\text{null}}\|_2}{\|h_t^{\text{real}}\|_2+\epsilon}$$  
$$d_{\text{real,null}}(t)=\frac{\|h_t^{\text{real}}-h_t^{\text{null}}\|_2}{\|h_t^{\text{real}}\|_2+\epsilon}$$  
  
Per-token cosine similarities:  
  
$$c_{\text{free,real}}(t)=\cos(h_t^{\text{free}},h_t^{\text{real}}),\;  
c_{\text{free,null}}(t)=\cos(h_t^{\text{free}},h_t^{\text{null}}),\;  
c_{\text{real,null}}(t)=\cos(h_t^{\text{real}},h_t^{\text{null}})$$  
  
### 13.3 Similarity/logit/probability matrices  
  
Whitened cosine similarity matrices ($\in\mathbb{R}^{T\times M}$):  
  
$$S^{\text{real}}_{t,j}=\cos(\hat h_t^{\text{real}},\hat v_j^{\text{real}}),\quad  
S^{\text{null}}_{t,j}=\cos(\hat h_t^{\text{null}},\hat v_j^{\text{real}})$$  
$$\Delta S_{t,j}=S^{\text{real}}_{t,j}-S^{\text{null}}_{t,j}$$  
$$S^{\text{shiftvec}}_{t,j}=\cos(\widehat{h_t^{\text{real}}-h_t^{\text{null}}},\hat v_j^{\text{real}})$$  
  
Temperature-scaled logits:  
  
$$z^{\text{real}}_{t,j}=S^{\text{real}}_{t,j}/\tau,\quad z^{\text{null}}_{t,j}=S^{\text{null}}_{t,j}/\tau$$  
  
Probability matrices:  
  
$$P^{\text{real}}_{t,:}=\operatorname{Softmax}(z^{\text{real}}_{t,:}),\quad  
P^{\text{null}}_{t,:}=\operatorname{Softmax}(z^{\text{null}}_{t,:})$$  
  
Contrastive matrices:  
  
$$A^\Delta_{t,j}=P^{\text{real}}_{t,j}-P^{\text{null}}_{t,j},\quad  
A^+_{t,j}=\max(0,A^\Delta_{t,j})$$  
  
### 13.4 Baseline scalar grounding score (current Stage 4)  
  
Per token:  
  
$$G_t^{\text{state}}=\sum_{j=1}^M A^+_{t,j}  
\=\frac{1}{2}\|P^{\text{real}}_{t,:}-P^{\text{null}}_{t,:}\|_1$$  
  
Per mention and caption:  
  
$$G_{\text{mention}}(m)=\frac{1}{|S_m|}\sum_{t\in S_m}G_t^{\text{state}},\quad  
\bar G_{\text{mention}}(I)=\frac{1}{|M(I)|}\sum_{m\in M(I)}G_{\text{mention}}(m)$$  
  
### 13.5 Distribution-shape metrics (reviewed alternatives)  
  
For any patch-distribution vector $p\in\mathbb{R}^M$ with $\sum_j p_j=1$:  
  
$$H(p)=-\sum_j p_j\log p_j,\quad  
H_{\text{norm}}(p)=\frac{H(p)}{\log M},\quad  
N_{\text{eff}}(p)=e^{H(p)}$$  
  
Concentration and spread:  
  
$$CR_k(p)=\sum_{j\in\text{TopK}(p)} p_j,\quad  
\text{peak/mean}(p)=\frac{\max_j p_j}{\frac{1}{M}\sum_j p_j}$$  
  
Pairwise divergence (real vs null):  
  
$$L1_t=\|P^{\text{real}}_{t,:}-P^{\text{null}}_{t,:}\|_1,\quad  
L2_t=\|P^{\text{real}}_{t,:}-P^{\text{null}}_{t,:}\|_2$$  
$$KL_t=D_{\text{KL}}(P^{\text{real}}_{t,:}\,\|\,P^{\text{null}}_{t,:})$$  
$$JS_t=\frac{1}{2}D_{\text{KL}}(P^{\text{real}}_{t,:}\,\|\,M_t)+\frac{1}{2}D_{\text{KL}}(P^{\text{null}}_{t,:}\,\|\,M_t),\;  
M_t=\frac{1}{2}(P^{\text{real}}_{t,:}+P^{\text{null}}_{t,:})$$  
  
Spatial shift (24x24 patch grid):  
  
$$COM(p)=\sum_j p_j\,c_j,\quad  
g_{\text{com-shift},t}=\|COM(P^{\text{real}}_{t,:})-COM(P^{\text{null}}_{t,:})\|_2$$  
  
Alternative scalar score candidates evaluated:  
  
- $g_{\text{l1-pos}}=\sum_j\max(0,A^\Delta_{t,j})$ (baseline)  
- $g_{\text{js}}=JS_t$  
- $g_{\text{kl}}=KL_t$  
- $g_{\text{l2}}=L2_t$  
- $g_{\text{topk-shift}}=\sum_{j\in\text{TopK}(A^+_{t,:})}A^+_{t,j}$  
- $g_{\text{com-shift}}$ (defined above)  
  
### 13.6 Dataset-level discrimination metrics  
  
Given token set $U_+$ (mention tokens) and $U_-$ (non-mention tokens), for score $g$:  
  
$$\Delta\mu_g=\mathbb{E}[g\mid U_+]-\mathbb{E}[g\mid U_-]$$  
  
AUC-like directionality score used in diagnostics:  
  
$$\operatorname{AUC\_like}(g)=\Pr(g(u_+) > g(u_-)) + \frac{1}{2}\Pr(g(u_+)=g(u_-))$$  
  
Interpretation:  
  
- $>0.5$: mention tokens tend to score higher  
- $\<0.5$: wrong direction for token-level semantic discrimination  
  
---  
  
## 14. Current Issues (Autopsy Findings — 2026-02-17)  
  
This section records current known failures and risks from the latest review run.  
  
### 14.1 What is working (integrity and separability)  
  
1\. Stage 4 matrix mechanics and identities pass:  
- row sums of `P_real` / `P_null` are \~1  
- `A_delta = P_real - P_null`  
- `g_state = sum(A_pos) = 0.5*L1(P_real,P_null)` within float tolerance  
  
2\. Tri-scenario state separation is strong for real-vs-null:  
- source: `tables/stage4_state_separability_tri_scenario.json`  
- dataset means:  
 - `d_free_real_mean = 0.00118257`  
 - `d_free_null_mean = 0.50412493`  
 - `d_real_null_mean = 0.50412866`  
 - `c_free_real_mean = 0.99999897`  
 - `c_free_null_mean = 0.85007003`  
 - `c_real_null_mean = 0.85006747`  
  
Interpretation: the model state changes materially under null conditioning; this is not a no-signal failure.  
  
### 14.2 What is failing (semantic discrimination at token level)  
  
1\. Baseline token-level score is in the wrong direction:  
- source: `tables/stage4_discrimination_diagnostics.json`  
- `mean_mention = 0.04856148`  
- `mean_nonmention = 0.05048453`  
- `mean_diff = -0.00192305`  
- `auc_like_p_mention_gt_nonmention = 0.44033690` (\< 0.5)  
  
2\. Alternative scalar metrics tested so far also fail directional discrimination:  
- source: `tables/stage4_distribution_metric_benchmark.csv`  
- best observed AUC-like among tested metrics: `g_com_shift = 0.47423611` (\< 0.5)  
- all tested metrics remain below `0.5`  
  
3\. Visual interpretability remains weak:  
- overlays are numerically distinct, but semantic interpretability is still low for many tokens.  
  
### 14.3 Current diagnosis  
  
At present, this is best interpreted as a **metric-objective mismatch**, not a pure implementation bug:  
  
- the pipeline is sensitive to real-vs-null state changes,  
- but token-level scalarization does not align with mention-token semantic grounding.  
  
### 14.4 Decision status (effective immediately)  
  
Until a metric passes discrimination gates:  
  
1\. Treat token-level scores as **diagnostic only**.  
2\. Do not make semantic hallucination claims from token-level rankings.  
3\. Keep semantic evaluation anchored at mention/caption levels.  
4\. Continue critical review in:  
- `artifacts/experiments/experiment1/stage4_critical_review.ipynb`  
- `artifacts/experiments/experiment1/STAGE4_CRITICAL_REVIEW_PROTOCOL.md`  
  
### 14.5 Open remediation work  
  
1\. Expand score families beyond current distribution-shift metrics.  
2\. Audit mention-token alignment/subword aggregation effects.  
3\. Add logit-space and similarity-space semantic discrimination tests.  
4\. Reassess token-level objective before any Stage 5+ interpretation claims depend on it.  