from shared import app_dir, champs_df, data
from shiny import reactive
from shiny.express import input, render, ui
import seaborn as sns
from faicons import icon_svg

ui.page_opts(
    title="App with navbar",  
)

with ui.nav_panel("A"):  
    with ui.layout_columns():        
        @render.data_frame
        def champs_df():
            return render.DataGrid(champs_df, width='100%', summary=False)

with ui.nav_panel("B"):  
    "Page B content"

with ui.nav_panel("C"):  
    "Page C content"