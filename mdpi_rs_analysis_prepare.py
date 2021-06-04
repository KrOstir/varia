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
from tqdm import tqdm
import os

# %%
# Remove duplicates from list


def remove_duplicates(list):
    """
    remove_duplicates Removes duplicates from Python list

    Args:
        list (list): Incoming list

    Returns:
        list: List with duplicates
    """
    res = []
    [res.append(x) for x in list if x not in res]

    return res


# %%
# Remote Sensing URL
# https://www.mdpi.com/journal/remotesensing
mdpi_url = 'http://www.mdpi.com/'
rs_issn = '2072-4292'
rs_url = 'journal/remotesensing'
# CSV file to store results
mdpi_file = './data/mdpi_rs_analysis.csv'
# Skip flag
skip = True

# %%
print('Analyzing ISSN:', rs_issn)

# %%
# Check if output exists and open it
if skip and os.path.isfile(mdpi_file):
    mdpi_df = pd.read_csv(mdpi_file)
    # Delete last record as papers might have updates
    l_v = mdpi_df['vol_n'].max()
    l_i = mdpi_df['issue_n'].max()
    mdpi_df.drop(mdpi_df[
        (mdpi_df['vol_n'] == l_v) & (mdpi_df['issue_n'] == l_i)].index,
        inplace=True)
else:
    mdpi_df = pd.DataFrame(columns=['vol_n', 'issue_n', 'articles'])

# %%
mdpi_df.head()

# Papers list
papers = []

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

1  # %%
for vol in volumes:
    print('Processing {}'.format(vol))

    url = mdpi_url + vol
    req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    client = ul.urlopen(req)
    htmldata = client.read()
    client.close()
    # Create soup
    pagesoup = soup(htmldata, "html.parser")

    # Issues
    issues = []
    itemlocator = pagesoup.findAll('div', {"class": "ul-spaced"})
    for link in itemlocator[0].findAll('a'):
        iss = link.get('href')
        if iss.startswith(vol):
            issues.append(link.get('href'))
    issues = remove_duplicates(issues)

    # Process issues
    for issue in tqdm(issues):
        # Volume and issue
        vol_n = int(vol.split('/')[-1])
        issue_n = int(issue.split('/')[-1])

        # Skip if volume in DF
        if (vol_n in mdpi_df['vol_n'].values) & (issue_n in mdpi_df['issue_n'].values):
            continue

        # Get URL
        url = mdpi_url + issue
        req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        client = ul.urlopen(req)
        htmldata = client.read()
        client.close()
        # Create soup
        pagesoup = soup(htmldata, "html.parser")

        # Papers
        itemlocator = pagesoup.find_all('h1')[0]
        ils = str(itemlocator).split()
        articles = int(ils[ils.index('articles') - 1])

        # Add papers
        papers.append([vol_n, issue_n, articles])


# %%
# Add new data
df = pd.DataFrame(papers, columns=['vol_n', 'issue_n', 'articles'])
mdpi_df = mdpi_df.append(df)

# %%
# Save to file
mdpi_df.to_csv(mdpi_file, index=False)

# Finished
print('Finished')
# %%
