import requests
import geopandas as gpd
from io import BytesIO
import pandas as pd

resale = pd.read_csv("data/resale_prices.csv")

gdf = gpd.read_file("raw/Master Plan 2019 Subzone Boundary (No Sea) (GEOJSON).geojson")
gdf.drop(columns=["SUBZONE_NO", "SUBZONE_C", "PLN_AREA_C", "REGION_C", "SUBZONE_N", "CA_IND"], inplace=True)
gdf = gdf.rename(columns={"PLN_AREA_N": "Town"})

gdf = gdf.dissolve(by="Town", as_index=False)
gdf['Town'] = gdf['Town'].str.title()

# 1. Get unique values from both, ensuring they are clean strings
resale_towns = set(resale['town'].unique())
gdf_towns = set(gdf['Town'].unique())

print(sorted(gdf_towns))

# 2. Find towns in resale but NOT in gdf
missing_in_gdf = resale_towns - gdf_towns

"""
# 3. Print the results
print(f"Count of missing towns: {len(missing_in_gdf)}")
print("Towns in resale data not found in GDF:")
print(missing_in_gdf)
"""

# 2. Sort them alphabetically so they are easier to read
central_area_streets = sorted(resale[resale['town'] == 'Central Area']['street_name'].unique())

# 3. Print the list
print(f"Unique streets in Central Area ({len(central_area_streets)} total):")
print(central_area_streets)