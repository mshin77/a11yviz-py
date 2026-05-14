"""Discrete WCAG-tagged categorical palettes."""

import warnings
from typing import Optional

from a11yviz._constants import diverging, palettes, sequential


def a11y_palette(name: str = "dark2_8", n: Optional[int] = None,
                 bg: Optional[str] = None) -> list[str]:
    """Return hex codes for a categorical palette."""
    spec = _palette_spec(name)
    colors = spec["colors"]
    if n is not None:
        colors = colors[:n]
    if bg is not None:
        _warn_if_unsafe(name, spec, bg)
    return list(colors)


def a11y_palette_info(name: str = "dark2_8") -> dict:
    """Return the full spec for a palette."""
    spec = _palette_spec(name)
    return {"name": name, **spec}


def a11y_palette_list(type: Optional[str] = None) -> list[dict]:
    """List discrete, diverging, and sequential palettes; filter by `type` if set."""
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
