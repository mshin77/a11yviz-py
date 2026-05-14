"""WCAG 1.4.12 text-spacing ratios (reference data)."""


def a11y_text_spacing_ratios() -> dict:
    """Return WCAG 1.4.12 text-spacing ratios (multiples of font size)."""
    return {
        "line_height": 1.5,
        "paragraph":   2.0,
        "letter":      0.12,
        "word":        0.16,
    }
