"""Accessible discrete color and fill scales for plotnine."""

from a11yviz._utils import require_pkg
from a11yviz.a11y_palette import a11y_palette


def scale_color_a11y(palette: str = "dark2_8", **kwargs):
    """Categorical color scale using a WCAG-tagged palette."""
    pn = require_pkg("plotnine", "scale_color_a11y")
    return pn.scale_color_manual(values=a11y_palette(palette), **kwargs)


def scale_fill_a11y(palette: str = "dark2_8", **kwargs):
    """Categorical fill scale using a WCAG-tagged palette."""
    pn = require_pkg("plotnine", "scale_fill_a11y")
    return pn.scale_fill_manual(values=a11y_palette(palette), **kwargs)
