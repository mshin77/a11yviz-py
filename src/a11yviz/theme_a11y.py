"""Accessible plotnine theme."""

from a11yviz._constants import wcag_rules
from a11yviz._utils import check_level, require_pkg


def theme_a11y(level: str = "AA", base_family: str = "DejaVu Sans", dark: bool = False):
    """Accessible plotnine theme. Title, axis title, and legend sit at the body floor (12 pt AA / 14 pt AAA); axis tick text drops 2 pt below.

    Parameters
    ----------
    level
        WCAG contrast level: "AA" (default) or "AAA". The level controls contrast targets and the package's default font sizes; only the contrast targets are WCAG-defined.
    base_family
        Font family. Defaults to system sans.
    dark
        Logical; if TRUE, use a dark-mode palette appropriate for darkly-style themes.

    Returns
    -------
        A theme object.
    """
    pn = require_pkg("plotnine", "theme_a11y")
    level = check_level(level)
    fz = wcag_rules["font_size"][level]
    axis_sz = fz.get("axis_text", fz["body"])
    fg = "#dee2e6" if dark else "#222222"
    bg = "#2d2d2d" if dark else "#ffffff"
    grid = "#495057" if dark else "#e5e5e5"

    base = pn.theme_minimal(base_family=base_family, base_size=fz["body"])
    overrides = pn.theme(
        text=pn.element_text(color=fg, family=base_family),
        plot_title=pn.element_text(size=fz["body"], weight="bold", color=fg),
        plot_subtitle=pn.element_text(size=fz["body"], color=fg),
        axis_title=pn.element_text(size=fz["body"], color=fg),
        axis_text=pn.element_text(size=axis_sz, color=fg),
        legend_title=pn.element_text(size=fz["body"], color=fg),
        legend_text=pn.element_text(size=fz["body"], color=fg),
        strip_text=pn.element_text(size=fz["body"], color=fg),
        panel_background=pn.element_rect(fill=bg, color="none"),
        plot_background=pn.element_rect(fill=bg, color="none"),
        panel_grid_major=pn.element_line(color=grid),
        panel_grid_minor=pn.element_line(color=grid, size=0.25),
    )
    return base + overrides
