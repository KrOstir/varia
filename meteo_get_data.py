# coding: utf-8
#
# Read precipitation radar and hail meteorologic data
#
# Query ARSO web page for meteorological data, get JSON, download PNG images if
# new
# http://www.vreme.si/uploads/probase/www/nowcast/inca/{PRODUKT}.json
#
# Products:
#
# inca_sp_data - clouds
# inca_tp_data - precipitation
# inca_t2m_data - temperature
# inca_wind_data - wind
# inca_hp_data - hail
# inca_si0zm_data - precipitation radar
#
# Kristof Ostir, 2018-07-17
# University of Ljubljana, Faculty of Civil and Geodetic Engineering
# (c) 2018

#%% Imports
import requests
import os
import json
import pandas as pd
import datetime

#%% Basic URL for queries
meteo_url = "http://www.vreme.si"
meteo_url_q = meteo_url + "/uploads/probase/www/nowcast/inca/"
# Data folder
meteo_data = "./meteo_data/"

#%% Open log file, all messages are written to log
meteo_log = "meteo_get_data_" + datetime.datetime.now().strftime('%y%m') + ".log"
log_file = open(meteo_log, "a")

#%% Available datasets
meteo_prod = {
    'clouds': "inca_sp_data",
    'prec': "inca_tp_data",
    'temp': "inca_t2m_data",
    'wind': "inca_wind_data",
    'hail': "inca_hp_data",
    'radar': "inca_si0zm_data"
    }

#%% Downland images for hail and radar
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end="", file=log_file)
meteo_par = ["hail", "radar"]
for par in meteo_par:
    print(",", par, end="", file=log_file)
    meteo_req_url = meteo_url_q + meteo_prod[par] + ".json"
    meteo_req_url
    # Get DF of meteo data
    meteo_df = pd.read_json(meteo_req_url, convert_dates=['valid'])
    # DL links
    meteo_dl = meteo_url + meteo_df["path"]
    # Download new images
    dl_num = 0
    for item in meteo_dl:
        item_img = item.split("/")[-1]
        item_fn = meteo_data + item_img
        if not os.path.exists(item_fn):
            response = requests.get(item)
            if response.status_code == 200:
                with open(item_fn, 'wb') as f:
                    f.write(response.content)
                dl_num += 1
            else:
                print("Can not get:", item)
    print(":", dl_num, end="", file=log_file)
print("", file=log_file)
