from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
champ_df = pd.read_csv(app_dir / "data" / "champs1.csv", sep=';')
