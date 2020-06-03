import os
import pandas as pd

pd.options.display.max_rows = None
pd.options.display.max_columns = None

# UNregion, subregion, intermediate regions
df = pd.read_excel("../reference_data/UNSDMethodology.xlsx", dtype='str')
df = df[['Region Name', 'Region Code', 'Sub-region Name', 'Sub-region Code', 
         'Intermediate Region Name', 'Intermediate Region Code', 'ISO-alpha3 Code']]
df.fillna('', inplace=True)
df.rename(columns={'ISO-alpha3 Code': 'iso3'}, inplace=True)
df = df.query("iso3 != ''")
df.rename(columns={'Region Name': 'UNRegion'}, inplace=True)
df = df.query("UNRegion != ''")

# df.rename(columns={'Region Name': 'UNRegion'}, inplace=True)
df.rename(columns={'Region Code': 'UNRegionCode'}, inplace=True)
df.rename(columns={'Sub-region Name': 'UNSubRegion'}, inplace=True)
df.rename(columns={'Sub-region Code': 'UNSubRegionCode'}, inplace=True)
df.rename(columns={'Intermediate Region Name': 'UNIntermediateRegion'}, inplace=True)
df.rename(columns={'Intermediate Region Code': 'UNIntermediateRegionCode'}, inplace=True)
# df.rename(columns={'ISO-alpha3 Code': 'iso3'}, inplace=True)

# Assign unique identifiers
df['UNRegionCode'] = 'm49:' + df['UNRegionCode']
df['UNSubRegionCode'] = 'm49:' + df['UNSubRegionCode'] 
df['UNIntermediateRegionCode'] = 'm49:' + df['UNIntermediateRegionCode']

additions = pd.read_csv("UNRegionAdditions.csv")
additions.fillna('', inplace=True)
additions.tail(10)

df = df.append(additions)

intermediateRegion = df[df['UNIntermediateRegion'] != '']
intermediateRegion.to_csv("UNIntermediateRegion.csv", index=False)                          

subRegion = df[(df['UNSubRegion'] != '') & (df['UNIntermediateRegion'] == '')]
subRegion.to_csv("UNSubRegion.csv", index=False)

region = df[(df['UNSubRegion'] == '') & (df['UNIntermediateRegion'] == '')]
region.to_csv("UNRegion.csv", index=False)  