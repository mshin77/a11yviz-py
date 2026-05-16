"""Accessibility toolkit for plotnine, plotly, and Quarto Python documents."""

from a11yviz.a11y_alpha_presets import a11y_alpha_presets
from a11yviz.a11y_alt_template import a11y_alt_template
from a11yviz.a11y_alt_text import a11y_alt_text
from a11yviz.a11y_announce import a11y_announce
from a11yviz.a11y_aria_label import a11y_aria_label
from a11yviz.a11y_audit import (
    a11y_audit,
    a11y_audit_actionable,
    a11y_audit_chart,
    a11y_audit_doc,
    a11y_audit_summary,
)
from a11yviz.a11y_check_alt_text import a11y_check_alt_text
from a11yviz.a11y_check_headings import a11y_check_headings
from a11yviz.a11y_check_overlap import a11y_check_overlap
from a11yviz.a11y_check_palette import a11y_check_palette
from a11yviz.a11y_check_palette_size import a11y_check_palette_size
from a11yviz.a11y_check_readability import a11y_check_readability
from a11yviz.a11y_check_separability import a11y_check_separability
from a11yviz.a11y_check_tabindex import a11y_check_tabindex
from a11yviz.a11y_css import a11y_css, a11y_css_contents
from a11yviz.a11y_describe import a11y_describe
from a11yviz.a11y_layout import a11y_layout
from a11yviz.a11y_palette import a11y_palette, a11y_palette_info, a11y_palette_list
from a11yviz.a11y_palette_continuous import a11y_palette_div, a11y_palette_seq
from a11yviz.a11y_plotly import a11y_plotly
from a11yviz.a11y_plotly_sequences import a11y_plotly_sequences
from a11yviz.a11y_rubric import a11y_rubric
from a11yviz.a11y_show_palette import a11y_show_palette
from a11yviz.a11y_text_spacing import a11y_text_spacing_ratios
from a11yviz.a11y_wcag_url import a11y_wcag_url
from a11yviz.make_a11y import make_a11y
from a11yviz.run_app import run_app
from a11yviz.scale_a11y import scale_color_a11y, scale_fill_a11y
from a11yviz.scale_a11y_continuous import (
    scale_color_a11y_div, scale_color_a11y_seq,
    scale_fill_a11y_div, scale_fill_a11y_seq,
)
from a11yviz.theme_a11y import theme_a11y

__version__ = "0.1.4"

__all__ = [
    "a11y_alpha_presets",
    "a11y_alt_template",
    "a11y_alt_text",
    "a11y_announce",
    "a11y_aria_label",
    "a11y_audit",
    "a11y_audit_actionable",
    "a11y_audit_chart",
    "a11y_audit_doc",
    "a11y_audit_summary",
    "a11y_check_alt_text",
    "a11y_check_headings",
    "a11y_check_overlap",
    "a11y_check_palette",
    "a11y_check_palette_size",
    "a11y_check_readability",
    "a11y_check_separability",
    "a11y_check_tabindex",
    "a11y_css",
    "a11y_css_contents",
    "a11y_describe",
    "a11y_layout",
    "a11y_palette",
    "a11y_palette_info",
    "a11y_palette_list",
    "a11y_palette_div",
    "a11y_palette_seq",
    "a11y_plotly",
    "a11y_plotly_sequences",
    "a11y_rubric",
    "a11y_show_palette",
    "a11y_text_spacing_ratios",
    "a11y_wcag_url",
    "make_a11y",
    "run_app",
    "scale_color_a11y",
    "scale_fill_a11y",
    "scale_color_a11y_div",
    "scale_fill_a11y_div",
    "scale_color_a11y_seq",
    "scale_fill_a11y_seq",
    "theme_a11y",
]
