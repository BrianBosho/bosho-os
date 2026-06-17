---
title: Experiment Protocol (Propagator Analysis)
type: experiment-protocol
source: google-drive
drive-id: 13dusgXpzxQnYrDnS2JphJ-aBdwjjzaiWeqvXMjMMkck
tags: [fedprop, experiments, protocol, operators]
project: tmlr_fedprop_paper
---

# Propagator Analysis — Experimental Protocol

# For use with IDE agent / codebase implementation

## 0. Context

This protocol generates the experiments for the paper: **"Intrinsic Evaluation of Propagation Operators for Communication-Free Subgraph Federated Learning"**

The codebase already implements FedProp with two operators (Adj, Diffusion). This protocol extends it with three new operators, adds intrinsic evaluation instrumentation, and defines the exact run matrix.

## 1. What Already Exists — Do Not Reimplement

| Component | Status | Notes |
|---|---|---|
| Normalized Adjacency propagator | DONE | FedProp-Adj |
| Diffusion / Taylor propagator | DONE | FedProp-Diff |
| IID/non-IID partitioning (β) | DONE | β = 10000, 10, 1 |
| GCN backbone | DONE | 2-layer, 16 hidden |
| GAT backbone | DONE | 2-layer, 8×8 heads |
| Cora, Citeseer, Pubmed datasets | DONE |   |
| OGBN-Arxiv dataset | DONE |   |
| Downstream accuracy logging | DONE | per-client + aggregate |
| FedAvg aggregation | DONE |   |

## 2. New Operators to Implement

Implement each as a standalone propagation function with the same interface as the existing Adj/Diffusion operators.

### 2.1 Interface Contract

Every propagator must accept:
- A : adjacency matrix (sparse, local client subgraph)
- X : feature matrix [n_nodes × n_features]
- boundary_mask : boolean mask, True = known boundary node
- X_boundary : known feature values for boundary nodes
- T_max : maximum iterations (default: 100)
- eps : convergence tolerance on feature change norm (default: 1e-4)

Every propagator must return:
- X_imputed : completed feature matrix [n_nodes × n_features]
- n_iters : number of iterations run
- residuals : list of per-iteration residual values (see Section 3)
- wall_time : total propagation time in seconds

### 2.2 Operators to Add

**Chebyshev (O4)**
- Approximate the heat kernel using Chebyshev polynomials of order K
- Parameter: K ∈ {3, 5, 10} — default K=5
- Apply boundary reset at each iteration as with existing operators
- Expected behaviour: faster convergence than Taylor on denser graphs

**APPNP / PPR (O6)**
- Update rule: X^(t+1) = (1−α) · Â · X^(t) + α · X^(0)
- Where Â is the normalized adjacency, X^(0) is the initialization
- Apply boundary reset after each update
- Parameter: α ∈ {0.05, 0.1, 0.2} — default α=0.1
- Note: fixed point is NOT the Dirichlet minimizer — it is a personalized PageRank solution.

**Random Walk (O2)**
- Propagation matrix: P = D^{-1} A  (asymmetric)
- Apply boundary reset at each iteration
- Note: asymmetric operator; fixed point differs from Adj. Include as comparison baseline, not as a Dirichlet solver.

**Heat Kernel Exact (O5) — Reference Only**
- Compute exp(−t·L) via eigendecomposition
- Run ONLY on Cora and Citeseer (small graphs — O(n^3) cost)
- Single-shot (no iteration); t = 1.0 default
- Use as a theoretical reference point, not a practical operator

## 3. Instrumentation to Add

### 3.1 Per-Iteration Logging (inside loop)

At each iteration t, record:
```
log[t] = {
  "iter": t,
  "dirichlet_residual": frob_norm(L @ X_t) ** 2,
  "feature_change_norm": frob_norm(X_t1 - X_t),
  "reconstruction_mse": mse(X_t[unknown_mask], X_true[unknown_mask])
      # only if X_true is available (intrinsic eval mode)
}
```

Store log as a list and return it as residuals.

### 3.2 Feature Reconstruction Evaluation (intrinsic mode)

Add an `intrinsic_eval` flag to the propagation call.

When `intrinsic_eval=True`:
- Accept `X_true` as an additional argument (ground truth features)
- At convergence, compute and return:

```
intrinsic_metrics = {
  "mse":              mean over unknown nodes of ||x*_i - x_true_i||^2,
  "cosine_sim":       mean cosine similarity over unknown nodes,
  "recovery_ratio":   (mse_zero_hop - mse_operator) / mse_zero_hop,
  "spectral_fidelity": frob_norm(cov(X_imputed) - cov(X_true))
}
```

### 3.3 Wall-Clock Timing

Wrap the propagation loop only (exclude graph construction and matrix precomputation).

## 4. Datasets

| Dataset | Scale | Homophily | Role | New? |
|---|---|---|---|---|
| Cora | Small | 0.81 | Primary | No |
| Citeseer | Small | 0.74 | Primary | No |
| Pubmed | Medium | 0.80 | Primary | No |
| OGBN-Arxiv | Large | 0.66 | Scaling | No |
| Texas | Small | 0.11 | Heterophilic test | Yes — add |
| Wisconsin | Small | 0.20 | Heterophilic test | Yes — add |

**Dropped:** Amazon Computers, Amazon Photos.

## 5. Run Matrix

### Layer 1+2+3 — Intrinsic / Process / Efficiency

- **Operators:** Adj, Diffusion, Chebyshev(K=5), APPNP(α=0.1), RW
- **Datasets:** Cora, Citeseer, Pubmed, OGBN-Arxiv, Texas, Wisconsin
- **Partitions:** β = 10000, β = 10, β = 1
- **Seeds:** 3 seeds
- **Hop depth:** L=1 (default); L=2 as ablation on Cora only

Heat kernel exact: Cora + Citeseer only, β = 10000 only, 1 seed.

**Total Layer 1–3 runs:** 5 × 6 × 3 × 3 = 270 runs  
Heat kernel: 2 × 1 = 2 runs  
L=2 ablation on Cora: 5 × 3 × 3 = 45 runs

### Layer 4 — Downstream Accuracy

- **Operators:** Adj, Diffusion, Chebyshev(K=5), APPNP(α=0.1), RW
- **Datasets:** Cora, Citeseer, Pubmed, OGBN-Arxiv
- **Partitions:** β = 10000, β = 1
- **Backbones:** GCN, GAT
- **Seeds:** 5 seeds

Also run Zero-hop and Oracle baselines.

**Total Layer 4 runs:** 5 × 4 × 2 × 2 × 5 = 400 runs  
Zero-hop: 4 × 2 × 2 × 5 = 80 runs  
Oracle: 3 × 2 × 2 × 5 = 60 runs

## 6. Ablations

| Ablation | Factor | Levels | Datasets | Seeds |
|---|---|---|---|---|
| K sensitivity | Chebyshev order | K = 3, 5, 10 | Pubmed | 3 |
| α sensitivity | APPNP α | 0.05, 0.1, 0.2 | Cora | 3 |
| ε sensitivity | Convergence tol. | 1e-2, 1e-3, 1e-4 | Cora, OGBN | 3 |
| L=2 topology | Hop depth | L=1, L=2 | Cora | 3 |

## 7. Output Format

File naming convention:
```
results/{layer}/{operator}/{dataset}/beta{beta}_seed{seed}.json
```

## 8. Priority Order

**Phase 1 — Implement and validate new operators (2–3 days)**
1. Implement Chebyshev propagator
2. Implement APPNP propagator
3. Implement Random Walk propagator
4. Validate each on Cora
5. Implement Heat Kernel exact on Cora only as a sanity check

**Phase 2 — Add instrumentation (1 day)**
1. Add per-iteration logging
2. Add intrinsic evaluation mode
3. Add wall-clock timing
4. Validate on Cora

**Phase 3 — Run Layer 1–3 (2–3 days)**
1. Run all operators on Cora first
2. Run full matrix: all operators × all datasets × all β
3. Texas and Wisconsin last

**Phase 4 — Run Layer 4 (3–5 days)**
1. Run zero-hop and oracle baselines first
2. Run Adj and Diffusion (already implemented)
3. Run Chebyshev, APPNP, RW downstream
4. GCN before GAT

**Phase 5 — Ablations (if time)** Run only if Phase 3 and Phase 4 are complete before June 1.

## 9. Fixed-Point Notes

| Operator | Fixed Point | Equals Dirichlet minimizer? |
|---|---|---|
| Normalized Adj (O1) | Harmonic extension of X_V | YES |
| Random Walk (O2) | Asymmetric smoothing | NO |
| Diffusion/Taylor (O3) | Harmonic extension (same as O1) | YES |
| Chebyshev (O4) | Heat kernel steady state | APPROXIMATELY |
| Heat Kernel exact (O5) | Exact heat kernel solution | APPROXIMATELY |
| APPNP/PPR (O6) | Personalized PageRank solution | NO |

## 10. Scope Freeze

The experiment matrix above is final. Do not add:
- Additional operators beyond the five primary + heat kernel
- Additional datasets beyond the six listed
- Additional backbone architectures
- Link prediction or graph classification tasks

Emergency rule: if Phase 3 is complete and Phase 4 is running but not finished by June 5, submit with Phase 3 results only.
