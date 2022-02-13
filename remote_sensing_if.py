# %%
# Impact Factor for remote sensing journals
#
# Krištof Oštir
# (c) 2021

# %%
# Libraries
import pandas as pd
import matplotlib.pyplot as plt
# from dateutil import parser
from urllib.request import Request, urlopen
import urllib.parse

# %%
# Parameters
# IF URL
# https://plus.si.cobiss.net/opac7/jcr?py=&ti=&sc=&max=100
if_base_url = 'https://plus.si.cobiss.net/opac7/jcr?py={0}&ti={1}&sc={2}&max=100'
# Where to put plots
plots_folder = './figures/'
# IF data
if_fn = './data/remote_sensing_if.csv'
# Keywords
journal_kw = 'remote sensing'
# Top journals
top_n = 15
top_if = 2

# %%
# Find last year data is published
s_year = urllib.parse.quote('')
s_kw = urllib.parse.quote('')
s_issn = urllib.parse.quote('2168-6831')
if_url = if_base_url.format(s_year, s_kw, s_issn)
# Read webpage
req = Request(if_url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
if_rs_df = pd.read_html(webpage)[0]
# %%
year = if_rs_df['Leto'].max()

# %%
# Create list of journals
print('Getting list of journals for {}'.format(year))
s_year = urllib.parse.quote(str(year))
s_kw = urllib.parse.quote(journal_kw)
s_issn = urllib.parse.quote('')
if_url = if_base_url.format(s_year, s_kw, s_issn)
# Read webpage
req = Request(if_url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
# Read IF
if_rs_df = pd.read_html(webpage)[0]
if_rs_df.head()

# %%
if_rs_df = if_rs_df.drop(['Št.'], axis=1)
if_rs_df

# %%
if_rs_df.dtypes

# %%
# Top n journals
# if_rs_df = if_rs_df.sort_values('Faktor vpliva', ascending=False).head(top_n)

# %%
# IF larger then treshold
if_rs_df = if_rs_df.loc[if_rs_df['Faktor vpliva'] >= top_if]

# %%
# Print top
print(if_rs_df[['Naslov serijske publikacije', 'Faktor vpliva']])

# %%
# Get ISSNs
issn_list = if_rs_df['ISSN'].str.split('/').str[0].to_list()

# %%
# Create empty DF
if_df = pd.DataFrame()


# %%
for issn in issn_list:
    print('Reading IF for {}'.format(issn))
    s_year = urllib.parse.quote('')
    s_kw = urllib.parse.quote('')
    s_issn = urllib.parse.quote(issn)
    if_url = if_base_url.format(s_year, s_kw, s_issn)
    # Read webpage
    req = Request(if_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    # Read IF
    df = pd.read_html(webpage)[0]
    df.drop(['Št.'], axis=1, inplace=True)

    # Only after 2000
    df = df.loc[df['Leto'] >= 2000]

    # Append DF
    if_df = if_df.append(df, ignore_index=True)


# %%
if_df.to_csv(if_fn, index=False)


# %%
if_df.drop('ISSN', inplace=True, axis=1)

# %%
if_wide = if_df.groupby(['Leto', 'Naslov serijske publikacije']).agg('sum')
if_wide

# %%
if_wide = if_wide.unstack()

# %%
if_wide = if_wide.droplevel(level=0, axis=1)

# %%
if_wide.head()

# %%
# Make plot
# plt.figure() # A4 landscape
if_wide.plot(figsize=(11.69,8.27), marker='.')
plt.title('Remote Sensing IF by Year')
plt.legend(loc='upper left', frameon=False)
plt.xlabel('Year')
plt.ylabel('IF')
plt.xticks([2000, 2005, 2010, 2015, 2020])
plt.tight_layout()
# plt.savefig(plots_folder + 'remote_sensing_if.png', dpi=600)
# plt.savefig(plots_folder + 'remote_sensing_if.pdf', dpi=600)
plt.show()
plt.close()

# %%
