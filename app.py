import shared
from shiny import App, ui, reactive, render
import seaborn as sns
from faicons import icon_svg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from shinywidgets import output_widget, render_widget  

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
                     ui.input_select("select_champ", "Choose Champion:", ["TOP"]),
                     ui.input_checkbox_group("select_metrics", "Show:",
                                            {"win_pct": "Win %", "pick_pct": "Pick %", "ban_pct": "Ban %"},),
                     width="15%",),
                 ui.input_radio_buttons("role_select", "Select Role", {"TOP": "Toplane", "JUNGLE": "Jungle", "MID": "Midlane", "ADC": "ADC", "SUPPORT": "Support"},),
                 ui.output_plot("time_series_plot"),),
),

    # page 4
    ui.nav_panel("D",
                        output_widget("bubble_plot"),),
        
    
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
        champ = input.select_champ()
        role = input.role_select()
        selected_metrics = input.select_metrics()
        champ_df = shared.get_all_patches()

        #This is regex magic, DON NO TOUCH THIS or this shit will break. It is so the patches are in correct order
        patch_split = champ_df["patch"].str.extract(r"(\d+)\.(\d+)")
        champ_df["patch_major"] = patch_split[0].astype(int)
        champ_df["patch_minor"] = patch_split[1].astype(int)
        champ_df = champ_df.sort_values(["patch_major", "patch_minor"])
        
        #Only shows the champ in the chosen role, so no duplicates basically
        champ_df = champ_df[(champ_df["name"] == champ) & (champ_df["role"] == role)]
        print(input.select_metrics())
        #Creates the plot
        fig, ax = plt.subplots(figsize=(8, 5))

        for metric in selected_metrics:
            if metric in champ_df.columns:
                ax.plot(champ_df["patch"], champ_df[metric], marker="o", label=metric)

        ax.set_title(f"{champ} - Win Rate over Patches")
        ax.set_xlabel("Patch")
        ax.set_ylabel("Win Rate (%)")
        ax.grid(True)
        return fig
    
    @render_widget 
    def bubble_plot():
        # Get selected patch from the global input
        patch = input.patch_select()  # e.g., "patch_13.1.csv"

        # Get the data for this patch
        df = shared.get_patch(patch)  # already returns only this patch

        if df.empty:
            return px.scatter(title=f"No data for {patch}")

        # Create bubble chart
        fig = px.scatter(
            df,
            x="pick_pct",            # X-axis: Pick %
            y="win_pct",             # Y-axis: Win %
            size="ban_pct",          # Bubble size: Ban %
            color="class",           # Bubble color: Champion class
            hover_name="name",       # Champion name on hover
            hover_data={
                "pick_pct": True,
                "win_pct": True,
                "ban_pct": True,
                "class": True
            },
            title=f"Win % vs Pick % (Patch {patch})",
            size_max=60              # Maximum bubble size
        )

        fig.update_layout(
            xaxis_title="Pick %",
            yaxis_title="Win %",
            legend_title="Class",
        )

        return fig
    
    @ reactive.effect
    def update_champ_choices():
        role = input.role_select()
        champ_list = shared.get_champs_per_role(role)
        ui.update_select(id="select_champ", choices=champ_list, session=session)
        
# Create the Shiny app object
app=App(app_ui, server)

