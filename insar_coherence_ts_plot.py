# %%
# Plot InSAR time series per polygon
# Filter polarisation, ID
# Krištof Oštir
# 2020-07-22

# %%
# Libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %%
# Filenames
ts_fn = './data/coherence_pregledani.csv'

# %%
# Read TS data for polygons
ts_df = pd.read_csv(ts_fn, nrows=100)
# ts_df = pd.read_csv(ts_fn)

# %%
# Create orbit ASC/DES and polarisation VH/VV columns
ts_df['pol'] = ts_df['Obmocje'].str[-2:]
ts_df['orb'] = ts_df['Obmocje'].str[-6:-3]

# %%
# Drop unneeded columns
ts_df.drop(['Unnamed: 0', 'Obmocje', 'Razred', 'area', 'slope', 'aspect', 'latitude', 'HAB'], axis=1, inplace=True)

# %%
# Set ID, orbit and polarisation as index
ts_df.set_index(['ID_travnik', 'orb', 'pol'], inplace=True)

# %%
# Put all 0 to nan
ts_df.replace(0, np.nan, inplace=True)

# %%
# Transpose DF
ts_df = ts_df.transpose()

# %%
# Set datetime
ts_df.index = pd.to_datetime(ts_df.index)

# %%
# Select one polygon
tr_id = 4007
ts_df_id = ts_df.xs(tr_id, level='ID_travnik', axis=1, drop_level=True)

# %%
ts_df_id_asc = ts_df_id.xs('ASC', level='orb', axis=1, drop_level=True).dropna()
ts_df_id_des = ts_df_id.xs('DES', level='orb', axis=1, drop_level=True).dropna()

# %%
ts_df_id_asc.plot()
plt.show()

# %%
ts_df_id_des.plot()
plt.show()
