# %%

# Analyse financial data
# Import data from Gorenjska banka and perform financial analysis.

# %%

# Libraries
import pandas as pd
from io import StringIO
import glob

# %%

# Path
fd_path = './data/finance/'

# %%

# All files
fd_files = glob.glob(fd_path + "/promet_izvoz_*.txt")

# %%

# Read DFs

li = []

for filename in fd_files:
    print(filename)
    with open(filename, "r", encoding="utf-8") as myfile:
        data = myfile.read()
    data = data.replace('GEODEZIJO;', 'GEODEZIJO-')
    df = pd.read_csv(StringIO(data), sep=';')
    li.append(df)

# %%

# Joind DFs
fd_df = pd.concat(li, axis=0, ignore_index=True)

# %%
