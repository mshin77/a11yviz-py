"""Audit plotly's built-in discrete color sequences against WCAG contrast."""

import statistics

from a11yviz._constants import plotly_sequences
from a11yviz._utils import check_level, contrast_ratio


def a11y_plotly_sequences(bg: str = "#ffffff", level: str = "AA") -> list[dict]:
    """Return contrast statistics for plotly's built-in discrete sequences."""
    level = check_level(level)
    threshold = 4.5 if level == "AA" else 7.0

    rows = []
    for name, cols in plotly_sequences.items():
        ratios = [contrast_ratio(c, bg) for c in cols]
        n_pass = sum(r >= threshold for r in ratios)
        rows.append({
            "name":         name,
            "n":            len(cols),
            "min_ratio":    round(min(ratios), 2),
            "median_ratio": round(statistics.median(ratios), 2),
            "n_pass":       n_pass,
            "pct_pass":     round(100 * n_pass / len(cols), 1),
        })
    rows.sort(key=lambda r: -r["pct_pass"])
    return rows
