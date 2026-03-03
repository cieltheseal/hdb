import requests
import pandas as pd
import numpy as np

"""
dataset_id = "d_2d493bdcc1d9a44828b6e71cb095b88d"
url = "https://data.gov.sg/api/action/datastore_search?resource_id=" + dataset_id

response = requests.get(url)
data = response.json()

# Extract records
records = data['result']['records']

# Convert to DataFrame
df = pd.DataFrame(records)
"""

### Read Df
df = pd.read_csv("raw/PriceRangeofHDBFlatsOffered.csv")

price_cols = [
    "min_selling_price",
    "max_selling_price",
    "min_selling_price_less_ahg_shg",
    "max_selling_price_less_ahg_shg"
]

for col in price_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df["room_type"] = df["room_type"].str.strip()
df = df[(df["min_selling_price"] != 0)]
df.loc[df["max_selling_price_less_ahg_shg"] == 0, "max_selling_price_less_ahg_shg"] = np.nan
df.loc[df["min_selling_price_less_ahg_shg"] == 0, "min_selling_price_less_ahg_shg"] = np.nan


is_new_project = df['room_type'] < df['room_type'].shift(1)
df['project_id'] = is_new_project.cumsum()
df['project_id'] = df['project_id'] + 1

df.to_csv("data/bto_price.csv")

