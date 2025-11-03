import shared
from shiny import App, ui, reactive, render
import seaborn as sns
from faicons import icon_svg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

list_of_champions = shared.champ_df['Name'].tolist()
list_of_champions = list(dict.fromkeys(list_of_champions))


# This is the UI part of the app
app_ui = ui.page_navbar(

    # Page 1
    ui.nav_panel("A",
        ui.card(ui.output_data_frame("champ_df"), height="600px")),

    # page 2
    ui.nav_panel("B",
                ui.h2("Top 10 Champions by Pick %"),
                ui.row(
                    ui.column(4, ui.output_plot("top10_win")),
                    ui.column(4, ui.output_plot("top10_ban")),
                    ui.column(4, ui.output_plot("top10_pick")),
                    )),



    # page 3
    ui.nav_panel("C",
                 ui.layout_sidebar(
                 ui.sidebar(
                     ui.input_select("select_champ", "Choose Champion:", list_of_champions),
                     ui.input_checkbox_group("select_metrics", "Select Metrics to Display:",
                                            {"win_pct": "Win %", "pick_pct": "Pick %", "ban_pct": "Ban %"},),
                     width="15%",),
                 ui.output_plot("time_series_plot"),),
),

    # page 4
    ui.nav_panel("D",),
        
    
    #Other stuff
    title="PiDo.gg",
    id="page",
    header=ui.input_select(
        "patch_select",
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
)


# This is the server/logic part of the app
def server(input, output, session):
    @ render.data_frame
    def champ_df():
        df=shared.get_patch(input.patch_select())
        return render.DataGrid(df, width="100%")

    @ render.plot
    def top10_win():
        df = shared.get_patch(input.patch_select())

        # Top 10 by Pick %
        top10 = df.nlargest(10, "win_pct")
        
        clean_string = input.patch_select().split(".")
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
        df = shared.get_patch(input.patch_select())

        # Top 10 by Pick %
        top10 = df.nlargest(10, "ban_pct")
        
        clean_string = input.patch_select().split(".")
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
        df = shared.get_patch(input.patch_select())

        # Top 10 by Pick %
        top10 = df.nlargest(10, "pick_pct")
        
        clean_string = input.patch_select().split(".")
        patch_number = clean_string[0] + "." + clean_string[1]
        
        fig, ax = plt.subplots(figsize=(8,6))
        ax.barh(top10["name"], top10["pick_pct"], color='#66c908')
        ax.set_xlabel("Pick %")
        ax.set_ylabel("Champion")
        ax.set_title(f"Top 10 Champions by Pick % — {patch_number}")
        ax.invert_yaxis()  # Highest at top

        return fig
    
    @ render.plot
    def time_series_plot():
        champ = "Ahri"
        champ_df = shared.get_all_patches()

        #This is regex magic, DON NO TOUCH THIS or this shit will break. It is so the patches are in correct order
        patch_split = champ_df["patch"].str.extract(r"(\d+)\.(\d+)")
        champ_df["patch_major"] = patch_split[0].astype(int)
        champ_df["patch_minor"] = patch_split[1].astype(int)

        champ_df = champ_df.sort_values(["patch_major", "patch_minor"])
        champ_df = champ_df[champ_df["name"] == champ]
        
        #Creates the plot
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(champ_df["patch"], champ_df["win_pct"], marker="o")
        ax.set_title(f"{champ} - Win Rate over Patches")
        ax.set_xlabel("Patch")
        ax.set_ylabel("Win Rate (%)")
        ax.grid(True)
        return fig
        
# Create the Shiny app object
app=App(app_ui, server)

