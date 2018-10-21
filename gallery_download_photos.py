# coding: utf-8
#%%
# Download images from the NextGEN Gallery (WordPress)
# 
# Use list of base URLs and download all images in the gallery.
# 
# Krištof Oštir  
# 2018-09-19
#%%

#%% Load libraries
import os
import requests
import time
import smtplib
from bs4 import BeautifulSoup

#%% Folder for storing images
image_folder = "D:/Kristof/Dropbox/Foto/Taborjenje 2018/"
# Gallery location
gallery_url = "http://taborniki.net/galerija/taborjenje-2018/"
# URL positions
gal_id = "gallery/"

#%% Start processing
print("Downloading images")
print("URL:", gallery_url)

#%% Download page from URL
print("Reading ...")
page = requests.get(gallery_url).text
print("Parsing ...")
soup = BeautifulSoup(page, 'html.parser')

#%% Total and new images
gal_new = 0
# Image URl list
img_urls = []

#%% Check all URLs
print("Finding images ...")
img_urls = []
for link in soup.find_all('a', href=True):
    img_url = link['href']
    # If URL is image download it
    if img_url.endswith(".jpg") and gal_id in img_url:
        img_urls.append(img_url)

#%% Download all images from list
print("Downloading images ...")
gal_num = len(img_urls)
for i, link in enumerate(img_urls, start=1):
    img_fn = link[link.rindex("/") + 1:]
    img_name = image_folder + img_fn
    if os.path.exists(img_name):
        skip_yn = True
        print("%d/%d Exists - skipping" % (i, gal_num))
    else:
        print("%d/%d Downloading -" % (i, gal_num), img_fn)
        img_data = requests.get(link).content
        with open(img_name, 'wb') as handler:
            handler.write(img_data)
            gal_new += 1
print("")

#%% End
print("Finished")
print("Gallery:", len(img_urls))
print("New    :", gal_new)
