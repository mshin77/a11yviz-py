"""Validate alt-text presence and length (WCAG 1.1.1)."""

import warnings
from typing import Optional


def a11y_check_alt_text(alt_text: Optional[str],
                        element_type: str = "image",
                        decorative: bool = False,
                        min_length: int = 10) -> bool:
    """Check alt-text presence and length (WCAG 1.1.1)

    Parameters
    ----------
    alt_text
        Character or NULL. Candidate alt text.
    element_type
        Character. Element type for the warning, e.g. "plot".
    decorative
        Logical. If TRUE, empty alt text is allowed.
    min_length
        Integer. Minimum length for informative alt text (default 10).

    Returns
    -------
        TRUE if valid; FALSE with a warning otherwise.
    """
    if decorative:
        return True
    if alt_text is None or alt_text == "":
        warnings.warn(f"Missing alt text for {element_type} (WCAG 1.1.1)",
                      stacklevel=2)
        return False
    if len(alt_text) < min_length:
        warnings.warn(
            f"Alt text too short for {element_type} "
            f"(< {min_length} chars; consider more descriptive text)",
            stacklevel=2,
        )
        return False
    return True
