# Ablation Scorecard

- Winner: **None (no variant passed gates)**

| Variant | Pass Gates | Score | Rel Prec | Rel Rec | Ret P@5 | Ret R@5 | Runtime (h) | Cost ($) | Overmerge | Gate Reasons |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| GLiNER+Splink baseline | False | 0.00 | - | - | - | - | - | 0.00 | - | missing:relation_precision;missing:relation_recall;missing:retrieval_precision_at5;missing:retrieval_recall_at5;missing:avg_degree;missing:components_reduction_pct;missing:total_runtime_hours;missing:overmerge_rate;missing:max_cluster_size |
| Baseline+Classifier | False | 0.00 | - | - | - | - | - | - | - | missing:relation_precision;missing:relation_recall;missing:retrieval_precision_at5;missing:retrieval_recall_at5;missing:avg_degree;missing:components_reduction_pct;missing:total_runtime_hours;missing:estimated_cost_usd;missing:overmerge_rate;missing:max_cluster_size |
| Baseline+Enrichment LLM | False | 0.00 | - | - | - | - | - | - | - | missing:relation_precision;missing:relation_recall;missing:retrieval_precision_at5;missing:retrieval_recall_at5;missing:avg_degree;missing:components_reduction_pct;missing:evidence_coverage;missing:json_validity;missing:total_runtime_hours;missing:estimated_cost_usd;missing:overmerge_rate;missing:max_cluster_size |
| Baseline+Classifier+Enrichment LLM | False | 0.00 | - | - | - | - | - | - | - | missing:relation_precision;missing:relation_recall;missing:retrieval_precision_at5;missing:retrieval_recall_at5;missing:avg_degree;missing:components_reduction_pct;missing:evidence_coverage;missing:json_validity;missing:total_runtime_hours;missing:estimated_cost_usd;missing:overmerge_rate;missing:max_cluster_size |

## Notes
- `weighted_score` is only meaningful among gate-passing variants.
- Any gate failure should be treated as production risk, even if some metrics are strong.