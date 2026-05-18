"""Add alt text to a plotly Figure."""


def a11y_alt_text(p, text: str):
    """Add alt text to a plot

    Parameters
    ----------
    p
        A plotly or ggplot object.
    text
        Character. Concise description for screen readers.

    Returns
    -------
        The object with alt text attached.
    """
    p._a11y_alt = text
    try:
        p.update_layout(meta=dict(a11y_alt=text))
    except AttributeError:
        pass
    return p
