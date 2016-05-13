# Analyse MDPI Remote Sensing journal data
# 
# Get paper metadata from web, store it in a data frame.
#
# Krištof Oštir
# 2016-05-12

# Load libraries
from bs4 import BeautifulSoup
import requests
import re

# TODO Define data frame

# Remote Sensing URL
mdpi_url = "http://www.mdpi.com/"
rs_url = "2072-4292/"
# Ranges 1 - 8 in 2016
# mdpi_url_rs_vols = range(1,9)
mdpi_url_rs_vols = range(6,7)
mdpi_file_out = "~/Documents/R/R Varia/mdpi_rs_analysis.xlsx"

for i in mdpi_url_rs_vols:
    print("Processing Volume", i)
    vol_url = rs_url+str(i)+"/"
    url_i = mdpi_url+vol_url
    print(url_i)
    url_ir = requests.get(url_i)
    soup = BeautifulSoup(url_ir.text)
    for link in soup.find_all('a'):
        link_url = link.get('href')
        if vol_url in link_url:
            k = link_url.rfind("/")
            j = int(link_url[k + 1:])
            iss_url = vol_url+str(j)+"/"
            print("Volume", i, "Issue", j)
            url_ij = mdpi_url + iss_url
            print(iss_url)
            url_ijr = requests.get(url_ij)
            soup_j = BeautifulSoup(url_ijr.text)
            for link_j in soup_j.find_all('a'):
                link_url_j = link.get('href')
                print(link_j)
                # if iss_url in link_url_j:
                #     print(link_url_j)


