"""Splink 4.x config for EQUIPMENT entity deduplication."""

import re

import splink.comparison_library as cl
from splink import SettingsCreator, block_on

# ---------------------------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------------------------

def preprocess(df):
    """Add normalized columns to equipment DataFrame.

    Expects a DataFrame with at least 'entity_id' and 'value' columns.
    Returns a copy with added: value_normalized, first_3_chars, token_set.
    """
    df = df.copy()
    df["value_normalized"] = (
        df["value"]
        .str.lower()
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    # Remove trailing 's' for plural normalization (keep 'ss' words like 'glass')
    df["value_normalized"] = df["value_normalized"].apply(
        lambda v: v[:-1] if len(v) > 3 and v.endswith("s") and not v.endswith("ss") else v
    )
    df["first_3_chars"] = df["value_normalized"].str[:3]
    df["token_set"] = df["value_normalized"].apply(
        lambda v: " ".join(sorted(set(v.split())))
    )
    return df

# ---------------------------------------------------------------------------
# Splink settings
# ---------------------------------------------------------------------------

settings = SettingsCreator(
    link_type="dedupe_only",
    comparisons=[
        cl.JaroWinklerAtThresholds("value_normalized", [0.9, 0.8]),
        cl.ExactMatch("first_3_chars"),
        cl.ExactMatch("token_set"),
    ],
    blocking_rules_to_generate_predictions=[
        block_on("first_3_chars"),
        block_on("token_set"),
    ],
    retain_matching_columns=True,
    retain_intermediate_calculation_columns=False,
    max_iterations=10,
)

# Auto-merge threshold: match_weight >= 6.0
# Review threshold: 3.0 <= match_weight < 6.0
AUTO_MERGE_THRESHOLD = 6.0
REVIEW_THRESHOLD = 3.0
