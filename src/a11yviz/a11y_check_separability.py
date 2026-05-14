"""Flag color pairs below WCAG 1.4.11 non-text contrast threshold."""

from itertools import combinations
from typing import Sequence

from a11yviz._utils import contrast_ratio


def a11y_check_separability(colors: Sequence[str],
                            min_ratio: float = 3.0) -> list[dict]:
    """Return per-pair contrast rows; pairs below `min_ratio` get status 'todo'."""
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
