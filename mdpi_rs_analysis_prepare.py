# %%
# MDPI Remote Sensing
#
# Get paper metadata from web and store it in a csv file. Track all volumes,
# all issues and all papers
#
# Krištof Oštir
# 2021-05

# %%
# Load libraries
import urllib.request as ul
import pandas as pd
from bs4 import BeautifulSoup as soup


# %%
# Remote Sensing URL
# https://www.mdpi.com/journal/remotesensing
mdpi_url = 'http://www.mdpi.com/'
rs_issn = '2072-4292'
rs_url = 'journal/remotesensing'
mdpi_file_out = '/data/mdpi_rs_analysis.csv'

# %%
print('Analyzing ISSN:', rs_issn)

# %%
mdpi_df = pd.DataFrame(columns=['vol_n', 'issue_n', 'articles'])
mdpi_df

# %%
# Create list of volumes
volumes = []
url = mdpi_url + rs_url
req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
client = ul.urlopen(req)
htmldata = client.read()
client.close()
# Create soup
pagesoup = soup(htmldata, "html.parser")
# Volumes info
itemlocator = pagesoup.findAll('div', {"class": "journal-browser-volumes"})
for link in itemlocator[0].findAll('a'):
    volumes.append(link.get('href'))

# %%
volumes
# %%
vol = volumes[1]

# %%

url = mdpi_url + vol
req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
client = ul.urlopen(req)
htmldata = client.read()
client.close()
# Create soup
pagesoup = soup(htmldata, "html.parser")


# %%
vol
# %%
# Issues
issues = []
itemlocator = pagesoup.findAll('div', {"class": "ul-spaced"})
for link in itemlocator[0].findAll('a'):
    iss = link.get('href')
    if iss.startswith(vol):
        issues.append(link.get('href'))
        print(link.get('href'))


# %%
# Remove duplicates from list
def remove_duplicates(list):
    res = []
    [res.append(x) for x in list if x not in res]

    return res


# %%
issues = remove_duplicates(issues)
issues

# %%
issue = issues[3]
issue

# %%
url = mdpi_url + issue
req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
client = ul.urlopen(req)
htmldata = client.read()
client.close()
# Create soup
pagesoup = soup(htmldata, "html.parser")

# %%
# Papers
itemlocator = pagesoup.find_all('h1')[0]

# itemlocator = pagesoup.findAll('div', {"class":"generic-item article-item"})

# %%
articles = int(str(itemlocator).split()[-3])
print(articles)


# %%
vol_n = int(vol.split('/')[-1])
issue_n = int(issue.split('/')[-1])
# %%
df = pd.DataFrame([[vol_n, issue_n, articles]], columns=[
                  'vol_n', 'issue_n', 'articles'])
print(df)

# %%
mdpi_df.append(df)

# %%
