"""Locate the vendored a11yviz CSS file."""

from importlib.resources import files


def a11y_css() -> str:
    """Return the absolute path to the bundled a11yviz CSS."""
    return str(files("a11yviz.data").joinpath("a11yviz.css"))


def a11y_css_contents() -> str:
    """Return the CSS file contents as a string for inline embedding."""
    return files("a11yviz.data").joinpath("a11yviz.css").read_text(encoding="utf-8")
