# NL Query Interface for Safety KG

Translates natural language questions → structured QuerySpec → executes against the existing benchmark query engine. Zero new dependencies beyond `pydantic` and `requests`.

**Requirements:** Python 3.9+ (current `pydantic` and pip do not support 3.8). On Windows with multiple Pythons, use the py launcher: `py -3.12 -m venv .venv` so the venv uses 3.12.

## Setup

```bash
# Use Python 3.9+ for the venv (Windows: py -3.12 -m venv .venv)
python -m venv .venv
source .venv/bin/activate   # or on Windows: .\.venv\Scripts\Activate.ps1

# Install deps
pip install pydantic requests

# Make sure Ollama is running with a model
ollama pull qwen3:8b        # or qwen3.5:latest when available
ollama serve                 # if not already running
```

## Quick Test

```bash
# Interactive mode — type questions, see translations
python -m natural_language_query.eval_harness -i

# Run full eval against Ollama
python -m natural_language_query.eval_harness --backend ollama --model qwen3:8b

# Run against Anthropic API
ANTHROPIC_API_KEY=sk-... python -m natural_language_query.eval_harness --backend anthropic

# Save results
python -m natural_language_query.eval_harness -o eval_results.json
```

## Integration with Existing Pipeline

```python
from natural_language_query.translator import translate
from query_engine import QuerySpec, execute_query

# Step 1: Translate NL → QuerySpec
result = translate("How many forklift incidents in 2022?")

if result["query_spec"] is None:
    print(f"Failed: {result['clarification']}")
else:
    # Step 2: Create QuerySpec from dict
    spec = QuerySpec(**result["query_spec"])

    # Step 3: Execute against graph (same as benchmark runner)
    output = execute_query(spec, G, entities_df, relations_df, metadata_df)
    print(output["result_summary"])
```

## Streamlit Dashboard Integration

```python
# In your existing Streamlit app:
from natural_language_query.streamlit_widget import render_nl_query_widget

# Add this wherever you want the NL interface
render_nl_query_widget(G, entities_df, relations_df, metadata_df)

# Or test standalone:
# streamlit run natural_language_query/streamlit_widget.py
```

## Golden Set (Dashboard query coverage)

The golden set (~258 queries) is defined in `kg_schema/golden_set.csv`. The NLQ
runner walks **every CSV row** by default. Use `--skip-iogp` to exclude `IOGP-*`
rows (~230 queries) for a smaller run.

```bash
# Translation only — all rows
python -m natural_language_query.run_golden_set

# Smoke test (first 20 rows)
python -m natural_language_query.run_golden_set --limit 20

# Bedrock, reproducible temperature
python -m natural_language_query.run_golden_set --backend bedrock --temperature 0 -o golden_set_results.json

# Save detailed results (JSON has `meta` + `queries`)
python -m natural_language_query.run_golden_set -o golden_set_results.json

# Execute each translated query against the pipeline graph (if data is present)
python -m natural_language_query.run_golden_set --execute -o results.json
```

Exit code is 0 if every query translated successfully, 1 otherwise.

## File Structure

```
natural_language_query/
├── schema.py             # Pydantic models + QuerySpec bridge
├── prompt.py             # System prompt (the core artifact)
├── translator.py         # LLM call + validation + retry
├── eval_harness.py       # Evaluation against benchmark ground truth
├── paraphrases.py        # Test set: 6-10 phrasings per query
├── run_golden_set.py     # Run translator on golden set (reads from kg_schema/golden_set.csv)
├── streamlit_widget.py   # Drop-in Streamlit component
└── README.md             # This file
```

## Swapping Backends

The translator currently supports three backends:

| Backend | Dev/Test | Production | Cost |
|---------|----------|------------|------|
| `ollama` | ✅ local | depends on host resources | $0 |
| `anthropic` | ✅ | ✅ | API cost |
| `gemini` | ✅ | ✅ | API cost |

```python
# Local dev
result = translate(query, backend="ollama", model="qwen3:8b")

# Production API
result = translate(query, backend="anthropic", model="claude-sonnet-4-5-20250514")

# Gemini API
result = translate(query, backend="gemini", model="gemini-2.5-flash")
```

## Evaluation Metrics

The harness checks per-field accuracy against benchmark ground truth:
- **strategy**: correct execution strategy selected
- **entity_types**: correct entity types identified
- **entity_pattern**: regex pattern captures the right entities
- **meta_fields**: correct metadata fields used
- **output_mode**: correct output format selected
- **agg_entity_type**: correct aggregation target

Target: ≥90% full-pass rate across all paraphrases.

## Prompt Tuning

The system prompt in `prompt.py` is the entire product. To tune:

1. Run eval: `python -m natural_language_query.eval_harness -o before.json`
2. Edit `prompt.py` (add examples, clarify rules)
3. Re-run eval: `python -m natural_language_query.eval_harness -o after.json`
4. Compare pass rates

Most failures will be in entity pattern generation (synonyms) and
strategy selection (entity_filter vs intersect). Fix by adding examples
to the prompt for the specific failure mode.
