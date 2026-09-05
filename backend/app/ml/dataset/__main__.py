"""Command-line dataset export with a machine-readable statistics report."""

import argparse
import json
from pathlib import Path

from app.ml.dataset.dataset_generator import DatasetGenerator


def main() -> None:
    """Generate a dataset without changing the application database."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--output", type=Path, default=Path("../datasets/telemetry.csv")
    )
    args = parser.parse_args()
    if args.size < 1:
        parser.error("--size must be positive")
    result = DatasetGenerator(random_seed=args.seed).generate(args.size, args.output)
    summary = args.output.with_suffix(".statistics.json")
    summary.write_text(json.dumps(result.statistics, indent=2), encoding="utf-8")
    print(f"CSV: {result.csv_path}")
    print(f"Statistics: {summary}")
    print(
        f"Samples: {len(result.rows)}; failure rate: {result.statistics['failure_rate']:.2%}"
    )


if __name__ == "__main__":
    main()
