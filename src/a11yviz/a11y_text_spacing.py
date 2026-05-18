"""WCAG 1.4.12 text-spacing ratios (reference data)."""


def a11y_text_spacing_ratios() -> dict:
    """WCAG 1.4.12 text-spacing ratios (reference data)

    Returns
    -------
        Named numeric vector with line_height, paragraph, letter, word.
    """
    return {
        "line_height": 1.5,
        "paragraph":   2.0,
        "letter":      0.12,
        "word":        0.16,
    }
