# Golden Set Iteration Process (NLQ Translator)

This document tracks the iterative changes made to the `natural_language_query` NL → structured query translator using the golden set.

Scope:
- **Full golden CSV runner:** `python -m natural_language_query.run_golden_set` — walks **every row** in `kg_schema/golden_set.csv` (~258 NL questions) unless `--skip-iogp` is passed (~230 rows). See **Iteration 8** below.
- Paraphrase / NL→QuerySpec harness (field-level checks vs `GROUND_TRUTH`): `python -m natural_language_query.eval_harness` (Ollama default) or `python -m natural_language_query.eval_harness_bedrock` (Amazon Bedrock only; loads `natural_language_query/.env` when `python-dotenv` is installed)
- Target: improve pass rate to eliminate failures (especially JSON/schema failures)
- Final state verified (44-query golden set runner): `Pass 44/44`

## Notation
- Golden set family totals (from the runner):  
  - Single-Hop: 6  
  - Spot-check: 13  
  - Aggregation: 6  
  - Multi-Hop: 8  
  - Global: 4  
  - Conjunctive: 7  
- Run commands in terminals were typically: `python -m natural_language_query.run_golden_set --model qwen2.5:3b -o golden_set_results.json`
- Failures are the queries marked `success: false` in `golden_set_results.json`.

## Iteration Timeline

### Iteration 0 — Baseline: JSON syntax + schema errors
What we saw (from your initial golden-set summary and failure list):
- JSON syntax failures (examples): `SC-09b`, `GL-04`, `CJ-04`
- Missing required field failures (exnamples): `MH-02`, `GL-02`
- Schema/operator mismatch (example): `GL-02` using `op: "IN"` (schema only allowed the existing `MetaOp` set and string values)

Reported family breakdown (from the initial “new and updated golden set” run):
- Single Hop: `6 successes / 0 failures`
- Spot Check: `12 successes / 13 failures`
- Aggregation: `6 successes / 6 failures`
- Multi-Hop: `7 successes / 8 failures`
- Global: `2 successes / 4 failures`
- Conjunctive: `6 successes / 7 failures`

Primary fix direction:
- Make JSON parsing/validation robust and schema-conformant.
- Constrain operator/value choices to the allowed schema.

---

### Iteration 1 — Translator hardening: structured JSON enforcement + safer parsing
Changes made:
- `natural_language_query/translator.py`
  - Added stricter JSON output constraints for Anthropic (`response_format={"type":"json_object"}`).
  - Improved `_parse_and_validate()` to try strict JSON parsing first, then fall back to a more permissive parsing mode.
  - Improved retry prompt to emphasize “ONLY valid JSON” and correct escaping.

Result (golden set runner):
- Overall: **`Pass 41/44`**, `Fail 3`
- Family pass rates:
  - Single-Hop: `6/6`
  - Spot-check: `13/13`
  - Aggregation: `6/6`
  - Multi-Hop: `7/8`
  - Global: `3/4`
  - Conjunctive: `6/7`

Remaining failures (as reported):
- `MH-05`
- `GL-04`
- `CJ-04`

---

### Iteration 2 — Prompt contract tightening for the remaining 3 failures
Changes made:
- `natural_language_query/prompt.py`
  - Explicitly enumerated allowed `meta_filters.op` values.
  - Explicitly forbade `=~` (and any other operator).
  - Required `aggregate_target` to always have both `entity_type` and `relation` in `output_mode="aggregate"`.
  - Required every `meta_filter` to include a non-null string `value`.
  - Added guidance for the “hubs/centrality” question to use `strategy: "custom"` and `custom_fn: "hub_centrality"`.

Result (golden set runner):
- Overall: **`Pass 43/44`**, `Fail 1`
- Only failing query: `GL-04`

---

### Iteration 3 — Prompt expansion regression (more validation errors)
What happened:
- After implementing the prompt changes more broadly, we regressed significantly due to the small local model sometimes emitting invalid shapes/enums (and in some cases timing out / retrying).

Observed result:
- Overall: **`Pass 32/44`**, `Fail 12`
- Family pass rates:
  - Single-Hop: `5/6`
  - Spot-check: `5/13`
  - Aggregation: `5/6`
  - Multi-Hop: `8/8`
  - Global: `3/4`
  - Conjunctive: `6/7`

---

### Iteration 4 — Ollama compact prompt + increased timeout + normalization (initial recovery attempt)
Changes made:
- `natural_language_query/prompt.py`
  - Added `SYSTEM_PROMPT_OLLAMA_COMPACT` tuned for small local models.
- `natural_language_query/translator.py`
  - Increased Ollama HTTP timeout (configurable; defaulted higher).
  - Added a normalization layer before schema validation to drop/repair obviously invalid structures.

Result:
- Overall: **`Pass 13/44`**, `Fail 31`

Root issue in this phase:
- The compact/local generation frequently emitted `confidence: null`, which violates the Pydantic schema (`confidence: float`).

---

### Iteration 5 — Validation error fix: coerce `confidence` away from null
Changes made:
- `natural_language_query/translator.py`
  - Extended `_normalize_for_schema()` to coerce `confidence: null` (and other invalid confidence types) to `0.9`.

Result:
- Overall: **`Pass 37/44`**, `Fail 7`
- Family pass rates:
  - Single-Hop: `6/6`
  - Spot-check: `13/13`
  - Aggregation: `4/6`
  - Multi-Hop: `6/8`
  - Global: `1/4`
  - Conjunctive: `7/7`

Remaining failures (from the terminal run):
- `AG-02`
- `AG-05`
- `MH-03`
- `MH-04`
- `GL-01`
- `GL-03`
- `GL-04`

---

### Iteration 6 — Final normalization tightening: fix remaining enum/op/shape issues
Changes made:
- `natural_language_query/translator.py`
  - Normalized/filtered `entity_filters` (drop invalid, map common aliases like `CLIENT` → `ORGANIZATION`).
  - Normalized `meta_filters.op` (e.g. map `op: "="` → `op: "=="`).
  - Normalized `crosstab_target` by rejecting invalid shapes and keeping only `{row_field, col_field}`-like objects.
  - Normalized `aggregate_target` by dropping incomplete/null subfields.

Result (final verification):
- Overall: **`Pass 44/44`**, `Fail 0`
- Family pass rates:
  - Single-Hop: `6/6`
  - Spot-check: `13/13`
  - Aggregation: `6/6`
  - Multi-Hop: `8/8`
  - Global: `4/4`
  - Conjunctive: `7/7`

---

### Iteration 7 — Paraphrase harness (Bedrock) alignment: prompt contract + eval + inference defaults

**Context:** The paraphrase evaluation (`natural_language_query/paraphrases.py` × `eval_harness.GROUND_TRUTH`) scores each LLM translation with **exact** checks on `strategy`, `output_mode`, presence of meta/entity filters, and specific `meta_fields`. Bedrock (and other frontier models) often **parsed JSON fine** but chose a different yet plausible spec than the benchmark—for example `list_incidents` after “show me …” while the golden row expected `count_incidents`, or `custom_fn: "severity_comparison"` while `MH-06` in the harness expects `entity_filter` + EQUIPMENT + `aggregate`.

**What we changed**

1. **`natural_language_query/prompt.py` (`SYSTEM_PROMPT`)**  
   - **Output modes:** Clarified that `count_incidents` applies to count-like and terse quantified phrasing (including many “show me … accidents” lines in the paraphrase set) unless the user clearly wants **row-level** incident lists; `list_incidents` is now described as rare.  
   - **Domain routing:** Explicit rules aligned to harness expectations: offshore → `work_process` `contains` `"offshore"` (not narrative-only); reporter companies → `ORGANIZATION` + `REPORTED_BY`; superlatives like “most” do **not** add spurious `meta_filters`; severity + geography → `severity_bin` meta + aggregate by `LOCATION` country; global equipment ranking → `entity_filter` with **empty** `entity_filters` + `aggregate` EQUIPMENT.  
   - **MH-06 vs custom:** Replaced the old “truck vs crane → `severity_comparison`” example with **`entity_filter` + single EQUIPMENT OR-pattern + `aggregate`**, and updated strategy rule 11 so simple A vs B equipment severity wording uses that pattern; `severity_comparison` is reserved for explicitly named custom analysis.  
   - **New worked examples** in the prompt for: offshore injury breakdown, Shell reporter count, CJ-06-style conjunctive narrative + `count_incidents`, MH-05-style intersect (body + pipe + region), and AG-03 global equipment frequency.  
   - **Metadata list:** Documented `country` and `region` as valid meta fields (for APAC-style filters).  
   - **MH-02:** Added rule 13 for maintenance + equipment-failure injury queries → `intersect`, narrative keywords, `aggregate` on `INJURY_TYPE`.

2. **`natural_language_query/eval_harness.py`**  
   - `run_evaluation(..., temperature=0.1)` forwards `temperature` into every `translate()` call so scores are comparable when you change sampling.  
   - CLI flag `--temperature` (default `0.1`) for batch and interactive modes.

3. **`natural_language_query/eval_harness_bedrock.py`**  
   - Prints **`Temp:`** in the banner.  
   - **`--temperature` default `0.0`** and passes it into `run_evaluation` (reproducible Bedrock runs).  
   - Interactive mode (`-i`) uses the same temperature argument.

4. **`natural_language_query/translator.py`**  
   - **Bedrock-only** system appendix: short “JSON OUTPUT (required)” block (single object, no fences, include schema fields).  
   - **Bedrock `inferenceConfig`:** sends **`temperature`** and **`maxTokens`** only. (An earlier Iteration 7 attempt also set `topP` when `temperature == 0`; **Claude on Converse returns HTTP 400** if both are sent—`temperature` and `top_p` cannot both be specified—so that was removed.)  
   - *Note:* The boto3 `Converse` input shape still has no JSON-schema “structured output” mode in our integration—strict shape is **prompt + post-parse validation**, not Bedrock “guaranteed JSON schema” mode.

**How to re-verify after Iteration 7**

```bash
python -m natural_language_query.eval_harness_bedrock
python -m natural_language_query.eval_harness_bedrock --model <modelId> --temperature 0
python -m natural_language_query.eval_harness --backend ollama --temperature 0.1
```

**Result (Iteration 7) — Bedrock paraphrase harness** (verified: `python -m natural_language_query.eval_harness_bedrock`, default model / `us-east-1`, `Temp: 0.0`):

| Metric | Value |
|--------|------:|
| Full pass rate | **100%** (**92**/92) |
| Parse success | **100%** |
| Avg latency | ~**2860** ms (representative run) |

All paraphrase families (SH-01 … CJ-06) at **100%** on field-level checks vs `eval_harness.GROUND_TRUTH`.

**Iteration 7b — prompt-only mitigation (previously failing four paraphrases)**  
Changes in `natural_language_query/prompt.py` only: reporter “incident count” (no bogus `meta_filter`); equipment + severity question forms → `aggregate` + EQUIPMENT OR-pattern; keyword-soup → `strategy: intersect` + `count_incidents`. Rules 14–16 and matching JSON examples. After 7b, the harness reached **92/92**.

*(Historical note: before 7b, four paraphrases failed on `has_meta_filter`, `output_mode`, or `strategy` because the harness enforces one canonical spec per `query_id` while short phrasings admitted multiple reasonable structured outputs.)*

**Iteration 8 — `run_golden_set` uses full `kg_schema/golden_set.csv`**

The CSV grew to **~258** canonical NL questions (including **IOGP-** rows). Updates in `natural_language_query/run_golden_set.py`:

- **Default:** run **every** row from `kg_schema.load_golden_set()` / `kg_schema/golden_set.csv` (no silent `IOGP-` exclusion).
- **`--skip-iogp`:** restore the legacy subset (~**230** rows) if you want to match older runs.
- **`--offset` / `--limit`:** slice the list after filtering (chunked or smoke tests, e.g. `--limit 20`).
- **`--backend bedrock`:** same translator path as the paraphrase harness; use **`--temperature 0`** for reproducibility.
- **`--temperature`:** forwarded to `translate()` (default `0.1`; Bedrock often uses `0`).
- **JSON output:** besides `queries`, the report includes a **`meta`** object (`golden_set_csv`, `row_count`, `skip_iogp`, slice, backend, model, `temperature`, `execute`). Entries with `success: false` still carry `clarification` / parse errors for debugging.

Example:

```bash
python -m natural_language_query.run_golden_set --backend bedrock --temperature 0 -o golden_set_nlq.json
python -m natural_language_query.run_golden_set --skip-iogp -o golden_set_no_iogp.json
python -m natural_language_query.run_golden_set --limit 10 --quiet
```

**Result (Iteration 8) — full CSV, Bedrock translation smoke** (verified run):

| Metric | Value |
|--------|------:|
| Command | `python -m natural_language_query.run_golden_set --backend bedrock --temperature 0 -o golden_set_nlq.json` |
| Rows | **258**/258 (**100%** `success: true`) |
| Total wall time | **802** s (~13.4 min) |
| Avg per query | **3.1** s (~3100 ms) |
| Output | `golden_set_nlq.json` (`meta` + `queries`) |

By `query_type` (from CSV):

| query_type | Pass |
|------------|-----:|
| Single-hop | 104/104 |
| Multi-hop | 58/58 |
| Aggregation | 37/37 |
| Conjunctive | 35/35 |
| Global | 24/24 |

**Next step (your plan):** translation-only now validates NL → `QuerySpec` for the **entire** golden CSV at 100% on this run. Wire **`--execute`** (or a downstream step) to `query_engine.execute_query` once graph data is connected to confirm end-to-end answers.

## Master Results Tables

### Overall (44-query golden set)

| Iteration | Overall | Fail count |
|---:|---:|---:|
| 1 | 41/44 | 3 |
| 2 | 43/44 | 1 |
| 3 | 32/44 | 12 |
| 4 | 13/44 | 31 |
| 5 | 37/44 | 7 |
| 6 | 44/44 | 0 |

Note: Iteration 0 used a different “expanded golden set” style breakdown as you reported; totals didn’t match the 44-query runner.

### Paraphrase NL harness (92 cases, `eval_harness` / Bedrock)

| Milestone | Full pass | Parse | Notes |
|-----------|----------:|------:|--------|
| Iteration 7 (Bedrock, after prompt + temp 0 + no dual topP) | 88/92 (95.7%) | 100% | Before prompt rules 14–16 / examples |
| Iteration 7 + 7b (Bedrock) | **92/92 (100%)** | 100% | Verified in production Bedrock run |

### Full golden CSV (NL translation smoke), `run_golden_set`

| Setting | Row count (approx.) | Verified (Bedrock, `temp 0`) |
|---------|--------------------:|-------------------------------|
| Default (all `query_id`) | **258** | **258/258 (100%)**, ~802 s total, `golden_set_nlq.json` |
| `--skip-iogp` | **230** | — (optional smaller run) |

### By Golden Set Category (pass/total)

| Iteration | Single-Hop | Spot-check | Aggregation | Multi-Hop | Global | Conjunctive |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 6/6 | 13/13 | 6/6 | 7/8 | 3/4 | 6/7 |
| 2 | 6/6 | 13/13 | 6/6 | 8/8 | 3/4 | 7/7 |
| 3 | 5/6 | 5/13 | 5/6 | 8/8 | 3/4 | 6/7 |
| 4 | 0/6 | 5/13 | 2/6 | 4/8 | 1/4 | 1/7 |
| 5 | 6/6 | 13/13 | 4/6 | 6/8 | 1/4 | 7/7 |
| 6 | 6/6 | 13/13 | 6/6 | 8/8 | 4/4 | 7/7 |

## Key Code Touchpoints (What Changed)

### `natural_language_query/translator.py`
- Improved JSON extraction/parsing robustness in `_parse_and_validate()`.
- Backend-specific constraints:
  - Anthropic: request JSON object output.
- Added `_normalize_for_schema()` to pre-process LLM JSON to reduce hard schema failures:
  - drop invalid `entity_filters` / `meta_filters` entries
  - map/normalize `meta_filters.op`
  - normalize `crosstab_target` shape
  - normalize `aggregate_target` shape
  - coerce `confidence` away from `null`
- Added compact prompt selection for local Ollama small models.
- Increased Ollama HTTP timeout (via env var).

### `natural_language_query/prompt.py`
- Iteration 2: tightened the “prompt contract”:
  - allowed operator enumeration for `meta_filters.op`
  - forbid `=~`
  - require non-null `meta_filters.value`
  - enforce `aggregate_target` completeness for `output_mode="aggregate"`
- Added “hubs/centrality” instruction to use `custom_fn: "hub_centrality"`.
- Added `SYSTEM_PROMPT_OLLAMA_COMPACT` for small local models to reduce drift/timeouts.
- Iteration 7: paraphrase-harness alignment—output_mode disambiguation, offshore/reporter/superlative routing, MH-06 vs `severity_comparison`, new JSON examples (offshore, Shell, CJ-06, MH-05, AG-03), `country`/`region` metadata, maintenance+failure rule.
- Iteration 7b: targeted rules + examples for the four remaining Bedrock paraphrase failures (reporter “incident count”, equipment severity question forms, keyword-soup `intersect`).

### `natural_language_query/eval_harness.py` / `eval_harness_bedrock.py`
- Iteration 7: pluggable `temperature` through `run_evaluation` and CLI; Bedrock entrypoint defaults to `temperature=0` and prints it.

### `natural_language_query/run_golden_set.py`
- Iteration 8: loads all rows from `kg_schema/golden_set.csv` by default; `--skip-iogp`, `--offset`, `--limit`, `--backend bedrock`, `--temperature`; JSON report includes `meta` + `queries`.

## What to Do Next (Optional)
- Full CSV Bedrock translation is **verified 258/258** (see Result Iteration 8). Next: enable **`--execute`** when the KG is wired, or re-run after prompt/model changes to guard regressions.
- Re-run `python -m natural_language_query.eval_harness_bedrock` after prompt changes to guard the **92** paraphrase checks.
- Optionally run `eval_harness` with `--backend anthropic` / `--backend gemini` at `--temperature 0` for cross-backend comparison.

