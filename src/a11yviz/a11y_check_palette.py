"""Check a palette against WCAG contrast thresholds."""

from typing import Iterable, Sequence, Union

from a11yviz._utils import alpha_composite, contrast_ratio

_levels = {"AA": 4.5, "AAA": 7.0, "AA-large": 3.0}


def a11y_check_palette(colors: Sequence[str],
                       bg: Union[str, Iterable[str]] = "#ffffff",
                       level: str = "AA",
                       alpha: float = 1.0) -> list[dict]:
    """Check a palette against WCAG contrast thresholds

    Parameters
    ----------
    colors
        Character vector of hex codes.
    bg
        Reference background hex(es). Pass a single value (e.g. "#ffffff") or a vector (e.g. c("#ffffff", "#1a1a1a")) to verify against multiple backgrounds. Returns one row per (color, bg) pair.
    level
        "AA" (4.5:1) or "AAA" (7:1). Use "AA-large" (3:1) for non-text elements such as data marks, axis lines, and focus rings.
    alpha
        Opacity in [0, 1]. 1 (default) checks the raw color. Values below 1 composite each color over bg first, then check the rendered result -- useful when chart geoms use alpha < 1.

    Returns
    -------
        Data frame with columns color, bg, alpha, rendered, ratio, status.
    """
    if level not in _levels:
        raise ValueError(f"level must be one of {sorted(_levels)}")
    threshold = _levels[level]
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
