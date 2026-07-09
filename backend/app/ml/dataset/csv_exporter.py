"""CSV export utilities for generated ML datasets."""

import csv
from pathlib import Path
from typing import Any


class CSVExporter:
    """Export generated dataset rows to CSV."""

    def export(
        self,
        rows: list[dict[str, Any]],
        output_path: str | Path,
    ) -> Path:
        """Write rows to a CSV file and return the resolved path."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not rows:
            path.write_text("", encoding="utf-8")
            return path

        fieldnames = list(rows[0].keys())
        with path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        return path.resolve()
