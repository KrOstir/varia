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
# Set date as index
df.set_index('Date', inplace=True)
# Sort
df.sort_index(inplace=True)

# %%
df.drop(
    ['Experimental', 'Minimum QGIS version', 'Uploaded by'],
    axis=1, inplace=True)

# %%
# Split version to major.minor.micro
df[['Major','Minor', 'Micro']] = df['Version'].str.split(".", n = 2, expand = True)
df.drop('Version', axis=1, inplace=True)

# %%
df.head()

# %%
# Compute cumulative sum
df['Downloads_sum'] = df['Downloads'].cumsum()

# %%
# Plot downloads per time
fig, ax = plt.subplots(figsize=(10, 8))
plt.plot(df['Downloads'], drawstyle="steps-post")
plt.fill_between(df.index, df['Downloads'], step="post", alpha=0.4)
# plt.savefig(ps_plots + 'ps_sciences.png', dpi=300)
plt.show()
# plt.close()

# %%
# Plot cumulative downloads per time
fig, ax = plt.subplots(figsize=(10, 8))
plt.plot(df['Downloads_sum'], drawstyle="steps-post")
plt.fill_between(df.index, df['Downloads_sum'], step="post", alpha=0.4)
# plt.savefig(ps_plots + 'ps_sciences.png', dpi=300)
plt.show()
# plt.close()


# %%
# Group by major.minor
df_version = df.groupby(['Major', 'Minor']).agg('sum')

# %%
# Compute cumulative sum
df_version['Downloads_sum'] = df_version[['Downloads']].cumsum()

# %%
df_version.reset_index(inplace=True)

# %%
df_version['Version'] = df_version['Major'].str.cat(df_version['Minor'],sep='.')
# %%
# Plot downloads per time
fig, ax = plt.subplots(figsize=(10, 8))
plt.plot(df_version['Version'], df_version['Downloads_sum'], drawstyle="steps-post")
# df_version['Downloads_sum'].plot(drawstyle="steps-post")
# plt.fill_between(df.index, df_version['Downloads'], step="mid", alpha=0.4)
# plt.savefig(ps_plots + 'ps_sciences.png', dpi=300)
plt.show()
# plt.close()
# %%
# %%
type(df_version)
# %%
df_version
# %%
