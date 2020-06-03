import os
import pandas as pd

pd.options.display.max_rows = None
pd.options.display.max_columns = None

census_url = 'https://raw.githubusercontent.com/baltimore-sun-data/bridge-data/master/input/all-geocodes-v2017.xlsx'

df = pd.read_excel(census_url, dtype='str', skiprows=4)
df.rename(columns={'Area Name (including legal/statistical area description)': 'name'}, inplace=True)
df.rename(columns={'County Code (FIPS)': 'fips'}, inplace=True)
df.rename(columns={'County Subdivision Code (FIPS)': 'sfips'}, inplace=True)

# USCounties
counties = df.query("fips != '000'").query("sfips == '00000'").copy()
counties['stateFips'] = counties['State Code (FIPS)']
counties = counties[['name', 'fips', 'stateFips']]

counties.to_csv("USCensus2017County.csv", index=False)

# US Cities
df.rename(columns={'fips': '_fips'}, inplace=True)
df.rename(columns={'Place Code (FIPS)': 'fips'}, inplace=True)

cities = df.query("fips != '00000'").copy()
cities['stateFips'] = cities['State Code (FIPS)']
cities = cities[['name', 'fips', 'stateFips']]

cities['name'] = cities['name'].str.replace(' city','')
cities['name'] = cities['name'].str.replace(' town','')

cities.to_csv("USCensus2017City.csv", index=False)