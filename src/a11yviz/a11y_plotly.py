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
    """Accessible plotly wrapper (Python version of R's a11y_ggplotly)

    Python plotnine has no equivalent native plotly converter, so this
    function operates on a plotly Figure directly rather than converting
    from plotnine.

    Parameters
    ----------
    p
        A plotly Figure.
    level
        WCAG contrast level: "AA" (default) or "AAA".
    palette
        Optional palette name applied as plotly's colorway. None (default)
        keeps the figure's existing scale.
    alt
        Alt-text override. When None, inherited from the figure's
        attached alt text.
    strip_title
        Logical; when True (default) drops title so the host page heading
        is authoritative.

    Returns
    -------
        A plotly Figure with a11y layout and optional alt text applied.
    """
    carried_alt = alt if alt is not None else getattr(p, "_a11y_alt", None)
    if strip_title:
        p.update_layout(title=None)
    p = a11y_layout(p, level=level, palette=palette)
    if carried_alt:
        p = a11y_alt_text(p, carried_alt)
    return p
