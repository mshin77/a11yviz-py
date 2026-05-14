"""Diverging and sequential continuous palettes."""

from typing import Optional

from a11yviz._constants import DIVERGING, SEQUENTIAL
from a11yviz._utils import require_pkg


def a11y_palette_div(name: str = "rdbu") -> dict:
    """Return low/mid/high anchor colors for a diverging gradient."""
    spec = _lookup_continuous(name, "diverging")
    src = spec.get("source", "literal")
    if src == "literal":
        return {"low": spec["low"], "mid": spec["mid"], "high": spec["high"]}
    if src == "rcolorbrewer":
        cols = spec["colors"]
        pos = spec.get("positions", [10, 6, 2])
        return {"low":  cols[pos[0] - 1],
                "mid":  cols[pos[1] - 1],
                "high": cols[pos[2] - 1]}
    raise ValueError(f"Unsupported source '{src}' for diverging palette")


def a11y_palette_seq(name: str = "cividis", n: Optional[int] = None):
    """Return a viridis-style spec or, with `n`, n sampled hex codes."""
    spec = _lookup_continuous(name, "sequential")
    src = spec.get("source", "viridislite")
    if src != "viridislite":
        raise ValueError(f"Unsupported source '{src}' for sequential palette")
    out = {
        "option":    spec["option"],
        "begin":     spec.get("begin", 0.0),
        "end":       spec.get("end", 1.0),
        "direction": spec.get("direction", 1),
    }
    if n is None:
        return out
    return _sample_viridis(out, n)


def _lookup_continuous(name: str, kind: str) -> dict:
    pals = {"diverging": DIVERGING, "sequential": SEQUENTIAL}[kind]
    if name not in pals:
        raise ValueError(
            f"Unknown {kind} palette '{name}'. Available: {', '.join(pals)}"
        )
    return pals[name]


def _sample_viridis(spec: dict, n: int) -> list[str]:
    colors_mod = require_pkg("plotly.colors", "a11y_palette_seq")
    scale_name = spec["option"].title()
    begin, end = spec["begin"], spec["end"]
    if spec["direction"] == -1:
        begin, end = end, begin
    sample_points = [begin + (end - begin) * (i / max(n - 1, 1)) for i in range(n)]
    rgb_strings = colors_mod.sample_colorscale(scale_name, sample_points, colortype="rgb")
    return [_rgb_string_to_hex(s) for s in rgb_strings]


def _rgb_string_to_hex(s: str) -> str:
    inner = s.strip().removeprefix("rgb(").rstrip(")")
    r, g, b = (int(round(float(v.strip()))) for v in inner.split(","))
    return "#{:02X}{:02X}{:02X}".format(r, g, b)
