"""Alpha presets for chart layers (mirror of WCAG_RULES.overlay_presets)."""

from a11yviz._constants import WCAG_RULES


def a11y_alpha_presets() -> dict:
    """Return a dict of named alpha presets for chart layers."""
    return dict(WCAG_RULES["overlay_presets"])
