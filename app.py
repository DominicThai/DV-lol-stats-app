import shared 
from shiny import App, ui, reactive, render
import seaborn as sns
from faicons import icon_svg
import os
import pandas as pd


app_ui = ui.page_navbar(  
    ui.nav_panel("A",
        ui.input_select(
        "select",  
        "Change Game Patch:",  
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
    ui.nav_panel("B", "Page B content"),  
    ui.nav_panel("C", "Page C content"),  
    title="PiDo.gg",  
    id="page",  
)  

def server(input, output, session):
    @render.data_frame
    def champ_df():
        df = shared.update_patch(input.select())
        return render.DataGrid(df, width="100%")


""" 
ui.page_opts(
    title="PiDo.gg",  
)

ui.input_select(  
        "select",  
        "Change Game Patch:",  
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
    )  

with ui.navset_bar(title="", id="main_nav"):

    #Page 1
    with ui.nav_panel("Champion Overview"):
        with ui.layout_columns():
            @render.data_frame
            def champs_df():
                df = shared.update_patch(input.select())
                return render.DataGrid(df, width="100%")

    #page2
    with ui.nav_panel("Winrates"):
        with ui.layout_columns():
            "test"
            df = pd.DataFrame({
    "Name": ["Aatrox", "Ahri", "Garen", "Lux", "Yasuo"],
    "Role": ["TOP", "MID", "TOP", "MID", "MID"],
    "Win %": [48.84, 50.90, 52.30, 49.50, 51.10]
})
            @render.plot
            def winrate_plot():
                # Create a simple histogram of Win %
                ax = sns.histplot(df, x="Win %", bins=5)
                ax.set_title("Distribution of Winrates")
                ax.set_xlabel("Winrate (%)")
                ax.set_ylabel("Count")
                return ax.get_figure()


    #page3
    with ui.nav_panel("Stats or somn"):
        "Page C content"
         """

# __APP__
app = App(app_ui, server)