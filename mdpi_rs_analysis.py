# MDPI Remote Sensing
#
# Get paper metadata from web and store it in a csv file. Track all volumes,
# all issues and all papers
#
# Krištof Oštir
# 2016-05-12

# Load libraries
from bs4 import BeautifulSoup
import requests

# Remote Sensing URL
mdpi_url = "http://www.mdpi.com/"
rs_url = "2072-4292/"
# Ranges 1 - 8 in 2016
# TODO automatically find volumes
# mdpi_url_rs_vols = range(1,9)
mdpi_url_rs_vols = range(6,7)
mdpi_file_out = "mdpi_rs_analysis.csv"

mdpi_f = open(mdpi_file_out, 'w+')
print("Volume, Issue, Paper, URL", file=mdpi_f)

# TODO Generate list of volumes
# TODO Generate list of issues
# TODO Generate list of papers
for i in mdpi_url_rs_vols:
    print("Processing Volume", i)
    vol_url = rs_url+str(i)+"/"
    url_i = mdpi_url+vol_url
    url_ir = requests.get(url_i)
    soup = BeautifulSoup(url_ir.text)
    for link in soup.find_all('a'):
        link_url = link.get('href')
        if vol_url in link_url:
            k = link_url.rfind("/")
            j = int(link_url[k + 1:])
            print("Volume", i, "Issue", j)
            iss_url = vol_url+str(j)+"/"
            url_ij = mdpi_url + iss_url
            url_ijr = requests.get(url_ij)
            soup_j = BeautifulSoup(url_ijr.text)
            for link_j in soup_j.find_all('a'):
                link_url_j = link_j.get('href')
                if (iss_url in link_url_j) & ("pdf" in link_url_j):
                    l = link_url_j.rfind("/pdf")
                    m = len(iss_url) + 1
                    p = int(link_url_j[m:l])
                    url_p = mdpi_url + link_url_j[1:l]
                    entry = "{0}, {1}, {2}, {3}".format(i, j, p, url_p)
                    print(entry, file=mdpi_f)
# Close file
mdpi_f.close()