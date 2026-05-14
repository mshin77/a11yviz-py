"""Alpha presets for chart layers (mirror of wcag_rules.overlay_presets)."""

from a11yviz._constants import wcag_rules


def a11y_alpha_presets() -> dict:
    """Return a dict of named alpha presets for chart layers."""
    return dict(wcag_rules["overlay_presets"])
