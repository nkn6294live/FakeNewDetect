import os
import pandas as pd
import dateutil
from pathlib import Path

pd.options.display.max_rows = None
pd.options.display.max_columns = None

df = pd.read_csv("../reference_data/nextstrain_ncov_global_metadata.tsv", sep = '\t', dtype=str, error_bad_lines=False)


# Transform and standardize data
df.replace('?', '', inplace=True)
df.replace('Unknown', '', inplace=True)
df.fillna('', inplace=True)

df.rename(columns={'Strain': 'name', 'Clade': 'clade', 'Age': 'age', 'Sex': 'sex', 'Collection Data': 'collectionDate'}, inplace=True)
df.rename(columns={'Country of exposure': 'exposureCountry', 'Division of exposure': 'exposureAdmin1'}, inplace=True)

df['collectionDate'] = df['collectionDate'].apply(lambda d: dateutil.parser.parse(d) if len(d) > 0 else '')
# assign taxonomy for SARS-CoV-2
df['taxonomyId'] = 'taxonomy:2697049'

taxonomy_to_id = {'Human': 'taxonomy:9606', 
                  'Homo sapiens': 'taxonomy:9606',
                  'Rhinolophus affinis': 'taxonomy:59477', 
                  'Rhinolophus sp. (bat)': 'taxonomy:49442',
                  'Mustela lutreola': 'taxonomy:9666',
                  'Panthera tigris jacksoni': 'taxonomy:419130',
                  'bat': 'taxonomy:49442',
                  'Manis javanica': 'taxonomy:9974',
                  'palm civet': 'taxonomy:71116',
                  'Canine': 'taxonomy:9608',
                  'Felis catus': 'taxonomy:9685'
                 }
# assign taxonomy id for host
df['Host'] = df['Host'].str.strip()
df['hostTaxonomyId'] = df['Host'].apply(lambda s: taxonomy_to_id.get(s, ''))
df = df.query("hostTaxonomyId != ''")
df['hostTaxonomyId'].unique()
df['sex'] = df['sex'].str.lower()

df['id'] = 'https://www.gisaid.org/' + df['gisaid_epi_isl']

df = df[['id', 'name', 'taxonomyId', 'collectionDate',
         'hostTaxonomyId', 'sex', 'age', 'clade',
         'exposureCountry', 'exposureAdmin1']]

df.to_csv("Nextstrain.csv", index=False)