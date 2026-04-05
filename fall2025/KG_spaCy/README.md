# KG_spaCy — Fall 2025 Rule-Based Extraction

Archived Fall 2025 implementation using spaCy dependency parsing with
Subject-Verb-Object (SVO) rules for entity and relation extraction.

This approach was the fastest (15 min / 30K records) and achieved the
highest Unique Entity Rate (0.960), but could only recover direct
syntactic relations — no semantic or causal edges. Superseded by the
Spring 2026 two-layer pipeline (`pipeline/`).

## Files

| File | Purpose |
|------|---------|
| `KG_test.py` | SVO extraction and graph construction |
| `triple_clean.py` | Post-processing and deduplication of extracted triples |
