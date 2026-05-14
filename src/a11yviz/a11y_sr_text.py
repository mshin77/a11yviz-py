"""Wrap text for screen readers (visually hidden, announced live)."""


def a11y_sr_text(text: str) -> str:
    """Return a `<span class="sr-only" role="status" aria-live="polite">` wrapper."""
    return (
        '<span class="sr-only" role="status" aria-live="polite">'
        f"{text}"
        "</span>"
    )
