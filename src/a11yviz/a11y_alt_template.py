"""Emit a deterministic alt-text template for a plotly Figure."""

from typing import Optional

from a11yviz._utils import coalesce


def a11y_alt_template(p) -> str:
    """Return a sentence scaffold pre-filled with chart type and axis labels."""
    return _alt_template_plotly(p)


def _alt_template_plotly(p) -> str:
    layout = getattr(p, "layout", None)
    data = getattr(p, "data", ()) or ()
    trace_types = []
    for t in data:
        kind = getattr(t, "type", None) or "scatter"
        mode = getattr(t, "mode", None)
        trace_types.append(f"scatter:{mode}" if kind == "scatter" and mode else kind)
    chart_type = _plotly_phrase(trace_types[0]) if trace_types else "Plot"

    x_lab = coalesce(_axis_title(getattr(layout, "xaxis", None)), "x")
    y_lab = coalesce(_axis_title(getattr(layout, "yaxis", None)), "y")

    parts = [f"{chart_type} of {y_lab} versus {x_lab}."]
    if len(data) > 1:
        parts.append(f"{len(data)} traces.")
    parts.append("[REPLACE - describe the substantive trend.]")
    return " ".join(parts)


def _plotly_phrase(t: str) -> str:
    return {
        "scatter":               "Scatter plot",
        "scatter:markers":       "Scatter plot",
        "scatter:lines":         "Line plot",
        "scatter:lines+markers": "Line plot with markers",
        "bar":                   "Bar chart",
        "heatmap":               "Heatmap",
        "contour":               "Contour plot",
        "box":                   "Boxplot",
        "violin":                "Violin plot",
        "histogram":             "Histogram",
        "surface":               "3-D surface plot",
    }.get(t, "Plot")


def _axis_title(axis) -> Optional[str]:
    if axis is None:
        return None
    title = getattr(axis, "title", None)
    if title is None:
        return None
    text = getattr(title, "text", None)
    return text or None
