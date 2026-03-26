"""Splink 4.x config for LOCATION entity deduplication."""

import re

import pandas as pd
import splink.comparison_library as cl
from splink import SettingsCreator, block_on

# ---------------------------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------------------------

def preprocess(df):
    """Add normalized columns to location DataFrame.

    Only compares within same granularity level.
    Strips 'zObsolete' prefix for matching.
    """
    df = df.copy()

    def normalize(val):
        v = str(val).strip()
        if v.lower().startswith("zobsolete"):
            v = re.sub(r"^zObsolete\s*[-\u2013\u2014]\s*", "", v, flags=re.IGNORECASE).strip()
        return v.lower()

    df["value_normalized"] = df["value"].apply(normalize)
    df["granularity_key"] = df["granularity"].apply(
        lambda g: str(g) if pd.notna(g) else "unk"
    )
    df["first_3_chars"] = df["value_normalized"].str[:3]
    # Composite block key: granularity + first 3 chars
    df["block_key"] = df["granularity_key"] + "_" + df["first_3_chars"]
    return df

# ---------------------------------------------------------------------------
# Splink settings
# ---------------------------------------------------------------------------

settings = SettingsCreator(
    link_type="dedupe_only",
    comparisons=[
        cl.JaroWinklerAtThresholds("value_normalized", [0.9, 0.8]),
        cl.ExactMatch("granularity_key"),
        cl.ExactMatch("first_3_chars"),
    ],
    blocking_rules_to_generate_predictions=[
        block_on("block_key"),
    ],
    retain_matching_columns=True,
    retain_intermediate_calculation_columns=False,
    max_iterations=10,
)

AUTO_MERGE_THRESHOLD = 6.0
REVIEW_THRESHOLD = 3.0
