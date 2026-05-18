"""One-shot accessibility wrapper for plotnine or plotly figures."""

from typing import Optional

from a11yviz.a11y_alt_text import a11y_alt_text
from a11yviz.a11y_layout import a11y_layout
from a11yviz.scale_a11y import scale_color_a11y, scale_fill_a11y
from a11yviz.theme_a11y import theme_a11y


def make_a11y(p, level: str = "AA", palette: str = "dark2_8",
              alt: Optional[str] = None):
    """One-shot accessibility wrapper

    Parameters
    ----------
    p
        A ggplot or plotly object.
    level
        "AA" or "AAA".
    palette
        Categorical palette name passed to a11y_palette().
    alt
        Optional alt-text string.

    Returns
    -------
        The transformed object.
    """
    if _is_plotnine(p):
        p = p + theme_a11y(level=level)
        p = p + scale_color_a11y(palette=palette)
        p = p + scale_fill_a11y(palette=palette)
        if alt:
            p = a11y_alt_text(p, alt)
        return p
    if _is_plotly(p):
        p = a11y_layout(p, level=level, palette=palette)
        if alt:
            p = a11y_alt_text(p, alt)
        return p
    raise TypeError("make_a11y() supports plotnine and plotly objects.")


def _is_plotnine(p) -> bool:
    return type(p).__module__.startswith("plotnine")


def _is_plotly(p) -> bool:
    return type(p).__module__.startswith("plotly")
