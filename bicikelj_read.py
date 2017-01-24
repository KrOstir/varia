# coding: utf-8
# 
# Read BicikeLJ station data
#
# Read JSON BicikeLJ station data, parse and store data
# for all stations
#
# Kristof Ostir, 2017-01-17
# University of Ljubljana, Faculty of Civil and Geodetic Engineering
# (c) 2017

# Imports
from urllib.request import urlopen
import json
import numpy as np
import pandas as pd
import datetime

# Parameters
# API Key 
bicikelj_api_key= "0a494317d60d3d556d0755600b078ea6b26af90f"
# Bicycle, station dynamic infos
station_data_url = "https://api.jcdecaux.com/vls/v1/stations?contract=Ljubljana&apiKey=" + bicikelj_api_key
# Output file
station_data_fn = "bicikelj_station_data_" + datetime.datetime.now().strftime('%y%m') + ".csv"
bicikelj_log = "bicikelj_read_" + datetime.datetime.now().strftime('%y%m') + ".log"

# Open log file, all messages are written to log
log_file = open(bicikelj_log, "a")

print("BicikeLJ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), sep=",", end=",", file=log_file)
 
# Read station data
response = urlopen(station_data_url)
if response.code == 200:
    data = response.read().decode('utf-8')
else:
    print(0, "Wrong API response", sep=",", file=log_file)
    raise
station_data_json = json.loads(data)
station_data = pd.DataFrame(station_data_json).sort_values(["number"]).reset_index(drop=True)
station_data_real = station_data[['available_bike_stands', 'available_bikes', 'bike_stands',
                                 'last_update', 'number']].copy()
station_data_real["last_update_time"] = pd.to_datetime(station_data_real["last_update"]*1e6)
station_data_real = station_data_real.drop(["last_update"], 1)
station_data_real = station_data_real.set_index(["last_update_time"]).sort_index()
# Add to file
try:
    station_data_full = pd.read_csv(station_data_fn, index_col="last_update_time", parse_dates=True)
    len_before = len(station_data_full.index)
    station_data_full = station_data_full.append(station_data_real).drop_duplicates().sort_index()
    len_after = len(station_data_full.index)
    station_data_full.to_csv(station_data_fn, index=True)
    print(len_after-len_before, "Added", sep=",", file=log_file)
except:
    station_data_real.to_csv(station_data_fn, index=True)
    len_after = len(station_data_real.index)
    print(len_after, "Added", sep=",", file=log_file)
