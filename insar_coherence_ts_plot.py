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
# tr_id = 4007
tr_id = 4020
# tr_id = 4026
ts_df_id = ts_df.xs(tr_id, level='ID_travnik', axis=1, drop_level=True)

# %%
# Average by polarisation
ts_df_id_pol = ts_df_id.mean(axis=1, level=1)

# %%
ts_df_id_pol['VH'].dropna().plot(style = 'r-', label = 'VH', alpha=0.3)
ts_df_id_pol['VH'].dropna().rolling(5, center=True).mean().plot(style= 'r-', label='')
ts_df_id_pol['VV'].dropna().plot(style = 'b-', label = 'VV', alpha=0.3)
ts_df_id_pol['VV'].dropna().rolling(5, center=True).mean().plot(style= 'b-', label='')
plt.legend()
plt.show()

# %%
ts_df_id_pol.plot(marker='o')
plt.show()
