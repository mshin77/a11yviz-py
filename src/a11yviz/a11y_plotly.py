"""Accessible plotly wrapper (Python version of R's a11y_ggplotly).

R's `a11y_ggplotly(gg)` accepts a ggplot, converts via `plotly::ggplotly()`,
then applies a11y layout. Python plotnine has no equivalent native plotly
converter, so `a11y_plotly()` operates on a plotly Figure directly. For a
plotnine plot, render it first or use `make_a11y()`, which dispatches on
type.
"""

from typing import Optional

from a11yviz.a11y_alt_text import a11y_alt_text
from a11yviz.a11y_layout import a11y_layout


def a11y_plotly(p, level: str = "AA", palette: Optional[str] = None,
                alt: Optional[str] = None, strip_title: bool = True):
    """One-call wrapper applying a11y layout and optional alt text.

    Pass ``palette=None`` (default) to preserve the figure's existing colors.
    Python version of R's `a11y_ggplotly()`; takes a plotly Figure rather
    than a ggplot (no native plotnine→plotly conversion in Python).
    """
    carried_alt = alt if alt is not None else getattr(p, "_a11y_alt", None)
    if strip_title:
        p.update_layout(title=None)
    p = a11y_layout(p, level=level, palette=palette)
    if carried_alt:
        p = a11y_alt_text(p, carried_alt)
    return p
