import shared 
from shiny import reactive
from shiny.express import input, render, ui
import seaborn as sns
from faicons import icon_svg
import os
import pandas as pd


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
        "Page B content"


    #page3
    with ui.nav_panel("Stats or somn"):
        "Page C content"