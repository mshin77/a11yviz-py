"""Smoke tests for a11y_minimum on plotnine and plotly."""

import pytest

pn = pytest.importorskip("plotnine")
import pandas as pd

from a11yviz import a11y_minimum
from a11yviz.a11y_audit import _font_size


@pytest.fixture
def gg():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 4, 9], "g": ["a", "b", "c"]})
    return pn.ggplot(df, pn.aes("x", "y", color="g")) + pn.geom_point()


def test_alt_text_attached_when_supplied(gg):
    out = a11y_minimum(gg, alt="demo")
    assert out._a11y_alt == "demo"


def test_no_alt_when_alt_is_none(gg):
    out = a11y_minimum(gg)
    assert not hasattr(out, "_a11y_alt")


def test_text_size_bumped_when_below_aa(gg):
    small = gg + pn.theme(text=pn.element_text(size=8))
    out = a11y_minimum(small, level="AA")
    assert _font_size(out) >= 12


def test_text_size_unchanged_when_already_ok(gg):
    big = gg + pn.theme(text=pn.element_text(size=16))
    out = a11y_minimum(big, level="AA")
    assert _font_size(out) == 16


def test_aaa_threshold_is_14(gg):
    small = gg + pn.theme(text=pn.element_text(size=11))
    out = a11y_minimum(small, level="AAA")
    assert _font_size(out) >= 14


def test_rejects_invalid_level(gg):
    with pytest.raises(ValueError):
        a11y_minimum(gg, level="A")
