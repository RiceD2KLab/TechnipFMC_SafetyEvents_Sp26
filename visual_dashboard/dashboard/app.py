# app.py
import streamlit as st
import pandas as pd
from pathlib import Path
from handler.handler import (
    generate_chart,
    generate_kg_visualization,
    search_kg_entities,
    get_kg_incident_options,
)
from handler.kg_loader import ENTITY_COLORS, ENTITY_TYPE_LABELS

st.set_page_config(page_title="Safety Event Dashboard", layout="wide")


st.title("Safety Event Dashboard")

# Load unique values for filters (cached for performance)
@st.cache_data
def load_filter_options():
    """Load unique values for filter dropdowns."""
    data_file = Path(__file__).parent.parent.parent / "data" / "merged_incidents_tsne.csv"
    df = pd.read_csv(data_file, low_memory=False)

    return {
        'status': sorted(df['STATUS'].dropna().unique().tolist()),
        'impact_type': sorted(df['IMPACT_TYPE'].dropna().unique().tolist()),
        'risk_color': sorted(df['RISK_COLOR'].dropna().unique().tolist()),
        'gbu': sorted(df['GBU'].dropna().unique().tolist()),
        'workplace_country': sorted(df['WORKPLACE_COUNTRY'].dropna().unique().tolist()),
        'severity_min': float(df['LOSS_POTENTIAL_SEVERITY'].dropna().min()),
        'severity_max': float(df['LOSS_POTENTIAL_SEVERITY'].dropna().max()),
        'likelihood_min': float(df['LIKELIHOOD_VALUE'].dropna().min()),
        'likelihood_max': float(df['LIKELIHOOD_VALUE'].dropna().max()),
        'available_years': sorted(df['YEAR_OF_INCIDENT'].dropna().unique().tolist()),
    }

filter_options = load_filter_options()

# --- Sidebar filters (apply to Dashboard tab only) ---
st.sidebar.header("Filter Settings")
st.sidebar.caption("Filters apply to the Dashboard tab only.")

# Toggle for month view
filter_by_month = st.sidebar.toggle("By month", value=False)

# Year selection based on toggle
if filter_by_month:
    # Single year selection when filtering by month
    # Default to most recent year (last in sorted list)
    default_year_index = len(filter_options['available_years']) - 1
    selected_year = st.sidebar.selectbox(
        "Select Year",
        options=filter_options['available_years'],
        index=default_year_index
    )
    # Month range slider
    month_range = st.sidebar.slider("Month Range", 1, 12, (1, 12))
else:
    # Year range slider when filtering by year
    year_range = st.sidebar.slider("Year Range", 2015, 2025, (2015, 2025))

st.sidebar.markdown("---")
# Incident Types
incident_types = st.sidebar.multiselect("Incident Types", ["Accident", "Near Miss", "Hazard Observation"])

# Status
status_options = st.sidebar.multiselect("Status", filter_options['status'])

# Impact Type
impact_types = st.sidebar.multiselect("Impact Type", filter_options['impact_type'])

# Risk Color
risk_colors = st.sidebar.multiselect("Risk Color", filter_options['risk_color'])

# GBU
gbu_options = st.sidebar.multiselect("GBU", filter_options['gbu'])

# Workplace Country
workplace_countries = st.sidebar.multiselect("Workplace Country", filter_options['workplace_country'])

# Severity range
st.sidebar.markdown("---")
severity_range = st.sidebar.slider(
    "Loss Potential Severity",
    int(filter_options['severity_min']),
    int(filter_options['severity_max']),
    (int(filter_options['severity_min']), int(filter_options['severity_max']))
)

# Likelihood range
likelihood_range = st.sidebar.slider(
    "Likelihood Value",
    int(filter_options['likelihood_min']),
    int(filter_options['likelihood_max']),
    (int(filter_options['likelihood_min']), int(filter_options['likelihood_max']))
)

# Build filter requirements based on month toggle
if filter_by_month:
    # When filtering by month: use specific year and month range
    filter_requirements = {
        "YEAR_OF_INCIDENT": {"min": selected_year, "max": selected_year},
        "MONTH_OF_INCIDENT": {"min": month_range[0], "max": month_range[1]},
    }
else:
    # When filtering by year: use year range
    filter_requirements = {
        "YEAR_OF_INCIDENT": {"min": year_range[0], "max": year_range[1]},
    }

if incident_types:
    filter_requirements["INCIDENT_TYPE"] = incident_types

if status_options:
    filter_requirements["STATUS"] = status_options

if impact_types:
    filter_requirements["IMPACT_TYPE"] = impact_types

if risk_colors:
    filter_requirements["RISK_COLOR"] = risk_colors

if gbu_options:
    filter_requirements["GBU"] = gbu_options

if workplace_countries:
    filter_requirements["WORKPLACE_COUNTRY"] = workplace_countries

# Add severity range if not at full range
if severity_range[0] > filter_options['severity_min'] or severity_range[1] < filter_options['severity_max']:
    filter_requirements["LOSS_POTENTIAL_SEVERITY"] = {"min": float(severity_range[0]), "max": float(severity_range[1])}

# Add likelihood range if not at full range
if likelihood_range[0] > filter_options['likelihood_min'] or likelihood_range[1] < filter_options['likelihood_max']:
    filter_requirements["LIKELIHOOD_VALUE"] = {"min": float(likelihood_range[0]), "max": float(likelihood_range[1])}

# ============================================================
# Tab structure
# ============================================================
tab_dashboard, tab_kg = st.tabs(["Dashboard", "Knowledge Graph Explorer"])

# ============================================================
# Tab 1: Dashboard (existing content)
# ============================================================
with tab_dashboard:
    # --- Big Numbers ---
    st.subheader("Statistical Summary")
    summary = generate_chart("statistical_summary", filter_requirements)
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Incidents", summary["total_incidents"])
    col2.metric("High Risk (%)", f"{summary['high_risk_percentage']:.1f}%")
    avg_severity = summary.get('avg_severity', 0)
    avg_likelihood = summary.get('avg_likelihood', 0)
    if avg_severity is not None and not pd.isna(avg_severity):
        col3.metric("Avg. Severity", f"{avg_severity:.2f}")
    else:
        col3.metric("Avg. Severity", "N/A")
    if avg_likelihood is not None and not pd.isna(avg_likelihood):
        col4.metric("Avg. Likelihood", f"{avg_likelihood:.2f}")
    else:
        col4.metric("Avg. Likelihood", "N/A")
    col5.metric("Open Actions", summary["open_actions"])

    # --- Temporal Distribution ---
    if filter_by_month:
        st.subheader("Incident Frequency by Month")
        temporal_chart = generate_chart("temporal_distribution", filter_requirements, time_column="DATE_OF_INCIDENT", groupby="month")
    else:
        st.subheader("Incident Frequency by Year")
        temporal_chart = generate_chart("temporal_distribution", filter_requirements, time_column="YEAR_OF_INCIDENT", groupby="year")
    st.plotly_chart(temporal_chart, use_container_width=True)

    # --- Top Locations ---
    st.subheader("Top Locations")
    top_locations = generate_chart("top_locations", filter_requirements)
    st.plotly_chart(top_locations, use_container_width=True)

    # --- Top Units ---
    st.subheader("Top Units")
    top_units = generate_chart("top_units", filter_requirements)
    st.plotly_chart(top_units, use_container_width=True)

    # ==============================
    # 4. Incident Type (Pie Chart)
    # ==============================
    st.subheader("Incident Type Distribution")
    incident_type_pie = generate_chart("incident_type", filter_requirements, subtype="pie")
    st.plotly_chart(incident_type_pie, use_container_width=True)

    # ==============================
    # 5. Impact Type (Pie Chart)
    # ==============================
    st.subheader("Impact Type Distribution")
    impact_type_pie = generate_chart("pie_chart", filter_requirements, column="IMPACT_TYPE", title="Impact Type Distribution")
    st.plotly_chart(impact_type_pie, use_container_width=True)

    # ==============================
    # 6. Risk Color (Stacked Bar)
    # ==============================
    st.subheader("Risk Color Distribution by Severity Level")
    risk_color_stacked = generate_chart("risk_color", filter_requirements, subtype="stacked")
    st.plotly_chart(risk_color_stacked, use_container_width=True)

    # ==============================
    # 7. Top Causes/Hazards (Bar Chart)
    # ==============================
    st.subheader("Top Causes / Hazards")
    top_causes = generate_chart("top_causes", filter_requirements)
    st.plotly_chart(top_causes, use_container_width=True)

    # ==============================
    # 8. Severity vs Likelihood (Heatmap)
    # ==============================
    st.subheader("Severity vs Likelihood Heatmap")
    severity_likelihood = generate_chart("severity_likelihood_heatmap", filter_requirements)
    st.plotly_chart(severity_likelihood, use_container_width=True)

    # ==============================
    # 9. Word Cloud
    # ==============================
    st.subheader("Word Cloud of Incident Titles")
    wordcloud = generate_chart("wordcloud", filter_requirements)
    st.plotly_chart(wordcloud, use_container_width=True)

    sample_ratio = st.slider(
        "Sample Ratio (default 10%)",
        min_value=0.01,
        max_value=1.0,
        value=0.10,
        step=0.01
    )
    fig = generate_chart(
        "event_cluster",
        filter_requirements,
        sample_ratio=sample_ratio,
        color_column="IMPACT_TYPE"  # optional
    )
    st.plotly_chart(fig)

    st.markdown("---")
    st.caption("© 2025 Safety Event Dashboard | Powered by Streamlit + Plotly")

# ============================================================
# Tab 2: Knowledge Graph Explorer
# ============================================================
with tab_kg:
    st.subheader("Knowledge Graph Explorer")
    st.caption(
        "Explore the incident knowledge graph interactively. "
        "Select an incident or search for an entity to visualize its neighborhood."
    )

    # --- KG Controls ---
    kg_col1, kg_col2 = st.columns([2, 1])

    with kg_col1:
        search_mode = st.radio(
            "Search mode",
            ["Browse incidents", "Search entities"],
            horizontal=True,
        )

    with kg_col2:
        hop_depth = st.radio("Hop depth", [1, 2], horizontal=True)

    # --- Entity type filter ---
    all_entity_types = list(ENTITY_TYPE_LABELS.keys())
    selected_entity_types = st.multiselect(
        "Show only these entity types (leave empty to show all)",
        options=all_entity_types,
        format_func=lambda x: ENTITY_TYPE_LABELS.get(x, x),
        default=all_entity_types,
        key="kg_entity_type_filter",
    )
    # All selected = no filter; partial selection = filter to those types
    if not selected_entity_types or set(selected_entity_types) == set(all_entity_types):
        entity_type_filter = None
    else:
        entity_type_filter = set(selected_entity_types)

    # --- Mode-specific controls ---
    selected_node_id = None

    @st.cache_resource
    def _cached_incident_options():
        return get_kg_incident_options()

    if search_mode == "Browse incidents":
        try:
            incident_map = _cached_incident_options()
            incident_labels = sorted(incident_map.keys())

            selected_label = st.selectbox(
                "Select an incident (type to search)",
                options=[""] + incident_labels,
                index=0,
                help="Start typing a record number or keyword to search",
            )
            if selected_label:
                selected_node_id = incident_map[selected_label]
        except FileNotFoundError as e:
            st.error(str(e))

    else:  # "Search entities"
        search_col1, search_col2 = st.columns([1, 2])
        with search_col1:
            search_type = st.selectbox(
                "Entity type",
                ["ALL"] + all_entity_types,
                format_func=lambda x: "All types" if x == "ALL"
                    else ENTITY_TYPE_LABELS.get(x, x),
            )
        with search_col2:
            search_query = st.text_input(
                "Search value (regex supported)",
                placeholder="e.g., forklift, scaffold, fall.*",
            )

        if search_query:
            try:
                results = search_kg_entities(
                    entity_type=search_type if search_type != "ALL" else None,
                    value_pattern=search_query,
                    max_results=50,
                )
                if results:
                    result_options = {
                        f"{r[1]}: {str(r[2])[:60]} ({r[0]})": r[0] for r in results
                    }
                    selected_result = st.selectbox(
                        f"Found {len(results)} results - select one:",
                        options=list(result_options.keys()),
                    )
                    selected_node_id = result_options[selected_result]
                else:
                    st.warning("No entities matched your search.")
            except FileNotFoundError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Search error: {e}")

    # --- Render the graph ---
    if selected_node_id:
        with st.spinner("Building subgraph..."):
            try:
                result = generate_kg_visualization(
                    node_id=selected_node_id,
                    hops=hop_depth,
                    entity_type_filter=entity_type_filter,
                )

                stats = result["stats"]
                fig = result["figure"]
                truncated = result.get("truncated", False)

                if truncated:
                    st.warning(
                        "The subgraph was too large and has been capped at 500 nodes. "
                        "Try reducing hop depth or filtering entity types."
                    )

                # Summary metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Nodes", stats["node_count"])
                m2.metric("Edges", stats["edge_count"])
                m3.metric("Entity Types", len(stats["entity_type_counts"]))

                # Entity type breakdown
                with st.expander("Subgraph breakdown", expanded=False):
                    bcol1, bcol2 = st.columns(2)
                    with bcol1:
                        st.write("**Entity types:**")
                        for et, count in sorted(stats["entity_type_counts"].items()):
                            color = ENTITY_COLORS.get(et, "#999")
                            st.markdown(
                                f'<span style="color:{color};">&#9679;</span> '
                                f'{ENTITY_TYPE_LABELS.get(et, et)}: {count}',
                                unsafe_allow_html=True,
                            )
                    with bcol2:
                        st.write("**Relation types:**")
                        for rel, count in sorted(stats["relation_type_counts"].items()):
                            st.write(f"- {rel}: {count}")

                # Color legend
                legend_html = " &nbsp; ".join(
                    f'<span style="color:{ENTITY_COLORS[et]};">&#9679;</span> '
                    f'{ENTITY_TYPE_LABELS[et]}'
                    for et in all_entity_types
                    if et in stats["entity_type_counts"]
                )
                st.markdown(f"**Legend:** {legend_html}", unsafe_allow_html=True)

                # Interactive graph
                st.plotly_chart(fig, use_container_width=True)

            except FileNotFoundError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error generating visualization: {e}")
    else:
        st.info("Select an incident or search for an entity above to visualize its knowledge graph neighborhood.")

    st.markdown("---")
    st.caption("Knowledge Graph: 61,545 entities, 202,141 relations | Powered by PyVis + NetworkX")
