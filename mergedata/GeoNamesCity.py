import os
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from pathlib import Path
import pandas as pd

pd.options.display.max_rows = None 
pd.options.display.max_columns = None 

names = [
        'geonameid','name','asciiname','alternatenames','latitude','longitude','feature class',
        'feature code','country code','cc2','admin1 code','admin2 code','admin3 code','admin4 code',
        'population','elevation','dem','timezone','modification date'
]

export_file_path = "GeoNamesCity.csv"

url = 'https://download.geonames.org/export/dump/cities15000.zip'
file_name = "cities15000.txt"
resp = urlopen(url)
zipfile = ZipFile(BytesIO(resp.read()))
city_15k = pd.read_csv(zipfile.open(file_name), sep="\t", low_memory=False, names=names)

url = 'https://download.geonames.org/export/dump/cities5000.zip'
file_name = "cities5000.txt"
resp = urlopen(url)
zipfile = ZipFile(BytesIO(resp.read()))
city_5k = pd.read_csv(zipfile.open(file_name), sep="\t", low_memory=False, names=names)

url = 'https://download.geonames.org/export/dump/cities1000.zip'
file_name = "cities1000.txt"
resp = urlopen(url)
zipfile = ZipFile(BytesIO(resp.read()))
city_1k = pd.read_csv(zipfile.open(file_name), sep="\t", low_memory=False, names=names)


city = pd.concat([city_15k, city_5k, city_1k])

city = city[['geonameid', 'asciiname', 'country code', 'admin1 code', 'admin2 code', 'population', 'elevation']]
city = city.fillna('')

city = city.drop_duplicates('geonameid')


def get_location_id(country, admin1, admin2):
    location = country
    if admin1 != '':
        location = location + '.' + admin1
    if admin2 != '':
        location = location + '.' + admin2
        
    return location

# Standardize column names: id, name, parentId
city.rename(columns={'geonameid': 'id'}, inplace=True)
city.rename(columns={'asciiname': 'name'}, inplace=True)
city['parentId'] = city.apply(lambda row: get_location_id(row['country code'], 
                                                         row['admin1 code'], 
                                                         row['admin2 code']), axis=1)

city = city[['id', 'name', 'population', 'elevation', 'parentId']]
city.fillna('', inplace=True)
city.to_csv(export_file_path)