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
from urllib.request import Request, urlopen

# %%
# Files
# Where to put plots
rvt_plots = './figures/'
# Site
site = "https://plugins.qgis.org/plugins/rvt-qgis/"

# %%
# Read webpage
req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

# %%
# Read downloads
df = pd.read_html(webpage)[0]
df.head()

# %%
# Replace noon with time
df['Date'] = df['Date'].str.replace('noon','12:00 p.m.')

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
# Drop unnecessary columns
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
plt.plot(df['Downloads'], marker='.', markersize=10)
# plt.fill_between(df.index, df['Downloads'], alpha=0.4)
plt.title('Downloads per time')
ax.set_xlabel('Date')
ax.set_ylabel('Downloads')
plt.grid()
plt.savefig(rvt_plots + 'rvt_downloads_time.png', dpi=300)
# plt.show()
plt.close()

# %%
# Plot cumulative downloads per time
fig, ax = plt.subplots(figsize=(10, 8))
plt.plot(df['Downloads_sum'], marker='.', markersize=10)
plt.title('Cumulative downloads per time')
ax.set_xlabel('Date')
ax.set_ylabel('Downloads')
# plt.fill_between(df.index, df['Downloads_sum'], step="mid", alpha=0.4)
plt.grid()
plt.savefig(rvt_plots + 'rvt_downloads_cummulative_time.png', dpi=300)
# plt.show()
plt.close()

# %%
# Group by major.minor
df_version = df.groupby(['Major', 'Minor']).agg('sum')

# %%
# Compute cumulative sum
df_version['Downloads_sum'] = df_version[['Downloads']].cumsum()
df_version.reset_index(inplace=True)

# %%
# Generate major.minor versions
df_version['Version'] = df_version['Major'].str.cat(df_version['Minor'],sep='.')

# %%
# Plot downloads per time
fig, ax = plt.subplots(figsize=(10, 8))
plt.plot(
    df_version['Version'], df_version['Downloads_sum'],
    marker='.', markersize=10)
plt.grid()
plt.title('Cumulative downloads per version')
# df_version['Downloads_sum'].plot(drawstyle="steps-mid")
# plt.fill_between(df.index, df_version['Downloads'], step="mid", alpha=0.4)
ax.set_xlabel('Version (major.minor)')
ax.set_ylabel('Downloads')
# plt.show()
plt.savefig(rvt_plots + 'rvt_downloads_cumulative_version.png', dpi=300)
plt.close()

# %%
# Plot downloads per time
fig, ax = plt.subplots(figsize=(10, 8))
plt.plot(
    df_version['Version'], df_version['Downloads'],
    marker='.', markersize=10)
plt.title('Downloads per version')
# df_version['Downloads_sum'].plot(drawstyle="steps-mid")
# plt.fill_between(df.index, df_version['Downloads'], step="mid", alpha=0.4)
ax.set_xlabel('Version (major.minor)')
ax.set_ylabel('Downloads')
plt.grid()
# plt.show()
plt.savefig(rvt_plots + 'rvt_downloads_version.png', dpi=300)
plt.close()

# %%

# %%
