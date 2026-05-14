"""Smoke tests covering the public API surface."""

import os
import textwrap

import pytest

plotly = pytest.importorskip("plotly")
import plotly.express as px

from a11yviz import (
    a11y_alt_text,
    a11y_aria_label,
    a11y_audit,
    a11y_check_headings,
    a11y_check_palette,
    a11y_check_readability,
    a11y_check_separability,
    a11y_css,
    a11y_css_contents,
    a11y_describe,
    a11y_layout,
    a11y_palette,
    a11y_palette_div,
    a11y_palette_info,
    a11y_palette_list,
    a11y_palette_seq,
    a11y_plotly,
    a11y_rubric,
    a11y_sr_text,
    a11y_wcag_url,
)
from a11yviz import (
    a11y_alpha_presets,
    a11y_alt_template,
    a11y_check_alt_text,
    a11y_check_overlap,
    a11y_check_palette_size,
    a11y_check_tabindex,
    a11y_plotly_sequences,
    a11y_text_spacing_ratios,
)


@pytest.fixture
def fig():
    return px.scatter(x=[1, 2, 3, 4], y=[4, 5, 6, 5])


# css ---------------------------------------------------------------------

def test_a11y_css_exists():
    assert os.path.exists(a11y_css())


def test_a11y_css_contents_non_empty():
    assert ".js-plotly-plot" in a11y_css_contents()


# core plotly wrapper ------------------------------------------------------

def test_a11y_plotly_keeps_palette_when_none(fig):
    out = a11y_plotly(fig, palette=None)
    assert not out.layout.colorway


def test_a11y_plotly_applies_colorway_when_named(fig):
    out = a11y_plotly(fig, palette="dark2_8")
    assert list(out.layout.colorway) == a11y_palette("dark2_8")


def test_a11y_plotly_attaches_config(fig):
    out = a11y_plotly(fig)
    assert out._a11y_config["displaylogo"] is False


def test_a11y_layout_strips_title(fig):
    fig.update_layout(title="Some title")
    out = a11y_layout(fig, palette=None)
    fig.update_layout(title=None)
    assert out.layout.title.text is None or out.layout.title.text == ""


# alt text / ARIA / describe ----------------------------------------------

def test_a11y_alt_text_round_trip(fig):
    out = a11y_alt_text(fig, "Scatter of x vs y.")
    assert out._a11y_alt == "Scatter of x vs y."


def test_a11y_aria_label():
    assert a11y_aria_label("button", "analyze", "readability") == "Analyze readability button"
    assert a11y_aria_label("input", "search") == "Search input"


def test_a11y_describe_uses_backend(fig):
    out = a11y_describe(fig, backend=lambda ctx: f"chart={ctx['chart_type']}")
    assert out._a11y_alt.startswith("chart=")


def test_a11y_alt_template(fig):
    fig.update_layout(xaxis_title="X", yaxis_title="Y")
    template = a11y_alt_template(fig)
    assert "[REPLACE" in template
    assert "X" in template and "Y" in template


def test_a11y_sr_text():
    out = a11y_sr_text("Loading")
    assert 'class="sr-only"' in out and 'aria-live="polite"' in out
    assert ">Loading<" in out


# palettes ----------------------------------------------------------------

def test_a11y_palette_truncation():
    assert len(a11y_palette("dark2_8", n=3)) == 3


def test_a11y_palette_unknown():
    with pytest.raises(ValueError):
        a11y_palette("does_not_exist")


def test_a11y_palette_info_round_trip():
    info = a11y_palette_info("aaa_5")
    assert info["name"] == "aaa_5"
    assert len(info["colors"]) == 5


def test_a11y_palette_list_shape():
    rows = a11y_palette_list()
    assert all({"name", "n"} <= r.keys() for r in rows)


def test_a11y_palette_div_literal():
    out = a11y_palette_div("coolwarm_aaa")
    assert out == {"low": "#3b4cc0", "mid": "#ffffff", "high": "#b40426"}


def test_a11y_palette_div_brewer_positions():
    out = a11y_palette_div("rdbu")
    assert out["low"]  == "#2166AC"
    assert out["mid"]  == "#F7F7F7"
    assert out["high"] == "#B2182B"


def test_a11y_palette_div_dual_positions():
    out = a11y_palette_div("rdbu_dual")
    assert out["low"]  == "#4393C3"
    assert out["mid"]  == "#F7F7F7"
    assert out["high"] == "#D6604D"


def test_a11y_palette_seq_spec():
    spec = a11y_palette_seq("cividis")
    assert spec["option"] == "cividis"
    assert spec["begin"] == 0.0
    assert spec["end"] == 1.0


def test_a11y_palette_seq_materialize():
    hexes = a11y_palette_seq("viridis", n=5)
    assert len(hexes) == 5
    assert all(h.startswith("#") and len(h) == 7 for h in hexes)


# constants / rubric / URLs / spacing -------------------------------------

def test_a11y_alpha_presets():
    presets = a11y_alpha_presets()
    assert presets["raw_points"] == 0.4
    assert presets["fill"] == 0.9


def test_a11y_text_spacing_ratios():
    assert a11y_text_spacing_ratios()["line_height"] == 1.5


def test_a11y_wcag_url_single():
    assert a11y_wcag_url("1.4.3") == "https://www.w3.org/TR/WCAG21/#contrast-minimum"


def test_a11y_wcag_url_vector():
    urls = a11y_wcag_url(["1.1.1", "2.4.7"])
    assert urls[0].endswith("#non-text-content")
    assert urls[1].endswith("#focus-visible")


def test_a11y_wcag_url_unknown_falls_back():
    assert a11y_wcag_url("9.9.9") == "https://www.w3.org/TR/WCAG21/"


def test_a11y_rubric_filter():
    all_rows = a11y_rubric()
    aaa_rows = a11y_rubric(level="AAA")
    assert len(aaa_rows) == len(all_rows)
    aa_rows = a11y_rubric(level="AA")
    assert all(r["level"] != "AAA" for r in aa_rows)


# audit and checks --------------------------------------------------------

def test_a11y_audit_returns_rows(fig):
    rows = a11y_audit(a11y_plotly(fig, alt="demo plot"))
    criteria = [r["criterion"] for r in rows]
    assert "1.1.1" in criteria and "2.4.7" in criteria


def test_a11y_audit_aaa_extra_row(fig):
    rows = a11y_audit(a11y_plotly(fig), level="AAA")
    assert any(r["criterion"] == "1.4.6" for r in rows)


def test_a11y_check_alt_text_valid():
    assert a11y_check_alt_text("Bar chart showing word frequency", "plot")


def test_a11y_check_alt_text_missing_warns():
    with pytest.warns():
        assert not a11y_check_alt_text("", "plot")


def test_a11y_check_alt_text_decorative_ok():
    assert a11y_check_alt_text("", "icon", decorative=True)


def test_a11y_check_palette_pass_fail():
    rows = a11y_check_palette(["#000000", "#cccccc"], bg="#ffffff", level="AA")
    statuses = {r["color"]: r["status"] for r in rows}
    assert statuses["#000000"] == "ok"
    assert statuses["#cccccc"] == "todo"


def test_a11y_check_palette_multi_bg():
    rows = a11y_check_palette(["#0072B2"], bg=["#ffffff", "#1a1a1a"], level="AA-large")
    bgs = sorted({r["bg"] for r in rows})
    assert bgs == ["#1a1a1a", "#ffffff"]


def test_a11y_check_palette_alpha_composites():
    rows = a11y_check_palette(["#0072B2"], bg="#ffffff", level="AA-large", alpha=0.5)
    assert rows[0]["rendered"] != "#0072B2"
    assert rows[0]["alpha"] == 0.5


def test_a11y_check_palette_size():
    assert a11y_check_palette_size(5)["status"] == "ok"
    assert a11y_check_palette_size(12)["status"] == "todo"


def test_a11y_check_separability_pairs():
    rows = a11y_check_separability(["#1B9E77", "#D95F02", "#7570B3"])
    assert len(rows) == 3
    assert {r["status"] for r in rows} <= {"ok", "todo"}


def test_a11y_check_tabindex_ok():
    assert a11y_check_tabindex(0)
    assert a11y_check_tabindex(-1)


def test_a11y_check_tabindex_high_warns():
    with pytest.warns():
        assert not a11y_check_tabindex(999)


def test_a11y_check_overlap_scatter(fig):
    res = a11y_check_overlap(fig)
    assert res["total"] == 4
    assert res["obscured"] == 0


def test_a11y_check_readability_paragraph():
    out = a11y_check_readability("The cat sat on the mat. The dog ran away.")
    assert out["sentences"] == 2
    assert out["words"] >= 8
    assert out["flesch_kincaid_grade"] is not None


def test_a11y_check_readability_empty():
    out = a11y_check_readability("")
    assert out["flesch_kincaid_grade"] is None


def test_a11y_check_headings_skip(tmp_path):
    path = tmp_path / "doc.md"
    path.write_text(textwrap.dedent("""\
        ## Section
        #### Sub
        """))
    issues = a11y_check_headings(str(path))
    assert any("Level skip" in i["issue"] for i in issues)


def test_a11y_check_headings_clean(tmp_path):
    path = tmp_path / "doc.md"
    path.write_text(textwrap.dedent("""\
        ## Intro
        ### Background
        #### Detail
        """))
    assert a11y_check_headings(str(path)) == []


def test_a11y_check_headings_short(tmp_path):
    path = tmp_path / "doc.md"
    path.write_text("## A\n")
    issues = a11y_check_headings(str(path), min_chars=3)
    assert issues and "non-descriptive" in issues[0]["issue"]


# plotly sequences --------------------------------------------------------

def test_a11y_plotly_sequences_default():
    rows = a11y_plotly_sequences()
    assert all({"name", "min_ratio", "median_ratio", "pct_pass"} <= r.keys() for r in rows)
    assert rows == sorted(rows, key=lambda r: -r["pct_pass"])
