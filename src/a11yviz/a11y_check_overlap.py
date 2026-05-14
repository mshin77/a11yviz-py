"""Scatter overlap check for plotly figures (WCAG 1.3.1 / 1.4.11)."""


def a11y_check_overlap(p, bins: int = 100) -> dict:
    """Bin scatter coordinates and report the fraction sharing a grid cell."""
    xs, ys = _collect_scatter_points(p)
    total = len(xs)
    if total == 0:
        return {"total": 0, "obscured": 0, "fraction": 0.0,
                "recommendation": "no scatter points to evaluate"}

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    x_span = (x_max - x_min) or 1.0
    y_span = (y_max - y_min) or 1.0

    counts: dict[tuple[int, int], int] = {}
    for x, y in zip(xs, ys):
        ix = min(int((x - x_min) / x_span * bins), bins - 1)
        iy = min(int((y - y_min) / y_span * bins), bins - 1)
        counts[(ix, iy)] = counts.get((ix, iy), 0) + 1

    obscured = sum(c for c in counts.values() if c > 1)
    fraction = round(obscured / total, 3)
    if obscured == 0:
        rec = "no alpha needed (no occlusion; WCAG 1.3.1 satisfied)"
    else:
        rec = (f"{round(fraction * 100)}% of points share a grid cell; if alpha is "
               "added, verify composited contrast >= 3:1 via "
               "a11y_check_palette(alpha=...) (WCAG 1.4.11)")
    return {"total": total, "obscured": obscured,
            "fraction": fraction, "recommendation": rec}


def _collect_scatter_points(p):
    xs: list[float] = []
    ys: list[float] = []
    for trace in getattr(p, "data", ()) or ():
        if (getattr(trace, "type", None) or "scatter") != "scatter":
            continue
        mode = getattr(trace, "mode", None) or "markers"
        if "markers" not in mode:
            continue
        tx = getattr(trace, "x", None)
        ty = getattr(trace, "y", None)
        if tx is None or ty is None:
            continue
        for x, y in zip(tx, ty):
            if x is None or y is None:
                continue
            try:
                xs.append(float(x))
                ys.append(float(y))
            except (TypeError, ValueError):
                continue
    return xs, ys
