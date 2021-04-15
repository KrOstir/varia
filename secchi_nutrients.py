# %%
# Read and reformat Secchi measurements data
#
# Krištof Oštir
# (c) 2021

# %%
# Imports
import os
import pandas as pd

# %%
# Filenames
# Nutrients data
in_fn = 'C:/Data/GeoData/Secchi/Nutrienti.csv'
filename = os.path.splitext(in_fn)
out_fn = filename[0] + '_ref' + filename[1]

# %%
# Read dataframe
df = pd.read_csv(in_fn)
df.head()
df.columns

# %%
# Create date
df['Date'] = pd.to_datetime(dict(
    year=df['Godina'],
    month = df['Mjesec'],
    day = df['Dan'])) + pd.to_timedelta(df['Sat i minute (hh:mi)'])

# %%
df.drop(
    ['Godina', 'Mjesec', 'Dan', 'Sat i minute (hh:mi)'],
    inplace=True,
    axis='columns')
# %%
df_secchi = df[df['Nutrient'] == 'Secchi depth'].copy()
df_secchi.drop(['Nutrient', 'Mjerna jedinica', 'Dubina uzorkovanja'],
    inplace=True,
    axis='columns')

# %%
df_secchi.columns
# %%
