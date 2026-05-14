"""Build an ARIA label string for an interactive element."""

from typing import Optional


def a11y_aria_label(element_type: str, action: str,
                    context: Optional[str] = None) -> str:
    """Return an ARIA label combining action, optional context, and element type."""
    parts = [action.title()]
    if context is not None:
        parts.append(context)
    parts.append(element_type)
    return " ".join(parts)
