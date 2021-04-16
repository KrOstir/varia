# %%
# Relief Visualization Tool Download Statistics
#
# Krištof Oštir
# (c) 2021

# %%
# Imports
import pandas as pd
import matplotlib.pyplot as plt
from dateutil import parser

# %%
# Files
rvt_dl_fn = './data/rvt_qgis_plugins.csv'
# Where to put plots
rvt_plots = './data/'

# %%
# Read downloads
df = pd.read_csv(rvt_dl_fn)
df.head()

# %%
# Parse dates
df['Date'] = df.apply(
    lambda x: parser.parse(x['Date']), axis=1)

# %%
df.head()

# %%
# %%
# Plot downloads per time
fig, ax = plt.subplots(figsize=(10, 8))
plt.plot(df['Date'], df['Downloads'])
# plt.savefig(ps_plots + 'ps_sciences.png', dpi=300)
plt.show()
# plt.close()


# %%
# Group by date
df_cum = df.groupby('Date').agg('sum').apply(lambda x: x.cumsum())

# %%
# Plot cumulative downloads per time
fig, ax = plt.subplots(figsize=(10, 8))
plt.step(df_cum.index, df_cum)
# plt.savefig(ps_plots + 'ps_sciences.png', dpi=300)
plt.show()
# plt.close()
