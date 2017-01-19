# Read BicikeLJ station data
#
# Read XML BicikeLJ station data, parse XML and store data
# for all stations
#
# Kristof Ostir, 2017-01-17
# University of Ljubljana, Faculty of Civil and Geodetic Engineering
# (c) 2017

# Imports
import urllib.request
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from datetime import datetime

# Parameters
# Base XML url
base_url = "http://www.bicikelj.si/service/stationdetails/ljubljana/"
# Station parameters
station_pars = ['station_id', 'available', 'free', 'total', 'ticket', 'open', 'updated', 'connected']
station_list = range(1,39)

# For all stations
station_table = []
for station in station_list:
    station_xml_req = urllib.request.urlopen(base_url+str(station))
    station_xml_data = station_xml_req.read()

    tree = ET.fromstring(station_xml_data)

    row_data = [station]
    for c in tree:
        row_data.append(int(c.text))
    station_table.append(row_data)

    # bicikelj_data = pd.DataFrame(columns=row_names, dtype=int)
    #bicikelj_data = pd.DataFrame()

    # bicikelj_series = pd.Series(row_data, row_names, dtype=int)

    # bicikelj_data = bicikelj_data.append(bicikelj_series, ignore_index=True)
    # bicikelj_data = bicikelj_data.append([row_data], ignore_index=True)

    #print(bicikelj_data)

station_df = pd.DataFrame(station_table, columns=station_pars)
#station_df["date"] =
print(station_df)