"""Smoke tests for the plotnine-side scales, theme, and make_a11y."""

import pytest

pn = pytest.importorskip("plotnine")
import pandas as pd

from a11yviz import (
    a11y_palette,
    a11y_palette_div,
    a11y_palette_seq,
    a11y_show_palette,
    make_a11y,
    scale_color_a11y,
    scale_color_a11y_div,
    scale_color_a11y_seq,
    scale_fill_a11y,
    scale_fill_a11y_div,
    scale_fill_a11y_seq,
    theme_a11y,
)


@pytest.fixture
def gg():
    df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [1, 4, 9, 16],
                       "g": list("aabb")})
    return pn.ggplot(df, pn.aes("x", "y", color="g")) + pn.geom_point()


# theme --------------------------------------------------------------------

def test_theme_a11y_returns_theme():
    t = theme_a11y(level="AA")
    assert t is not None


def test_theme_a11y_dark_mode():
    t = theme_a11y(dark=True)
    assert t is not None


# discrete scales ----------------------------------------------------------

def test_scale_color_a11y_uses_palette():
    s = scale_color_a11y("dark2_8")
    cols = a11y_palette("dark2_8")
    assert list(s.palette(len(cols))) == cols


def test_scale_fill_a11y_uses_palette():
    s = scale_fill_a11y("set2_8")
    cols = a11y_palette("set2_8")
    assert list(s.palette(len(cols))) == cols


# diverging scales ---------------------------------------------------------

def test_scale_color_a11y_div():
    d = a11y_palette_div("rdbu")
    s = scale_color_a11y_div("rdbu")
    assert s is not None
    assert "low" in d and "high" in d


def test_scale_fill_a11y_div():
    s = scale_fill_a11y_div("coolwarm_aaa")
    assert s is not None


# sequential scales --------------------------------------------------------

def test_scale_color_a11y_seq():
    spec = a11y_palette_seq("cividis")
    s = scale_color_a11y_seq("cividis")
    assert s is not None
    assert spec["option"] == "cividis"


def test_scale_fill_a11y_seq():
    s = scale_fill_a11y_seq("viridis")
    assert s is not None


# composability + make_a11y -----------------------------------------------

def test_compose_scale_with_ggplot(gg):
    p = gg + scale_color_a11y("dark2_8")
    assert isinstance(p, pn.ggplot)


def test_compose_theme_with_ggplot(gg):
    p = gg + theme_a11y(level="AA")
    assert isinstance(p, pn.ggplot)


def test_make_a11y_plotnine(gg):
    p = make_a11y(gg, palette="dark2_8", alt="demo scatter")
    assert isinstance(p, pn.ggplot)
    assert p._a11y_alt == "demo scatter"


def test_make_a11y_unsupported_type():
    with pytest.raises(TypeError):
        make_a11y(object())


# a11y_show_palette --------------------------------------------------------

def test_a11y_show_palette_returns_ggplot():
    p = a11y_show_palette("dark2_8")
    assert isinstance(p, pn.ggplot)


def test_a11y_show_palette_aaa_level():
    p = a11y_show_palette("aaa_5", level="AAA")
    assert isinstance(p, pn.ggplot)
