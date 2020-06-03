import os
import pandas as pd

pd.options.display.max_rows = None
pd.options.display.max_columns = None

admin1_url = 'https://download.geonames.org/export/dump/admin1CodesASCII.txt'
export_file_path = "GeoNamesAdmin1.csv"

names = ['code', 'name', 'name_ascii', 'geonameid']

admin1 = pd.read_csv(admin1_url, sep='\t', dtype='str', names=names)
admin1 = admin1[['code', 'name_ascii']]

### Standardize column names: id, name, parentId,...
admin1.rename(columns={'code': 'id'}, inplace=True)
admin1.rename(columns={'name_ascii': 'name'}, inplace=True)
admin1['code'] = admin1['id'].str.split('.', expand=True)[1]
admin1['parentId'] = admin1['id'].str.split('.', expand=True)[0]

admin1 = admin1[['id','name','code','parentId']]
admin1 = admin1.fillna('')

admin1.to_csv(export_file_path, index=False)