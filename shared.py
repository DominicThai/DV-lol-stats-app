from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
data = pd.read_csv(app_dir / "data" / "champ_stats_13.1.csv", sep=';')

#sorts the tiers in a custom order instead of alphabetically
tier_order = {"S": 1, "A": 2, "B": 3, "C": 4, "D": 5}
data["Tier_sort"] = data["Tier"].map(tier_order)

champ_df = data.sort_values("Tier")