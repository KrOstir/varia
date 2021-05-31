# %%
# MDPI Remote Sensing
#
# Get paper metadata from web and store it in a csv file. Track all volumes,
# all issues and all papers
#
# Krištof Oštir
# 2016-10-08

# %%
# Load libraries
from bs4 import BeautifulSoup
import requests

# %%
# Remote Sensing URL
# https://www.mdpi.com/journal/remotesensing
mdpi_url = 'http://www.mdpi.com/'
rs_issn = '2072-4292'
rs_url = 'journal/remotesensing'
mdpi_file_out = 'mdpi_rs_analysis.csv'

# %%
print('Analyzing ', mdpi_url+rs_issn)

# %%
mdpi_f = open(mdpi_file_out, 'w+')
print("Volume,Issue,Paper,URL", file=mdpi_f)


# %%
# Create list of volumes
volumes = []
i = 1
while True:
    r_url = '{0}/{1}'.format(rs_issn, i)
    mdpi_r = requests.get(mdpi_url + r_url, headers={'User-Agent': 'Mozilla/5.0'})
    if mdpi_r.status_code == 200:
        print('Found volume {}'.format(r_url))
        volumes.append(r_url)
        i += 1
    else:
        break


# %%
vol = volumes[0]

# for vol in volumes[0:1]:
print('Processing Volume', vol)
vol_url = mdpi_url+vol+'/'
url_i = mdpi_url+vol_url
url_ir = requests.get(url_i, headers={'User-Agent': 'Mozilla/5.0'})
# %%

# %%
soup = BeautifulSoup(url_ir.text, 'html.parser')
# %%
soup.findAll('div', {"class":"ul-spaced"})
# %%
soup.find_all('a')

# %%
issues = []
for link in soup.find_all('a'):
    link_url = link.get('href')
    if link_url == None:
        continue
    if vol_url in link_url:
        issues.append(link_url)
print(issues)
    # issues = sorted(set(issues))
    # for link in issues:
    #     k = link.rfind('/')
    #     j = int(link[k + 1:])
    #     print('Volume', i, 'Issue', j)
    #     iss_url = vol_url+str(j)+'/'
    #     url_ij = mdpi_url + iss_url
    #     url_ijr = requests.get(url_ij)
    #     soup_j = BeautifulSoup(url_ijr.text, 'lxml')
    #     for link_j in soup_j.find_all('a'):
    #         link_url_j = link_j.get('href')
    #         if link_url_j == None:
    #             continue
    #         if (iss_url in link_url_j) & ('pdf' in link_url_j):
    #             l = link_url_j.rfind('/pdf')
    #             m = len(iss_url) + 1
    #             p = int(link_url_j[m:l])
    #             url_p = mdpi_url + link_url_j[1:l]
    #             entry = '{0}, {1}, {2}, {3}'.format(i, j, p, url_p)
    #             # print(entry, file=mdpi_f)
    #             print(entry)

# %%
# Close file
mdpi_f.close()

# %%
