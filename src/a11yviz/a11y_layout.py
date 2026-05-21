"""Apply WCAG-conformant fonts, axis, hover, and legend styling to a plotly Figure."""

from typing import Any, Optional

from a11yviz._constants import wcag_rules
from a11yviz._utils import check_level
from a11yviz.a11y_palette import a11y_palette


def a11y_layout(p, level: str = "AA", palette: Optional[str] = "dark2_8"):
    """Apply accessible layout to a plotly figure

    Parameters
    ----------
    p
        A plotly object (from plotly::plot_ly or plotly::ggplotly).
    level
        "AA" or "AAA".
    palette
        Discrete palette name applied as plotly's colorway. See a11y_palette_list(). Pass NULL to leave plotly's default colors unchanged.

    Returns
    -------
        Modified plotly object.
    """
    level = check_level(level)
    fz = wcag_rules["font_size"][level]
    tt = wcag_rules["tooltip"]
    axis_sz = fz.get("axis_text", fz["body"])

    body  = dict(family=tt["font"], size=fz["body"],  color="#222")
    title = dict(family=tt["font"], size=fz["title"], color="#222")
    tick  = dict(family=tt["font"], size=axis_sz,     color="#222")
    hover = dict(family=tt["font"], size=tt["size"],  color=tt["text"])
    axis  = dict(tickfont=tick, title=dict(font=title),
                 gridcolor="#e5e5e5", zerolinecolor="#c0c0c0")

    args: dict[str, Any] = dict(
        autosize=True,
        font=body,
        title=None,
        margin=dict(t=30, b=60, l=90, r=30, autoexpand=True),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=axis,
        yaxis=axis,
        hoverlabel=dict(bgcolor=tt["bg"], bordercolor=tt["border"],
                        font=hover, align="left", namelength=-1),
        legend=dict(orientation="v", x=1.02, xanchor="left",
                    y=0.5, yanchor="middle", font=body,
                    title=dict(font=title)),
        coloraxis=dict(colorbar=dict(tickfont=body, title=dict(font=title))),
    )
    if palette is not None:
        args["colorway"] = a11y_palette(palette)

    p.update_layout(**args)
    p._a11y_config = dict(
        displayModeBar=True,
        displaylogo=False,
        responsive=True,
        toImageButtonOptions=dict(format="png", scale=2),
    )
    return p
