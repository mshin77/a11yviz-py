"""Layer minimum accessibility onto a chart without replacing its visual."""

from typing import Optional

from a11yviz._constants import wcag_rules
from a11yviz._utils import check_level
from a11yviz.a11y_alt_text import a11y_alt_text
from a11yviz.a11y_audit import _font_size, _is_plotnine


def a11y_minimum(p, alt: Optional[str] = None, level: str = "AA"):
    """Layer minimum accessibility onto a chart

    Adds only the non-destructive moves: attaches alt text, and raises the
    base text size to the WCAG minimum only when the current size is below
    it. Palette, theme, legend, and geom aesthetics stay intact. Suitable
    for retrofitting charts with an existing visual; ``theme_a11y()`` and
    ``scale_color_a11y()`` are the greenfield path. Pair with
    :func:`a11y_audit_chart` to surface remaining gaps.

    Parameters
    ----------
    p
        A plotnine ``ggplot`` or plotly ``Figure``.
    alt
        Optional alt text attached via :func:`a11y_alt_text`.
    level
        ``"AA"`` (12 pt minimum) or ``"AAA"`` (14 pt minimum).

    Returns
    -------
        The chart with alt text attached (if supplied) and base text size
        raised to the level threshold when it was below.
    """
    level = check_level(level)
    threshold = wcag_rules["font_size"][level]["body"]
    size = _font_size(p)
    if alt:
        p = a11y_alt_text(p, alt)
    if isinstance(size, (int, float)) and size < threshold:
        if _is_plotnine(p):
            import plotnine as pn
            p = p + pn.theme(text=pn.element_text(size=threshold))
        elif hasattr(p, "update_layout"):
            p.update_layout(font=dict(size=threshold))
    return p
