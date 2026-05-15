"""Accessible discrete color and fill scales for plotnine."""

from a11yviz._utils import require_pkg
from a11yviz.a11y_palette import a11y_palette


def _scale_a11y_palette(palette, level):
    return palette or ("aaa_5" if str(level).upper() == "AAA" else "dark2_8")


def scale_color_a11y(palette=None, level="AA", **kwargs):
    """Categorical color scale using a WCAG-tagged palette."""
    pn = require_pkg("plotnine", "scale_color_a11y")
    return pn.scale_color_manual(values=a11y_palette(_scale_a11y_palette(palette, level)), **kwargs)


def scale_fill_a11y(palette=None, level="AA", **kwargs):
    """Categorical fill scale using a WCAG-tagged palette."""
    pn = require_pkg("plotnine", "scale_fill_a11y")
    return pn.scale_fill_manual(values=a11y_palette(_scale_a11y_palette(palette, level)), **kwargs)
