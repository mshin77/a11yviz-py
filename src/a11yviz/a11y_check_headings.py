"""Check Markdown / Quarto / HTML heading hierarchy and labels."""

import os
import re

_heading_md_re = re.compile(r"^(#{1,6})(\s|$)")
_fence_re = re.compile(r"^```")
_heading_html_re = re.compile(r"<h([1-6])[^>]*>(.*?)</h\1>", re.IGNORECASE | re.DOTALL)
_tag_re = re.compile(r"<[^>]+>")


def a11y_check_headings(path: os.PathLike, min_chars: int = 3) -> list[dict]:
    """Check Markdown / Quarto / HTML heading hierarchy and labels

    Parameters
    ----------
    path
        Path to a .md, .qmd, .Rmd, or .html file.
    min_chars
        Minimum heading text length (after trimming) considered descriptive. Default 3.

    Returns
    -------
        Data frame with one row per issue, columns line, level, text, issue. Empty data frame if no issues.
    """
    path = os.fspath(path)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    headings = (_parse_headings_html(path) if ext == ".html"
                else _parse_headings_md(path))
    if not headings:
        return []

    issues = []
    issues.extend(_skip_rows(headings))
    issues.extend(_empty_rows(headings))
    issues.extend(_short_rows(headings, min_chars))
    issues.sort(key=lambda r: r["line"])
    return issues


def _parse_headings_md(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    in_yaml = _yaml_mask(lines)
    in_fence = [False] * len(lines)
    fence_open = False
    for i, line in enumerate(lines):
        if _fence_re.match(line) and not in_yaml[i]:
            in_fence[i] = True
            fence_open = not fence_open
            continue
        in_fence[i] = fence_open

    rows = []
    for i, line in enumerate(lines):
        if in_yaml[i] or in_fence[i]:
            continue
        m = _heading_md_re.match(line)
        if not m:
            continue
        level = len(m.group(1))
        text = line[level:].strip()
        rows.append({"line": i + 1, "level": level, "text": text})
    return rows


def _yaml_mask(lines: list[str]) -> list[bool]:
    mask = [False] * len(lines)
    if len(lines) < 2 or lines[0] != "---":
        return mask
    for i in range(1, len(lines)):
        if lines[i] == "---":
            for j in range(i + 1):
                mask[j] = True
            return mask
    return mask


def _parse_headings_html(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    rows = []
    for match in _heading_html_re.finditer(raw):
        level = int(match.group(1))
        body = _tag_re.sub("", match.group(2)).strip()
        line = raw.count("\n", 0, match.start()) + 1
        rows.append({"line": line, "level": level, "text": body})
    return rows


def _skip_rows(headings: list[dict]) -> list[dict]:
    out = []
    for prev, curr in zip(headings, headings[1:]):
        if curr["level"] - prev["level"] > 1:
            out.append({
                "line": curr["line"], "level": curr["level"], "text": curr["text"],
                "issue": f"Level skip from h{prev['level']} to h{curr['level']}",
            })
    return out


def _empty_rows(headings: list[dict]) -> list[dict]:
    return [
        {"line": h["line"], "level": h["level"], "text": h["text"],
         "issue": "Empty heading"}
        for h in headings if not h["text"].strip()
    ]


def _short_rows(headings: list[dict], min_chars: int) -> list[dict]:
    return [
        {"line": h["line"], "level": h["level"], "text": h["text"],
         "issue": f"Heading text under {min_chars} chars (likely non-descriptive)"}
        for h in headings
        if h["text"].strip() and len(h["text"].strip()) < min_chars
    ]
