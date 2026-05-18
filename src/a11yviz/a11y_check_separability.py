"""Flag color pairs below WCAG 1.4.11 non-text contrast threshold."""

from itertools import combinations
from typing import Sequence

from a11yviz._utils import contrast_ratio


def a11y_check_separability(colors: Sequence[str],
                            min_ratio: float = 3.0) -> list[dict]:
    """Flag color pairs below the WCAG 2.1 Success Criterion 1.4.11 contrast threshold

    Parameters
    ----------
    colors
        Character vector of hex codes.
    min_ratio
        Numeric threshold; default 3.0 per WCAG Success Criterion 1.4.11.

    Returns
    -------
        Data frame with columns from, to, ratio, status.
    """
    if len(colors) < 2:
        return []
    rows = []
    for c1, c2 in combinations(colors, 2):
        ratio = contrast_ratio(c1, c2)
        rows.append({
            "from":   c1,
            "to":     c2,
            "ratio":  round(ratio, 2),
            "status": "ok" if ratio >= min_ratio else "todo",
        })
    return rows
