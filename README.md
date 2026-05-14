# a11yviz (Python)

Accessibility toolkit for [plotnine](https://plotnine.org/) and [plotly](https://plotly.com/python/) figures plus Quarto Python documents. Python sibling of [a11yviz (R)](https://github.com/mshin77/a11yviz). Targets WCAG 2.1 AA.

## Install

```bash
pip install -e ".[plotly,plotnine]"
```

## Usage

```python
import plotly.express as px
import a11yviz

fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])

# Apply a11y layout while preserving the figure's existing colors
fig = a11yviz.a11y_plotly(fig, palette=None,
                          alt="Bar chart of three categories.")

# Audit against WCAG criteria
for row in a11yviz.a11y_audit(fig):
    print(row)

# Quarto Python doc: embed the CSS once at the top
from IPython.display import HTML
HTML(f"<style>{open(a11yviz.a11y_css()).read()}</style>")
```

## Public API

| Function | Purpose |
|---|---|
| `a11y_plotly(fig, palette=None, alt=None)` | One-call wrapper: layout + alt text |
| `a11y_layout(fig, level="AA", palette=...)` | WCAG fonts, axis, hover, legend |
| `a11y_alt_text(fig, text)` | Attach alt text to figure |
| `a11y_aria_label(element_type, action, context=None)` | Build an ARIA label string |
| `a11y_describe(fig, backend, attach=True)` | LLM-generated alt text (caller supplies backend) |
| `a11y_audit(fig, level="AA")` | Per-criterion status rows |
| `a11y_palette(name, n=None, bg=None)` | WCAG-tagged categorical palette |
| `a11y_palette_info(name)` | Single palette spec |
| `a11y_palette_list()` | All available palettes |
| `a11y_css()` | Absolute path to bundled CSS |
| `theme_a11y(level="AA", dark=False)` | Plotnine theme with WCAG contrast and font sizes |
| `scale_color_a11y(palette)` / `scale_fill_a11y(palette)` | Plotnine categorical scales |
| `scale_color_a11y_div(palette)` / `scale_fill_a11y_div(palette)` | Plotnine diverging scales |
| `scale_color_a11y_seq(palette)` / `scale_fill_a11y_seq(palette)` | Plotnine sequential viridis scales |
| `make_a11y(p, palette, alt)` | One-shot wrapper for plotnine or plotly figures |

## Citation

Shin, M. (2026). *a11yviz: Accessibility toolkit for ggplot2, plotly, and Quarto* (R package version 0.1.2). <https://mshin77.github.io/a11yviz>

Shin, M. (2026). *a11yviz: Accessibility toolkit for plotly and Quarto* (Python package version 0.1.2). <https://github.com/mshin77/a11yviz-py>
