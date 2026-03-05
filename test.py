import requests
import geopandas as gpd
from io import BytesIO
import pandas as pd

resale = pd.read_csv("data/resale_prices.csv")

# Create a new dataframe containing only the long-lease rows
long_lease_df = resale[resale['remaining_lease'] > 99]

# To just see the first few rows
print(long_lease_df.head())
print(long_lease_df.tail())