"""Streamlit integration for NL query interface.

Drop this into the existing dashboard. Requires:
    pip install streamlit

Usage in your Streamlit app:
    from nl_query.streamlit_widget import render_nl_query_widget
    render_nl_query_widget(G, entities_df, relations_df, metadata_df)

Or run standalone for testing:
    streamlit run nl_query/streamlit_widget.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st


def render_nl_query_widget(
    G=None,
    entities_df=None,
    relations_df=None,
    metadata_df=None,
    backend: str = "ollama",
    model: str | None = None,
    base_url: str = "http://localhost:11434",
):
    """Render the NL query interface as a Streamlit component.

    Args:
        G, entities_df, relations_df, metadata_df: Graph data from load_data().
            If None, only translation is shown (no execution).
        backend: LLM backend ("ollama", "anthropic", "gemini").
        model: Model name (None = use default for backend).
        base_url: Ollama server URL.
    """
    from nl_query.translator import translate

    st.subheader("Natural Language Query")

    query = st.text_input(
        "Ask a question about safety incidents:",
        placeholder="e.g., How many forklift incidents happened in 2022?",
        key="nl_query_input",
    )

    col1, col2 = st.columns([3, 1])
    with col2:
        show_debug = st.checkbox("Show debug info", value=False)

    if query:
        with st.spinner("Translating query..."):
            result = translate(
                query,
                backend=backend,
                model=model,
                base_url=base_url,
            )

        # ── Handle failure ───────────────────────────────────────
        if result["query_spec"] is None:
            st.error(
                f"Could not parse query: {result['clarification']}"
            )
            if show_debug:
                st.code(result["raw_response"][:500], language="json")
            return

        nl = result["nl_output"]
        spec_dict = result["query_spec"]

        # ── Confidence check ─────────────────────────────────────
        if result["confidence"] < 0.7:
            st.warning(
                f"Low confidence ({result['confidence']:.0%}): "
                f"{nl.clarification or 'The query may be ambiguous.'}"
            )

        # ── Show translation ─────────────────────────────────────
        with st.expander("Query interpretation", expanded=True):
            st.markdown(f"**Strategy:** {spec_dict['strategy']}")
            if spec_dict["entity_filters"]:
                for ef in spec_dict["entity_filters"]:
                    st.markdown(
                        f"**Entity filter:** {ef[0]} "
                        f"matching `{ef[1]}` via {ef[2]}"
                    )
            if spec_dict["meta_filters"]:
                for mf in spec_dict["meta_filters"]:
                    st.markdown(
                        f"**Metadata filter:** {mf[0]} {mf[1]} {mf[2]}"
                    )
            if spec_dict["narrative_keywords"]:
                mode = "ANY" if spec_dict["match_any_keyword"] else "ALL"
                st.markdown(
                    f"**Narrative keywords ({mode}):** "
                    f"{', '.join(spec_dict['narrative_keywords'])}"
                )
            st.markdown(f"**Output mode:** {spec_dict['output_mode']}")
            st.markdown(
                f"**Confidence:** {result['confidence']:.0%} "
                f"| **Latency:** {result['latency_ms']:.0f}ms"
            )

        # ── Execute against graph ────────────────────────────────
        if G is not None:
            try:
                # Import the existing query engine
                sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
                from benchmark.query_engine import QuerySpec, execute_query

                spec = QuerySpec(**spec_dict)
                exec_result = execute_query(
                    spec, G, entities_df, relations_df, metadata_df
                )

                st.markdown("---")
                st.markdown(f"### Result")
                st.markdown(
                    f"**{exec_result['coverage']}** "
                    f"{exec_result['result_summary']}"
                )

                if exec_result.get("detail"):
                    with st.expander("Detail"):
                        st.text(exec_result["detail"])

            except Exception as e:
                st.error(f"Query execution failed: {e}")

        # ── Debug panel ──────────────────────────────────────────
        if show_debug:
            with st.expander("Raw LLM output"):
                st.code(result["raw_response"], language="json")
            with st.expander("QuerySpec dict"):
                # Make it JSON-serializable
                debug_spec = {
                    k: (list(v) if isinstance(v, set) else v)
                    for k, v in spec_dict.items()
                }
                st.code(json.dumps(debug_spec, indent=2), language="json")
            if nl.reasoning:
                with st.expander("LLM reasoning"):
                    st.markdown(nl.reasoning)


# ── Standalone mode ──────────────────────────────────────────────────────

def _standalone():
    """Run as a standalone Streamlit app for testing (no graph data)."""
    st.set_page_config(
        page_title="NL Query Interface",
        page_icon="🔍",
        layout="wide",
    )
    st.title("Safety Incident NL Query Interface")
    st.caption("Test mode — translation only, no graph execution")

    with st.sidebar:
        backend = st.selectbox(
            "Backend", ["ollama", "anthropic", "gemini"]
        )
        model = st.text_input(
            "Model",
            value="" if backend == "ollama" else "",
            placeholder="Leave empty for default",
        )
        base_url = st.text_input(
            "Ollama URL",
            value="http://localhost:11434",
        )

    render_nl_query_widget(
        backend=backend,
        model=model or None,
        base_url=base_url,
    )


if __name__ == "__main__":
    _standalone()
