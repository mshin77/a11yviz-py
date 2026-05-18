"""Generate alt text via a user-supplied LLM backend."""

from typing import Callable, Optional

from a11yviz._utils import coalesce
from a11yviz.a11y_alt_text import a11y_alt_text


def a11y_describe(p, backend: Callable[[dict], str], attach: bool = True):
    """Generate alt text via a user-supplied LLM backend

    Parameters
    ----------
    p
        A ggplot or plotly object.
    backend
        A function function(context) -> character(1). Receives a list with fields chart_type, title, x, y, color, n_observations. Returns a single string.
    attach
        If TRUE (default), attach via a11y_alt_text(). Otherwise return the string.

    Returns
    -------
        The plot with alt text attached, or the string itself.
    """
    context = _plot_context(p)
    text = backend(context)
    return a11y_alt_text(p, text) if attach else text


def _plot_context(p) -> dict:
    layout = getattr(p, "layout", None)
    data = getattr(p, "data", ()) or ()
    trace_types = []
    for t in data:
        kind = getattr(t, "type", None) or "scatter"
        mode = getattr(t, "mode", None)
        trace_types.append(f"scatter:{mode}" if kind == "scatter" and mode else kind)
    return {
        "chart_type": _plotly_phrase(trace_types[0]) if trace_types else "Plot",
        "title":     _title_text(getattr(layout, "title", None)),
        "x":         {"label": coalesce(_axis_title(getattr(layout, "xaxis", None)), "x")},
        "y":         {"label": coalesce(_axis_title(getattr(layout, "yaxis", None)), "y")},
        "n_traces":  len(data),
    }


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


def _title_text(title) -> Optional[str]:
    if title is None:
        return None
    t = getattr(title, "text", None)
    return t or None


def _axis_title(axis) -> Optional[str]:
    if axis is None:
        return None
    title = getattr(axis, "title", None)
    if title is None:
        return None
    text = getattr(title, "text", None)
    return text or None
