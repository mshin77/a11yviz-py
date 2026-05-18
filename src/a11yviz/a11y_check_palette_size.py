"""Flag categorical palettes above the recommended maximum."""


def a11y_check_palette_size(n: int, max: int = 7) -> dict:
    """Flag categorical palettes above the recommended maximum

    Parameters
    ----------
    n
        Integer; number of categories.
    max
        Integer; recommended maximum. Default 7.

    Returns
    -------
        Named list with n, max, status ("ok" / "todo"), note.
    """
    ok = n <= max
    note = (f"{n} categories within recommended max {max}" if ok
            else f"{n} categories exceeds recommended max {max}; "
                 "consider faceting or aggregation")
    return {"n": n, "max": max, "status": "ok" if ok else "todo", "note": note}
