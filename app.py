import shared
from shiny import App, ui, reactive, render
import seaborn as sns
from faicons import icon_svg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# This is the UI part of the app
app_ui = ui.page_navbar(

    # Page 1
    ui.nav_panel("A",
                      ui.input_select(
        "select_a",
        "Choose Game Patch:",
        {
        "patch_13.1.csv": "13.1",
        "patch_13.2.csv": "13.2",
        "patch_13.3.csv": "13.3",
        "patch_13.4.csv": "13.4",
        "patch_13.5.csv": "13.5",
        "patch_13.6.csv": "13.6",
        "patch_13.7.csv": "13.7",
        "patch_13.8.csv": "13.8",
        "patch_13.9.csv": "13.9",
        "patch_13.10.csv": "13.10",
        "patch_13.11.csv": "13.11",
        "patch_13.12.csv": "13.12",
        },
        ),
        ui.card(ui.output_data_frame("champ_df"), height="600px")),

    # page 2
    ui.nav_panel("B",
                      ui.input_select(
        "select_b",
        "Choose Game Patch:",
        {
        "patch_13.1.csv": "13.1",
        "patch_13.2.csv": "13.2",
        "patch_13.3.csv": "13.3",
        "patch_13.4.csv": "13.4",
        "patch_13.5.csv": "13.5",
        "patch_13.6.csv": "13.6",
        "patch_13.7.csv": "13.7",
        "patch_13.8.csv": "13.8",
        "patch_13.9.csv": "13.9",
        "patch_13.10.csv": "13.10",
        "patch_13.11.csv": "13.11",
        "patch_13.12.csv": "13.12",
        },
        ),
                ui.h2("Top 10 Champions by Pick %"),
                ui.row(
                    ui.column(4, ui.output_plot("top10_win")),
                    ui.column(4, ui.output_plot("top10_ban")),
                    ui.column(4, ui.output_plot("top10_pick")),
                    )),



    # page 3
    ui.nav_panel("C", "Page C content"),
    title="PiDo.gg",
    id="page",
)


# This is the server/logic part of the app
def server(input, output, session):
    @ render.data_frame
    def champ_df():
        df=shared.update_patch(input.select_a())
        return render.DataGrid(df, width="100%")

    @ render.plot
    def top10_win():
        df = shared.update_patch(input.select_b())

        # Top 10 by Pick %
        top10 = df.nlargest(10, "win_pct")
        
        clean_string = input.select_b().split(".")
        patch_number = clean_string[0] + "." + clean_string[1]
        
        fig, ax = plt.subplots(figsize=(8,6))
        ax.set_xlim(51,56)
        ax.barh(top10["name"], top10["win_pct"], color='skyblue')
        ax.set_xlabel("Win %")
        ax.set_ylabel("Champion")
        ax.set_title(f"Top 10 Champions by win % — {patch_number}")
        ax.invert_yaxis()  # Highest at top

        return fig
    
    @ render.plot
    def top10_ban():
        df = shared.update_patch(input.select_b())

        # Top 10 by Pick %
        top10 = df.nlargest(10, "ban_pct")
        
        clean_string = input.select_b().split(".")
        patch_number = clean_string[0] + "." + clean_string[1]
        
        fig, ax = plt.subplots(figsize=(8,6))
        ax.barh(top10["name"], top10["ban_pct"], color='#c40000')
        ax.set_xlabel("Ban %")
        ax.set_ylabel("Champion")
        ax.set_title(f"Top 10 Champions by ban % — {patch_number}")
        ax.invert_yaxis()  # Highest at top

        return fig
    
    @ render.plot
    def top10_pick():
        df = shared.update_patch(input.select_b())

        # Top 10 by Pick %
        top10 = df.nlargest(10, "pick_pct")
        
        clean_string = input.select_b().split(".")
        patch_number = clean_string[0] + "." + clean_string[1]
        
        fig, ax = plt.subplots(figsize=(8,6))
        ax.barh(top10["name"], top10["pick_pct"], color='#66c908')
        ax.set_xlabel("Pick %")
        ax.set_ylabel("Champion")
        ax.set_title(f"Top 10 Champions by Pick % — {patch_number}")
        ax.invert_yaxis()  # Highest at top

        return fig
        



# Create the Shiny app object
app=App(app_ui, server)
