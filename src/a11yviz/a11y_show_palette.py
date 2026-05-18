"""Visualize a palette with WCAG contrast overlay (plotnine)."""

from a11yviz._utils import (
    check_level, contrast_ratio, relative_luminance, require_pkg,
)
from a11yviz.a11y_palette import a11y_palette


def a11y_show_palette(name: str = "dark2_8", bg: str = "#ffffff",
                      level: str = "AA"):
    """Visualize a palette with WCAG contrast overlay

    Parameters
    ----------
    name
        Discrete palette name. See a11y_palette_list().
    bg
        Reference background hex (default "#ffffff").
    level
        "AA" or "AAA".

    Returns
    -------
        A ggplot object.
    """
    pn = require_pkg("plotnine", "a11y_show_palette")
    pd = require_pkg("pandas", "a11y_show_palette")
    level = check_level(level)
    cols = a11y_palette(name)
    ratios = [contrast_ratio(c, bg) for c in cols]
    threshold = 4.5 if level == "AA" else 7.0
    status = [level if r >= threshold else "todo" for r in ratios]
    text_col = ["#000000" if relative_luminance(c) > 0.179 else "#ffffff"
                for c in cols]

    df = pd.DataFrame({
        "idx":      list(range(1, len(cols) + 1)),
        "y":        [1] * len(cols),
        "hex":      cols,
        "label":    [f"{c}\n{r:.1f}:1\n{s}"
                     for c, r, s in zip(cols, ratios, status)],
        "text_col": text_col,
    })

    return (
        pn.ggplot(df, pn.aes("idx", "y", fill="hex"))
        + pn.geom_tile(color="white", size=1)
        + pn.geom_text(pn.aes(label="label", color="text_col"),
                       size=9, lineheight=0.9)
        + pn.scale_fill_identity()
        + pn.scale_color_identity()
        + pn.scale_x_continuous(breaks=[])
        + pn.scale_y_continuous(breaks=[])
        + pn.theme_void()
        + pn.labs(title=f"{name} palette  (vs {bg}, {level})")
    )
