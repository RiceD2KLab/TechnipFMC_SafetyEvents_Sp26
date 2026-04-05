"""Splink 4.x config for INJURY_TYPE entity deduplication."""

import splink.comparison_library as cl
from splink import SettingsCreator, block_on

SEVERITY_QUALIFIERS = {
    "minor", "small", "slight", "mild",
    "severe", "major", "deep", "superficial",
}

# ---------------------------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------------------------

def preprocess(df):
    """Add normalized columns to injury DataFrame.

    Strips severity qualifiers and trailing 'injury' suffix.
    """
    df = df.copy()
    df["value_normalized"] = (
        df["value"]
        .str.lower()
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    def strip_severity(val):
        tokens = val.split()
        stripped = [t for t in tokens if t not in SEVERITY_QUALIFIERS]
        # Also strip trailing "injury"
        if len(stripped) > 1 and stripped[-1] == "injury":
            stripped = stripped[:-1]
        return " ".join(stripped) if stripped else val

    df["base_form"] = df["value_normalized"].apply(strip_severity)
    # Normalize plural
    df["base_form"] = df["base_form"].apply(
        lambda v: v[:-1] if len(v) > 3 and v.endswith("s") and not v.endswith("ss") else v
    )
    df["first_3_chars"] = df["base_form"].str[:3]
    return df

# ---------------------------------------------------------------------------
# Splink settings
# ---------------------------------------------------------------------------

settings = SettingsCreator(
    link_type="dedupe_only",
    comparisons=[
        cl.JaroWinklerAtThresholds("base_form", [0.9, 0.8]),
        cl.ExactMatch("first_3_chars"),
    ],
    blocking_rules_to_generate_predictions=[
        block_on("base_form"),
        block_on("first_3_chars"),
    ],
    retain_matching_columns=True,
    retain_intermediate_calculation_columns=False,
    max_iterations=10,
)

AUTO_MERGE_THRESHOLD = 6.0
REVIEW_THRESHOLD = 3.0
