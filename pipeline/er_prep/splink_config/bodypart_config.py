"""Splink 4.x config for BODY_PART entity deduplication."""

import splink.comparison_library as cl
from splink import SettingsCreator, block_on

LATERALITY_TOKENS = {"left", "right"}
ORDINAL_TOKENS = {"index", "middle", "ring"}

# ---------------------------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------------------------

def preprocess(df):
    """Add normalized columns to body_part DataFrame.

    Expects 'entity_id' and 'value' columns.
    Returns copy with: value_normalized, base_form, first_3_chars.

    Key rule: "left hand" and "right hand" do NOT merge with each other,
    but both merge with "hand". This is enforced by blocking on base_form
    and post-filtering laterality conflicts.
    """
    df = df.copy()
    df["value_normalized"] = (
        df["value"]
        .str.lower()
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    # Strip laterality and ordinal tokens for base form
    def strip_laterality(val):
        tokens = val.split()
        stripped = [t for t in tokens if t not in LATERALITY_TOKENS and t not in ORDINAL_TOKENS]
        return " ".join(stripped) if stripped else val

    df["base_form"] = df["value_normalized"].apply(strip_laterality)
    # Normalize plural
    df["base_form"] = df["base_form"].apply(
        lambda v: v[:-1] if len(v) > 3 and v.endswith("s") and not v.endswith("ss") else v
    )
    df["first_3_chars"] = df["base_form"].str[:3]
    # Retain laterality for conflict detection
    df["laterality"] = df["value_normalized"].apply(
        lambda v: next((t for t in v.split() if t in LATERALITY_TOKENS), "none")
    )
    return df

# ---------------------------------------------------------------------------
# Post-filter: reject pairs where both have laterality but differ
# ---------------------------------------------------------------------------

def filter_laterality_conflicts(predictions_df):
    """Remove pairs where both entities have laterality but different sides.

    e.g., 'left hand' vs 'right hand' should NOT merge.
    'left hand' vs 'hand' is fine (one has no laterality).
    """
    mask = (
        (predictions_df["laterality_l"] != "none") &
        (predictions_df["laterality_r"] != "none") &
        (predictions_df["laterality_l"] != predictions_df["laterality_r"])
    )
    return predictions_df[~mask]

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
