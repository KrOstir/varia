# coding: utf-8
#
# Analiza podatkov sistema BicikeLJ
#%%

#%% Imports
from urllib.request import urlopen
import json
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *

#%% Figure size and style
plt.rcParams['figure.figsize'] = (15, 10)


#%% Branje podatkov po protokolih, opisanih v: https://developer.jcdecaux.com/#/opendata/vls?page=getstarted
# 
# Zanimiva je diplomska naloga: http://geo.ff.uni-lj.si/pisnadela/pdfs/zaksem_201409_ziga_jamnik.pdf

#%% Parameters
# Bicycle, station dynamic infos
station_data_url = "https://api.jcdecaux.com/vls/v1/stations?contract=Ljubljana&apiKey=0a494317d60d3d556d0755600b078ea6b26af90f"
# Station info dataframe
station_info_fn = "bicikelj_station_info.csv"
station_data_fn = "bicikelj_station_data_1703.csv"


#%% Informacije o postajah
response = urlopen(station_data_url)
if response.code == 200:
    data = response.read().decode('utf-8')
else:
    print("Wrong response from ", station_data_url)
station_info_json = json.loads(data)
station_info = pd.DataFrame(station_info_json).sort_values(["number"]).reset_index(drop=True)
station_info = station_info[station_info['status'] == "OPEN"]
station_info = station_info[['address', 'banking', 'bike_stands', 'bonus', 'name',
                             'number', 'position', 'status']].copy()
station_info = pd.concat([station_info.drop(['position'], axis=1), station_info["position"].apply(pd.Series)], axis=1)
station_info.head()

#%% Save to CSV
station_info.to_csv(station_info_fn, index=True)

#%% Clean database
station_info_s = station_info[["bike_stands", "name", "number"]]
station_info_s = station_info_s.set_index("number")

#%% Branje podatkov o postajah
station_data_full = pd.read_csv(station_data_fn, index_col="last_update_time", parse_dates=True)
station_data_full.describe()
station_data_full.index.min()
station_data_full.index.max()
station_data_full.head()
station_data_stands = station_data_full.pivot(columns='number', values='available_bike_stands')
station_data_bikes = station_data_full.pivot(columns='number', values='available_bikes')
station_data_stands_hour = station_data_stands.groupby(station_data_stands.index.hour).aggregate("mean")
station_data_bikes_hour = station_data_bikes.groupby(station_data_bikes.index.hour).aggregate("mean")
station_data_bikes_hour

#%% Porazdelitev razpoložljivih koles glede na uro
for col in station_data_bikes_hour.columns:
    data = station_data_bikes_hour[col].dropna()
    plt.title(str(col) + " - " + station_info_s["name"][col])
    plt.ylim(0, station_info_s["bike_stands"][col])
    plt.xlim(0,23)
    plt.xticks(range(0,25))
    plt.yticks(range(0,station_info_s["bike_stands"][col]+1))
    plt.grid(True)
    # plt.plot(data)
    plt.plot(data, linestyle="steps")
    plt.show()
station_data_bikes_hour.plot(linestyle="steps")


#%% Število koles po urah
# Enako kot zgoraj, samo z grupiranjem
station_data_full = pd.read_csv(station_data_fn, index_col="last_update_time", parse_dates=True)
station_data_full.head()
station_group_bikes_hour = station_data_full.groupby(["number", station_data_full.index.hour])["available_bikes"].mean()
# station_group_bikes_hour = station_group_bikes.unstack(level=1)
for key in station_group_bikes_hour.index.levels[0]:
    data = station_group_bikes_hour[key]
    plt.title(str(key) + " - " + station_info_s["name"][key])
    plt.ylim(0, station_info_s["bike_stands"][key])
    plt.xlim(0,23)
    plt.xticks(range(0,25))
    plt.yticks(range(0,station_info_s["bike_stands"][key]+1))
    plt.grid(True)
    plt.plot(data, linestyle="steps")
    plt.show()

#%% Izposoje koles
station_data_full = pd.read_csv(station_data_fn, index_col="last_update_time", parse_dates=True)
station_data_full.head()
# Urejeno po postajah
station_group_bikes = station_data_full.groupby("number")
data = station_group_bikes.get_group(1)
data["change"] = data["available_bikes"].diff()
data.head()
# List groups
for key, item in station_group_bikes:
    data = station_group_bikes.get_group(key).copy()
    data["change"] = data["available_bikes"].diff()
    plt.title(str(key) + " - " + station_info_s["name"][key])
    plt.plot(data[["available_bikes", "change"]], linestyle="steps")
    plt.grid(True)
    plt.show()
