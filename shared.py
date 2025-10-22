from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent

#defualt patch
patch_file = "champs.csv"

champ_df = pd.read_csv(app_dir / "data" / patch_file, sep=';')

def update_patch(patch):
    df = pd.read_csv(app_dir / "data" / patch, sep=';')
    return df