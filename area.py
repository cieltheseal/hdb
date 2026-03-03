import requests
import geopandas as gpd
from io import BytesIO

"""
def load_geo_dataset(dataset_id):
    url = f"https://api-open.data.gov.sg/v1/public/api/datasets/" + dataset_id + "/poll-download"
    response = requests.get(url).json()

    if response["code"] != 0:
        raise Exception(response["errMsg"])

    download_url = response["data"]["url"]
    geo_bytes = requests.get(download_url).content

    return gpd.read_file(BytesIO(geo_bytes))

gdf = load_geo_dataset("d_8594ae9ff96d0c708bc2af633048edfb")
"""

gdf = gpd.read_file("raw/Master Plan 2019 Subzone Boundary (No Sea) (GEOJSON).geojson")
gdf.drop(columns=["SUBZONE_NO", "SUBZONE_C", "PLN_AREA_C", "REGION_C", "SUBZONE_N", "CA_IND"], inplace=True)
gdf = gdf.rename(columns={"PLN_AREA_N": "Town"})
gdf = gdf.dissolve(by="Town", as_index=False)
gdf['Town'] = gdf['Town'].str.title()
gdf.to_file("data/planning_area.geojson", driver="GeoJSON")