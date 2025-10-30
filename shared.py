from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent

#defualt patch
patch_file = "patch_13.1.csv"

champ_df = pd.read_csv(app_dir / "data" / patch_file, sep=';')

def get_patch(patch):
    #Reads the file that is selected in the dropdown menu
    df = pd.read_csv(app_dir / "data" / patch, sep=';')
    
    # Rename the columns to remove spaces and weird characters like %
    df = df.rename(columns={
    "Pick %": "pick_pct",
    "Win %": "win_pct",
    "Ban %": "ban_pct",
    "Role %": "role_pct",
    "Name": "name",
    "Class": "class",
    "Role": "role"
    })
    
    # Converts percantage from string to float
    df["pick_pct"] = df["pick_pct"].str.replace("%", "").astype(float)
    df["win_pct"] = df["win_pct"].str.replace("%", "").astype(float)
    df["ban_pct"] = df["ban_pct"].str.replace("%", "").astype(float)
    return df
