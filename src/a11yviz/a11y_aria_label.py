"""Build an ARIA label string for an interactive element."""

from typing import Optional


def a11y_aria_label(element_type: str, action: str,
                    context: Optional[str] = None) -> str:
    """Build an ARIA label string

    Parameters
    ----------
    element_type
        Character. Element type, e.g. "button", "input".
    action
        Character. Action verb, e.g. "analyze", "download".
    context
        Character or NULL. Optional disambiguating context.

    Returns
    -------
        Character scalar suitable for aria-label.
    """
    parts = [action.title()]
    if context is not None:
        parts.append(context)
    parts.append(element_type)
    return " ".join(parts)
