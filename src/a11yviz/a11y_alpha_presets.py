"""Alpha presets for chart layers (mirror of wcag_rules.overlay_presets)."""

from a11yviz._constants import wcag_rules


def a11y_alpha_presets() -> dict:
    """Alpha presets for chart layers

    Returns
    -------
        Named numeric vector with elements raw_points, overlay_point, labels, fill, ci_ribbon, ci_band.
    """
    presets = dict(wcag_rules["overlay_presets"])
    presets.pop("draw_order", None)
    return presets
