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
        {"champs.csv": "13.1", "penguins.csv": "13.2"},  
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