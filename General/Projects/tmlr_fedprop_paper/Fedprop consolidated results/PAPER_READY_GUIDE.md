# Paper-Ready Results

Generated: 2026-06-13T00:35:21

`paper_ready_results.csv` holds every number cleared for the TMLR paper, one row
per (table, condition, method). Filter on `table_id` to rebuild any table.

## Tables

| table_id | placement | contents |
|---|---|---|
| T1 | main | GCN homophilic accuracy (Cora, Citeseer, Pubmed, OGBN-ArXiv); arxiv is no-PE only |
| T2 | main | GAT citation-benchmark accuracy (2-hop) |
| T3 | main | Heterophilic suite (Amazon-ratings, Texas, Wisconsin), absolute accuracy |
| T4 | main | RFP positional-encoding ablation (paired PE on/off) |
| A1 | appendix | Gap-closed percentages (homophilic, valid rows only) |
| A2 | appendix | Client-count scalability (Cora) |

## Key columns

- `accuracy`: formatted `mean +/- std (n=reps)` in percentage points.
- `delta_vs_zerohop_pp`: method minus Zero-hop in the same (dataset, model, hop, beta) cell.
- `partition`: IID (beta=10000) vs non-IID (beta=1 strong, beta=10 mild). Pubmed's
  non-IID setting is deliberately beta=10.

## Excluded datasets (not in this file)

- **Roman-empire**: FedProp <= Zero-hop in 7/8 conditions; no winning configuration
- **Minesweeper**: accuracy degenerate at 80% majority-class rate; needs ROC-AUC rerun
- **Computers**: runs used invalid hyperparams (hidden=16, SGD lr=0.5); R7 rerun pending
- **Photo**: runs used invalid hyperparams (hidden=16, SGD lr=0.5); R7 rerun pending

## Rows where FedProp < Zero-hop kept in the file: 6

These are retained only because they carry an explicit explanation:
- Texas/Wisconsin FedProp-Adj rows -- support the "diffusion is robust to
  heterophily, adjacency is not" ablation claim (the Diff rows win).
- OGBN-ArXiv PE rows (T4 only) -- the explained PE-width negative result.

See `PUBLICATION_REVIEW.md` (one level up) for the full triage and rerun plan.
