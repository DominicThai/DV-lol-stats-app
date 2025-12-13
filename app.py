import shared
from shiny import App, ui, reactive, render
import seaborn as sns
#from faicons import icon_svg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from shinywidgets import output_widget, render_widget  
import base64
from ipywidgets import Image

# This is the UI part of the app
app_ui = ui.page_navbar(

    # Page 1
    ui.nav_panel("Dataset",
        ui.card(ui.output_data_frame("champ_df"), height="600px")),

    # page 2
    ui.nav_panel("Bar graphs",
                ui.h2("Top 10 Champions by Pick %"),
                ui.row(
                    ui.column(4, ui.output_plot("top10_win")),
                    ui.column(4, ui.output_plot("top10_ban")),
                    ui.column(4, ui.output_plot("top10_pick")),
                    )),



    # page 3
    ui.nav_panel("Time Series plot",
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
    ui.nav_panel("Bubble Graphs",
                        output_widget("bubble_plot"),
                        output_widget("role_bubble_plot"),
                        output_widget("winrate_vs_ban_plot")),
    
    #page 5
    ui.nav_panel("Area chart",
                 output_widget("role_area_chart"),),

    # page 6
    ui.nav_panel("Pie charts",
    ui.row(
        ui.column(6, output_widget("pie_chart_class_ban")),
        ui.column(6, output_widget("pie_chart_ban")),
        ui.column(6, output_widget("pie_chart_ranks")),
    ),
),
    # page 7
    ui.nav_panel("AI generated",
                 output_widget("ai_generated"),),
    
    #page 8
    ui.nav_panel("Animated",
                 output_widget("pie_chart_ban"),),
    #Other stuff
    title="DoPi.gg",
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
    
    @render_widget
    def role_area_chart():
        df = shared.get_all_patches()

        # Extract and sort patch numbers
        patch_split = df["patch"].str.extract(r"(\d+)\.(\d+)")
        df["patch_major"] = patch_split[0].astype(int)
        df["patch_minor"] = patch_split[1].astype(int)
        df = df.sort_values(["patch_major", "patch_minor"])

        # Aggregate pick % by patch + class
        class_df = (
            df.groupby(["patch", "class"], as_index=False)
            .agg(class_pick_pct=("pick_pct", "sum"))
        )

        # Normalize so each patch sums to 100% and doesn't go above that
        class_df["total_patch_pick"] = (
            class_df.groupby("patch")["class_pick_pct"].transform("sum")
        )

        class_df["pick_share_pct"] = (
            class_df["class_pick_pct"] / class_df["total_patch_pick"] * 100
        )

        fig = px.area(
            class_df,
            x="patch",
            y="pick_share_pct",
            color="class",
            title="Class Share of Total Pick % Over Time",
            line_group="class",
        )

        fig.update_layout(
            xaxis_title="Patch",
            yaxis_title="Pick % Share",
            hovermode="x unified",
            legend_title="Class"
        )

        return fig

    
    @render_widget
    def role_bubble_plot():
        # Get selected patch from the global selector
        patch = input.patch_select()
        df = shared.get_patch(patch)  # returns DataFrame for selected patch

        # Aggregate by role
        role_summary = (
            df.groupby("role")
            .agg({
                "pick_pct": "sum",      # total pick % for the role
                "win_pct": "mean",      # average win % for the role
                "ban_pct": "mean"       # average ban % for the role
            })
            .reset_index()
        )
        
        # Normalize pick_pct so total across roles = 100%
        total_pick = role_summary["pick_pct"].sum()
        role_summary["pick_pct"] = (role_summary["pick_pct"] / total_pick) * 100

        # Create bubble chart
        fig = px.scatter(
            role_summary,
            x="pick_pct",
            y="win_pct",
            size="ban_pct",
            color="role",
            hover_name="role",
            size_max=120,
            title=f"Role Meta Bubble Chart — Patch {patch.replace('patch_','').replace('.csv','')}",
            labels={"Role": "Role"}
        )

        fig.update_layout(
            xaxis_title="Pick %",
            yaxis_title="Win %",
            template="plotly_white",
            legend_title="Role",
            hovermode="closest"
        )

        return fig
    
    @render_widget
    def pie_chart_ban():
        df = shared.get_patch(input.patch_select())

       
        if df.empty:
            return px.pie(title="No data available")

        
        pie_df = df.copy()

        # Threshold: champions below this ban % go into "Other champions"
        threshold = 1

        pie_df.loc[pie_df["ban_pct"] < threshold, "name"] = "Other champions"

        
        pie_df = (
            pie_df.groupby("name", as_index=False)
            .agg({"ban_pct": "sum"})
            .sort_values("ban_pct", ascending=False)
        )

        patch_label = input.patch_select().replace("patch_", "").replace(".csv", "")

        fig = px.pie(
            pie_df,
            values="ban_pct",
            names="name",
            title=f"Ban % Distribution by Champion — Patch {patch_label}",
            subtitle=f"Bans below {threshold} grouped into 'Other champions'",
            hole=0.4
        )

        fig.update_traces(
            textinfo="percent+label",
            textposition="inside",
            insidetextorientation="radial",
            pull=[0.05 if n != "Other champions" else 0 for n in pie_df["name"]],
        )

        fig.update_layout(
            showlegend=True,
            legend_title="Champion",
        )

        return fig

    @render_widget
    def pie_chart_class_ban():
        df = shared.get_patch(input.patch_select())

        if df.empty:
            return px.pie(title="No data available")

        # Aggregate ban % by class
        class_df = (
            df.groupby("class", as_index=False)
            .agg(total_ban_pct=("ban_pct", "sum"))
            .sort_values("total_ban_pct", ascending=False)
        )

        patch_label = input.patch_select().replace("patch_", "").replace(".csv", "")

        fig = px.pie(
            class_df,
            values="total_ban_pct",
            names="class",
            title=f"Ban % Share by Champion Class — Patch {patch_label}",
            hole=0.3
        )

        fig.update_traces(
            textinfo="percent+label",
            textposition="inside",
        )

        fig.update_layout(
            legend_title="Class",
            showlegend=True,
        )

        return fig
    
    @render_widget
    def pie_chart_ranks():
        df = shared.get_patch(input.patch_select())

        if df.empty or "Tier" not in df.columns:
            return px.pie(title="No GOD-tier data available")

        god_tier_df = df[df["Tier"] == "God"]

        if god_tier_df.empty:
            return px.pie(title="No God-tier champions in this patch")

        class_df = (
            god_tier_df.groupby("class", as_index=False)
                    .agg(count=("name", "count"))
                    .sort_values("count", ascending=False)
        )

        patch_label = input.patch_select().replace("patch_", "").replace(".csv", "")

        fig = px.pie(
            class_df,
            values="count",
            names="class",
            title=f"God-Tier Champion Share by Class — Patch {patch_label}",
            hole=0.3
        )

        fig.update_traces(
            textinfo="percent+label",
            textposition="inside",
        )

        fig.update_layout(
            legend_title="Class",
            showlegend=True,
        )

        return fig
    
    @render_widget
    def winrate_vs_ban_plot():
        df = shared.get_patch(input.patch_select())

        if df.empty:
            return px.scatter(title="No data available")

        fig = px.scatter(
            df,
            x="win_pct",
            y="ban_pct",
            color="class",
            size="pick_pct",
            hover_name="name",
            title="Champion Ban Pressure vs Win Rate",
            labels={
                "win_pct": "Win Rate (%)",
                "ban_pct": "Ban Rate (%)",
                "pick_pct": "Pick Rate (%)",
                "class": "Class"
            },
            size_max=40,
        )

        fig.update_layout(
            xaxis_title="Win Rate (%)",
            yaxis_title="Ban Rate (%)",
            hovermode="closest",
            height=600
        )

        return fig
    @render_widget
    def ai_generated():
        with open("data/ai_slop.png", "rb") as f:
            return Image(
                value=base64.b64decode(base64.b64encode(f.read())),
                format="png"
            )
    @ reactive.effect
    def update_champ_choices():
        role = input.role_select()
        champ_list = shared.get_champs_per_role(role)
        ui.update_select(id="select_champ", choices=champ_list, session=session)
        
# Create the Shiny app object
app=App(app_ui, server)

