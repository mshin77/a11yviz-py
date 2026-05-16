"""Local accessibility playground (Shiny for Python).

Mirrors inst/playground/app.R: a WCAG level toggle plus two tabs comparing
a baseline plotnine chart against the a11y-improved version with a
per-criterion audit table.
"""
import pandas as pd
from plotnine import aes, geom_point, ggplot, labs, theme
from plotnine.data import penguins

_penguins = penguins.dropna()
from shiny import App, reactive, render, ui

from a11yviz import (
    a11y_alt_text,
    a11y_audit_actionable,
    a11y_audit_chart,
    scale_color_a11y,
    theme_a11y,
)


app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_radio_buttons(
            "level", "WCAG level:",
            {"AA": "AA", "AAA": "AAA"},
            selected="AA", inline=True,
        ),
        width=240,
    ),
    ui.navset_card_underline(
        ui.nav_panel(
            "Baseline",
            ui.output_plot("plot_before", height="320px"),
            ui.tags.h3("Audit", class_="h6 mt-3"),
            ui.output_data_frame("audit_before"),
        ),
        ui.nav_panel(
            "Improved",
            ui.output_plot("plot_after", height="320px"),
            ui.tags.h3("Audit", class_="h6 mt-3"),
            ui.output_data_frame("audit_after"),
        ),
    ),
)


def server(input, output, session):
    @reactive.calc
    def base_plot():
        return (
            ggplot(_penguins, aes("flipper_length_mm", "body_mass_g", color="species"))
            + geom_point()
            + labs(title="Penguins (default plotnine)")
        )

    @reactive.calc
    def improved_plot():
        p = (
            ggplot(_penguins, aes("flipper_length_mm", "body_mass_g", color="species"))
            + geom_point(size=2, alpha=0.75)
            + theme_a11y(level=input.level())
            + scale_color_a11y(level=input.level())
            + labs(title="Penguins (theme_a11y + scale_color_a11y)",
                   x="Flipper length (mm)", y="Body mass (g)", color="Species")
            + theme(legend_position="top")
        )
        return a11y_alt_text(p, "Penguin body mass vs flipper length by species, AA accessible.")

    def actionable_df(p):
        return pd.DataFrame(
            a11y_audit_actionable(a11y_audit_chart(p, level=input.level()))
        )

    @output
    @render.plot
    def plot_before():
        return base_plot().draw()

    @output
    @render.plot
    def plot_after():
        return improved_plot().draw()

    @output
    @render.data_frame
    def audit_before():
        return render.DataGrid(actionable_df(base_plot()))

    @output
    @render.data_frame
    def audit_after():
        return render.DataGrid(actionable_df(improved_plot()))


app = App(app_ui, server)
