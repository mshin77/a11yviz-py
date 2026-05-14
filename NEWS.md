# a11yviz 0.1.2

* Shiny and HTML accessibility helpers added.
* Add-on stylesheet for Shiny apps.
* Alt-text audit now asks for a final manual check.

# a11yviz 0.1.1

* Documentation hyperlinks corrected.
* `check_overlap()` for scatter overlap (WCAG Success Criterion 1.3.1).
* `css` alias for parity with R `a11y_css()`.
* WCAG citations use `Success Criterion X.X.X` form.
* Defensive validation removed; bad input fails at the natural site.
* Vignette tables share a single `dt_options` dict.

# a11yviz 0.1.0

* First release: accessible themes, palettes, and audits for matplotlib, plotly, and Quarto.
* WCAG-tagged palettes for discrete, diverging, and sequential data, with a per-criterion audit and reference rubric.
* Bundled stylesheet covering tooltips, dark mode, focus rings, and tables.
* Helpers to flag colour pairs too similar to tell apart and warn when
  a palette has too many categories.
* Interactive playground ships as a static shinylive page inside the unified pkgdown + Quarto site — no install or Python server needed.
