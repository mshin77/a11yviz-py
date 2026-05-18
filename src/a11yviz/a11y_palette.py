"""Discrete WCAG-tagged categorical palettes."""

import warnings
from typing import Optional

from a11yviz._constants import diverging, palettes, sequential


def a11y_palette(name: str = "dark2_8", n: Optional[int] = None,
                 bg: Optional[str] = None) -> list[str]:
    """Discrete color palette (categorical)

    Parameters
    ----------
    name
        Discrete palette name. Built-in: "dark2_8" (default, RColorBrewer Dark2), "set2_8" (RColorBrewer Set2), "paired_12" (RColorBrewer Paired), "aaa_5" (custom AAA-on-white set).
    n
        Optional number of colors. Defaults to the palette's full size (truncates from the start when smaller).
    bg
        Plot background context. One of NULL (default -- no check), "white", or "dark". When set, the function warns if the palette's safe_on tag does not match.

    Returns
    -------
        Character vector of hex codes (e.g., "#1B9E77"). For sequential gradients, see a11y_palette_seq().
    """
    spec = _palette_spec(name)
    colors = spec["colors"]
    if n is not None:
        colors = colors[:n]
    if bg is not None:
        _warn_if_unsafe(name, spec, bg)
    return list(colors)


def a11y_palette_info(name: str = "dark2_8") -> dict:
    """Discrete palette metadata

    Parameters
    ----------
    name
        Discrete palette name. Built-in: "dark2_8" (default, RColorBrewer Dark2), "set2_8" (RColorBrewer Set2), "paired_12" (RColorBrewer Paired), "aaa_5" (custom AAA-on-white set).

    Returns
    -------
        Named list with name, colors, safe_on, purpose, notes, plus the source spec fields.
    """
    spec = _palette_spec(name)
    rest = {k: v for k, v in spec.items() if k != "colors"}
    return {"name": name, "colors": spec["colors"], **rest}


def a11y_palette_list(type: Optional[str] = None) -> list[dict]:
    """List available palettes

    Parameters
    ----------
    type
        Optional filter: "discrete", "diverging", or "sequential". NULL (default) returns all.

    Returns
    -------
        Data frame with columns name, type, source, n, safe_on, purpose. n is NA for continuous palettes. For the notes field of a single palette, call a11y_palette_info().
    """
    sources = {"discrete": palettes, "diverging": diverging, "sequential": sequential}
    if type is not None and type not in sources:
        raise ValueError(f"type must be one of {sorted(sources)}")
    return [_palette_row(nm, kind, spec)
            for kind, src in sources.items() if type in (None, kind)
            for nm, spec in src.items()]


def _palette_spec(name: str) -> dict:
    if name not in palettes:
        raise ValueError(
            f"Unknown palette '{name}'. Available: {', '.join(palettes)}"
        )
    return palettes[name]


def _palette_row(name: str, type_: str, spec: dict) -> dict:
    return {
        "name":    name,
        "type":    type_,
        "source":  spec.get("source", "literal"),
        "n":       len(spec["colors"]) if type_ == "discrete" else None,
        "safe_on": spec.get("safe_on"),
        "purpose": spec.get("purpose"),
    }


def _warn_if_unsafe(name: str, spec: dict, bg: str) -> None:
    if bg not in {"white", "dark"}:
        raise ValueError("bg must be 'white' or 'dark'")
    safe = spec.get("safe_on", "white")
    if safe in {"both", bg}:
        return
    if safe == "labeled":
        msg = (f"Palette '{name}' is mixed-contrast -- only safe when each fill carries "
               f"a high-contrast text label. {spec.get('notes', '')}")
    else:
        msg = (f"Palette '{name}' is tagged safe_on='{safe}' but bg='{bg}' was requested. "
               f"{spec.get('notes', '')}")
    warnings.warn(msg, stacklevel=3)
