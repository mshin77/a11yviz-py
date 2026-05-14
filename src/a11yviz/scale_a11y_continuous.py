"""Accessible diverging and sequential scales for plotnine."""

from a11yviz._utils import require_pkg
from a11yviz.a11y_palette_continuous import a11y_palette_div, a11y_palette_seq


def scale_color_a11y_div(palette: str = "rdbu", **kwargs):
    """Diverging color scale (gradient2)."""
    pn = require_pkg("plotnine", "scale_color_a11y_div")
    d = a11y_palette_div(palette)
    return pn.scale_color_gradient2(low=d["low"], mid=d["mid"], high=d["high"], **kwargs)


def scale_fill_a11y_div(palette: str = "rdbu", **kwargs):
    """Diverging fill scale (gradient2)."""
    pn = require_pkg("plotnine", "scale_fill_a11y_div")
    d = a11y_palette_div(palette)
    return pn.scale_fill_gradient2(low=d["low"], mid=d["mid"], high=d["high"], **kwargs)


def scale_color_a11y_seq(palette: str = "cividis", **kwargs):
    """Sequential continuous color scale (viridis-style)."""
    pn = require_pkg("plotnine", "scale_color_a11y_seq")
    s = a11y_palette_seq(palette)
    return pn.scale_color_cmap(cmap_name=s["option"], **kwargs)


def scale_fill_a11y_seq(palette: str = "cividis", **kwargs):
    """Sequential continuous fill scale (viridis-style)."""
    pn = require_pkg("plotnine", "scale_fill_a11y_seq")
    s = a11y_palette_seq(palette)
    return pn.scale_fill_cmap(cmap_name=s["option"], **kwargs)
