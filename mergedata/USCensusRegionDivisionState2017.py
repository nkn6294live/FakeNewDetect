import os
import pandas as pd

pd.options.display.max_rows = None
pd.options.display.max_columns = None

census_url = 'https://raw.githubusercontent.com/cumminsjp/Agema/master/fips/state-geocodes-v2017.xlsx'

df = pd.read_excel(census_url, dtype='str', skiprows=5)
df.rename(columns={'State (FIPS)': 'fips'}, inplace=True)
df.rename(columns={'Name': 'name'}, inplace=True)

# USRegion
regions = df.query("Division == '0'").copy()
regions.rename(columns={'Region': 'id'}, inplace=True)
regions['id'] = 'US.' + regions['id']
regions['parentId'] = 'US'
regions = regions[['id', 'name', 'parentId']]

regions.to_csv("USCensus2017Region.csv", index=False)

# Divisions 
divisions = df.query("Division != '0'").query("fips == '00'").copy()
divisions.rename(columns={'Division': 'id'}, inplace=True)
divisions['parentId'] = 'US.' + divisions['Region']
divisions['id'] = 'US.' + divisions['Region']  + '.' + divisions['id']
divisions = divisions[['id', 'name', 'parentId']]

divisions.to_csv("USCensus2017Division.csv", index=False)

# US State FIPS codes
states = df.query("Division != '0'").query("fips != '00'").copy()
states['parentId'] = 'US.' + states['Region']  + '.' + states['Division']
states = states[['name', 'fips', 'parentId']]

states.to_csv("USCensus2017State.csv", index=False)