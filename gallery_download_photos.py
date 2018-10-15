# coding: utf-8

# Download images from the NextGEN Gallery (WordPress)
# 
# Use list of base URLs and download all images in the gallery.
# 
# Krištof Oštir  
# 2018-09-19

# Load libraries
import os
import requests
import time
import smtplib
from bs4 import BeautifulSoup

# Folder for storing images
image_folder = "D:/Kristof/Dropbox/Foto/Taborjenje 2018/"
# Gallery location
gallery_url = "http://taborniki.net/galerija/taborjenje-2018/"
# URL positions
gal_id = "gallery/"

# Start processing
print("Downloading images")
print("URL:", gallery_url)

# Download page from URL
page = requests.get(gallery_url).text
soup = BeautifulSoup(page, 'html.parser')

# Total and new images
gal_new = 0
# Image URl list
img_urls = []

# Check all URLs
img_urls = []
for link in soup.find_all('a', href=True):
    img_url = link['href']
    # If URL is image download it
    if img_url.endswith(".jpg") and gal_id in img_url:
        img_urls.append(img_url) 
len(img_urls)

# Download all images from list
skip = 0
skip_yn = False
for link in img_urls:
    img_fn = link[link.rindex("/") + 1:]
    img_name = image_folder + img_fn
    if os.path.exists(img_name):
        skip_yn = True
        print('.', end="", flush=True)
        skip += 1
        if skip > 100:
            print()
            skip = 0
    else:
        if skip_yn:
            print()
            skip_yn = False
        print("Downloading", img_fn)
        img_data = requests.get(link).content
        with open(img_name, 'wb') as handler:
            handler.write(img_data)
            gal_new += 1
print("")

print("Finished")
print("Gallery:", len(img_urls))
print("New    :", gal_new)

