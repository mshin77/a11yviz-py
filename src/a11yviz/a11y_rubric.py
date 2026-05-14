"""WCAG 2.1 rubric for the success criteria a11yviz addresses."""

from typing import Optional

from a11yviz._utils import check_level

_ROWS = [
    {"criterion": "1.1.1",  "name": "Non-text Content",          "level": "A",
     "threshold_aa":  "alt text required",
     "threshold_aaa": "alt text required",
     "a11yviz_function": "a11y_alt_text(), a11y_alt_template(), a11y_describe()"},
    {"criterion": "1.3.1",  "name": "Info and Relationships",    "level": "A",
     "threshold_aa":  "headings nest without skips",
     "threshold_aaa": "headings nest without skips",
     "a11yviz_function": "a11y_check_headings()"},
    {"criterion": "1.4.1",  "name": "Use of Color",              "level": "A",
     "threshold_aa":  "redundant encoding (shape/linetype)",
     "threshold_aaa": "redundant encoding (shape/linetype)",
     "a11yviz_function": "redundant encoding via marker symbols / line dash"},
    {"criterion": "1.4.3",  "name": "Contrast (Minimum)",        "level": "AA",
     "threshold_aa":  "text 4.5:1; large text 3:1",
     "threshold_aaa": "--",
     "a11yviz_function": "a11y_layout(), a11y_check_palette()"},
    {"criterion": "1.4.4",  "name": "Resize Text",               "level": "AA",
     "threshold_aa":  "resizable to 200%",
     "threshold_aaa": "resizable to 200%",
     "a11yviz_function": "a11y_layout() (pt fonts; layout scales)"},
    {"criterion": "1.4.6",  "name": "Contrast (Enhanced)",       "level": "AAA",
     "threshold_aa":  "--",
     "threshold_aaa": "text 7:1; large text 4.5:1",
     "a11yviz_function": "a11y_layout(level='AAA'), a11y_check_palette(level='AAA')"},
    {"criterion": "1.4.10", "name": "Reflow",                    "level": "AA",
     "threshold_aa":  "no 2D scroll at 320 CSS px (vertical content)",
     "threshold_aaa": "no 2D scroll at 320 CSS px (vertical content)",
     "a11yviz_function": "a11y_css() (@media reflow rules)"},
    {"criterion": "1.4.11", "name": "Non-text Contrast",         "level": "AA",
     "threshold_aa":  "non-text 3:1",
     "threshold_aaa": "non-text 3:1",
     "a11yviz_function": "a11y_layout() (axis + gridline styling)"},
    {"criterion": "1.4.12", "name": "Text Spacing",              "level": "AA",
     "threshold_aa":  "line-height 1.5x; paragraph 2x; letter 0.12x; word 0.16x",
     "threshold_aaa": "line-height 1.5x; paragraph 2x; letter 0.12x; word 0.16x",
     "a11yviz_function": "a11y_css(), a11y_text_spacing_ratios()"},
    {"criterion": "1.4.13", "name": "Content on Hover or Focus", "level": "AA",
     "threshold_aa":  "tooltips dismissable, hoverable, persistent",
     "threshold_aaa": "tooltips dismissable, hoverable, persistent",
     "a11yviz_function": "a11y_layout() (hoverlabel styling); manual Esc/persist verify"},
    {"criterion": "2.4.6",  "name": "Headings and Labels",       "level": "AA",
     "threshold_aa":  "headings + labels describe topic or purpose",
     "threshold_aaa": "headings + labels describe topic or purpose",
     "a11yviz_function": "a11y_check_headings() (skips + empty + non-descriptive)"},
    {"criterion": "2.4.7",  "name": "Focus Visible",             "level": "AA",
     "threshold_aa":  "visible keyboard focus",
     "threshold_aaa": "visible keyboard focus",
     "a11yviz_function": "a11y_css() (focus rings)"},
    {"criterion": "2.4.10", "name": "Section Headings",          "level": "AAA",
     "threshold_aa":  "--",
     "threshold_aaa": "section headings organize content",
     "a11yviz_function": "a11y_check_headings() (level skips identify weak structure)"},
    {"criterion": "3.1.5",  "name": "Reading Level",             "level": "AAA",
     "threshold_aa":  "--",
     "threshold_aaa": "Flesch-Kincaid grade <= 9",
     "a11yviz_function": "a11y_check_readability()"},
    {"criterion": "4.1.3",  "name": "Status Messages",           "level": "AA",
     "threshold_aa":  "status updates announced without focus change",
     "threshold_aaa": "status updates announced without focus change",
     "a11yviz_function": "host-app live region (any HTML role='status' element)"},
]


def a11y_rubric(level: Optional[str] = None) -> list[dict]:
    """Return the chart-relevant WCAG 2.1 rubric, optionally filtered by level."""
    if level is None:
        return [dict(r) for r in _ROWS]
    level = check_level(level)
    keep = {"A", "AA"} | ({"AAA"} if level == "AAA" else set())
    return [dict(r) for r in _ROWS if r["level"] in keep]
