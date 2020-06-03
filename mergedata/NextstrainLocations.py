import os
import pandas as pd
import dateutil
from pathlib import Path

pd.options.display.max_rows = None  
pd.options.display.max_columns = None  

df = pd.read_csv("Nextstrain.csv")
df = df.fillna('')

# TODO