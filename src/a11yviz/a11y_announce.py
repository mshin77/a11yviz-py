"""Wrap text in a live region for screen-reader-only announcement."""


def a11y_announce(text: str) -> str:
    """Announce a status message to assistive technology

    Parameters
    ----------
    text
        Character. Message to announce.

    Returns
    -------
        Character scalar containing HTML.
    """
    return (
        '<span class="screen-reader-only" role="status" aria-live="polite">'
        f"{text}"
        "</span>"
    )
