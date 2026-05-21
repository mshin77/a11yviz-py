"""Smoke tests covering the public API surface."""

import os
import textwrap

import pytest

plotly = pytest.importorskip("plotly")
import plotly.express as px
import plotly.graph_objects as go

from a11yviz._constants import diverging, palettes, sequential, wcag_rules
from a11yviz import (
    a11y_alt_text,
    a11y_announce,
    a11y_aria_label,
    a11y_audit,
    a11y_audit_actionable,
    a11y_audit_chart,
    a11y_audit_doc,
    a11y_audit_summary,
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
    a11y_wcag_url,
    make_a11y,
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


def test_a11y_css_shiny_returns_two_paths():
    paths = a11y_css(mode="shiny")
    assert len(paths) == 2
    assert all(os.path.exists(p) for p in paths)
    assert paths[0].endswith("a11yviz.css")
    assert paths[1].endswith("a11yviz-shiny.css")


def test_a11y_css_contents_shiny_includes_addon_rules():
    css = a11y_css_contents(mode="shiny")
    assert ".skip-link" in css
    assert "prefers-reduced-motion" in css
    assert "prefers-contrast" in css


def test_a11y_css_invalid_mode():
    with pytest.raises(ValueError):
        a11y_css(mode="bogus")
    with pytest.raises(ValueError):
        a11y_css_contents(mode="bogus")


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


def test_a11y_layout_transparent_paper(fig):
    out = a11y_layout(fig)
    assert out.layout.paper_bgcolor.replace(" ", "") == "rgba(0,0,0,0)"
    assert out.layout.plot_bgcolor.replace(" ", "")  == "rgba(0,0,0,0)"


def test_a11y_layout_applies_palette_colorway(fig):
    out = a11y_layout(fig, palette="dark2_8")
    assert list(out.layout.colorway) == a11y_palette("dark2_8")


def test_a11y_layout_palette_none_leaves_colorway_unset(fig):
    out = a11y_layout(fig, palette=None)
    assert not out.layout.colorway


# alt text / ARIA / describe ----------------------------------------------

def test_a11y_alt_text_round_trip(fig):
    out = a11y_alt_text(fig, "Scatter of x vs y.")
    assert out._a11y_alt == "Scatter of x vs y."


def test_a11y_aria_label():
    assert a11y_aria_label("button", "analyze", "readability") == "Analyze readability button"
    assert a11y_aria_label("input", "search") == "Search input"


def test_a11y_aria_label_no_context():
    assert a11y_aria_label("button", "analyze") == "Analyze button"


def test_a11y_describe_uses_backend(fig):
    out = a11y_describe(fig, backend=lambda ctx: f"chart={ctx['chart_type']}")
    assert out._a11y_alt.startswith("chart=")


def test_a11y_alt_template(fig):
    fig.update_layout(xaxis_title="X", yaxis_title="Y")
    template = a11y_alt_template(fig)
    assert "[REPLACE" in template
    assert "X" in template and "Y" in template


def test_a11y_announce():
    out = a11y_announce("Loading")
    assert 'class="screen-reader-only"' in out and 'aria-live="polite"' in out
    assert ">Loading<" in out


def test_a11y_announce_role_status():
    assert 'role="status"' in a11y_announce("Loading")


# palettes ----------------------------------------------------------------

def test_a11y_palette_truncation():
    assert len(a11y_palette("dark2_8", n=3)) == 3


def test_a11y_palette_dark2_8_full():
    cols = a11y_palette("dark2_8")
    assert len(cols) == 8
    assert cols[0].upper() == "#1B9E77"


def test_a11y_palette_aaa_5_literal():
    assert a11y_palette("aaa_5") == [
        "#154E8A", "#7C2C5E", "#5C5108", "#8A3A1F", "#2D5C53",
    ]


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


def test_a11y_palette_list_columns():
    rows = a11y_palette_list()
    assert all({"name", "type", "n", "safe_on", "purpose"} <= r.keys() for r in rows)


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


def test_a11y_palette_seq_keys():
    spec = a11y_palette_seq("cividis")
    assert set(spec.keys()) == {"option", "begin", "end", "direction"}


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


def test_a11y_wcag_url_all_rubric_resolve():
    crits = [r["criterion"] for r in a11y_rubric()]
    urls = a11y_wcag_url(crits)
    assert all("#" in u for u in urls)


def test_a11y_rubric_filter():
    all_rows = a11y_rubric()
    aaa_rows = a11y_rubric(level="AAA")
    assert len(aaa_rows) == len(all_rows)
    aa_rows = a11y_rubric(level="AA")
    assert all(r["level"] != "AAA" for r in aa_rows)


def test_a11y_rubric_full_default():
    rb = a11y_rubric()
    assert len(rb) == 15
    expected = {"1.1.1", "1.3.1", "1.4.1", "1.4.3", "1.4.4",
                "1.4.6", "1.4.10", "1.4.11", "1.4.12", "1.4.13",
                "2.4.6", "2.4.7", "2.4.10", "3.1.5", "4.1.3"}
    assert {r["criterion"] for r in rb} == expected


def test_a11y_rubric_columns():
    assert set(a11y_rubric()[0].keys()) == {
        "criterion", "name", "level",
        "threshold_aa", "threshold_aaa", "a11yviz_function",
    }


# audit and checks --------------------------------------------------------

def test_a11y_audit_returns_rows(fig):
    rows = a11y_audit(a11y_plotly(fig, alt="demo plot"))
    criteria = [r["criterion"] for r in rows]
    assert "1.1.1" in criteria and "2.4.7" in criteria


def test_a11y_audit_aaa_extra_row(fig):
    rows = a11y_audit(a11y_plotly(fig), level="AAA")
    assert any(r["criterion"] == "1.4.6" for r in rows)


def test_a11y_audit_empty_alt_todo():
    rows = a11y_audit(go.Figure())
    alt_row = next(r for r in rows if r["check"] == "Alt text on figure")
    assert alt_row["status"] == "todo"


def test_a11y_audit_partial_after_alt_text():
    fig = a11y_alt_text(go.Figure(), "An empty figure used in tests.")
    rows = a11y_audit(fig)
    alt_row = next(r for r in rows if r["check"] == "Alt text on figure")
    assert alt_row["status"] == "partial"
    assert alt_row["note"]


def test_a11y_audit_row_counts():
    fig = go.Figure()
    assert len(a11y_audit(fig, level="AA"))  == 11
    assert len(a11y_audit(fig, level="AAA")) == 12


def test_a11y_audit_columns():
    rows = a11y_audit(go.Figure())
    assert list(rows[0].keys()) == ["criterion", "check", "status", "note"]


def test_a11y_audit_criteria_match_wcag():
    fig = go.Figure()
    aa = {"1.1.1", "1.3.1", "1.4.1", "1.4.3", "1.4.4",
          "1.4.10", "1.4.11", "1.4.12", "1.4.13", "2.4.7"}
    assert {r["criterion"] for r in a11y_audit(fig, level="AA")}  == aa
    assert {r["criterion"] for r in a11y_audit(fig, level="AAA")} == aa | {"1.4.6"}


def test_a11y_audit_chart_returns_chart_rows():
    fig = go.Figure()
    assert len(a11y_audit_chart(fig, level="AA"))  == 6
    assert len(a11y_audit_chart(fig, level="AAA")) == 7
    assert {r["criterion"] for r in a11y_audit_chart(fig)} == {
        "1.1.1", "1.4.1", "1.4.3", "1.4.4", "1.4.11", "1.4.13"
    }


def test_a11y_audit_doc_returns_doc_rows():
    rows = a11y_audit_doc()
    assert len(rows) == 5
    assert {r["criterion"] for r in rows} == {
        "1.3.1", "1.4.4", "1.4.10", "1.4.12", "2.4.7"
    }


def test_a11y_audit_actionable_keeps_todo_and_ok():
    rows = a11y_audit_actionable(a11y_audit(go.Figure()))
    assert all(r["status"] in ("todo", "ok") for r in rows)


def test_a11y_audit_summary_is_one_sentence():
    msg = a11y_audit_summary(a11y_audit(go.Figure()))
    assert "to do" in msg and "ok" in msg and "already handled" in msg


def test_a11y_check_alt_text_valid():
    assert a11y_check_alt_text("Bar chart showing word frequency", "plot")


def test_a11y_check_alt_text_missing_warns():
    with pytest.warns():
        assert not a11y_check_alt_text("", "plot")


def test_a11y_check_alt_text_decorative_ok():
    assert a11y_check_alt_text("", "icon", decorative=True)


def test_a11y_check_alt_text_none_warns():
    with pytest.warns():
        assert not a11y_check_alt_text(None, "image")


def test_a11y_check_alt_text_short_warns():
    with pytest.warns(match="too short"):
        assert not a11y_check_alt_text("short", "image")


def test_a11y_check_alt_text_min_length_configurable():
    assert a11y_check_alt_text("abc", "image", min_length=3)


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


def test_a11y_check_palette_black_high_ratio():
    rows = a11y_check_palette(["#000000"], bg="#ffffff", level="AA")
    assert rows[0]["status"] == "ok"
    assert rows[0]["ratio"] > 20


def test_a11y_check_palette_aaa_rejects_aa_only():
    rows = a11y_check_palette(["#0072B2"], bg="#ffffff", level="AAA")
    assert rows[0]["status"] == "todo"


def test_a11y_check_palette_columns():
    rows = a11y_check_palette(["#000000", "#ffffff", "#888888"])
    assert len(rows) == 3
    assert set(rows[0].keys()) == {"color", "bg", "alpha", "rendered", "ratio", "status"}


def test_a11y_check_palette_aa_large_threshold():
    rows_large = a11y_check_palette(["#888888"], bg="#ffffff", level="AA-large")
    rows_aa    = a11y_check_palette(["#888888"], bg="#ffffff", level="AA")
    assert rows_large[0]["status"] == "ok"
    assert rows_aa[0]["status"]    == "todo"


def test_a11y_check_palette_alpha_one_unchanged():
    rows = a11y_check_palette(["#000000"], bg="#ffffff", alpha=1.0)
    assert rows[0]["rendered"].lower() == "#000000"
    assert rows[0]["alpha"] == 1.0


def test_a11y_check_palette_alpha_half_grey():
    rows = a11y_check_palette(["#000000"], bg="#ffffff", alpha=0.5)
    assert rows[0]["rendered"].lower() in {"#808080", "#7f7f7f"}


def test_a11y_check_palette_alpha_lowers_contrast():
    full  = a11y_check_palette(["#0072B2"], bg="#ffffff", alpha=1.0)[0]["ratio"]
    faded = a11y_check_palette(["#0072B2"], bg="#ffffff", alpha=0.4)[0]["ratio"]
    assert faded < full


def test_a11y_check_palette_dual_bg_both_ok():
    rows = a11y_check_palette(["#0072B2"], bg=["#ffffff", "#1a1a1a"], level="AA-large")
    assert len(rows) == 2
    assert all(r["status"] == "ok" for r in rows)


def test_a11y_check_palette_size():
    assert a11y_check_palette_size(5)["status"] == "ok"
    assert a11y_check_palette_size(12)["status"] == "todo"


def test_a11y_check_palette_size_custom_max():
    assert a11y_check_palette_size(8, max=10)["status"] == "ok"


def test_a11y_check_separability_pairs():
    rows = a11y_check_separability(["#1B9E77", "#D95F02", "#7570B3"])
    assert len(rows) == 3
    assert {r["status"] for r in rows} <= {"ok", "todo"}


def test_a11y_check_separability_identical():
    rows = a11y_check_separability(["#1B9E77", "#1B9E77"])
    assert rows[0]["ratio"] == 1
    assert rows[0]["status"] == "todo"


def test_a11y_check_separability_widely_spaced():
    rows = a11y_check_separability(["#000000", "#FFFFFF"])
    assert rows[0]["ratio"] > 20
    assert rows[0]["status"] == "ok"


def test_a11y_check_separability_min_ratio_configurable():
    permissive = a11y_check_separability(["#666666", "#777777"], min_ratio=1)
    strict     = a11y_check_separability(["#666666", "#777777"], min_ratio=3)
    assert permissive[0]["status"] == "ok"
    assert strict[0]["status"]     == "todo"


def test_a11y_check_separability_default_threshold():
    rows = a11y_check_separability(["#000000", "#888888"])
    assert rows[0]["ratio"] >= 3
    assert rows[0]["status"] == "ok"


def test_a11y_check_tabindex_ok():
    assert a11y_check_tabindex(0)
    assert a11y_check_tabindex(-1)


def test_a11y_check_tabindex_high_warns():
    with pytest.warns():
        assert not a11y_check_tabindex(999)


def test_a11y_check_tabindex_non_numeric_warns():
    with pytest.warns():
        assert not a11y_check_tabindex("a")


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


# make_a11y on plotly -----------------------------------------------------

def test_make_a11y_plotly_attaches_alt(fig):
    out = make_a11y(fig, level="AA", alt="Test scatter.")
    assert out._a11y_alt == "Test scatter."


def test_make_a11y_plotly_forwards_palette(fig):
    out = make_a11y(fig, level="AA", palette="set2_8")
    assert list(out.layout.colorway) == a11y_palette("set2_8")


def test_make_a11y_unknown_type_errors():
    with pytest.raises(TypeError):
        make_a11y(123)


# wcag rules constants (replaces R rules_yaml test) -----------------------

def test_wcag_rules_top_level_keys():
    assert {"contrast", "font_size", "tooltip", "overlay_presets"} <= set(wcag_rules)
    assert set(wcag_rules["contrast"]) == {"AA", "AAA"}


def test_wcag_font_sizes_per_level():
    assert wcag_rules["font_size"]["AA"]["body"]  == 12
    assert wcag_rules["font_size"]["AAA"]["body"] == 14
    assert wcag_rules["font_size"]["AA"]["axis_text"]  == 10
    assert wcag_rules["font_size"]["AAA"]["axis_text"] == 12


def test_palette_constants_cover_families():
    assert "dark2_8" in palettes
    assert "rdbu"    in diverging
    assert "cividis" in sequential
