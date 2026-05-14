"""Accessible plotnine theme."""

from a11yviz._constants import WCAG_RULES
from a11yviz._utils import check_level, require_pkg


def theme_a11y(level: str = "AA", base_family: str = "", dark: bool = False):
    """Plotnine theme with WCAG contrast settings and recommended font sizes."""
    pn = require_pkg("plotnine", "theme_a11y")
    level = check_level(level)
    fz = WCAG_RULES["font_size"][level]
    fg = "#dee2e6" if dark else "#222222"
    bg = "#2d2d2d" if dark else "#ffffff"
    grid = "#495057" if dark else "#e5e5e5"

    base = pn.theme_minimal(base_family=base_family, base_size=fz["body"])
    overrides = pn.theme(
        text=pn.element_text(color=fg, family=base_family),
        plot_title=pn.element_text(size=fz["body"], weight="bold", color=fg),
        plot_subtitle=pn.element_text(size=fz["body"], color=fg),
        axis_title=pn.element_text(size=fz["body"], color=fg),
        axis_text=pn.element_text(size=fz["body"], color=fg),
        legend_title=pn.element_text(size=fz["body"], color=fg),
        legend_text=pn.element_text(size=fz["body"], color=fg),
        strip_text=pn.element_text(size=fz["body"], color=fg),
        panel_background=pn.element_rect(fill=bg, color="none"),
        plot_background=pn.element_rect(fill=bg, color="none"),
        panel_grid_major=pn.element_line(color=grid),
        panel_grid_minor=pn.element_line(color=grid, size=0.25),
    )
    return base + overrides
