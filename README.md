<img src="https://raw.githubusercontent.com/mshin77/a11yviz-py/main/logo.svg" alt="a11yviz Logo" align="right" width="220px"/>

[![PyPI version](https://img.shields.io/pypi/v/a11yviz.svg)](https://pypi.org/project/a11yviz/)
[![Project status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Makes charts and documents accessible across
[plotnine](https://plotnine.org/),
[plotly](https://plotly.com/python/), and [Quarto](https://quarto.org/)
in Python, aligned with the [Web Content Accessibility Guidelines
(WCAG 2.1)](https://www.w3.org/TR/WCAG21/). Includes WCAG-tagged
palettes, alt-text scaffolds, audits, a document rubric, heading and
reading-level checks, `shiny` ARIA helpers, and a stylesheet.

R version: [a11yviz](https://github.com/mshin77/a11yviz).

## Installation

    pip install a11yviz

## Quick start

```python
from plotnine import aes, geom_point, ggplot, labs
from plotnine.data import penguins
import a11yviz

p = (ggplot(penguins.dropna(),
            aes("flipper_length_mm", "body_mass_g",
                color="species", shape="species"))
     + geom_point()
     + a11yviz.scale_color_a11y("dark2_8")
     + labs(x="Flipper length (mm)", y="Body mass (g)"))

a11yviz.a11y_alt_text(p, "Scatter of penguin body mass vs flipper length by species.")
```

## Citation

Shin, M. (2026). *a11yviz: Accessibility toolkit for ggplot2, plotly, and
Quarto* (R package version 0.1.7). <https://mshin77.github.io/a11yviz>

Shin, M. (2026). *a11yviz: Accessibility toolkit for plotnine, plotly,
and Quarto* (Python package version 0.1.7). <https://github.com/mshin77/a11yviz-py>
