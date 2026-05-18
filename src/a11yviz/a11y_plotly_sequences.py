"""Audit plotly's built-in discrete color sequences against WCAG contrast."""

import statistics

from a11yviz._constants import plotly_sequences
from a11yviz._utils import check_level, contrast_ratio


def a11y_plotly_sequences(bg: str = "#ffffff", level: str = "AA") -> list[dict]:
    """Audit plotly's built-in discrete color sequences

    Parameters
    ----------
    bg
        Reference background hex (default "#ffffff").
    level
        "AA" (4.5:1) or "AAA" (7:1).

    Returns
    -------
        Data frame with one row per sequence: name, n, min_ratio, median_ratio, n_pass, pct_pass.
    """
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
