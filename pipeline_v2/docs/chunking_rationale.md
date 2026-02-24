# Subword-Aware Chunking Rationale

*Extracted from docs/preflight_gate.md — documents the implemented chunking strategy in `extraction/gliner_extract.py`.*

## The Problem

GLiNER's model window is 384 **subword** tokens (`urchade/gliner_medium-v2.1` uses a SentencePiece tokenizer). Without chunking, long narratives get silently truncated.

| Metric (full 23,311-record dataset) | Value |
|--------------------------------------|------:|
| Narratives exceeding 384 subword tokens | **1,143 (4.9%)** |
| Narratives exceeding 512 subword tokens | **482 (2.1%)** |
| Long narratives with tail-only entity keywords | **374 / 1,143 (32.7%)** |
| Estimated entity instances lost to truncation | **~588** |
| As % of all narratives | **1.6%** |

The missed entities come from detailed English investigation reports where root cause equipment, secondary injuries, and corrective action details appear late in the narrative. These are typically the highest-severity incidents.

## Why Whitespace Chunking Failed

An initial implementation chunked by whitespace tokens (350 words per chunk). This failed: non-ASCII text (Portuguese, Norwegian) expands heavily under subword tokenization. A 350-word Portuguese chunk can produce 663 subword tokens (1.9x expansion), still triggering truncation.

| Language pattern | Subword/whitespace ratio |
|-----------------|:------------------------:|
| English (mean) | 1.15x |
| English (P95) | 1.35x |
| Portuguese/bilingual (worst) | **2.16x** |

## The Fix — Subword-Aware Chunking

The production implementation uses GLiNER's own SentencePiece tokenizer to count subword tokens per word, then greedily fills each chunk up to the 350-subword-token budget. This guarantees every chunk fits within the model window regardless of language.

| Parameter | Value | Rationale |
|-----------|------:|-----------|
| `CHUNK_MAX_TOKENS` | 350 | Leaves 34-token headroom for special tokens and label encoding |
| `CHUNK_OVERLAP` | 50 | Catches entities that span chunk boundaries |

## Verified Results (1,000-incident test set)

| Metric | No chunking | Whitespace chunking | Subword chunking |
|--------|:----------:|:-------------------:|:----------------:|
| Truncation warnings | many | 75 | **0** |
| Max subword tokens/chunk | >600 | 663 | **350** |
| Multi-chunk narratives | 0 | 26 | **88** |
| Total chunks | 1,000 | 1,026 | **1,108** |
| Unique entity nodes | 4,328 | 4,396 | **4,507** |
| Edges | 9,988 | 10,091 | **10,261** |
| Gate 1 | PASS | PASS | **PASS** |

**Deduplication:** Entities extracted from overlapping chunks are deduplicated by `(span.strip().upper(), type)`, keeping the highest confidence score.

## Language Composition

| Category | Count | >384 subword tokens | Notes |
|----------|------:|:-------------------:|-------|
| English-only | 22,821 (97.9%) | ~1,076 | Chunked correctly |
| Bilingual EN+PT | 535 (2.3%) | ~67 | Heavily expanded by subword tokenizer; chunking critical |
| Norwegian | 88 (0.4%) | ~0 | Mostly short; GLiNER produces garbage (e.g. "pallen" -> BODY_PART) |
| Other non-English | 109 (0.5%) | ~0 | Very short (median 12 tokens) |

## Remaining Gap

The ~88 Norwegian and ~109 other non-English narratives produce low-quality GLiNER output regardless of chunking. The translator pipeline (`translator/csv_translator_m2m100_gpu.py`) exists but is not wired in. Low priority (0.8% of data).
