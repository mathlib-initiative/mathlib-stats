#!/usr/bin/env python3
"""Generate a summary of tactic usage by counting name occurrences in the tactics dataset."""

import json
from collections import Counter
from pathlib import Path

import pyarrow.parquet as pq


def main():
    tactics_dir = Path("tactics")
    name_counts: Counter[str] = Counter()

    for parquet_file in tactics_dir.glob("*.parquet"):
        table = pq.read_table(parquet_file, columns=["kind"])
        names = table.column("kind").to_pylist()
        name_counts.update(name for name in names if name is not None)

    # Sort by count descending
    summary = dict(sorted(name_counts.items(), key=lambda x: x[1], reverse=True))

    output_path = Path("tactic_summary.json")
    with output_path.open("w") as f:
        json.dump(summary, f, indent=2)

    print(f"Summary written to {output_path}")
    print(f"Total unique names: {len(summary)}")
    print(f"Total occurrences: {sum(summary.values())}")


if __name__ == "__main__":
    main()
