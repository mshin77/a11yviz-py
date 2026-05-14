"""Wrap text in a live region for screen-reader-only announcement."""


def a11y_announce(text: str) -> str:
    return (
        '<span class="screen-reader-only" role="status" aria-live="polite">'
        f"{text}"
        "</span>"
    )
