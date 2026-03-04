# NL Query Interface for Safety KG

Translates natural language questions → structured QuerySpec → executes against the existing benchmark query engine. Zero new dependencies beyond `pydantic` and `requests`.

## Setup

```bash
# Install deps (you probably have these already)
pip install pydantic requests

# Make sure Ollama is running with a model
ollama pull qwen3:8b        # or qwen3.5:latest when available
ollama serve                 # if not already running
```

## Quick Test

```bash
# Interactive mode — type questions, see translations
python -m nl_query.eval_harness -i

# Run full eval against Ollama
python -m nl_query.eval_harness --backend ollama --model qwen3:8b

# Run against Anthropic API
ANTHROPIC_API_KEY=sk-... python -m nl_query.eval_harness --backend anthropic

# Save results
python -m nl_query.eval_harness -o eval_results.json
```

## Integration with Existing Pipeline

```python
from nl_query.translator import translate
from benchmark.query_engine import QuerySpec, execute_query

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
from nl_query.streamlit_widget import render_nl_query_widget

# Add this wherever you want the NL interface
render_nl_query_widget(G, entities_df, relations_df, metadata_df)

# Or test standalone:
# streamlit run nl_query/streamlit_widget.py
```

## File Structure

```
nl_query/
├── __init__.py           # Package init
├── __main__.py           # python -m nl_query entry point
├── schema.py             # Pydantic models + QuerySpec bridge
├── prompt.py             # System prompt (the core artifact)
├── translator.py         # LLM call + validation + retry
├── eval_harness.py       # Evaluation against benchmark ground truth
├── paraphrases.py        # Test set: 6-10 phrasings per query
├── streamlit_widget.py   # Drop-in Streamlit component
└── README.md             # This file
```

## Swapping Backends

The translator supports three backends with zero code changes:

| Backend | Dev/Test | Production | Cost |
|---------|----------|------------|------|
| `ollama` | ✅ M1 Mac, NOTS | ❌ needs GPU | $0 |
| `anthropic` | ✅ | ✅ | ~$0.003/query |
| `openai` | ✅ | ✅ | ~$0.002/query |

```python
# Local dev
result = translate(query, backend="ollama", model="qwen3:8b")

# Production API
result = translate(query, backend="anthropic", model="claude-sonnet-4-5-20250514")

# OpenAI-compatible (vLLM, Together, etc.)
OPENAI_BASE_URL=http://your-server/v1 \
result = translate(query, backend="openai", model="your-model")
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

1. Run eval: `python -m nl_query.eval_harness -o before.json`
2. Edit `prompt.py` (add examples, clarify rules)
3. Re-run eval: `python -m nl_query.eval_harness -o after.json`
4. Compare pass rates

Most failures will be in entity pattern generation (synonyms) and
strategy selection (entity_filter vs intersect). Fix by adding examples
to the prompt for the specific failure mode.
