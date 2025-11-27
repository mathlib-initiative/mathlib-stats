#!/usr/bin/env python3
"""Generate a static HTML dashboard from tactic_summary.json."""

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def format_number(value: int) -> str:
    return f"{value:,}"


def generate_dashboard(
    input_path: Path = Path("tactic_summary.json"),
    output_path: Path = Path("_site/index.html"),
) -> None:
    with input_path.open() as f:
        data = json.load(f)

    total_occurrences = sum(data.values())
    total_unique = len(data)

    # Set up Jinja2
    env = Environment(loader=FileSystemLoader("templates"))
    env.filters["format_number"] = format_number
    template = env.get_template("dashboard.html")

    html = template.render(
        tactics=data,
        total_unique=total_unique,
        total_occurrences=total_occurrences,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        f.write(html)

    print(f"Dashboard generated: {output_path}")


if __name__ == "__main__":
    generate_dashboard()
