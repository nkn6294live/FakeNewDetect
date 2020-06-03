import os
import pandas as pd

pd.options.display.max_rows = None 
pd.options.display.max_columns = None 

admin2_url = 'https://download.geonames.org/export/dump/admin2Codes.txt'
export_file_path = "GeoNamesAdmin2.csv"
names = ['code', 'name', 'name_ascii', 'geonameid']

admin2 = pd.read_csv(admin2_url, sep='\t', dtype='str', names=names)
admin2 = admin2[['code', 'name_ascii']]

# Standardize column names: id, name, parent_id
admin2.rename(columns={'code': 'id'}, inplace=True)
admin2.rename(columns={'name_ascii': 'name'}, inplace=True)
admin2['parentId'] = admin2['id'].str.rsplit('.', 1, expand=True)[0]

admin2 = admin2[['id', 'name', 'parentId']]
admin2 = admin2.fillna('')

admin2.to_csv(export_file_path, index=False)
