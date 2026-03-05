import pandas as pd
import requests
import os

"""
url = f"https://api-open.data.gov.sg/v1/public/api/datasets/" + "d_8b84c4ee58e3cfc0ece0d773c8ca6abc" + "/poll-download"
response = requests.get(url)
data = response.json()

download_url = data["data"]["url"]
df2017 = pd.read_csv(download_url)
df2017.to_csv("raw/ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv")
"""

df1990 = pd.read_csv("raw/ResaleFlatPricesBasedonApprovalDate19901999.csv")
df2000 = pd.read_csv("raw/ResaleFlatPricesBasedonApprovalDate2000Feb2012.csv")
df2012 = pd.read_csv("raw/ResaleFlatPricesBasedonRegistrationDateFromMar2012toDec2014.csv")
df2015 = pd.read_csv("raw/ResaleFlatPricesBasedonRegistrationDateFromJan2015toDec2016.csv")
df2017 = pd.read_csv("raw/ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv")

# Append (stack rows)
resale = pd.concat(
    [df1990, df2000, df2012, df2015, df2017],
    ignore_index=True
)

resale["year"] = pd.to_datetime(resale["month"]).dt.year
resale["remaining_lease"] = 99 - (resale["year"] - resale["lease_commence_date"])
resale['flat_type'] = resale['flat_type'].str.replace('MULTI-GENERATION', 'MULTI GENERATION')
resale["flat_model"] = resale["flat_model"].str.upper()
resale['flat_type'] = resale['flat_type'].str.capitalize().str.replace(' ', '-')
resale['town'] = resale['town'].str.title()

def get_midpoint(storey_str):
    try:
        # Split "04-06" into ["04", "06"]
        start, end = storey_str.split(' TO ')
        return (int(start) + int(end)) / 2
    except:
        return None

resale['avg_storey'] = resale['storey_range'].apply(get_midpoint).astype(int)


# Removing flats which were apparently sold before MOP
# 1. Condition for lease > 1971, not a small flat, and lease > 95
# (Focuses on 3-room and larger flats that shouldn't have such high leases)
cond1 = (resale['lease_commence_date'] > 1971) & (~resale['flat_type'].isin(['1-room', '2-room'])) & (resale['remaining_lease'] > 95)

# 2. Condition for lease > 1971 and remaining_lease > 97
cond2 = (resale['lease_commence_date'] > 1971) & (resale['remaining_lease'] > 97)

# 3. Condition for lease > 2010 and remaining_lease > 95
cond3 = (resale['lease_commence_date'] > 2010) & (resale['remaining_lease'] > 95)

resale = resale[~(cond1 | cond2 | cond3)].copy()
resale.drop(columns=["block"], inplace=True)

resale['lease_commence_date'] = resale['lease_commence_date'].fillna(
    resale['year'] - (99 - resale['remaining_lease'])
)

### 2019 planning area updates (Fix Kallang and assign Central Area)
resale.loc[resale['town'].str.contains('Kallang', case=False, na=False), 'town'] = 'Kallang'
#central_area_streets = sorted(resale[resale['town'] == 'Central Area']['street_name'].unique())
#print(f"Unique streets in Central Area ({len(central_area_streets)} total):")
#print(central_area_streets)

resale.loc[resale['street_name'] == 'BAIN STREET', 'town'] = 'Downtown Core'
resale.loc[resale['street_name'] == 'BAIN ST', 'town'] = 'Downtown Core'
resale.loc[resale['street_name'] == 'BUFFALO ROAD', 'town'] = 'Rochor'
resale.loc[resale['street_name'] == 'BUFFALO RD', 'town'] = 'Rochor'
resale.loc[resale['street_name'] == 'CANTONMENT ROAD', 'town'] = 'Downtown Core'    # This is between Downtown Core and Outram, could be either
resale.loc[resale['street_name'] == 'CANTONMENT RD', 'town'] = 'Downtown Core'    # This is between Downtown Core and Outram, could be either
resale.loc[resale['street_name'] == 'CHANDER RD', 'town'] = 'Rochor'
resale.loc[resale['street_name'] == 'CHIN SWEE RD', 'town'] = 'Outram'
resale.loc[resale['street_name'] == 'JLN BERSEH', 'town'] = 'Rochor'
resale.loc[resale['street_name'] == 'JLN KUKOH', 'town'] = 'Outram'
resale.loc[resale['street_name'] == 'KELANTAN RD', 'town'] = 'Rochor'
resale.loc[resale['street_name'] == 'KLANG LANE', 'town'] = 'Rochor'
resale.loc[resale['street_name'] == 'KRETA AYER RD', 'town'] = 'Outram'
resale.loc[resale['street_name'] == 'NEW MKT RD', 'town'] = 'Singapore River'
resale.loc[resale['street_name'] == 'OUTRAM HILL', 'town'] = 'Outram'
resale.loc[resale['street_name'] == 'OUTRAM PK', 'town'] = 'Outram'
resale.loc[resale['street_name'] == 'QUEEN ST', 'town'] = 'Rochor'
resale.loc[resale['street_name'] == 'ROCHOR RD', 'town'] = 'Downtown Core'   # This is between Downtown Core and Rochor, but a longer stretch is in Downtown Core
resale.loc[resale['street_name'] == 'ROWELL RD', 'town'] = 'Rochor'
resale.loc[resale['street_name'] == 'SAGO LANE', 'town'] = 'Outram'
resale.loc[resale['street_name'] == 'SELEGIE RD', 'town'] = 'Rochor'
resale.loc[resale['street_name'] == 'SHORT ST', 'town'] = 'Rochor'
resale.loc[resale['street_name'] == 'SMITH ST', 'town'] = 'Outram'
resale.loc[resale['street_name'] == 'TG PAGAR PLAZA', 'town'] = 'Downtown Core'
resale.loc[resale['street_name'] == 'UPP CROSS ST', 'town'] = 'Outram'
resale.loc[resale['street_name'] == 'VEERASAMY RD', 'town'] = 'Rochor'
resale.loc[resale['street_name'] == 'WATERLOO ST', 'town'] = 'Rochor'



resale.to_csv("data/resale_prices.csv")