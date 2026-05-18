"""Accessible discrete color and fill scales for plotnine."""

from a11yviz._utils import require_pkg
from a11yviz.a11y_palette import a11y_palette


def _scale_a11y_palette(palette, level):
    return palette or ("aaa_5" if str(level).upper() == "AAA" else "dark2_8")


def scale_color_a11y(palette=None, level="AA", **kwargs):
    """Accessible discrete color and fill scales

    Parameters
    ----------
    palette
        One of "dark2_8" (default), "set2_8", "paired_12", "aaa_5". See a11y_palette_list().
    level
        WCAG contrast level. "AAA" switches the default palette to "aaa_5" (deep, AAA-on-white set). Ignored if palette is set explicitly.

    Returns
    -------
        A ggplot2 scale.
    """
    pn = require_pkg("plotnine", "scale_color_a11y")
    return pn.scale_color_manual(values=a11y_palette(_scale_a11y_palette(palette, level)), **kwargs)


def scale_fill_a11y(palette=None, level="AA", **kwargs):
    """Accessible discrete color and fill scales

    Parameters
    ----------
    palette
        One of "dark2_8" (default), "set2_8", "paired_12", "aaa_5". See a11y_palette_list().
    level
        WCAG contrast level. "AAA" switches the default palette to "aaa_5" (deep, AAA-on-white set). Ignored if palette is set explicitly.

    Returns
    -------
        A ggplot2 scale.
    """
    pn = require_pkg("plotnine", "scale_fill_a11y")
    return pn.scale_fill_manual(values=a11y_palette(_scale_a11y_palette(palette, level)), **kwargs)
