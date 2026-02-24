"""Splink 4.x config for ORGANIZATION entity deduplication."""

import splink.comparison_library as cl
from splink import SettingsCreator, block_on

LEGAL_SUFFIXES = {"PLC", "INC", "INC.", "LLC", "LTD", "LTD.", "S.A.", "AG", "GMBH", "SAS"}

ABBREVIATION_MAP = {
    "TFMC": "TECHNIPFMC",
    "FMC": "FMC TECHNOLOGIES",
}

# ---------------------------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------------------------

def preprocess(df):
    """Add normalized columns to organization DataFrame.

    Strips legal suffixes, applies abbreviation expansion, uppercases.
    Uses first 5 chars for blocking (org names are longer).
    """
    df = df.copy()

    def normalize(val):
        tokens = str(val).upper().strip().split()
        stripped = [t for t in tokens if t not in LEGAL_SUFFIXES]
        v = " ".join(stripped).strip()
        # Apply abbreviation expansion
        for abbr, full in ABBREVIATION_MAP.items():
            if v == abbr:
                v = full
                break
        return v

    df["value_normalized"] = df["value"].apply(normalize)
    df["first_5_chars"] = df["value_normalized"].str[:5]
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
        cl.ExactMatch("first_5_chars"),
        cl.ExactMatch("token_set"),
    ],
    blocking_rules_to_generate_predictions=[
        block_on("first_5_chars"),
        block_on("token_set"),
    ],
    retain_matching_columns=True,
    retain_intermediate_calculation_columns=False,
    max_iterations=10,
)

AUTO_MERGE_THRESHOLD = 6.0
REVIEW_THRESHOLD = 3.0
