"""Check that a tabindex value follows WCAG 2.1.1."""

import warnings
from numbers import Real


def a11y_check_tabindex(tabindex: float = 0) -> bool:
    """Check that a tabindex value follows WCAG 2.1.1

    Parameters
    ----------
    tabindex
        Numeric scalar.

    Returns
    -------
        TRUE if valid; FALSE with a warning if non-numeric or > 100.
    """
    if not isinstance(tabindex, Real) or isinstance(tabindex, bool):
        warnings.warn("tabindex must be numeric", stacklevel=2)
        return False
    if tabindex > 100:
        warnings.warn(
            "tabindex > 100 creates unpredictable tab order (WCAG 2.1.1)",
            stacklevel=2,
        )
        return False
    return True
