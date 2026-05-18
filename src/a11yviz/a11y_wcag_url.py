"""WCAG 2.1 specification URLs for success criteria."""

from typing import Sequence, Union

from a11yviz._constants import wcag_slug

_base = "https://www.w3.org/TR/WCAG21/"


def a11y_wcag_url(criterion: Union[str, Sequence[str]]):
    """WCAG 2.1 specification URL for a success criterion

    Parameters
    ----------
    criterion
        Character vector of success-criterion numbers (e.g., "1.4.3"). Recognised values are the chart-relevant subset returned by a11y_rubric().

    Returns
    -------
        Character vector of URLs the same length as criterion. Returns the spec root URL for unrecognised values.
    """
    if isinstance(criterion, str):
        return _url(criterion)
    return [_url(c) for c in criterion]


def _url(criterion: str) -> str:
    slug = wcag_slug.get(criterion)
    return _base if slug is None else f"{_base}#{slug}"
