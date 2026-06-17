# Visual Grounding in Large Multimodal Models: A Technical Implementation Report  
  
> **Status:** Complete draft — implementation-aligned mathematical specification.  
  
---  
  
## Table of Contents  
  
1\. [Introduction](#1-introduction)  
2\. [Preliminaries: LLaVA Architecture and Information Flow](#2-preliminaries-llava-architecture-and-information-flow)  
3\. [Counterfactual Grounding Framework](#3-counterfactual-grounding-framework)  
4\. [General Metric Formulation](#4-general-metric-formulation)  
5\. [State Grounding Metrics](#5-state-grounding-metrics)  
6\. [Decision Grounding Metrics](#6-decision-grounding-metrics)  
7\. [Causal Grounding Metrics](#7-causal-grounding-metrics)  
8\. [Composite and Core Scores](#8-composite-and-core-scores)  
9\. [Experimental Controls and Validity](#9-experimental-controls-and-validity)  
10\. [Appendix](#10-appendix)  
  
---  
  
## 1. Introduction  
  
Large vision-language models (VLMs) can produce fluent descriptions even when  
visual evidence is weak or absent. This makes it difficult to distinguish  
**image-grounded generation** from **language-prior completion** based only on  
output text. The objective of this report is to provide an exact,  
implementation-faithful mathematical account of how grounding is measured in  
this codebase.  
  
The central principle is **counterfactual sensitivity**: hold prompt and token  
sequence fixed, replace the real image with a null visual baseline, and measure  
how internal states and output probabilities change. If a token is truly  
grounded in visual content, removing image evidence should produce measurable  
changes in representation, decision distribution, or causal response to  
intervention.  
  
The framework is decomposed into three complementary families:  
  
- **State grounding** (Section 5): hidden-state sensitivity to image patches via  
 real-vs-null cosine-delta geometry.  
- **Decision grounding** (Section 6): output-level probability and rank shifts,  
 plus concept-footprint divergence.  
- **Causal grounding** (Section 7): targeted patch ablation and log-probability  
 effect sizes with matched random controls.  
  
Together these produce a per-token grounding vector and normalized metric  
presets (Section 8), enabling GT-free intrinsic analysis and optional extrinsic  
evaluation overlays. The report is intentionally written as a mathematical  
specification of the implemented pipeline, not as API documentation.  
  
---  
  
## 2. Preliminaries: LLaVA Architecture and Information Flow  
  
This section describes the exact model used throughout all experiments:  
**LLaVA-1.5-7B** (`llava-hf/llava-1.5-7b-hf`), composed of a CLIP vision  
encoder, a two-layer MLP projector, and a Vicuna-7B language model. The  
exposition follows the signal path from raw pixels to output token  
probabilities, introducing the notation used in all subsequent sections.  
  
### 2.1 Vision Encoder  
  
The image $x \in \mathbb{R}^{3 \times 336 \times 336}$ is divided into a  
$24 \times 24$ grid of non-overlapping $14 \times 14$ pixel patches, giving  
$M = 576$ patch tokens. These are processed by a **CLIP ViT-L/14** backbone  
(frozen during inference). Formally, the encoder maps:  
  
$$  
\{u_0, u_1, \dots, u_M\} = \mathrm{CLIP\_ViT}(x), \quad u_i \in \mathbb{R}^{d_v}, \quad d_v = 1024  
$$  
  
where $u_0$ is the CLS token. Following LLaVA-1.5 convention, the CLS token  
is **discarded** and the output is taken from the **penultimate** transformer  
layer (second-to-last hidden state). The retained patch embeddings are:  
  
$$  
U = \{u_1, \dots, u_M\} \in \mathbb{R}^{M \times d_v}, \quad M = 576, \quad d_v = 1024  
$$  
  
These $M$ vectors constitute the visual signal that enters the language model. Their  
$\ell_2$ norms in CLIP space are in the range $\|\cdot\|_2 \approx 0.1$–$2.0$.  
  
### 2.2 Multimodal Projector  
  
The projector $\Phi: \mathbb{R}^{d_v} \rightarrow \mathbb{R}^d$ maps each  
CLIP patch embedding into the language model's embedding space ($d = 4096$).  
It is a two-layer MLP with GELU activation:  
  
$$  
v_i = W_2 \,\mathrm{GELU}(W_1 u_i + b_1) + b_2, \quad i \in \{1, \dots, M\}  
$$  
  
with $W_1 \in \mathbb{R}^{d \times d_v}$, $W_2 \in \mathbb{R}^{d \times d}$.  
The projected patch matrix is:  
  
$$  
X^{(r)} = \Phi(U) \in \mathbb{R}^{M \times d}, \quad d = 4096  
$$  
  
This is referred to throughout as the **projector-output space** or **Layer-0  
input space**. Projected patch norms satisfy $\|v_i\|_2 \approx 16$–$60$.  
  
> **Space caution.** $X^{(r)}$ is in a *different* vector space from the  
> Layer-32 hidden states extracted later. Cosine similarity between vectors  
> from these two spaces is geometrically invalid and never performed.  
  
### 2.3 Sequence Construction  
  
A multimodal input is assembled by interleaving the projected visual tokens  
with the tokenized text prompt. The prompt template used throughout is:  
  
```  
USER: \<image>  
{question}  
ASSISTANT:  
```  
  
The `\<image>` placeholder is a special token (token index 32000). During the  
forward pass, the model substitutes the learned embedding for token 32000 with  
the $M = 576$ projected patch vectors from $X^{(r)}$, inserting them at the  
corresponding positions in the embedding matrix. The full embedding sequence is:  
  
$$  
S_0 = [\underbrace{e_1, \dots, e_{N_{\text{pre}}}}_{\text{pre-image text}},\;  
 \underbrace{v_1, \dots, v_M}_{\text{image patches (Layer-0)}},\;  
 \underbrace{e_{N_{\text{pre}}+1}, \dots, e_{N_{\text{prompt}}}}_{\text{post-image text}} ]  
$$  
  
where $e_k \in \mathbb{R}^d$ are text token embeddings from the LM embedding  
table, and $N_{\text{prompt}}$ is the total prompt length. For teacher-forcing  
evaluations (Sections 5–7), the frozen answer tokens $Y^* = (y_1, \dots, y_T)$  
are appended to this sequence.  
  
### 2.4 Transformer Layer Equations  
  
The language model backbone is **Vicuna-7B**: a 32-layer autoregressive  
transformer with RMS-norm pre-normalization and grouped-query attention.  
  
For each layer $\ell \in \{1, \dots, L\}$ with $L = 32$, let  
$H_{\ell-1} \in \mathbb{R}^{N \times d}$ be the input (with $H_0 = S_0$)  
and $N$ the total sequence length. The layer computes:  
  
$$  
\tilde{H}_{\ell} = \mathrm{LN}_\ell(H_{\ell-1})  
$$  
  
$$  
Q_\ell = \tilde{H}_\ell W^Q_\ell,\quad  
K_\ell = \tilde{H}_\ell W^K_\ell,\quad  
V_\ell = \tilde{H}_\ell W^V_\ell  
$$  
  
$$  
A_\ell = \mathrm{softmax}\\!\left(\frac{Q_\ell K_\ell^\top}{\sqrt{d_k}} + \mathcal{M}\right),  
\quad d_k = d / n_{\text{heads}}  
$$  
  
$$  
\hat{H}_\ell = H_{\ell-1} + A_\ell V_\ell W^O_\ell  
$$  
  
$$  
H_\ell = \hat{H}_\ell + \mathrm{FFN}\\!\left(\mathrm{LN}_\ell(\hat{H}_\ell)\right)  
$$  
  
where $\mathcal{M}$ is the causal mask (upper triangular $-\infty$) and  
$\mathrm{LN}_\ell$ denotes RMSNorm. The final layer output is  
$H_L = H_{32} \in \mathbb{R}^{N \times d}$.  
  
The **Layer-32 hidden states** for any subsequence of positions (e.g., answer  
token positions $\{t_1, \dots, t_T\}$) are extracted by indexing into $H_L$.  
Their $\ell_2$ norms satisfy $\|h_{L,t}\|_2 \approx 80$–$130$.  
  
### 2.5 Output Head and Token Probabilities  
  
The language model head applies a final RMSNorm followed by an unembedding (also  
called the LM head) projection:  
  
$$  
\hat{h}_{L,t} = \mathrm{RMSNorm}_{\text{final}}(h_{L,t}), \quad \hat{h}_{L,t} \in \mathbb{R}^d  
$$  
  
$$  
z_t = W_u\,\hat{h}_{L,t} \in \mathbb{R}^{|V|}, \quad |V| = 32{,}000  
$$  
  
$$  
p_t = \mathrm{softmax}(z_t / \tau) \in \Delta^{|V|-1}  
$$  
  
where $W_u \in \mathbb{R}^{|V| \times d}$ is the unembedding matrix (tied  
with the input embedding in standard LLaMA-family models), and $\tau > 0$ is  
the softmax temperature (default $\tau = 1$ for greedy decoding). The  
probability of token $v$ at step $t$ is:  
  
$$  
p_t(v) = \frac{\exp(z_t(v) / \tau)}{\sum_{v'=1}^{|V|} \exp(z_t(v') / \tau)}  
$$  
  
The generated token at step $t$ under greedy decoding is  
$y_t = \arg\max_v z_t(v)$. In teacher-forcing contexts, the same token may be  
written as $y_t^*$ to emphasize that the sequence is fixed.  
  
### 2.6 Summary of Tensor Dimensions and Vector Spaces  
  
| Tensor | Shape | Space | Norm range |  
|---|---|---|---|  
| $U$ — CLIP patch embeddings | $(M, d_v) = (576, 1024)$ | CLIP feature space | $\approx 0.1$–$2.0$ |  
| $X^{(r)} = \Phi(U)$ — projected patches | $(M, d) = (576, 4096)$ | Projector output / Layer-0 input | $\approx 16$–$60$ |  
| $H_L$ — Layer-32 hidden states | $(N, d) = (N, 4096)$ | Layer-32 space | $\approx 80$–$130$ |  
| $V^{(r)}_{\text{L32}}$ — real-image patch states at Layer-32 | $(M, d) = (576, 4096)$ | Layer-32 space | $\approx 80$–$130$ |  
| $W_u$ — unembedding matrix | $(|V|, d) = (32000, 4096)$ | LM head weight space | — |  
| $z_t$ — logits | $(|V|,) = (32000,)$ | Logit space | — |  
| $p_t$ — token probabilities | $(|V|,) = (32000,)$ | Probability simplex $\Delta^{|V|-1}$ | sum $= 1$ |  
  
> **Key invariant used throughout.** Cosine similarity is only ever computed  
> between vectors confirmed to be in the **same space** — specifically,  
> $H_L^{(r)}$, $H_L^{(0)}$, and $V^{(r)}_{\text{L32}}$ are all in Layer-32  
> space and safe to compare. $X^{(r)}$ is **never** compared against Layer-32  
> vectors.  
  
---  
  
## 3. Counterfactual Grounding Framework  
  
The core methodology rests on a single question: *how does the model behave  
differently when the real image is replaced by a content-free visual baseline  
("null image") while everything else — prompt, token sequence, decoding  
policy, random seed — is held fixed?* Any measurable change is attributed to  
the visual content.  
  
### 3.1 Why Counterfactual Subtraction?  
  
Without a baseline, raw cosine alignments between hidden states and patch  
vectors have a non-zero floor driven by **anisotropy** in the embedding space  
and the projector's additive biases. Even for a purely textual token (e.g., a  
period `.`), the model's Layer-32 representation has non-trivial inner  
products with every patch vector simply because both live in the same $d =  
4096$ space with a learned mean offset. Subtracting a null-image pass removes  
this "background correlation", isolating the image-specific signal:  
  
$$  
\text{signal}(t,j) = \underbrace{\cos(H^{(r)}_t,\,V_j)}_{\text{real}} \;-\; \underbrace{\cos(H^{(0)}_t,\,V_j)}_{\text{null baseline}}  
$$  
  
### 3.2 Null Image Construction  
  
The null image is not a raw pixel image — it is a $M \times d_v$ tensor  
$P^{(0)} \in \mathbb{R}^{M \times d_v}$ in **CLIP space** ($d_v = 1024$) that  
serves as a content-free substitute for the real CLIP patch embeddings. Three  
construction strategies are implemented:  
  
**Strategy 1: Dataset-mean patch (default)**  
  
Compute the empirical mean of all CLIP patch vectors across the dataset. Let  
$\mathcal{D} = \{x^{(n)}\}_{n=1}^N$ be the dataset and $U^{(n)} \in  
\mathbb{R}^{M \times d_v}$ be the CLIP patches of image $n$. Then:  
  
$$  
\mu = \frac{1}{N \cdot M} \sum_{n=1}^{N} \sum_{i=1}^{M} u^{(n)}_i \in \mathbb{R}^{d_v}  
$$  
  
$$  
P^{(0)} = \mathbf{1}_M \otimes \mu \in \mathbb{R}^{M \times d_v}  
\quad \text{(same mean vector tiled into all $M$ slots)}  
$$  
  
This produces a **homogeneous** null: every patch slot carries the same  
representation, removing all spatial content while preserving the mean CLIP  
activation magnitude. $P^{(0)}$ is fixed for the entire dataset run and  
computed once.  
  
**Strategy 2: Per-image mean patch**  
  
$$  
P^{(0)}_x = \mathbf{1}_M \otimes \bar{u}_x, \quad  
\bar{u}_x = \frac{1}{M}\sum_{i=1}^M u_i^{(x)}  
$$  
  
Each image's null is its own spatial average — removes spatial variance while  
retaining overall image luminance/scene statistics. Must be computed per image  
at inference time so cannot be precomputed.  
  
**Strategy 3: White noise**  
  
$$  
P^{(0)}_{ij} \sim \mathcal{N}(0,\,\hat{\sigma}^2), \quad  
\hat{\sigma} = \mathrm{std}(\{u^{(n)}_i\})_{\text{sample}}  
$$  
  
Gaussian noise scaled to real CLIP patch statistics (estimated from a small  
image sample). Used for ablation and sanity checks. Seeded for  
reproducibility.  
  
> **Norm contract.** All three strategies must satisfy $\|P^{(0)}_i\|_2 \< 50$,  
> confirming CLIP-space norms. Any tensor with norms $\approx 100$ would  
> indicate accidental Layer-32 vectors — which is checked and rejected.  
  
### 3.3 The Two Forward Passes  
  
For each sample, with **frozen** answer token sequence  
$Y^* = (y_1, \dots, y_T)$ (obtained from a prior greedy generation pass), two  
teacher-forced forward passes are executed:  
  
**Pass 1 — Real image:**  
  
$$  
\text{Input: } x^{(r)}, \;w_{1:N_{\text{prompt}}}, \;Y^*  
$$  
  
$$  
X^{(0,r)} = \Phi(U^{(r)}) \in \mathbb{R}^{M \times d}  
\quad\text{(projector applied to real CLIP patches)}  
$$  
  
$$  
S = [e_{1:\text{pre}},\; X^{(0,r)},\; e_{\text{post}},\; e_{Y^*}]  
\quad\text{(full embedding sequence)}  
$$  
  
The model runs forward with `output_hidden_states=True`. Outputs extracted:  
  
$$  
H^{(r)} = H^{(r)}_L[\text{answer positions}] \in \mathbb{R}^{T \times d}  
\quad \text{(Layer-32 hidden states for $Y^*$)}  
$$  
  
$$  
X^{(0,r)} = \text{image\_hidden\_states from model output} \in \mathbb{R}^{M \times d}  
\quad \text{(projector output, Layer-0 space)}  
$$  
  
**Pass 2 — Null image:**  
  
The null patches $P^{(0)} \in \mathbb{R}^{M \times d_v}$ are first projected:  
  
$$  
X^{(0,\text{null})} = \Phi(P^{(0)}) \in \mathbb{R}^{M \times d}  
$$  
  
Then injected directly at image-token positions:  
  
$$  
S^{(0)} = [e_{1:\text{pre}},\; X^{(0,\text{null})},\; e_{\text{post}},\; e_{Y^*}]  
$$  
  
The embedding lookup for text tokens is done normally via `get_input_embeddings()`;  
only the $M$ image-token positions (where `input_ids == 32000`) are overwritten  
with $X^{(0,\text{null})}$ by direct index assignment. The model then runs forward:  
  
$$  
H^{(0)} = H^{(0)}_L[\text{answer positions}] \in \mathbb{R}^{T \times d}  
$$  
  
Both $H^{(r)}$ and $H^{(0)}$ are in Layer-32 space (norms $\approx 80$–$130$)  
and are safe to compare by cosine similarity.  
  
### 3.4 Additional Extraction: Layer-32 Patch States  
  
A separate forward pass (no teacher forcing) extracts patch hidden states at  
Layer 32. With only the prompt (no $Y^*$), the model runs with the real image  
and `output_hidden_states=True`. The final-layer hidden states at image-token  
positions give:  
  
$$  
V^{(r)}_{\text{L32}} = H_L[\mathcal{I}_{\text{img}}] \in \mathbb{R}^{M \times d}  
\quad \text{(Layer-32 patch states, real image)}  
$$  
  
where $\mathcal{I}_{\text{img}} = \{i : \text{input\_ids}[i] = 32000\}$ are  
the 576 image-token positions. The same extraction with null patches (used in  
Decision Grounding) gives $V^{(0)}_{\text{L32}} \in \mathbb{R}^{M \times d}$.  
  
Both $V^{(r)}_{\text{L32}}$ and $V^{(0)}_{\text{L32}}$ are in Layer-32 space,  
and are safe for cosine similarity against $H^{(r)}$ and $H^{(0)}$.  
  
### 3.5 Tensor Inventory After Extraction  
  
| Symbol | Shape | Space | Produced by |  
|---|---|---|---|  
| $H^{(r)}$ | $(T, d)$ | Layer-32 | `teacher_force()` real pass |  
| $H^{(0)}$ | $(T, d)$ | Layer-32 | `teacher_force()` null pass |  
| $X^{(0,r)}$ | $(M, d)$ | Layer-0 / projector output | `teacher_force()` real pass via `image_hidden_states` |  
| $V^{(r)}_{\text{L32}}$ | $(M, d)$ | Layer-32 | `extract_l32_patches()` real image |  
| $V^{(0)}_{\text{L32}}$ | $(M, d)$ | Layer-32 | `get_lm_artifacts()` null pass |  
| $W_u$ | $(|V|, d)$ | LM head weight space | `get_lm_artifacts()` via `get_output_embeddings()` |  
  
> **Critical invariant.** $X^{(0,r)}$ (projector output space) is **never**  
> compared by cosine similarity to $H^{(r)}$, $H^{(0)}$, $V^{(r)}_{\text{L32}}$,  
> or $V^{(0)}_{\text{L32}}$ (all Layer-32 space). $X^{(0,r)}$ is used  
> **only** as the injection vector for counterfactual patch ablation in Causal  
> Grounding (Section 7).  
  
### 3.6 Notation Conventions  
  
The following superscript/subscript conventions are used throughout Sections 5–7:  
  
| Notation | Meaning |  
|---|---|  
| Superscript $(r)$ | Real image condition |  
| Superscript $(0)$ | Null image condition |  
| Subscript $t$ | Token position index, $t \in \{1,\dots,T\}$ |  
| Subscript $j$ | Patch slot index, $j \in \{1,\dots,M\}$, $M=576$|  
| Subscript $v$ | Vocabulary index, $v \in \{1,\dots,|V|\}$, $|V|=32{,}000$ |  
| $y_t$ | Generated token at position $t$ (from $Y^*$) |  
| $\Omega$ | Support patch set (subset of $\{1,\dots,M\}$) |  
| $\tau$ | Softmax temperature (default $\tau = 1$; $\tau = 0.1$ for concept profiles) |  
  
---  
  
## 4. General Metric Formulation  
  
This section defines the mathematical operators and normalization transforms  
that are shared across all three grounding families. Rather than re-derive  
them in Sections 5–7, they are stated once here and referenced by name.  
  
### 4.1 The Delta Matrix — Shared Foundation  
  
All three grounding families begin from the same two-pass extraction described  
in Section 3. The central shared object is the **cosine delta matrix**:  
  
$$  
\Delta[t,j] = \cos\\!\left(H^{(r)}_t,\; V^{(r)}_{\text{L32},j}\right)  
 - \cos\\!\left(H^{(0)}_t,\; V^{(r)}_{\text{L32},j}\right),  
\quad t \in \{1,\dots,T\},\; j \in \{1,\dots,M\}  
$$  
  
where the cosine operator is:  
  
$$  
\cos(u, v) = \frac{\langle u, v \rangle}{\|u\|_2 \|v\|_2 + \epsilon}, \quad \epsilon = 10^{-9}  
$$  
  
Note that **both** real and null states are compared against the **same** patch  
coordinate system $V^{(r)}_{\text{L32}}$. This preserves the invariant that  
null subtraction removes only the baseline alignment, not the patch reference  
frame. The delta has the interpretation:  
  
- $\Delta[t,j] > 0$ — the real image raised token $t$'s alignment with patch $j$  
- $\Delta[t,j] \approx 0$ — no image-driven shift for this (token, patch) pair  
- $\Delta[t,j] \< 0$ — the real image lowered alignment with patch $j$  
  
$\Delta \in \mathbb{R}^{T \times M}$ is the input to all state grounding metrics  
and also used for support mask construction in causal grounding.  
  
### 4.2 Shared Mathematical Operators  
  
#### 4.2.1 Cosine Similarity (pairwise matrix form)  
  
For two matrices $A \in \mathbb{R}^{n \times d}$ and $B \in \mathbb{R}^{m \times d}$:  
  
$$  
\mathrm{CosMat}(A, B)_{ij} = \frac{\langle \hat{a}_i, \hat{b}_j \rangle}{1},  
\quad \hat{a}_i = \frac{a_i}{\|a_i\|_2 + \epsilon}, \quad \hat{b}_j = \frac{b_j}{\|b_j\|_2 + \epsilon}  
$$  
  
implemented as $\hat{A}\hat{B}^\top$, giving shape $(n, m)$. Used for the delta  
matrix and for Decision Grounding concept profile scores.  
  
#### 4.2.2 Softmax at Temperature $\tau$  
  
For a score vector $s \in \mathbb{R}^K$ (over patches or vocabulary):  
  
$$  
\sigma_\tau(s)_k = \frac{\exp(s_k / \tau)}{\sum_{k'=1}^K \exp(s_{k'} / \tau)}  
$$  
  
Lower $\tau$ sharpens the distribution. Used at:  
- $\tau = 1.0$ — default token probability decoding  
- $\tau = 0.1$ — concept profiles in Decision and Causal Grounding (sharper spatial focus)  
- $\tau = 0.1$ — delta entropy metric in State Grounding  
  
#### 4.2.3 Shannon Entropy  
  
For a distribution $p \in \Delta^{K-1}$:  
  
$$  
H(p) = -\sum_{k=1}^{K} p_k \log p_k, \quad H \in [0, \ln K] \text{ (nats)}  
$$  
  
with the convention $0 \log 0 = 0$. Internally clamped at $p_k \geq 10^{-12}$  
to avoid $\log 0$. Used in the state grounding entropy metric (over patch space,  
$K = M = 576$).  
  
#### 4.2.4 Jensen–Shannon Divergence  
  
For two distributions $p, q \in \Delta^{K-1}$, with mixture $m = \tfrac{1}{2}(p+q)$:  
  
$$  
\mathrm{JSD}(p, q) = \frac{1}{2}\mathrm{KL}(p \,\|\, m) + \frac{1}{2}\mathrm{KL}(q \,\|\, m)  
$$  
  
$$  
\mathrm{KL}(p \,\|\, q) = \sum_{k=1}^K p_k \log \frac{p_k}{q_k}  
$$  
  
Properties used in this work:  
- **Symmetric**: $\mathrm{JSD}(p,q) = \mathrm{JSD}(q,p)$  
- **Bounded**: $\mathrm{JSD}(p,q) \in [0, \ln 2] \approx [0, 0.693]$ (nats)  
- **Stable**: well-defined even when $p$ or $q$ has zero mass (unlike raw KL)  
  
Used in Decision Grounding concept footprint (over patch space) and vocabulary  
distribution comparisons. Inputs are clamped at $\epsilon = 10^{-9}$.  
  
#### 4.2.5 Entropy Delta  
  
$$  
\Delta H(p^{(r)}, p^{(0)}) = H(p^{(0)}) - H(p^{(r)})  
$$  
  
Positive value means the real image *focused* the distribution (reduced  
entropy); negative means it spread it. Used in Decision Grounding Track B  
to quantify spatial sharpening.  
  
#### 4.2.6 Positive Mass (TVD half-mass)  
  
For patch distributions $p^{(r)}, p^{(0)} \in \Delta^{M-1}$:  
  
$$  
p^+_j = \max\\!\left(0,\; p^{(r)}_j - p^{(0)}_j\right), \quad j \in \{1,\dots,M\}  
$$  
  
The sum $\sum_j p^+_j = \tfrac{1}{2}\|p^{(r)} - p^{(0)}\|_1 = \mathrm{TVD}(p^{(r)}, p^{(0)})$,  
equal to the total variation distance. Used as the unnormalized support  
distribution for causal support mask $\Omega$ construction.  
  
#### 4.2.7 Cumulative Support Mask  
  
Given a non-negative score vector $s \in \mathbb{R}^M_{\geq 0}$ (e.g. $p^+$ above),  
the support set $\Omega$ at coverage $\alpha$ with minimum size $k_{\min}$ is:  
  
$$  
\Omega = \operatorname*{arg\,top}_{\omega \subseteq [M]} \left\{  
 |\omega| \;\text{minimal} : \sum_{j \in \omega} \frac{s_j}{\|s\|_1} \geq \alpha  
 \;\text{ and }\; |\omega| \geq k_{\min}  
\right\}  
$$  
  
In practice: sort patches by $s_j$ descending, accumulate the normalised mass,  
stop when cumulative mass $\geq \alpha$ and at least $k_{\min}$ patches have  
been selected. Default $\alpha = 0.90$, $k_{\min} = 12$.  
  
### 4.3 Metric Normalization Variants  
  
Every raw metric $m$ is also provided in two population-normalized forms,  
applied post-hoc across the whole dataset.  
  
#### 4.3.1 Percentile Rank (`_pct`)  
  
$$  
m_{\text{pct}} = \hat{F}(m) = \frac{|\{m' \in \mathcal{M} : m' \leq m\}|}{|\mathcal{M}|}  
\in [0, 1]  
$$  
  
where $\mathcal{M}$ is the set of all raw metric values in the dataset. Ties  
are resolved by averaging ranks (`method="average"`). This is a  
distribution-free transform — it makes no Gaussianity assumption and is robust  
to heavy tails and outliers.  
  
#### 4.3.2 Robust Z-score (`_rz`)  
  
$$  
m_{\text{rz}} = \frac{m - \tilde{m}}{1.4826 \cdot \widetilde{|m - \tilde{m}|}}  
\= \frac{m - \mathrm{median}(\mathcal{M})}{1.4826 \cdot \mathrm{MAD}(\mathcal{M})}  
$$  
  
where $\mathrm{MAD}(\mathcal{M}) = \mathrm{median}\{|m' - \tilde{m}|\}$ is the  
median absolute deviation. The factor $1.4826 \approx 1/\Phi^{-1}(0.75)$ makes  
the MAD-based scale consistent with the standard deviation under a Gaussian.  
The result is clipped to $[-10, 10]$ to handle extreme outliers. When $\mathrm{MAD} = 0$  
(all values identical), $m_{\text{rz}} = 0$.  
  
Unlike a standard z-score, this transform is **robust** to the long-tailed  
distributions of grounding scores (many near-zero values, rare large spikes).  
  
#### 4.3.3 Summary  
  
| Suffix | Transform | Properties |  
|---|---|---|  
| *(none)* | Raw computed value | Physical units, interpretable magnitude |  
| `_pct` | Empirical percentile $\in [0,1]$ | Distribution-free, outlier-robust, comparable across metrics |  
| `_rz` | Robust z-score (MAD-scaled), clipped to $[-10,10]$ | Approximately scale-free, Gaussian-consistent under normality |  
  
---  
  
## 5. State Grounding Metrics  
  
**Definition.** State grounding measures how much the model's **Layer-32  
hidden-state representations** change between the real-image and null-image  
forward passes, specifically asking: *for each generated token $y_t$, does  
the real image cause that token's final representation to align more strongly  
with specific spatial patches than the null image does?* High state grounding  
at token $t$ indicates its Layer-32 representation is shaped by where the  
model is "looking" in the image.  
  
### 5.1 Input: The Delta Matrix  
  
All state grounding metrics operate on the delta matrix  
$\Delta \in \mathbb{R}^{T \times M}$ defined in Section 4.1:  
  
$$  
\Delta[t,j] = \cos\\!\left(H^{(r)}_t,\, V^{(r)}_{\text{L32},j}\right)  
 - \cos\\!\left(H^{(0)}_t,\, V^{(r)}_{\text{L32},j}\right)  
$$  
  
The vector $\Delta[t, :] \in \mathbb{R}^M$ is the **spatial grounding  
profile** of token $t$ — a signed score for each of the $M=576$ patches  
indicating whether the real image increased or decreased that token's  
alignment with that patch, relative to the null baseline.  
  
### 5.2 Token-Level Metric Derivations  
  
All five raw metrics are computed independently per row $\Delta[t,:] \in  
\mathbb{R}^{576}$, then collected into per-token score vectors of length $T$.  
  
#### 5.2.1 Spatial Variance (Primary Metric) — `state_delta_var`  
  
$$  
\boxed{  
\texttt{state\_delta\_var}_t = \mathrm{Var}_j\\!\left(\Delta[t,:]\right)  
\= \frac{1}{M}\sum_{j=1}^{M}\\!\left(\Delta[t,j] - \overline{\Delta[t,:]}\right)^2  
}  
$$  
  
**Interpretation.** A flat $\Delta[t,:]$ (uniform shift across all patches)  
yields low variance — the token's state changed similarly everywhere,  
consistent with a text-driven or non-visual token (e.g. punctuation). A  
peaked $\Delta[t,:]$ (concentrated shift on a small patch region) yields  
high variance — the token's state was pulled toward a specific spatial area  
by the real image, indicating **visual grounding**. This is the primary state  
grounding metric used throughout the pipeline.  
  
#### 5.2.2 Spatial Standard Deviation — `state_delta_std`  
  
$$  
\texttt{state\_delta\_std}_t = \sqrt{\texttt{state\_delta\_var}_t}  
\= \mathrm{Std}_j\\!\left(\Delta[t,:]\right)  
$$  
  
In the same units as $\Delta$ (cosine difference). Monotonically related to  
`state_delta_var` and used where linear scaling is preferred over quadratic.  
  
#### 5.2.3 Spatial Mean — `state_delta_mean`  
  
$$  
\texttt{state\_delta\_mean}_t = \frac{1}{M}\sum_{j=1}^{M} \Delta[t,j]  
$$  
  
Measures the **average shift** of token $t$'s alignment across all patches.  
A positive value means the real image globally raised alignment (broad  
scene-level grounding); near-zero means the image had no net directional  
effect on this token.  
  
#### 5.2.4 Spatial Entropy at $\tau = 0.1$ — `state_delta_entropy_tau01`  
  
This metric asks: *how focused is the spatial grounding profile when sharpened  
at low temperature?*  
  
Step 1 — temperature-scale and stabilize numerically:  
  
$$  
\tilde{s}_j = \frac{\Delta[t,j]}{\tau} - \max_k \frac{\Delta[t,k]}{\tau}, \quad \tau = 0.1  
$$  
  
Step 2 — convert to a distribution over patches:  
  
$$  
\pi_j = \frac{\exp(\tilde{s}_j)}{\sum_{k=1}^M \exp(\tilde{s}_k)}, \quad \pi \in \Delta^{M-1}  
$$  
  
Step 3 — compute Shannon entropy:  
  
$$  
\boxed{  
\texttt{state\_delta\_entropy\_tau01}_t = H(\pi) = -\sum_{j=1}^{M} \pi_j \log\\!\left(\pi_j + 10^{-12}\right)  
}  
$$  
  
where the entropy is measured in **nats** ($\log$ is natural log), bounded in  
$[0, \ln M] = [0, \ln 576] \approx [0,\, 6.36]$.  
  
**Interpretation.** Low entropy $\approx 0$ → the shifted profile is  
concentrated in a single patch (very sharp grounding). High entropy $\approx  
\ln 576$ → uniform distribution, no spatial preference. The low temperature  
$\tau = 0.1$ amplifies differences, making this metric sensitive to the peak  
of the spatial profile. Note the **inverse** relationship to variance: high  
`state_delta_var` corresponds to low `state_delta_entropy_tau01`.  
  
### 5.3 Normalized Variants  
  
The four normalized variants follow the definitions in Section 4.3 exactly,  
applied post-hoc across all token rows in the dataset:  
  
| Metric | Transform |  
|---|---|  
| `state_delta_mean_rz` | Robust z-score of `state_delta_mean` (MAD-scaled, clipped $[-10,10]$) |  
| `state_delta_var_rz` | Robust z-score of `state_delta_var` |  
| `state_delta_mean_pct` | Empirical percentile rank of `state_delta_mean` $\in [0,1]$ |  
| `state_delta_var_pct` | Empirical percentile rank of `state_delta_var` $\in [0,1]$ |  
  
### 5.4 Aggregation: Mention and Caption Scores  
  
Beyond individual token scores, state grounding is aggregated to *mention* and  
*caption* levels using the object mentions extracted from the generated text.  
  
**Mention-level score.** For a mention span covering token indices  
$\{t_s, t_{s+1}, \dots, t_e\}$ (from the `MentionSpan` of the caption):  
  
$$  
\texttt{mean\_delta\_var}_m = \frac{1}{|\mathcal{M}_m|}\sum_{t \in \mathcal{M}_m} \texttt{state\_delta\_var}_t  
$$  
  
where $\mathcal{M}_m = \{t : t_s \leq t \leq t_e\}$.  
  
**Caption-level score.** Mean across all mentions in the generated text:  
  
$$  
G_{\text{state, caption}} = \frac{1}{|\mathcal{M}|} \sum_{m \in \mathcal{M}} \texttt{mean\_delta\_var}_m  
$$  
  
### 5.5 Complete Metric Table  
  
| Metric name | Formula | Domain | Interpretation |  
|---|---|---|---|  
| `state_delta_var` | $\mathrm{Var}_j(\Delta[t,:])$ | $[0, \infty)$ | ↑ = more spatially localised grounding |  
| `state_delta_std` | $\mathrm{Std}_j(\Delta[t,:])$ | $[0, \infty)$ | ↑ = more localised (linear scale) |  
| `state_delta_mean` | $\mathrm{Mean}_j(\Delta[t,:])$ | $(-\infty, \infty)$ | ↑ = broader global alignment with real image |  
| `state_delta_entropy_tau01` | $H(\sigma_{0.1}(\Delta[t,:]))$ | $[0, \ln 576]$ | ↓ = sharper spatial focus (inverse of var) |  
| `state_delta_mean_rz` | Robust z-score of `state_delta_mean` | $[-10,\,10]$ | Population-relative mean shift |  
| `state_delta_var_rz` | Robust z-score of `state_delta_var` | $[-10,\,10]$ | Population-relative spatial peaking |  
| `state_delta_mean_pct` | Percentile rank of `state_delta_mean` | $[0,\,1]$ | Fraction of tokens with lower mean |  
| `state_delta_var_pct` | Percentile rank of `state_delta_var` | $[0,\,1]$ | Fraction of tokens with lower variance |  
  
### 5.6 Interpretation Guide  
  
| Token type | Expected behaviour |  
|---|---|  
| Object noun (e.g. "banana") | High `state_delta_var`, low `state_delta_entropy_tau01` — spatially concentrated |  
| Attribute (e.g. "yellow") | Moderate `state_delta_var` — grounded but spatially broader |  
| Function word (e.g. "on") | Low `state_delta_var` — flat spatial profile |  
| Punctuation (`.`, `,`) | Near-zero `state_delta_var` and `state_delta_mean` |  
  
A token is **hallucinated** in the state-grounding sense if it generates high  
`state_delta_var` but names an object not present — or conversely, names an  
object that is present but shows near-zero `state_delta_var` (generated from  
language priors rather than visual evidence).  
  
---  
  
## 6. Decision Grounding Metrics  
  
**Definition.** Decision grounding measures how much the model's **output  
probability distribution over the vocabulary** changes between the real-image  
and null-image forward passes. Where state grounding asks whether the internal  
representations shift, decision grounding asks: *did the real image actually  
change what the model decided to generate, and can we identify which spatial  
patches drive that decision?*  
  
Decision grounding is organized into two independent analysis tracks:  
  
- **Track A — Vocabulary shift**: measures how each token's generation  
 probability changes at every position in $Y^*$.  
- **Track B — Concept footprint**: measures whether the unembedding vector  
 $W_{y_t}$ (the concept direction for token $y_t$) is spatially grounded in  
 the image.  
  
### 6.1 Preamble: Logit Computation from Layer-32 States  
  
The output logits are reconstructed from the extracted Layer-32 hidden states  
$H^{(r)}, H^{(0)} \in \mathbb{R}^{T \times d}$ using the unembedding matrix  
$W_u \in \mathbb{R}^{|V| \times d}$ extracted from the LM head.  
  
Before applying $W_u$, an adaptive **RMSNorm selection** is performed. The  
norm is applied only when it improves rank-1 recovery:  
  
$$  
\hat{h}_t = \frac{h_t}{\sqrt{\frac{1}{d}\sum_{k=1}^d h_{t,k}^2 + 10^{-5}}} \odot \gamma  
$$  
  
where $\gamma \in \mathbb{R}^d$ is the final RMSNorm scale vector (extracted  
from `get_lm_artifacts()`). Whether to apply this is determined by comparing  
the fraction of positions where $\arg\max_v\,(H W_u^\top)_{t,v} = y_t$  
between the normed and un-normed variants — the one with higher rank-1  
recovery is used for all downstream computation.  
  
Logits and probabilities under each condition:  
  
$$  
z^{(r)}_t = \hat{H}^{(r)}_t W_u^\top \in \mathbb{R}^{|V|}, \qquad  
z^{(0)}_t = \hat{H}^{(0)}_t W_u^\top \in \mathbb{R}^{|V|}  
$$  
  
$$  
P^{(r)}_t = \mathrm{softmax}(z^{(r)}_t) \in \Delta^{|V|-1}, \qquad  
P^{(0)}_t = \mathrm{softmax}(z^{(0)}_t) \in \Delta^{|V|-1}  
$$  
  
$$  
\Delta P_t = P^{(r)}_t - P^{(0)}_t \in \mathbb{R}^{|V|}  
$$  
  
### 6.2 Track A: Vocabulary Shift Metrics  
  
All Track A metrics are computed for **every** token position $t \in  
\{1,\dots,T\}$ in $Y^*$.  
  
#### 6.2.1 Probability Shift — `decision_delta_p`  
  
$$  
\boxed{  
\texttt{decision\_delta\_p}_t = \Delta P_t[y_t] = P^{(r)}_t[y_t] - P^{(0)}_t[y_t]  
}  
$$  
  
Positive values indicate the real image raised the probability of the  
generated token — the model was more "confident" in that token due to visual  
input. Negative values indicate the null image was actually more favorable,  
suggesting the token may be language-prior driven.  
  
#### 6.2.2 Marginal Probabilities — `decision_p_real`, `decision_p_null`  
  
$$  
\texttt{decision\_p\_real}_t = P^{(r)}_t[y_t], \qquad  
\texttt{decision\_p\_null}_t = P^{(0)}_t[y_t]  
$$  
  
The raw probability mass on the generated token under each condition.  
  
#### 6.2.3 Vocabulary Rank — `decision_rank_real`, `decision_rank_null`  
  
$$  
\texttt{decision\_rank\_real}_t = \left|\{v : z^{(r)}_t[v] \geq z^{(r)}_t[y_t]\}\right|  
$$  
  
$$  
\texttt{decision\_rank\_null}_t = \left|\{v : z^{(0)}_t[v] \geq z^{(0)}_t[y_t]\}\right|  
$$  
  
Rank-1 means the generated token is the argmax. Lower rank $\Rightarrow$ more  
preferred. The comparison is on raw logits (not probabilities), so rank is  
equivalent to descending-sort position.  
  
### 6.3 Generation Step Selection  
  
The **focal generation step** $t^*$ (used throughout Track B and as the  
reference step in Causal Grounding) is chosen as:  
  
$$  
t^* = \arg\max_{t \in \mathcal{T}_{\text{valid}}} \Delta P_t[y_t]  
$$  
  
where $\mathcal{T}_{\text{valid}} = \{t : y_t \notin \mathcal{P}\}$ excludes  
punctuation tokens. $\mathcal{P}$ is identified by both token-ID matching (e.g.  
LLaMA period token ID 29889) and text matching against the set  
$\{".",\, ",",\, "\!",\, "?",\, ";",\, ":"\}$, making the selection  
model-agnostic.  
  
### 6.4 Track B: Concept Footprint Metrics  
  
Track B characterises whether the **concept vector** $W_{y_{t^*}}$ — the  
unembedding row for the chosen token — is spatially aligned with specific  
image patches differently under real vs. null conditions.  
  
#### 6.4.1 Concept Alignment Scores  
  
Let $\hat{W}_u$ and $\hat{V}^{(r)}_{\text{L32}}$, $\hat{V}^{(0)}_{\text{L32}}$  
denote the $\ell_2$-normalized versions (row-wise) of $W_u$, $V^{(r)}_{\text{L32}}$  
and $V^{(0)}_{\text{L32}}$. For a candidate token $c$ with concept vector  
$\hat{w}_c \in \mathbb{R}^d$:  
  
$$  
s^{(r)}_j(c) = \hat{V}^{(r)}_{\text{L32},j} \cdot \hat{w}_c, \quad  
s^{(0)}_j(c) = \hat{V}^{(0)}_{\text{L32},j} \cdot \hat{w}_c, \quad j \in \{1,\dots,M\}  
$$  
  
These are cosine similarities between each patch's Layer-32 state and the  
concept direction — measuring how much each patch "favors" that token concept.  
  
The **concept spatial delta** is:  
  
$$  
\delta s_j(c) = s^{(r)}_j(c) - s^{(0)}_j(c)  
$$  
  
#### 6.4.2 Concept Variance — `decision_concept_var`  
  
$$  
\boxed{  
\texttt{decision\_concept\_var}_c = \mathrm{Var}_j\\!\left(\delta s_j(c)\right)  
\= \mathrm{Var}_j\\!\left(s^{(r)}_j(c) - s^{(0)}_j(c)\right)  
}  
$$  
  
Analogous to `state_delta_var` but computed for the concept direction rather  
than text-token hidden states. High `concept_var` means the concept vector  
$\hat{w}_c$ is unevenly aligned with patches in the real vs. null condition —  
evidence that the concept is spatially grounded.  
  
#### 6.4.3 Concept Spatial JSD — `decision_jsd_tau0.1`  
  
Convert concept alignment scores into patch distributions at temperature $\tau$:  
  
$$  
\pi^{(r)}_j(c;\tau) = \frac{\exp(s^{(r)}_j(c)/\tau)}{\sum_{k=1}^M \exp(s^{(r)}_k(c)/\tau)},  
\qquad  
\pi^{(0)}_j(c;\tau) = \frac{\exp(s^{(0)}_j(c)/\tau)}{\sum_{k=1}^M \exp(s^{(0)}_k(c)/\tau)}  
$$  
  
$$  
\boxed{  
\texttt{decision\_jsd\_tau}\tau_c = \mathrm{JSD}\\!\left(\pi^{(r)}(c;\tau),\, \pi^{(0)}(c;\tau)\right)  
}  
$$  
  
The primary reported value uses $\tau = 0.1$ (`decision_jsd_tau0.1`). At low  
temperature, the distributions are sharply peaked; JSD measures whether the  
dominant patch region shifts between conditions, making the metric sensitive to  
spatial re-localization of the concept.  
  
Bounded: $\mathrm{JSD} \in [0, \ln 2] \approx [0, 0.693]$ nats.  
  
#### 6.4.4 Alignment With State Delta — `decision_align_gen`  
  
$$  
\boxed{  
\texttt{decision\_align\_gen}_{t^*} =  
\cos\\!\left(\Delta[t^*,:],\; \delta s(y_{t^*})\right)  
\= \frac{\langle \Delta[t^*,:],\; \delta s(y_{t^*}) \rangle}  
 {\|\Delta[t^*,:]\|_2 \cdot \|\delta s(y_{t^*})\|_2 + \epsilon}  
}  
$$  
  
This measures whether the **state grounding spatial profile** (which patches  
shifted hidden states) agrees with the **concept footprint** (which patches  
align with the concept direction). High `align_gen` means the two independent  
grounding signals point to the same region of the image — strong evidence of  
coherent visual grounding.  
  
### 6.5 Quadrant Classification  
  
Each (token, candidate) pair is classified into one of four quadrants based on  
$\texttt{decision\_delta\_p}_{t^*}$ and the concept JSD relative to the  
median JSD across candidates at $\tau = \tau_0 = 0.1$:  
  
$$  
\bar{J} = \mathrm{median}_{c \in \mathcal{C}}\\!\left(\texttt{decision\_jsd\_tau0.1}_c\right)  
$$  
  
| Quadrant | Condition | Interpretation |  
|---|---|---|  
| `Q1_True_Grounding` | $\Delta P_{t^*}[y_{t^*}] > 0$ AND $J_c > \bar{J}$ | Image raised probability AND concept is spatially grounded |  
| `Q2_Ungrounded_Hallucination` | $\Delta P_{t^*}[y_{t^*}] > 0$ AND $J_c \leq \bar{J}$ | Image raised probability but concept has no spatial footprint |  
| `Q3_Language_Hallucination` | $\Delta P_{t^*}[y_{t^*}] \leq 0$ AND $J_c \leq \bar{J}$ | Image suppressed this token AND no spatial grounding — pure language prior |  
| `Q4_Suppressed_Grounding` | $\Delta P_{t^*}[y_{t^*}] \leq 0$ AND $J_c > \bar{J}$ | Spatially grounded concept but image actually reduced probability |  
  
### 6.6 Normalized Variants  
  
| Metric | Transform |  
|---|---|  
| `decision_delta_p_rz` | Robust z-score of `decision_delta_p` (MAD-scaled, clipped $[-10, 10]$) |  
| `decision_delta_p_pct` | Empirical percentile rank of `decision_delta_p` $\in [0, 1]$ |  
  
### 6.7 Complete Metric Table  
  
| Metric name | Formula | Domain | Interpretation |  
|---|---|---|---|  
| `decision_delta_p` | $P^{(r)}_t[y_t] - P^{(0)}_t[y_t]$ | $(-1, 1)$ | ↑ = real image raised token probability |  
| `decision_p_real` | $P^{(r)}_t[y_t]$ | $(0, 1)$ | Token probability under real image |  
| `decision_p_null` | $P^{(0)}_t[y_t]$ | $(0, 1)$ | Token probability under null image |  
| `decision_rank_real` | count of logits $\geq z^{(r)}_t[y_t]$ | $\{1,\dots,|V|\}$ | ↓ = token more preferred; rank-1 = argmax |  
| `decision_rank_null` | count of logits $\geq z^{(0)}_t[y_t]$ | $\{1,\dots,|V|\}$ | ↓ = token more preferred under null |  
| `decision_concept_var` | $\mathrm{Var}_j(\delta s_j(y_{t^*}))$ | $[0,\infty)$ | ↑ = concept more spatially localized |  
| `decision_align_gen` | $\cos(\Delta[t^*,:],\, \delta s(y_{t^*}))$ | $[-1, 1]$ | ↑ = state and concept ground to same patches |  
| `decision_jsd_tau0.1` | $\mathrm{JSD}(\pi^{(r)}(y_{t^*}; 0.1),\, \pi^{(0)}(y_{t^*}; 0.1))$ | $[0, \ln 2]$ | ↑ = concept spatial footprint shifts between conditions |  
| `decision_delta_p_rz` | Robust z-score of `decision_delta_p` | $[-10, 10]$ | Population-relative probability lift |  
| `decision_delta_p_pct` | Percentile rank of `decision_delta_p` | $[0, 1]$ | Fraction of tokens with lower probability lift |  
  
---  
  
## 7. Causal Grounding Metrics  
  
**Definition.** Causal grounding measures the **drop in log-probability of the  
generated token** when a targeted subset of image patches is replaced with null  
patches. Unlike state and decision grounding — which compare real vs. null  
image holistically — causal grounding asks a surgical question: *which specific  
spatial patches are causally necessary for the model to assign high probability  
to token $y_{t^*}$?* It uses the generation step $t^*$ identified by decision  
grounding (Section 6.3).  
  
### 7.1 Step 1 — Concept Profile: What Patches Matter?  
  
The **concept profile** distributes probability mass over the $M = 576$ patches  
according to how much each patch supports the chosen concept $y_{t^*}$ beyond  
the null baseline. It requires $V^{(r)}_{\text{L32}}$, $V^{(0)}_{\text{L32}}$,  
and $W_u$ from $\texttt{LMArtifacts}$.  
  
**Step 1a — Concept direction.**  
  
$$  
\hat{w}_c = \frac{W_u[y_{t^*}]}{\|W_u[y_{t^*}]\|_2} \in \mathbb{R}^d  
$$  
  
**Step 1b — Patch alignment scores under each condition.**  
  
$$  
s^{(r)}_j = \hat{V}^{(r)}_{\text{L32},j} \cdot \hat{w}_c, \qquad  
s^{(0)}_j = \hat{V}^{(0)}_{\text{L32},j} \cdot \hat{w}_c, \qquad j \in \{1,\dots,M\}  
$$  
  
where $\hat{V}$ denotes row-wise $\ell_2$-normalization.  
  
**Step 1c — Convert to patch distributions at temperature $\tau$.**  
  
$$  
\pi^{(r)}_j = \frac{\exp(s^{(r)}_j / \tau)}{\sum_k \exp(s^{(r)}_k / \tau)}, \qquad  
\pi^{(0)}_j = \frac{\exp(s^{(0)}_j / \tau)}{\sum_k \exp(s^{(0)}_k / \tau)}  
$$  
  
The temperature $\tau$ is read from Track B output (the first $\tau$ in the  
`taus` list, typically $\tau = 0.1$).  
  
**Step 1d — Positive mass (concept-specific shift).**  
  
$$  
p^+_j = \mathrm{ReLU}\\!\left(\pi^{(r)}_j - \pi^{(0)}_j\right), \qquad  
\bar{p}^+_j = \frac{p^+_j}{\sum_{k=1}^M p^+_k}  
$$  
  
$\bar{p}^+$ is the normalized **concept mass distribution** — placing weight  
on patches where the real image increased the concept's probability concentration  
above the null baseline. This is the Exp3 methodology exactly.  
  
**Fallback path.** When $\texttt{LMArtifacts}$ are unavailable:  
  
$$  
p^+_j = \mathrm{ReLU}\\!\left(\Delta[t^*, j]\right), \qquad  
\bar{p}^+_j = \frac{p^+_j}{\sum_k p^+_k}  
$$  
  
i.e., the raw state delta row (non-concept-specific, token-level) is used  
instead of the concept profile.  
  
### 7.2 Step 2 — Support Mask $\Omega$ Construction  
  
The support set $\Omega \subseteq \{1,\dots,M\}$ identifies the minimal  
patch subset that accounts for fraction $\alpha$ of the total concept mass,  
with a minimum cardinality floor $k_{\min}$:  
  
$$  
\Omega = \arg\min_{|\omega|} \left\{  
 \omega \subseteq [M] :  
 \sum_{j \in \omega} \bar{p}^+_j \geq \alpha  
 \;\;\text{and}\;\;  
 |\omega| \geq k_{\min}  
\right\}  
$$  
  
Algorithm: sort patches by $\bar{p}^+_j$ descending; accumulate; stop at  
the first index $k$ where $\sum_{i=1}^k \bar{p}^+_{\sigma(i)} \geq \alpha$  
and $k \geq k_{\min}$.  
  
Default values: $\alpha = 0.90$, $k_{\min} = 12$.  
  
**Degenerate case.** If $\sum_j p^+_j \< 10^{-8}$ (no positive concept mass),  
the fallback is to take the top-$\max(k_{\min}, 32)$ patches by raw alignment  
score $s^{(r)}_j$. The output flags `mask_status = "degenerate_fallback_topk"`.  
  
### 7.3 Step 3 — Counterfactual Injection and Forward Passes  
  
The **counterfactual patch sequence** $X^{\text{cf}}$ is constructed by  
replacing the support patches with null projections at Layer 0:  
  
$$  
X^{\text{cf}} = X^{(0,r)}, \quad X^{\text{cf}}[\Omega] \leftarrow X^{(0,\text{null})}[\Omega]  
$$  
  
where $X^{(0,r)} \in \mathbb{R}^{M \times d}$ is the real projector output  
(`patches_proj_l0.pt`) and $X^{(0,\text{null})} \in \mathbb{R}^{M \times d}$  
is the projector-output null.  
  
Two teacher-forced forward passes are then executed at Layer 0 via  
`inject_and_forward()`, which bypasses the CLIP encoder and projector entirely  
and injects $X$ directly at image-token positions:  
  
$$  
\ell^{(r)}_t = \left[\texttt{inject\_and\_forward}(X^{(0,r)}, Y^*)\right]_t \in \mathbb{R}^{|V|}  
$$  
  
$$  
\ell^{\text{cf}}_t = \left[\texttt{inject\_and\_forward}(X^{\text{cf}}, Y^*)\right]_t \in \mathbb{R}^{|V|}  
$$  
  
Token probabilities and log-probabilities are extracted via  
$\log\text{softmax}$ at each step:  
  
$$  
\log p^{(r)}_t[v] = \ell^{(r)}_t[v] - \log\\!\sum_{v'}\exp(\ell^{(r)}_t[v']), \qquad  
p^{(r)}_t[v] = \exp(\log p^{(r)}_t[v])  
$$  
  
and analogously for $\ell^{\text{cf}}$.  
  
### 7.4 Causal Metric Derivations  
  
All metrics are evaluated at $(t, y_t)$ — the generated token at each step.  
  
#### 7.4.1 Log-Probability Drop — `causal_delta_logp`  
  
$$  
\boxed{  
\texttt{causal\_delta\_logp}_t = \log p^{(r)}_t[y_t] - \log p^{\text{cf}}_t[y_t]  
}  
$$  
  
Positive value: the real support patches are causally important — removing  
them reduces the log-probability. Near-zero: the support patches were not  
causally necessary (the token was likely generated from language priors or  
non-support image regions).  
  
#### 7.4.2 Probability Drop — `causal_delta_p`  
  
$$  
\texttt{causal\_delta\_p}_t = p^{(r)}_t[y_t] - p^{\text{cf}}_t[y_t]  
$$  
  
Probability-space analogue of `causal_delta_logp`. Less sensitive to  
near-zero probabilities but more interpretable as an absolute change.  
  
#### 7.4.3 Relative Drop — `causal_rel_drop`  
  
$$  
\texttt{causal\_rel\_drop}_t =  
\mathrm{clip}\\!\left(  
 \frac{\log p^{(r)}_t[y_t] - \log p^{\text{cf}}_t[y_t]}{|\log p^{(r)}_t[y_t]| + 10^{-12}},  
 \;-100,\; 100  
\right)  
$$  
  
Normalizes the log-probability drop by the magnitude of the real log-probability.  
Hard-clipped to $[-100, 100]$ to avoid numerical blowup when $\log p^{(r)} \approx 0$  
(probability near 1).  
  
**Interpretation.** $\texttt{causal\_rel\_drop} \approx 1$ means the  
counterfactual ablation reduced the log-probability to near zero — the support  
patches account for essentially all the model's confidence. Values $> 1$ can  
occur when the counterfactual actively suppresses the token (log-prob drops  
more than the original log-prob).  
  
#### 7.4.4 Support Size — `causal_mask_size`  
  
$$  
\texttt{causal\_mask\_size}_t = |\Omega_t|  
$$  
  
The number of patches ablated. Smaller $\Omega$ achieving the same drop is  
evidence of a tight, efficient causal footprint.  
  
#### 7.4.5 Marginal Probabilities — `causal_p_real`, `causal_p_cf`  
  
$$  
\texttt{causal\_p\_real}_t = p^{(r)}_t[y_t], \qquad  
\texttt{causal\_p\_cf}_t = p^{\text{cf}}_t[y_t]  
$$  
  
Raw probabilities under real and counterfactual conditions — used to verify  
that the targeted ablation had a meaningful effect and to diagnose degenerate  
cases.  
  
### 7.5 Specificity Margin (Focal Step Only)  
  
At the focal generation step $t^*$, an additional **random control ablation**  
is performed to test whether the targeted support $\Omega$ is *specifically*  
important, beyond what any random same-size ablation would cause.  
  
For each of $K$ random controls ($K = \texttt{n\_random\_controls}$, default  
3), a uniformly random subset $\Omega^{(k)}_{\text{rand}} \subset [M]$ with  
$|\Omega^{(k)}_{\text{rand}}| = |\Omega|$ is drawn (seeded), ablated, and the  
log-probability drop is measured:  
  
$$  
\delta^{(k)}_{\text{rand}} = \log p^{(r)}_{t^*}[y_{t^*}] - \log p^{\text{rand}(k)}_{t^*}[y_{t^*}]  
$$  
  
$$  
\texttt{specificity\_margin} =  
\texttt{causal\_delta\_logp}_{t^*}  
- \frac{1}{K}\sum_{k=1}^{K} \delta^{(k)}_{\text{rand}}  
$$  
  
$\texttt{specificity\_margin} > 0$ means the targeted support patches  
consistently cause a *larger* log-probability drop than random same-size  
ablations — i.e., they are not merely reflecting that any large mask disrupts  
the image, but that these specific patches are causally load-bearing. This is  
the primary diagnostic for hallucination detection in Exp3: a hallucinated  
token may show low `causal_delta_logp` (image not causally responsible) and  
low `specificity_margin`.  
  
### 7.6 Normalized Variants  
  
| Metric | Transform |  
|---|---|  
| `causal_delta_logp_rz` | Robust z-score of `causal_delta_logp` (MAD-scaled, clipped $[-10, 10]$) |  
| `causal_delta_logp_pct` | Empirical percentile rank of `causal_delta_logp` $\in [0, 1]$ |  
  
### 7.7 Complete Metric Table  
  
| Metric name | Formula | Domain | Interpretation |  
|---|---|---|---|  
| `causal_delta_logp` | $\log p^{(r)}_t[y_t] - \log p^{\text{cf}}_t[y_t]$ | $(-\infty, \infty)$ | ↑ = support patches causally necessary |  
| `causal_delta_p` | $p^{(r)}_t[y_t] - p^{\text{cf}}_t[y_t]$ | $(-1, 1)$ | ↑ = larger probability drop on ablation |  
| `causal_rel_drop` | $\Delta\log p / (|\log p^{(r)}| + \varepsilon)$, clipped | $[-100, 100]$ | ↑ near 1 = ablation explains most confidence |  
| `causal_mask_size` | $|\Omega_t|$ | $\{k_{\min},\dots,M\}$ | Smaller = tighter causal footprint |  
| `causal_p_real` | $p^{(r)}_t[y_t]$ | $(0, 1)$ | Token probability under real image |  
| `causal_p_cf` | $p^{\text{cf}}_t[y_t]$ | $(0, 1)$ | Token probability after support ablation |  
| `specificity_margin` | $\texttt{causal\_delta\_logp} - \bar{\delta}_{\text{rand}}$ | $(-\infty, \infty)$ | ↑ = targeted > random; causal footprint is specific |  
| `causal_delta_logp_rz` | Robust z-score of `causal_delta_logp` | $[-10, 10]$ | Population-relative causal drop |  
| `causal_delta_logp_pct` | Percentile rank of `causal_delta_logp` | $[0, 1]$ | Fraction of tokens with lower causal drop |  
  
### 7.8 Relationship to State and Decision Grounding  
  
The three grounding families measure the same underlying phenomenon at  
different levels of abstraction:  
  
| Family | What changes | Where | Signal type |  
|---|---|---|---|  
| State | Hidden representation $H^{(r)}_t$ vs $H^{(0)}_t$ | Layer 32, internal | Correlational — does the state shift spatially? |  
| Decision | Output distribution $P^{(r)}_t$ vs $P^{(0)}_t$ | Vocabulary head | Correlational — does the decision shift? |  
| Causal | Log-probability $\log p^{(r)}$ vs $\log p^{\text{cf}}$ after targeted patch removal | Layer 0 injection | Interventional — are specific patches causally necessary? |  
  
All three operate on the same frozen token sequence $Y^*$, the same null  
reference $P^{(0)}$, and the same model — their metrics are therefore directly  
comparable per token and per sample.  
  
---  
  
## 8. Composite and Core Scores  
  
Each grounding family produces a per-token numerical signal that is independent  
of ground-truth labels. Instead of collapsing these into a single weighted  
scalar, the framework exposes a *grounding vector* per token and defines a  
designated **core triad** for downstream evaluation.  
  
---  
  
### 8.1 Core Metric Triad  
  
The `core` preset selects one canonical metric from each family:  
  
| Core metric | Family | Quantity measured |  
|---|---|---|  
| `state_delta_mean` | State | Mean cosine shift across all 576 patch dimensions |  
| `decision_delta_p` | Decision | Probability mass transferred by image conditioning |  
| `causal_delta_logp` | Causal | Log-probability drop under targeted patch ablation |  
  
The three-way fingerprint for token $t$ is therefore:  
  
$$  
\mathbf{g}_t = \bigl(s^{\text{state}}_t,\; s^{\text{dec}}_t,\; s^{\text{caus}}_t\bigr)  
\= \bigl(\mu^\Delta_t,\; \Delta p_t,\; \Delta\ell^\text{cf}_t\bigr)  
$$  
  
where $\mu^\Delta_t$ is `state_delta_mean` (§5.3), $\Delta p_t$ is `decision_delta_p`  
(§6.3), and $\Delta\ell^\text{cf}_t$ is `causal_delta_logp` (§7.4).  
  
These three quantities operate in different numerical ranges and scales; they should  
not be summed without normalization.  
  
---  
  
### 8.2 Per-Token Grounding Vector and Normalized Representation  
  
For comparability across tokens and prompts, normalized variants are preferred.  
Two normalizations are defined (§4.3):  
  
**Robust z-score** (suffix `_rz`):  
  
$$  
z^{\text{rz}}(x) = \operatorname{clip}\\!\left(\frac{x - \tilde{x}}{1.4826 \cdot \mathrm{MAD}(x)},\;-10,\;10\right)  
$$  
  
**Percentile rank** (suffix `_pct`):  
  
$$  
p^{\text{pct}}(x) = \frac{\operatorname{rank}(x)}{N}  
\in [0,1]  
$$  
  
A practical normalized triad is:  
  
$$  
\hat{\mathbf{g}}_t = \left(z^{\text{rz}}(\mu^\Delta_t),\; p^{\text{pct}}(\Delta p_t),\; p^{\text{pct}}(\Delta\ell^\text{cf}_t)\right)  
$$  
  
This form is suitable for downstream classifiers or embeddings that require  
cross-metric comparability.  
  
---  
  
### 8.3 Sample-Level Aggregation  
  
All three families produce per-token values. Sample-level summaries are formed  
by averaging over generated tokens:  
  
**State** — mean delta-var across all $T$ generated tokens:  
  
$$  
\bar{s}^{\text{state}} = \frac{1}{T}\sum_{t=1}^{T} \sigma^2(\Delta_t)  
$$  
  
**Decision** — carried from the selected generation step $t^*$ (§6.4); the sample  
summary is a single scalar since decision grounding targets the representative token:  
  
$$  
s^{\text{dec}} = \Delta p_{t^*}  
$$  
  
**Causal** — the focal-token `delta_logp` from `causal_result.csv`; averaged if  
`per_token_metrics=True` produces multiple rows:  
  
$$  
s^{\text{caus}} = \frac{1}{|\mathcal{G}|}\sum_{t\in\mathcal{G}} \Delta\ell^\text{cf}_t  
$$  
  
where $\mathcal{G}$ is the set of targeted generation steps.  
  
These three sample-level scalars feed the **master grounding table**  
(`results/master_grounding_table.csv`) produced by `run_aggregate.py`.  
  
---  
  
### 8.4 Full Metric Inventory by Preset  
  
The `_METRIC_PRESETS` dictionary (defined in `scripts/run_multimodal_judge_eval.py`)  
partitions the full metric space into four named views:  
  
#### State preset (8 columns)  
  
| Column | Formula reference |  
|---|---|  
| `state_delta_mean` | §5.3 — mean of $\Delta_t$ |  
| `state_delta_var` | §5.1 — variance of $\Delta_t$ |  
| `state_delta_std` | §5.2 — standard deviation of $\Delta_t$ |  
| `state_delta_entropy_tau01` | §5.4 — entropy of $\operatorname{softmax}(\Delta_t/0.1)$ |  
| `state_delta_mean_rz` | §8.2 — robust z-score of `state_delta_mean` |  
| `state_delta_var_rz` | §8.2 — robust z-score of `state_delta_var` |  
| `state_delta_mean_pct` | §8.2 — percentile rank of `state_delta_mean` |  
| `state_delta_var_pct` | §8.2 — percentile rank of `state_delta_var` |  
  
#### Decision preset (10 columns)  
  
| Column | Formula reference |  
|---|---|  
| `decision_delta_p` | §6.3 Track A — $\Delta p_t = p^{(r)}_t - p^{(0)}_t$ |  
| `decision_p_real` | §6.3 — $p^{(r)}_t$ softmax probability under real image |  
| `decision_p_null` | §6.3 — $p^{(0)}_t$ softmax probability under null image |  
| `decision_rank_real` | §6.3 — rank of $y^*_t$ in $P^{(r)}$ |  
| `decision_rank_null` | §6.3 — rank of $y^*_t$ in $P^{(0)}$ |  
| `decision_concept_var` | §6.5 Track B — spatial variance of concept footprint |  
| `decision_align_gen` | §6.5 — cosine alignment $\cos(\Delta_t, \bar{\Delta}_s)$ |  
| `decision_jsd_tau0.1` | §6.5 — $\mathrm{JSD}(\pi^{(r)}, \pi^{(0)})$ at $\tau=0.1$ |  
| `decision_delta_p_rz` | §8.2 — robust z-score of `decision_delta_p` |  
| `decision_delta_p_pct` | §8.2 — percentile rank of `decision_delta_p` |  
  
#### Causal preset (8 columns)  
  
| Column | Formula reference |  
|---|---|  
| `causal_delta_logp` | §7.4 — $\Delta\ell^\text{cf} = \ell^{(r)} - \ell^{\text{cf}}$ |  
| `causal_delta_p` | §7.4 — $\Delta p^\text{cf} = p^{(r)} - p^\text{cf}$ |  
| `causal_rel_drop` | §7.4 — $\Delta\ell^\text{cf}/|\ell^{(r)}|$ clipped to $[-100,100]$ |  
| `causal_mask_size` | §7.4 — $|\Omega|$, number of ablated patches |  
| `causal_p_real` | §7.4 — $p^{(r)}$, probability under real image |  
| `causal_p_cf` | §7.4 — $p^\text{cf}$, probability under targeted ablation |  
| `causal_delta_logp_rz` | §8.2 — robust z-score of `causal_delta_logp` |  
| `causal_delta_logp_pct` | §8.2 — percentile rank of `causal_delta_logp` |  
  
#### Core preset (3 columns)  
  
| Column | Section |  
|---|---|  
| `state_delta_mean` | §5.3 |  
| `decision_delta_p` | §6.3 |  
| `causal_delta_logp` | §7.4 |  
  
---  
  
## 9. Experimental Controls and Validity  
  
Reproducibility of the counterfactual framework depends on holding several  
experimental degrees of freedom fixed across runs.  
  
---  
  
### 9.1 Decoding Regime and Prompt Template  
  
All hidden-state extractions use **greedy decoding** (`decoding: greedy` in  
`configs/base.yaml`). Teacher-forcing then re-feeds the greedy-decoded sequence so  
that each token's hidden states and logits are conditioned on the identical prefix  
regardless of run order. The default prompt is:  
  
```  
"Describe the image in one sentence."  
```  
  
Both the prompt text and decoding strategy are recorded in `caption_meta.json` per  
sample, ensuring that any change propagates into the artifact fingerprint.  
  
**Temperature for Track B / causal concept profiles** — softmax temperature $\tau$ is  
not a sampling temperature; it scales the patch-affinity distribution within the  
algorithm. The pipeline sweeps $\tau \in \{0.1, 1.0, 10.0\}$ for decision Track B.  
Causal grounding reads $\tau$ from `track_b.json` (first entry, typically 0.1) rather  
than hardcoding it.  
  
---  
  
### 9.2 Null-Image Design  
  
Three null strategies are available:  
  
| Strategy | Description | Typical CLIP-space norm |  
|---|---|---|  
| `dataset_mean_patch` (**primary**) | $\bar{P}_{\text{COCO}}$ — mean over all COCO val patches | $\approx 0.8$ |  
| `per_image_mean` | $\bar{P}_i$ — mean over the image's own 576 patches | $\approx 0.6$ |  
| `white_noise` | $\mathcal{N}(0, \sigma^2)$ rescaled to match mean patch norm | varies |  
  
All strategies enforce a CLIP-space norm guardrail ($\|\bar{P}\|_2 \< 50$) before  
projection. `dataset_mean_patch` is the preferred baseline because it removes  
image-specific signal while remaining within the model's learned CLIP distribution.  
  
`per_image_mean` collapses spatial structure to a DC offset, producing a "blurred"  
conditioning that still carries global colorimetric statistics. `white_noise` provides  
a maximally uninformative null but lies farther from the natural image manifold.  
  
---  
  
### 9.3 Hyperparameter Summary  
  
| Parameter | Value | Location |  
|---|---|---|  
| Quantization | 4-bit BnB | `model.quantize` |  
| Hidden-state layer | $L=32$ (final layer) | `extract_l32_patches()` |  
| Delta matrix | cosine, $T \times 576$ | `cosine_delta_matrix()` |  
| Track B temperature sweep | $\tau \in \{0.1, 1.0, 10.0\}$ | `grounding.decision.tau` |  
| Track B candidate pool | top-$k=10$ union | `grounding.decision.top_k` |  
| Causal support threshold | $\alpha = 0.90$ | `grounding.causal.alpha` |  
| Causal minimum mask size | $k_{\min} = 12$ | `grounding.causal.k_min` |  
| Causal random controls | $K = 3$ (default) | `grounding.causal.n_random_controls` |  
| Null patch count | $M = 576$ | `null.patch_count` |  
| Normalization clip | $\pm 10$ robust z-score | `--rz-clip` in `normalize_token_compact.py` |  
  
---  
  
### 9.4 Statistical Validity and Reporting  
  
**Token-level granularity.** All three metric families are defined at the token level.  
Sample-level summaries (§8.3) are arithmetic means over per-token values and do not  
weight tokens by length or part-of-speech.  
  
**Independence of signals.** The three core metrics are derived from independent  
computations:  
- State grounding uses only Layer-32 hidden states (no logit computation).  
- Decision grounding uses only the final-layer logit distribution (no patch ablation).  
- Causal grounding bypasses the vision encoder entirely via `inject_and_forward()`.  
  
Correlation between the three signals is an empirical property of the dataset,  
not an artifact of the methodology.  
  
**Specificity control.** Causal grounding applies $K$ matched random ablations (same  
mask size $|\Omega|$, random patch selection) to compute the specificity margin  
(§7.5). A positive margin is required for a causal claim to be considered reliable.  
  
**No ground-truth dependency.** The entire intrinsic pipeline is GT-free. External  
validation (extrinsic) requires reference captions or a multimodal judge, but the  
grounding metrics themselves are inference-only.  
  
**Reproducibility.** Given fixed `model_id`, `quantize`, `null.strategy`, and  
`extraction.prompt`, the pipeline output is deterministic: greedy decoding has no  
sampling randomness, and the causal random control seeds are derived deterministically  
from `gen_step * 1000 + chosen_id`.  
  
---  
  
## 10. Appendix  
  
### A. Complete Symbol Table  
  
#### Model Dimensions  
  
| Symbol | Value | Definition |  
|---|---|---|  
| $d_v$ | 1024 | CLIP ViT-L/14 hidden dimension |  
| $d$ | 4096 | LLM (Vicuna-7B) hidden dimension |  
| $M$ | 576 | Number of visual patch tokens ($24\times24$ grid) |  
| $L$ | 32 | Number of transformer layers in Vicuna-7B |  
| $\|V\|$ | 32 000 | Vocabulary size |  
| $T$ | — | Number of generated tokens in a caption |  
  
#### Inputs and Signals  
  
| Symbol | Shape | Definition |  
|---|---|---|  
| $x^{(r)}$ | — | Real input image (RGB) |  
| $x^{(0)}$ | — | Null input (mean-patch tiling or equivalent) |  
| $E^{(r)}$ | $(M, d_v)$ | CLIP patch embeddings for real image |  
| $E^{(0)}$ | $(M, d_v)$ | CLIP patch embeddings for null image |  
| $X^{(r)}$ | $(M, d)$ | Projected patch tokens after MLP projector (real) |  
| $X^{(0)}$ | $(M, d)$ | Projected patch tokens after MLP projector (null) |  
| $H^{(r)}$ | $(T, d)$ | Layer-32 hidden states for all generated tokens (real) |  
| $H^{(0)}$ | $(T, d)$ | Layer-32 hidden states for all generated tokens (null) |  
| $V^{(r)}_{32}$ | $(M, d)$ | Layer-32 hidden states at image-token positions (real) |  
| $V^{(0)}_{32}$ | $(M, d)$ | Layer-32 hidden states at image-token positions (null) |  
  
#### Delta Matrix  
  
| Symbol | Shape | Definition |  
|---|---|---|  
| $\Delta$ | $(T, M)$ | Cosine delta matrix: $\Delta_{t,j} = c^{(r)}_{t,j} - c^{(0)}_{t,j}$ |  
| $\Delta_t$ | $(M,)$ | Row $t$ of $\Delta$: patch sensitivity profile for token $t$ |  
| $c^{(r)}_{t,j}$ | scalar | $\cos(H^{(r)}_t,\, V^{(r)}_{32,j})$ |  
| $c^{(0)}_{t,j}$ | scalar | $\cos(H^{(0)}_t,\, V^{(r)}_{32,j})$ |  
  
#### Probability Distributions  
  
| Symbol | Definition |  
|---|---|  
| $z^{(r)}_t \in \mathbb{R}^{|V|}$ | Logit vector at token $t$ under real image |  
| $z^{(0)}_t \in \mathbb{R}^{|V|}$ | Logit vector at token $t$ under null image |  
| $P^{(r)}_t = \operatorname{softmax}(z^{(r)}_t)$ | Vocabulary distribution under real image |  
| $P^{(0)}_t = \operatorname{softmax}(z^{(0)}_t)$ | Vocabulary distribution under null image |  
| $y_t^*$ (or $y_t$) | Greedy-decoded token at position $t$ |  
| $p^{(r)}_t = P^{(r)}_t[y_t^*]$ | Probability of $y_t^*$ under real image |  
| $p^{(0)}_t = P^{(0)}_t[y_t^*]$ | Probability of $y_t^*$ under null image |  
  
#### Causal Grounding Specific  
  
| Symbol | Definition |  
|---|---|  
| $\hat{w}_c \in \mathbb{R}^d$ | $\ell_2$-normalized unembedding row for concept token $c$ |  
| $s^{(r)}_j$ | Real-image patch affinity $\hat{w}_c \cdot \hat{V}^{(r)}_{32,j}$ |  
| $s^{(0)}_j$ | Null-image patch affinity $\hat{w}_c \cdot \hat{V}^{(0)}_{32,j}$ |  
| $\pi^{(r)}_j$ | $\operatorname{softmax}(s^{(r)}/\tau)_j$ |  
| $\pi^{(0)}_j$ | $\operatorname{softmax}(s^{(0)}/\tau)_j$ |  
| $\bar{p}^+_j$ | $\operatorname{ReLU}(\pi^{(r)}_j - \pi^{(0)}_j)$, normalized to sum to 1 |  
| $\Omega$ | Support mask: indices $j$ where cumulative $\bar{p}^+$ first reaches $\alpha$ |  
| $X^{\text{cf}}$ | Counterfactual patch sequence with $\Omega$ ablated to null |  
  
#### Operators and Parameters  
  
| Symbol | Definition |  
|---|---|  
| $\tau$ | Softmax temperature (Track B / causal: typically 0.1) |  
| $\alpha$ | Causal support coverage threshold (default: 0.90) |  
| $k_{\min}$ | Minimum support mask size (default: 12) |  
| $K$ | Number of random control ablations (default: 3) |  
| $\mathrm{MAD}$ | Median Absolute Deviation |  
| $H(p)$ | Shannon entropy of distribution $p$ |  
| $\mathrm{JSD}(p,q)$ | Jensen–Shannon divergence |  
  
---  
  
### B. Key Mathematical Derivations  
  
#### B.1 Jensen–Shannon Divergence  
  
For distributions $p$ and $q$ over vocabulary $V$:  
  
$$  
\mathrm{JSD}(p, q) = \frac{1}{2}\,\mathrm{KL}(p \| m) + \frac{1}{2}\,\mathrm{KL}(q \| m),  
\quad m = \frac{p+q}{2}  
$$  
  
$$  
\mathrm{KL}(p \| m) = \sum_{v \in V} p_v \log\frac{p_v}{m_v}  
$$  
  
Properties: $\mathrm{JSD}(p,q) \in [0, \ln 2]$; zero iff $p = q$; symmetric;  
well-defined even when $p$ or $q$ has zeros (since $m_v > 0$ whenever $p_v > 0$ or  
$q_v > 0$). In this implementation KL is computed with a $10^{-12}$ floor on $m_v$.  
  
#### B.2 Softmax Temperature Scaling  
  
For a vector $s \in \mathbb{R}^M$:  
  
$$  
\operatorname{softmax}(s/\tau)_j = \frac{\exp(s_j / \tau)}{\sum_{k=1}^{M} \exp(s_k / \tau)}  
$$  
  
- As $\tau \to 0^+$: distribution concentrates on $\arg\max_j s_j$ (hard argmax).  
- As $\tau \to \infty$: distribution approaches uniform ($1/M$ for all $j$).  
- $\tau = 0.1$ produces near-peaked distributions appropriate for identifying  
 dominant patches; $\tau = 10$ approximates a flat prior.  
  
The pipeline uses $\tau = 0.1$ as the default for state entropy and causal concept  
profiles; Track B also evaluates $\tau \in \{1.0, 10.0\}$ for robustness.  
  
#### B.3 Shannon Entropy  
  
For a distribution $\pi \in \Delta^{M-1}$:  
  
$$  
H(\pi) = -\sum_{j=1}^{M} \pi_j \log(\pi_j + \epsilon), \quad \epsilon = 10^{-12}  
$$  
  
Maximum entropy for $M = 576$ patches: $H_{\max} = \ln 576 \approx 6.36$ nats.   
For `state_delta_entropy_tau01`, the delta row $\Delta_t$ is passed through  
$\operatorname{softmax}(\cdot/0.1)$ before entropy computation, so values near $H_{\max}$  
indicate diffuse (uniform) sensitivity and values near 0 indicate a single  
dominant patch.  
  
#### B.4 Robust Z-Score  
  
$$  
z^{\text{rz}}(x) = \operatorname{clip}\\!\left(\frac{x - \operatorname{median}(\mathbf{x})}{1.4826 \cdot \mathrm{MAD}(\mathbf{x})},\;-10,\;10\right)  
$$  
  
The factor $1.4826$ is the consistency constant for normally distributed data  
($1 / \Phi^{-1}(0.75) \approx 1.4826$), making $1.4826 \cdot \mathrm{MAD} \to \hat{\sigma}$  
under normality. The clip to $\pm 10$ prevents extreme outliers (GPU saturation  
artifacts, pathological prompts) from dominating downstream analysis.  
  
#### B.5 Cosine Similarity Matrix  
  
For matrices $A \in \mathbb{R}^{m \times d}$ and $B \in \mathbb{R}^{n \times d}$:  
  
$$  
\operatorname{CosMat}(A, B)_{i,j} = \frac{A_i \cdot B_j}{\|A_i\|_2 \, \|B_j\|_2}  
$$  
  
Computed as $\hat{A}\hat{B}^\top$ where $\hat{A} = A / \|A\|_2$ row-wise. This is  
numerically stable for the Layer-32 space (norms $\approx 80$–$130$) but ill-conditioned  
if accidentally applied to mixed-space vectors (e.g. projector output norms $\approx 16$–$60$  
vs. Layer-32 norms $\approx 80$–$130$).  
  
---  
  
### C. Calibration Thresholds and Decision Quadrants  
  
#### C.1 Decision Grounding Quadrants  
  
The quadrant classifier (§6.6) partitions the $( \Delta p_t,\, \mathrm{JSD}_t )$ plane:  
  
| Quadrant | $\Delta p_t$ condition | $\mathrm{JSD}_t$ condition | Interpretation |  
|---|---|---|---|  
| Q1 | $> 0$ | $\geq$ median JSD | Image raises probability; broad vocabulary shift |  
| Q2 | $\leq 0$ | $\geq$ median JSD | Image suppresses probability; broad shift |  
| Q3 | $> 0$ | $\<$ median JSD | Image raises probability; local shift |  
| Q4 | $\leq 0$ | $\<$ median JSD | Image suppresses probability; local shift |  
  
Median JSD is computed across the candidate pool (top-$k$ union) for the current  
sample. Q1 tokens are the most strongly image-grounded among generated content.  
  
#### C.2 Causal Specificity Threshold  
  
A causal attribution is considered **specific** when:  
  
$$  
\gamma = \Delta\ell^\text{cf} - \bar{\Delta\ell}^\text{rand} > 0  
$$  
  
where $\bar{\Delta\ell}^\text{rand}$ is the mean log-probability drop over $K$ random  
ablations of the same mask size $|\Omega|$. A negative specificity margin indicates  
the observed drop is no larger than chance-level ablation damage and the attribution  
should be treated with caution.  
  
#### C.3 State Grounding Signal Ranges (LLaVA-1.5-7B reference)  
  
| Metric | Typical range (COCO val) | Higher value means |  
|---|---|---|  
| `state_delta_var` | $[0.001, 0.08]$ | More patch-localized sensitivity |  
| `state_delta_mean` | $[-0.02, 0.12]$ | Stronger average representation shift |  
| `state_delta_entropy_tau01` | $[0.0, 3.5]$ nats | More diffuse patch sensitivity |  
| `decision_delta_p` | $[-0.4, 0.6]$ | More probability mass added by image |  
| `causal_delta_logp` | $[-5.0, 8.0]$ | Stronger causal patch influence |  
| `causal_rel_drop` | $[-100, 100]$ | Relative log-prob change on ablation |  
  
---  
  
### D. Reproducibility Checklist  
  
Below is the minimum set of conditions required to reproduce a pipeline run.  
  
**Model configuration**  
-  `model.model_id` fixed to `llava-hf/llava-1.5-7b-hf`  
-  `model.quantize` fixed (4bit recommended)  
-  `model.device` set to a CUDA device  
  
**Null image**  
-  `null.strategy = dataset_mean_patch`  
-  Pre-computed mean-patch file path recorded in run metadata  
  
**Extraction**  
-  `extraction.prompt` fixed to the target prompt string  
-  `extraction.decoding = greedy`  
-  `patches_l32.pt` extracted via `extract_l32_patches()` (Layer-32, not projector output)  
  
**Grounding configuration**  
-  `grounding.decision.tau` list recorded (default: `[0.1, 1.0, 10.0]`)  
-  `grounding.decision.top_k` recorded (default: 10)  
-  `grounding.causal.alpha` recorded (default: 0.90)  
-  `grounding.causal.k_min` recorded (default: 12)  
-  `grounding.causal.n_random_controls` recorded  
  
**Software versions**  
-  PyTorch version, `transformers` version, `bitsandbytes` version logged  
-  CUDA driver version and GPU SKU logged  
-  Python version logged  
  
**Output artifacts**  
-  `grounding_scores.csv` (state) present per sample  
-  `decision_matrix.csv` + `decision_per_token.csv` present per sample  
-  `causal_result.csv` + `causal_per_token.csv` present per sample  
-  `results/token_intrinsic_extended.parquet` built via `build_intrinsic_token_extended.py`  
-  Normalized table built via `normalize_token_compact.py`  
