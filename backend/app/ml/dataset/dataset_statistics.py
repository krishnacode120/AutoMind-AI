"""Dataset summary statistics for generated ML datasets."""

from collections import defaultdict
from typing import Any


class DatasetStatistics:
    """Calculate quality and range statistics for dataset rows."""

    def summarize(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        """Return sample count, failure rate, ranges, and missing counts."""
        if not rows:
            return {
                "sample_count": 0,
                "failure_rate": 0.0,
                "feature_ranges": {},
                "missing_values": {},
            }

        return {
            "sample_count": len(rows),
            "failure_rate": self._failure_rate(rows),
            "feature_ranges": self._feature_ranges(rows),
            "missing_values": self._missing_values(rows),
        }

    def _failure_rate(self, rows: list[dict[str, Any]]) -> float:
        """Return the ratio of positive failure labels."""
        positive_labels = sum(1 for row in rows if row.get("failure") == 1)
        return round(positive_labels / len(rows), 4)

    def _feature_ranges(
        self,
        rows: list[dict[str, Any]],
    ) -> dict[str, dict[str, float]]:
        """Return min and max for numeric features."""
        numeric_values: dict[str, list[float]] = defaultdict(list)

        for row in rows:
            for key, value in row.items():
                if key == "failure":
                    continue
                if isinstance(value, bool):
                    continue
                if isinstance(value, (int, float)):
                    numeric_values[key].append(float(value))

        return {
            key: {
                "min": min(values),
                "max": max(values),
            }
            for key, values in numeric_values.items()
            if values
        }

    def _missing_values(self, rows: list[dict[str, Any]]) -> dict[str, int]:
        """Return missing-value counts for each column."""
        missing_counts: dict[str, int] = {key: 0 for key in rows[0]}

        for row in rows:
            for key in missing_counts:
                value = row.get(key)
                if value is None or value == "":
                    missing_counts[key] += 1

        return missing_counts
