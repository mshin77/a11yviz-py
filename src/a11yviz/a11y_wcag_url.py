"""WCAG 2.1 specification URLs for success criteria."""

from typing import Sequence, Union

from a11yviz._constants import WCAG_SLUG

_BASE = "https://www.w3.org/TR/WCAG21/"


def a11y_wcag_url(criterion: Union[str, Sequence[str]]):
    """Return a spec deep link for one or more success criteria."""
    if isinstance(criterion, str):
        return _url(criterion)
    return [_url(c) for c in criterion]


def _url(criterion: str) -> str:
    slug = WCAG_SLUG.get(criterion)
    return _BASE if slug is None else f"{_BASE}#{slug}"
