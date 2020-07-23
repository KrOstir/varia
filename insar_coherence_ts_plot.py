# Plot InSAR time series per polygon
# Filter polarisation, ID
# Krištof Oštir
# 2020-07-22

# %%
# Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %%
# Filenames
ts_fn = './data/coherence_pregledani.csv'

# %%
ts_df = pd.read_csv(ts_fn)

# %%
tr_id = 4007
ts_df_id = ts_df[ts_df['ID_travnik'] == tr_id].copy()
ts_df_id.set_index('Obmocje', inplace=True)
columns = ts_df_id.columns
cols = [0, 1, 2, len(columns)-2, len(columns)-1]
ts_df_id.drop(ts_df_id.columns[cols],axis=1,inplace=True)
ts_df_id = ts_df_id.transpose()
ts_df_id.index = pd.to_datetime(ts_df_id.index)
ts_df_id.replace(0, np.nan, inplace=True)

# %%
# plt.plot(ts_df_id['DoblicicaASC_VH'].dropna())
# plt.plot(ts_df_id['DoblicicaASC_VV'].dropna())
plt.plot(ts_df_id['DoblicicaDES_VH'].dropna())
plt.plot(ts_df_id['DoblicicaDES_VH'].dropna())
plt.show()
