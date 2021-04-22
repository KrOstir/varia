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
meta_fn = 'C:/Data/GeoData/Secchi/measuring_station_location.csv'
filename = os.path.splitext(in_fn)
out_fn = filename[0] + '_ref' + filename[1]

# %%
# Read dataframe
df = pd.read_csv(in_fn)
df.head()
# df.columns

# %%
# Read metadata
mdf = pd.read_csv(meta_fn, encoding='iso8859_2')
mdf.head()
# mdf.columns

# %%
# Create date
df['Date'] = pd.to_datetime(dict(
    year=df['Godina'],
    month = df['Mjesec'],
    day = df['Dan'])) + pd.to_timedelta(df['Sat i minute (hh:mi)'])

# %%
# Drop date remaining data
df.drop(
    ['Godina', 'Mjesec', 'Dan', 'Sat i minute (hh:mi)'],
    inplace=True,
    axis='columns')
# %%
# Select only Secchi depth and measurement attributes
df_secchi = df[df['Nutrient'] == 'Secchi depth'].copy()
df_secchi.drop(['Nutrient', 'Mjerna jedinica', 'Dubina uzorkovanja'],
    inplace=True,
    axis='columns')

# %%
# Rename columns
df_secchi.rename(columns={'Koncentracija': 'Secchi'}, inplace=True)

# %%
# Join dataframe with metadata
df_secchi = df_secchi.merge(mdf, on='Postaja')

# %%
# Columns
df_secchi.columns
# %%
# Write to CSV
df_secchi.to_csv(out_fn, index=False, encoding='utf-8')

# %%
