#!/usr/bin/env python3
"""NL -> QuerySpec evaluation harness using Amazon Bedrock only.

This entry point is isolated from ``eval_harness.py`` (Ollama/Qwen) so you can
experiment with Bedrock without touching the legacy CLI while you migrate.

Loads environment variables from ``natural_language_query/.env`` when
``python-dotenv`` is installed (optional but recommended).

Required for Bedrock API key auth (console long-term API key):
    AWS_BEARER_TOKEN_BEDROCK   Official env name boto3 reads for the key
    AWS_REGION                 e.g. us-east-1 (must match where the model is enabled)

Convenience alias (if you already use this name in .env):
    AWS_BEDROCK_KEY            Copied to AWS_BEARER_TOKEN_BEDROCK when the latter is unset

IAM auth instead of an API key (typical for production / CI):
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    Optional: AWS_SESSION_TOKEN

    Do not set AWS_BEARER_TOKEN_BEDROCK when using IAM keys.

Optional:
    AWS_DEFAULT_REGION         Used if AWS_REGION is not set

Usage:
    pip install boto3 python-dotenv
    python -m natural_language_query.eval_harness_bedrock
    python -m natural_language_query.eval_harness_bedrock --model us.anthropic.claude-haiku-4-5-20251001-v1:0
    python -m natural_language_query.eval_harness_bedrock --temperature 0
    python -m natural_language_query.eval_harness_bedrock -i

The harness defaults to temperature 0.0 and passes it through ``run_evaluation`` → ``translate`` so Bedrock runs are reproducible. Override with ``--temperature`` if needed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.is_file():
        load_dotenv(env_path)


def main() -> None:
    _load_dotenv()

    # Import after dotenv so translator sees env vars
    from .eval_harness import interactive_mode, print_report, run_evaluation

    parser = argparse.ArgumentParser(
        description="Evaluate NL -> QuerySpec translation via Amazon Bedrock",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Bedrock modelId (default: translator default for bedrock backend)",
    )
    parser.add_argument(
        "--region",
        default=None,
        help="AWS region (sets AWS_REGION for this process; e.g. us-east-1)",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Interactive query mode",
    )
    parser.add_argument(
        "--paraphrases",
        default=None,
        help="Path to custom paraphrases JSON file",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Save results JSON to this path",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="LLM temperature (default 0 for reproducible paraphrase eval)",
    )

    args = parser.parse_args()

    if args.region:
        os.environ["AWS_REGION"] = args.region

    if args.interactive:
        interactive_mode(
            "bedrock", args.model, base_url="", temperature=args.temperature
        )
        return

    paraphrases = None
    if args.paraphrases:
        with open(args.paraphrases, encoding="utf-8") as f:
            paraphrases = json.load(f)

    print("Backend: bedrock (Amazon Bedrock Runtime / Converse)")
    print(f"Model:   {args.model or '(default)'}")
    print(f"Region:  {os.environ.get('AWS_REGION') or os.environ.get('AWS_DEFAULT_REGION') or 'us-east-1'}")
    print(f"Temp:    {args.temperature}")
    print("Running evaluation...\n")

    summary = run_evaluation(
        backend="bedrock",
        model=args.model,
        base_url="",
        paraphrases=paraphrases,
        temperature=args.temperature,
    )

    print_report(summary)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
