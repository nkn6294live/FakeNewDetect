import os
import pandas as pd

pd.options.display.max_rows = None
pd.options.display.max_columns = None

country_url = 'https://download.geonames.org/export/dump/countryInfo.txt'
export_file_path = "GeoNamesCountry.csv"

names = [
    'ISO','ISO3','ISO-Numeric','fips','Country','Capital','Area(in sq km)','Population',
    'Continent','tld','CurrencyCode','CurrencyName','Phone','Postal Code Format',
    'Postal Code Regex','Languages','geonameid','neighbours','EquivalentFipsCode'
]

countries = pd.read_csv(country_url, sep='\t',comment='#', dtype='str', names=names)
index = countries.query("ISO3 == 'NAM'").index
countries.at[index, 'ISO'] = 'NA'

# Standardize column names: id, name, parentId, ...

countries['id'] = countries['ISO']
countries.rename(columns={'ISO': 'iso'}, inplace=True)
countries.rename(columns={'ISO3': 'iso3'}, inplace=True)
countries.rename(columns={'Country': 'name'}, inplace=True)
countries.rename(columns={'Population': 'population'}, inplace=True)
countries.rename(columns={'Area(in sq km)': 'areaSqKm'}, inplace=True)
countries.rename(columns={'Continent': 'parentId'}, inplace=True)

countries = countries[['id','name','iso','iso3','population','areaSqKm','parentId']]
countries = countries.fillna('')

countries.to_csv(export_file_path, index=False)