"""Audit a plotly Figure or plotnine plot against WCAG 2.1."""

from typing import Optional

from a11yviz._constants import wcag_rules
from a11yviz._utils import check_level


def a11y_audit_chart(p, level: str = "AA") -> list[dict]:
    """Chart-only accessibility audit

    Parameters
    ----------
    p
        A plotly or ggplot object.
    level
        "AA" or "AAA".

    Returns
    -------
        Data frame with columns criterion, check, status, note.
    """
    level = check_level(level)
    alt_text = getattr(p, "_a11y_alt", None) or _meta_alt(p)
    has_alt = bool(alt_text)
    text  = _check_text_size(p, level)
    hover = _check_hover(p)
    color = _check_color_only(p)

    rows = [
        _row("1.1.1", "Alt text on figure",
             "partial" if has_alt else "todo",
             "alt stored on figure; emit via the renderer's <img alt> or save with explicit alt -- audit cannot verify the rendered output"
             if has_alt else "call a11y_alt_text() or a11y_alt_template()"),
        _row("1.4.1", "Redundant group encoding",
             color["status"], color["note"]),
        _row("1.4.3", "Text contrast (Min)",
             "applied", "theme_a11y() / a11y_layout() set 4.5:1 text on 3:1 non-text"),
        _row("1.4.4", f"Recommended text size ({level} default)",
             text["status"], text["note"]),
        _row("1.4.11", "Non-text contrast",
             "applied", "axis lines, gridlines, error bars styled"),
        _row("1.4.13", "Content on hover or focus",
             hover["status"], hover["note"]),
    ]
    if level == "AAA":
        rows.append(_row("1.4.6", "AAA text contrast",
                         "applied", "AAA contrast ratios applied"))
    return rows


def a11y_audit_doc(level: str = "AA") -> list[dict]:
    """Document-level accessibility audit

    Parameters
    ----------
    level
        "AA" or "AAA". Doc-level rows are identical for both.

    Returns
    -------
        Data frame with columns criterion, check, status, note.
    """
    check_level(level)
    return [
        _row("1.3.1", "Heading hierarchy",
             "doc", "run a11y_check_headings() on the host document"),
        _row("1.4.4", "Text resizable",
             "applied", "fonts set in pt; layout scales with container"),
        _row("1.4.10", "Reflow at 320 CSS px",
             "manual", "verify the host page reflows at 320 px without 2D scroll; "
                       "a11y_css() ships @media rules"),
        _row("1.4.12", "Body text spacing",
             "css", "include a11y_css() for line-height and paragraph spacing"),
        _row("2.4.7", "Visible keyboard focus",
             "css", "include a11y_css() for keyboard focus rings"),
    ]


def a11y_audit(p, level: str = "AA") -> list[dict]:
    """Chart + document accessibility audit

    Parameters
    ----------
    p
        A plotly or ggplot object.
    level
        "AA" or "AAA".

    Returns
    -------
        Data frame with columns criterion, check, status, note. Join to a11y_rubric() for principle, guideline, and threshold.
    """
    return a11y_audit_chart(p, level) + a11y_audit_doc(level)


def a11y_audit_actionable(audit: list[dict]) -> list[dict]:
    """Actionable rows from an audit

    Parameters
    ----------
    audit
        Output of a11y_audit(), a11y_audit_chart(), or a11y_audit_doc().

    Returns
    -------
        Data frame with the same columns as audit, filtered.
    """
    return [r for r in audit if r["status"] in ("todo", "ok")]


def a11y_audit_summary(audit: list[dict]) -> str:
    """One-line summary of an audit

    Parameters
    ----------
    audit
        Output of a11y_audit(), a11y_audit_chart(), or a11y_audit_doc().

    Returns
    -------
        Length-1 character vector.
    """
    todo = sum(1 for r in audit if r["status"] == "todo")
    ok   = sum(1 for r in audit if r["status"] == "ok")
    return f"{todo} to do, {ok} ok, {len(audit) - todo - ok} already handled."


def _row(criterion: str, check: str, status: str, note: str) -> dict:
    return {"criterion": criterion, "check": check,
            "status": status, "note": note}


def _meta_alt(p) -> Optional[str]:
    layout = getattr(p, "layout", None)
    meta = getattr(layout, "meta", None) if layout else None
    if isinstance(meta, dict):
        return meta.get("a11y_alt")
    return getattr(meta, "a11y_alt", None) if meta is not None else None


def _check_text_size(p, level: str) -> dict:
    threshold = wcag_rules["font_size"][level]["body"]
    size = _font_size(p)
    if size is None:
        return {"status": "manual",
                "note": f"verify text size manually (min {threshold} pt for {level})"}
    ok = size >= threshold
    return {"status": "ok" if ok else "todo",
            "note":   (f"base size {size} pt (min {threshold} pt)" if ok
                       else f'base size {size} pt; bump to >= {threshold} pt or call theme_a11y("{level}")')}


def _font_size(p):
    if _is_plotnine(p):
        theme = getattr(p, "theme", None)
        themeables = getattr(theme, "themeables", None) if theme else None
        for key in ("text", "axis_text", "plot_title"):
            t = themeables.get(key) if themeables else None
            size = getattr(t, "properties", {}).get("size") if t else None
            if size is not None:
                return size
        return None
    layout = getattr(p, "layout", None)
    font = getattr(layout, "font", None) if layout else None
    return getattr(font, "size", None) if font else None


def _check_hover(p) -> dict:
    if _is_plotnine(p):
        return {"status": "n/a",
                "note":   "plotnine output has no interactive hover tooltips"}
    layout = getattr(p, "layout", None)
    has = getattr(layout, "hoverlabel", None) is not None if layout else False
    return {"status": "applied" if has else "todo",
            "note":   ("hover labels styled by a11y_layout(); verify Esc dismiss + "
                       "persistent on hover" if has
                       else "call a11y_layout(); also verify tooltips dismiss with Esc and persist while hovered")}


def _check_color_only(p) -> dict:
    if not _is_plotnine(p):
        return {"status": "manual",
                "note":   "verify category encoding is not color-only"}
    mapping = getattr(p, "mapping", None) or {}
    has_color     = any(k in mapping for k in ("color", "colour", "fill"))
    has_redundant = any(k in mapping for k in ("shape", "linetype"))
    if not has_color:
        return {"status": "n/a", "note": "no color/fill aesthetic"}
    if has_redundant:
        return {"status": "ok",
                "note":   "shape or linetype redundantly encodes group"}
    return {"status": "todo",
            "note":   "add direct group labels (geom_text at cluster centroids), facet by group, or aes(shape=) / aes(linetype=) to redundantly encode the group"}


def _is_plotnine(p) -> bool:
    return type(p).__module__.startswith("plotnine")
