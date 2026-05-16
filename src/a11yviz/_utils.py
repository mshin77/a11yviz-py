"""Internal helpers mirroring R's a11yviz/R/utils.R."""

from typing import Iterable, Union

Color = str


def check_level(level: str) -> str:
    """Validate WCAG level argument."""
    level = level.upper()
    if level not in {"AA", "AAA"}:
        raise ValueError("level must be 'AA' or 'AAA'")
    return level


def require_pkg(pkg: str, fn: str):
    """Import a package or raise an informative error pointing to install."""
    import importlib
    try:
        return importlib.import_module(pkg)
    except ImportError as exc:
        raise ImportError(
            f"`{fn}()` requires the '{pkg}' package. "
            f"Install with: pip install {pkg}"
        ) from exc


def hex_to_rgb(hex_str: Color) -> tuple[int, int, int]:
    """Convert a #RRGGBB or #RGB hex string to (r, g, b) ints in [0, 255]."""
    s = hex_str.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f"Invalid hex color: {hex_str!r}")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def rgb_to_hex(r: float, g: float, b: float) -> Color:
    """Convert (r, g, b) ints in [0, 255] to a #RRGGBB hex string."""
    return "#{:02X}{:02X}{:02X}".format(int(round(r)), int(round(g)), int(round(b)))


def relative_luminance(hex_str: Color) -> float:
    """WCAG 2.x relative luminance for an sRGB color."""
    r, g, b = (c / 255 for c in hex_to_rgb(hex_str))
    def _lin(v: float) -> float:
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast_ratio(fg: Color, bg: Color) -> float:
    """WCAG contrast ratio between two sRGB colors."""
    l1, l2 = relative_luminance(fg), relative_luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def alpha_composite(fg: Color, bg: Color, alpha: float) -> Color:
    """Alpha-composite fg over bg and return the resulting hex."""
    fr, fg_, fb = hex_to_rgb(fg)
    br, bg_, bb = hex_to_rgb(bg)
    return rgb_to_hex(
        alpha * fr + (1 - alpha) * br,
        alpha * fg_ + (1 - alpha) * bg_,
        alpha * fb + (1 - alpha) * bb,
    )


def coalesce(*values):
    """Return the first non-None value (Python version of R's `%||%`)."""
    for v in values:
        if v is not None:
            return v
    return None
