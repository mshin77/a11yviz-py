"""Locate or load the bundled a11yviz CSS files."""

from importlib.resources import files
from typing import Union


def a11y_css(mode: str = "default") -> Union[str, list[str]]:
    if mode == "default":
        return _path("a11yviz.css")
    if mode == "shiny":
        return [_path("a11yviz.css"), _path("a11yviz-shiny.css")]
    raise ValueError("mode must be 'default' or 'shiny'")


def a11y_css_contents(mode: str = "default") -> str:
    if mode == "default":
        return _read("a11yviz.css")
    if mode == "shiny":
        return _read("a11yviz.css") + "\n" + _read("a11yviz-shiny.css")
    raise ValueError("mode must be 'default' or 'shiny'")


def _path(name: str) -> str:
    return str(files("a11yviz.data").joinpath(name))


def _read(name: str) -> str:
    return files("a11yviz.data").joinpath(name).read_text(encoding="utf-8")
