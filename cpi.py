import pandas as pd
import requests
import os
import re

def get_jan_columns_post_1990(df):
    selected_cols = []
    for col in df.columns:
        if 'Jan' in col:
            match = re.search(r'(\d{4})', col)
            if match:
                year = int(match.group(1))
                if year >= 1990:
                    selected_cols.append(col)
    return df[selected_cols]

# Example usage:
# df = pd.read_csv('your_data.csv')
# filtered_df = get_jan_columns_post_1990(df)

"""
url = f"https://api-open.data.gov.sg/v1/public/api/datasets/" + "d_bdaff844e3ef89d39fceb962ff8f0791"
response = requests.get(url)
data = response.json()

download_url = data["data"]["url"]
df = pd.read_csv(download_url)
df.to_csv("raw/ConsumerPriceIndexCPI2024AsBaseYearMonthly.csv")
"""

df = pd.read_csv("raw/ConsumerPriceIndexCPI2024AsBaseYearMonthly.csv")
df['DataSeries'] = df['DataSeries'].str.strip()
target_rows = ['All Items']
df = df[df['DataSeries'].isin(target_rows)]

df = get_jan_columns_post_1990(df)

df.columns = [col.replace('Jan', '') for col in df.columns]
df = df.melt(var_name='Year', value_name='Overall')


print(df.head())

df.to_csv("data/cpi.csv")