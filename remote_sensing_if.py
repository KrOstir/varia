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
# Keywords
journal_kw = 'remote sensing'
# year = 2019

# %%
# Create list of journals
s_year = urllib.parse.quote(str(year))
s_kw = urllib.parse.quote(journal_kw)
s_issn = urllib.parse.quote('')
if_url = if_base_url.format(s_year, s_kw, s_issn)
# Read webpage
req = Request(if_url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

# %%
# Read downloads
if_rs_df = pd.read_html(webpage)[0]
if_rs_df.head()

# %%
if_rs_df = if_rs_df.drop(['Št.'], axis=1)
if_rs_df



# %%
if_rs_df.columns

# %%
# Top 10 journals
if_rs_df = if_rs_df.sort_values('Faktor vpliva', ascending=False).head(10)

# %%
# Print top 10
print(if_rs_df[['Naslov serijske publikacije', 'Faktor vpliva']])

# %%
issn_list = if_rs_df['ISSN'].to_list()
if_df = pd.DataFrame()

# %%
for issn in issn_list:
    print('Reading IF for {}'.format(issn))

# %%
plt.plot(if_rs_df, marker='o')
plt.title('Geodetski vestnik IF')
# plt.show()
plt.savefig(plots_folder + 'geodetski_vestnik_if.png', dpi=300)
# plt.show()
plt.close()

# %%



