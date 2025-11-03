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


#Combines all CSVs into one dataframe for time series analysis
def get_all_patches():
    all_files = sorted((app_dir / "data").glob("patch_*.csv"))
    df_list = []
    for file in all_files:
        temp_df = pd.read_csv(file, sep=';')
        # Extract patch number from filename
        patch_number = file.stem.split("_")[1]
        temp_df["patch"] = patch_number
        df_list.append(temp_df)
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Rename the columns to remove spaces and weird characters like %
    combined_df = combined_df.rename(columns={
    "Pick %": "pick_pct",
    "Win %": "win_pct",
    "Ban %": "ban_pct",
    "Role %": "role_pct",
    "Name": "name",
    "Class": "class",
    "Role": "role"
    })
    
    # Converts percantage from string to float
    combined_df["pick_pct"] = combined_df["pick_pct"].str.replace("%", "").astype(float)
    combined_df["win_pct"] = combined_df["win_pct"].str.replace("%", "").astype(float)
    combined_df["ban_pct"] = combined_df["ban_pct"].str.replace("%", "").astype(float)
    
    return combined_df

def get_champs_per_role(role):
    df = get_all_patches()
    champs_list = df.loc[df['role'] == role, 'name'].tolist()
    champs_list = list(dict.fromkeys(champs_list))
    return champs_list
    
