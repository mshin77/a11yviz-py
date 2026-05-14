"""Add alt text to a plotly Figure."""


def a11y_alt_text(p, text: str):
    """Attach alt text to a figure for screen readers and audits."""
    p._a11y_alt = text
    try:
        p.update_layout(meta=dict(a11y_alt=text))
    except AttributeError:
        pass
    return p
