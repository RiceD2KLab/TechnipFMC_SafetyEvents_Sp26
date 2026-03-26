# Documentation Index

Navigation hub for all project documentation.

---

## Core References

| Document | Purpose |
|----------|---------|
| [Schema Contract v1](schema_contract_v1.md) | v1 schema: 7 entity types, 6 relation types |
| [Schema v2 Definitions](../kg_schema/README.md) | v2 schema: 7 L1 entity types, 7 L1 relation types, 4 L2 relation types (CAUSAL/PRECEDED_BY/FAILED_CONTROL/MITIGATED_BY), 9 L2 entity types |
| [Schema Validation Evidence](../eda/v2_design/schema_validation/schema_validation_evidence.md) | Empirical data report justifying each v1→v2 change (8 analyses, 23K records) |
| [Relation Labeling Rules](relation_labeling_rules.md) | CAUSED_BY / RESULTED_IN / NO_RELATION labeling constitution |
| [Gold Slice Spec](gold_slice_spec.md) | 200-incident benchmark specification |
| [Preflight Gate](preflight_gate.md) | GO/NO-GO extraction quality gates |

## Pipeline Operations

| Document | Purpose |
|----------|---------|
| [V2 Pipeline (`pipeline/`)](../pipeline/run_gliner_pipeline.py) | Self-contained v2 schema pipeline: GLiNER extraction → metadata parsing → graph assembly → Gate 1 evaluation |
| [ER Prep (`pipeline/er_prep/`)](../pipeline/er_prep/run_er_prep.py) | Pre-ER cleanup analysis: garbage filter, multi-type resolution, merge candidates, Splink configs |
| [Splink ER Runner (`pipeline/er_prep/run_splink.py`)](../pipeline/er_prep/run_splink.py) | Per-type Splink probabilistic ER: EM training, F0.5 threshold calibration, 647 merge decisions |
| [Splink ER Decision Record](splink_er_decision.md) | Design decisions, iteration history, results, and integration path for Splink probabilistic ER |
| [ER Execution (`pipeline/er_execution/`)](../pipeline/er_execution/run_er_execution.py) | Full ER pipeline: deterministic normalization, similarity merge, graph rebuild, Gate 2 evaluation |
| [Schema Violation Fix](../pipeline/er_execution/fix_schema_violations.py) | Post-ER relation type alignment: fixes mismatched edge types after multi-type resolution |
| [Location Dedup Diagnostic](../pipeline/er_execution/location_dedup_diagnostic.py) | Post-ER exact-match location entity merge: 87 merged, 43 orphans removed, 459 edges redirected |
| [Data Processing Pipeline](data_processing_pipeline.md) | How raw CSVs become GraphRAG/GLiNER input: load, merge, text-map, known data quality gaps |
| [Operational Runbook](operational_runbook.md) | End-to-end pipeline operations: incremental processing, backfill, 30k working-set CLI commands, confidence routing, fail-fast rules |

## Layer 2: Causal Enrichment

| Document | Purpose |
|----------|---------|
| [L2 Enrichment Runner](../pipeline/enrichment/run_l2_enrichment.py) | Main runner: Ollama LLM → causal edge extraction → validation → JSONL output. Flags: `--mock`, `--ground-truth`, `--prompt-variant` |
| [Causal Prompts](../pipeline/enrichment/prompts.py) | 3 system prompt variants (full/minimal/cot), CAUSAL direction rule, JSON schema |
| [L2 Merge](../pipeline/enrichment/merge_l2_edges.py) | Merge L2 JSONL edges into L1 graph: entity resolution, dedup, layer tagging |
| [L2 Stats](../pipeline/enrichment/compute_l2_stats.py) | Compute and report L2 production run statistics |
| [Ollama Client](../pipeline/enrichment/ollama_client.py) | Pure `urllib.request` Ollama client with retries and grammar-constrained decoding |
| [vLLM Client](../pipeline/enrichment/vllm_client.py) | OpenAI-compatible vLLM client with structured output (guided JSON), drop-in replacement for Ollama client |
| [Edge Validator](../pipeline/enrichment/validate.py) | Hard-gate validation: entity grounding, evidence substring, relation/type checks |
| [Gate 3 Metrics](../pipeline/evaluation/gate3_metrics.py) | Honest precision, optimal bipartite matching, TF-IDF cosine similarity, chain-compression credit, `--sweep` threshold sensitivity |
| [Cohen's Kappa](../pipeline/evaluation/compute_kappa.py) | Inter-annotator agreement (CSV + JSONL modes, high-prevalence detection) |
| [Relation Entropy](../pipeline/evaluation/relation_entropy.py) | Shannon entropy over edge types with optional baseline comparison for run-to-run tracking |
| [L2 Production Stats](l2_production_stats.md) | qwen3:30b-a3b v1 run: 38,678 edges, 16,877 records, 0 errors |
| [L2 Review (2026-03-02)](l2_review_2026-03-02.md) | First L2 enrichment review |
| [L2 Review (2026-03-03)](l2_review_2026-03-03.md) | Gate 3 v1: PASS vs Codex GT (P@K 63.3%, recall 57.7%) |
| [L2 Review (2026-03-21)](l2_review_2026-03-21.md) | Gate 3 v2 overhaul + GT cleanup + v2 run results. Both GTs PASS (Codex P=60.6% R=72.8%, Claude P=53.3% R=63.2%) |
| [L2 SLURM Job (Ollama)](../cluster/submit_l2_enrichment.sbatch) | 4-shard GPU job: Ollama backend, per-shard ports, exclusive nodes |
| [L2 SLURM Job (vLLM)](../cluster/submit_l2_vllm.sbatch) | 4-shard GPU job: vLLM backend, GPTQ-Int4 quantized model, per-shard ports, exclusive nodes |

## Annotation & Evaluation

| Document | Purpose |
|----------|---------|
| [Annotation Template Generator](../pipeline/annotation/generate_annotation_set.py) | Generates 200-record stratified annotation set for Layer 2 causal extraction evaluation |
| [Annotation Template CSV](../pipeline/annotation/annotation_template.csv) | 200-record annotation template with metadata and entity context |
| [Annotation Guidelines](../pipeline/annotation/annotation_guidelines.md) | JSONL edge annotation instructions: CAUSAL/PRECEDED_BY/FAILED_CONTROL, 9 entity types |
| [Worked Examples](../pipeline/annotation/worked_examples.md) | 5 JSONL edge examples (simple, multi-factor, chain, no-causal, ambiguous) |
| [Annotation Summary](../pipeline/annotation/annotation_summary.md) | Selection statistics, Gate 3 thresholds, current results |
| [Selected Records](../pipeline/annotation/selected_records.csv) | 200 records with causal density scores and stratum labels |
| [Claude GT](../pipeline/annotation/l2_gt_v2_claude.jsonl) | 414 ground truth edges after cleanup (481 original — 29 dead records + systematic annotation errors removed 2026-03-21) |
| [Codex GT](../pipeline/annotation/l2_gt_v2_codex.jsonl) | 374 ground truth edges after cleanup (431 original — 27 dead records + systematic annotation errors removed 2026-03-21) |
| [Postprocess Annotations](../pipeline/annotation/postprocess_annotations.py) | Evidence re-anchoring and chain dedup for CSV annotations |

## Open Issues

| Document | Purpose |
|----------|---------|
| [INCIDENT Type Leak](data_issue_incident_type_leak.md) | 5,449 unlabeled INCIDENT records in GraphRAG input — root cause, impact, resolution options |

## Extensions

| Document | Purpose |
|----------|---------|
| [Overlay Proposal](overlay_proposal.md) | v1.1 barrier/control overlay specification |
| [Assessment Addendum: Working-Set vs Production GO](assessment_addendum_working_set_vs_production_go.md) | Criteria for Working-Set deployment vs Production GO |
| [Ablation Decision Framework](ablation_decision_framework.md) | Ablation variant comparison: classifier vs enrichment LLM vs combined |
| [GLiNER Integration Guide](gliner_integration_guide.md) | GLiNER extraction setup and usage guide |

## Deployment Status

| Document | Purpose |
|----------|---------|
| [Deployment Alignment Report (2026-02-13)](deployment_alignment_report_2026-02-13.md) | Latest deployment alignment audit |

## Submodule Documentation

| Document | Purpose |
|----------|---------|
| [cluster/README.md](../cluster/README.md) | Cluster execution toolkit: launchers, SLURM wrappers, variant hooks |
| [cluster/PRODUCTION_DECISIONS.md](../cluster/PRODUCTION_DECISIONS.md) | Production decision freeze and policy gates |
| [evaluation/README.md](../evaluation/README.md) | Graph evaluation methods and runner |
| [incident-embedding-analysis/README.md](../incident-embedding-analysis/README.md) | Incident embedding pipeline |
| [translator/README.md](../translator/README.md) | CSV translation pipeline |

## Benchmarks

| Document | Purpose |
|----------|---------|
| [Benchmark Results](../pipeline/benchmark/benchmark_results.md) | 52-query benchmark on L1+L2 merged graph. **49/52 pass, 3 warn (EXTRACTION_GAP), 0 fail** |
| [Benchmark Snapshot](../pipeline/benchmark/benchmark_snapshot.json) | Per-query coverage/diagnosis snapshot for regression diffing |
| [ER Final Comparison](../pipeline/docs/er_final_comparison.md) | Three-column pre/post-ER comparison: topology, entity compression, query improvements, remaining blockers |
| [Benchmark Runner](../pipeline/benchmark/run_benchmark.py) | CSV-driven benchmark: loads graph, runs 52 queries, generates report with regression diff |

## Generated Output Artifacts

| Document | Purpose |
|----------|---------|
| [pipeline/outputs/metrics_report.md](../pipeline/outputs/metrics_report.md) | V2 pipeline Gate 1 metrics report (latest run) |
| [ER Prep Summary](../pipeline/docs/er_prep_summary.md) | ER prep analysis: garbage entities, multi-type conflicts, merge candidates, Splink readiness |
| [Schema Validation Evidence](../eda/v2_design/schema_validation/schema_validation_evidence.md) | 478-line empirical evidence report for v2 schema decisions |
| [Schema Validation Script](../eda/v2_design/schema_validation/schema_validation_analysis.py) | Reproducible analysis script for the evidence report |
| [Ablation Scorecard](../eda/v2_design/ablation/ablation_scorecard.md) | Machine-generated ablation scorecard |

## Historical / Archive

| Document | Why Archived |
|----------|-------------|
| [Spring 2026 Strategic Assessment](archive/spring2026_strategic_assessment.md) | Historical 1600-line audit; overlaps with active docs |
| [Handoff Summary (2026-01-28)](archive/handoff_summary_2026-01-28.md) | Time-stamped handoff; superseded by deployment report |
| [Weekend Accelerated Plan](archive/weekend_accelerated_plan.md) | Stale sprint timeline; durable content in operational_runbook |
