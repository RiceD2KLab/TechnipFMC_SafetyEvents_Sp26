#!/usr/bin/env python3
"""Deterministic diff between two pipeline output directories.

Usage:
    python -m pipeline.telemetry.generate_diff \
        --a pipeline/outputs/v5 \
        --b pipeline/outputs/v6 \
        --report docs/v5_vs_v6_diff.md
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass
class DataDirDiff:
    """Container for a two-directory comparison."""
    a_name: str
    b_name: str
    entity_count_delta: dict[str, dict[str, int]]  # type → {a, b, delta}
    unique_canonical_delta: dict[str, dict[str, int]]
    relation_count_delta: dict[str, dict[str, int]]
    top_canonicals: dict[str, dict[str, list[tuple[str, int]]]]  # type → {a: [...], b: [...]}
    totals: dict[str, dict[str, int]]


def _load(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    entities = pd.read_parquet(data_dir / "entities.parquet")
    relations = pd.read_parquet(data_dir / "relations.parquet")
    return entities, relations


def _type_counts(entities_df: pd.DataFrame) -> dict[str, int]:
    return entities_df["entity_type"].value_counts().to_dict()


def _unique_counts(entities_df: pd.DataFrame) -> dict[str, int]:
    out: dict[str, int] = {}
    for etype, group in entities_df.groupby("entity_type"):
        out[etype] = group["value"].nunique()
    return out


def _relation_counts(relations_df: pd.DataFrame) -> dict[str, int]:
    if "relation" in relations_df.columns:
        return relations_df["relation"].value_counts().to_dict()
    return {}


def _top_n(entities_df: pd.DataFrame, entity_type: str, n: int = 20) -> list[tuple[str, int]]:
    sub = entities_df[entities_df["entity_type"] == entity_type]
    if len(sub) == 0:
        return []
    return list(sub["value"].value_counts().head(n).items())


def generate_diff(
    a_dir: Path,
    b_dir: Path,
    types_to_detail: tuple[str, ...] = ("BODY_PART", "EQUIPMENT", "INJURY_TYPE",
                                         "LOCATION", "ORGANIZATION"),
) -> DataDirDiff:
    a_ent, a_rel = _load(a_dir)
    b_ent, b_rel = _load(b_dir)

    a_types = _type_counts(a_ent)
    b_types = _type_counts(b_ent)
    a_uniq = _unique_counts(a_ent)
    b_uniq = _unique_counts(b_ent)
    a_rels = _relation_counts(a_rel)
    b_rels = _relation_counts(b_rel)

    all_types = sorted(set(a_types) | set(b_types))
    entity_count_delta = {
        t: {"a": a_types.get(t, 0), "b": b_types.get(t, 0),
            "delta": b_types.get(t, 0) - a_types.get(t, 0)}
        for t in all_types
    }
    unique_canonical_delta = {
        t: {"a": a_uniq.get(t, 0), "b": b_uniq.get(t, 0),
            "delta": b_uniq.get(t, 0) - a_uniq.get(t, 0)}
        for t in all_types
    }

    all_rels = sorted(set(a_rels) | set(b_rels))
    relation_count_delta = {
        r: {"a": a_rels.get(r, 0), "b": b_rels.get(r, 0),
            "delta": b_rels.get(r, 0) - a_rels.get(r, 0)}
        for r in all_rels
    }

    top_canonicals: dict[str, dict[str, list[tuple[str, int]]]] = {}
    for t in types_to_detail:
        top_canonicals[t] = {
            "a": _top_n(a_ent, t, 20),
            "b": _top_n(b_ent, t, 20),
        }

    totals = {
        "entities": {"a": len(a_ent), "b": len(b_ent),
                     "delta": len(b_ent) - len(a_ent)},
        "relations": {"a": len(a_rel), "b": len(b_rel),
                      "delta": len(b_rel) - len(a_rel)},
    }

    return DataDirDiff(
        a_name=a_dir.name,
        b_name=b_dir.name,
        entity_count_delta=entity_count_delta,
        unique_canonical_delta=unique_canonical_delta,
        relation_count_delta=relation_count_delta,
        top_canonicals=top_canonicals,
        totals=totals,
    )


def _fmt_delta(d: int) -> str:
    sign = "+" if d >= 0 else ""
    return f"{sign}{d:,}"


def write_report(diff: DataDirDiff, output_path: Path) -> None:
    a, b = diff.a_name, diff.b_name
    lines = []
    lines.append(f"# Pipeline Diff: {a} → {b}\n")

    lines.append("## Totals\n")
    lines.append(f"| | {a} | {b} | Δ |")
    lines.append("|---|---:|---:|---:|")
    for k, v in diff.totals.items():
        lines.append(f"| {k} | {v['a']:,} | {v['b']:,} | {_fmt_delta(v['delta'])} |")
    lines.append("")

    lines.append("## Entity count by type\n")
    lines.append(f"| Type | {a} | {b} | Δ |")
    lines.append("|---|---:|---:|---:|")
    for t, v in diff.entity_count_delta.items():
        lines.append(f"| {t} | {v['a']:,} | {v['b']:,} | {_fmt_delta(v['delta'])} |")
    lines.append("")

    lines.append("## Unique canonical count by type\n")
    lines.append(f"| Type | {a} | {b} | Δ |")
    lines.append("|---|---:|---:|---:|")
    for t, v in diff.unique_canonical_delta.items():
        lines.append(f"| {t} | {v['a']:,} | {v['b']:,} | {_fmt_delta(v['delta'])} |")
    lines.append("")

    lines.append("## Relation type counts\n")
    lines.append(f"| Relation | {a} | {b} | Δ |")
    lines.append("|---|---:|---:|---:|")
    for r, v in diff.relation_count_delta.items():
        lines.append(f"| {r} | {v['a']:,} | {v['b']:,} | {_fmt_delta(v['delta'])} |")
    lines.append("")

    for t, sides in diff.top_canonicals.items():
        lines.append(f"## Top 20 {t} canonicals\n")
        lines.append(f"| # | {a} | count | {b} | count |")
        lines.append("|---:|---|---:|---|---:|")
        a_rows = sides["a"]
        b_rows = sides["b"]
        maxlen = max(len(a_rows), len(b_rows))
        for i in range(maxlen):
            a_val, a_cnt = (a_rows[i] if i < len(a_rows) else ("—", ""))
            b_val, b_cnt = (b_rows[i] if i < len(b_rows) else ("—", ""))
            a_cnt_str = f"{a_cnt:,}" if isinstance(a_cnt, int) else a_cnt
            b_cnt_str = f"{b_cnt:,}" if isinstance(b_cnt, int) else b_cnt
            lines.append(f"| {i+1} | {a_val} | {a_cnt_str} | {b_val} | {b_cnt_str} |")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines))


def main() -> None:
    ap = argparse.ArgumentParser(description="Diff two pipeline data dirs")
    ap.add_argument("--a", type=str, required=True, help="Baseline data dir (e.g. pipeline/outputs/v5)")
    ap.add_argument("--b", type=str, required=True, help="Comparison data dir (e.g. pipeline/outputs/v6)")
    ap.add_argument("--report", type=str, required=True, help="Output Markdown path")
    args = ap.parse_args()

    a_dir = Path(args.a).resolve()
    b_dir = Path(args.b).resolve()
    report_path = Path(args.report).resolve()

    print(f"Diffing {a_dir.name} → {b_dir.name}")
    diff = generate_diff(a_dir, b_dir)
    write_report(diff, report_path)
    print(f"Wrote diff report → {report_path}")

    # Print a quick summary to stdout
    print()
    print(f"  Entities: {diff.totals['entities']['a']:,} → "
          f"{diff.totals['entities']['b']:,} "
          f"({_fmt_delta(diff.totals['entities']['delta'])})")
    print(f"  Relations: {diff.totals['relations']['a']:,} → "
          f"{diff.totals['relations']['b']:,} "
          f"({_fmt_delta(diff.totals['relations']['delta'])})")


if __name__ == "__main__":
    main()
