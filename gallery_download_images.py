# Download images from the NextGEN Gallery (WordPress)
#
# Use list of base URLs and download all images in the gallery.
#
#
# Krištof Oštir
# 2016-07-20

# Load libraries
import os
import requests
from bs4 import BeautifulSoup


def get_images(page_url, save_folder):
    '''
    Get all images from the gallery

    :param page_url: URL of the page
    :param save_folder: root for saving images
    '''
    print("Page:", page_url)
    # URL positions
    gal_id = "gallery/"
    fol_id = "uploads/"
    # Download page from URL
    page = requests.get(page_url).text
    soup = BeautifulSoup(page, 'html.parser')
    # Check all URLs
    for link in soup.find_all('a', href=True):
        img_url = link['href']
        # If URL is image download it
        if img_url.endswith(".jpg") and gal_id in img_url:
            # img_url[img_url.index(gal_id) + len(gal_id):]
            img_name = save_folder + img_url[img_url.rindex("/") + 1:]
            if os.path.exists(img_name):
                print('.', end="", flush=True)
            else:
                # print ("Downloading:", img_url)
                print('*', end="", flush=True)
                img_data = requests.get(img_url).content
                with open(img_name, 'wb') as handler:
                    handler.write(img_data)
    print("")

def list_pages(base_url):
    '''
    Create a list of all pages in the gallery

    :param page_url: URL of the page
    :return page_gallery: list of urls with images
    '''
    # URL positions
    pages_url = "nggallery/page/"
    page = requests.get(base_url).text
    soup = BeautifulSoup(page, 'html.parser')
    pages_num = 1
    # Check all URLs
    for link in soup.find_all('a', href=True):
        link_url = link['href']
        if base_url in link_url and pages_url in link_url:
            page_num = int(link_url[link_url.rindex("/")+1:])
            if page_num > pages_num:
                pages_num = page_num
    pages_base = base_url + pages_url
    page_gallery = []
    for r in range(pages_num):
        page_gallery.append(pages_base  + '%i' % (r+1) )
    return page_gallery

# Start processing images
print("\nDownload images from the NextGEN Gallery")

# List of base urls
image_folder = "/Users/Kristof/Documents/Zacasno/GootJam Gallery/"
# Galleries
base_urls = [
    "http://gootjam.net/galerija/tabor/18-7/",
    "http://gootjam.net/galerija/tabor/19-7-drugi-dan/",
    "http://gootjam.net/galerija/tabor/20-7-tretji-dan/",
]

# Download all pages and all data
for idx, base_url in enumerate(base_urls):
    print("\n", idx+1, "/", len(base_urls))
    print("URL:", base_url, "\n")
    fol_name = image_folder + base_url[(base_url[:(len(base_url)-1)].rindex("/"))+1:]
    # Check if folder exists
    if not os.path.exists(fol_name):
        print("Creating folder:", fol_name)
        os.makedirs(fol_name)
    # Get list of all galleries in base_url
    gal_list = list_pages(base_url)
    # Get images from all pages
    for page in gal_list:
        get_images(page, fol_name)

print("\nFinished")