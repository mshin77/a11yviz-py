"""Check a palette against WCAG contrast thresholds."""

from typing import Iterable, Sequence, Union

from a11yviz._utils import alpha_composite, contrast_ratio

_LEVELS = {"AA": 4.5, "AAA": 7.0, "AA-large": 3.0}


def a11y_check_palette(colors: Sequence[str],
                       bg: Union[str, Iterable[str]] = "#ffffff",
                       level: str = "AA",
                       alpha: float = 1.0) -> list[dict]:
    """Return per-color contrast rows against one or more backgrounds."""
    if level not in _LEVELS:
        raise ValueError(f"level must be one of {sorted(_LEVELS)}")
    threshold = _LEVELS[level]
    bg_list = [bg] if isinstance(bg, str) else list(bg)

    rows = []
    for color in colors:
        for b in bg_list:
            rendered = color if alpha == 1.0 else alpha_composite(color, b, alpha)
            ratio = contrast_ratio(rendered, b)
            rows.append({
                "color":    color,
                "bg":       b,
                "alpha":    alpha,
                "rendered": rendered,
                "ratio":    round(ratio, 2),
                "status":   "ok" if ratio >= threshold else "todo",
            })
    return rows
