# coding: utf-8
#
# Read meteorologic data
#
# Read XML meteorological data, parse XML and store data
# in CSV by month
#
# Kristof Ostir, 2017-01-21
# University of Ljubljana, Faculty of Civil and Geodetic Engineering
# (c) 2017

# Imports
import urllib.request
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import datetime
import pytz

# Parameters
# Station ID
meteo_station_ID = "LJUBL-ANA_BEZIGRAD"
# Meteo data
meteo_xml_head = "http://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/recent/observationAms_"
meteo_xml_tail = "_history.xml"
meteo_xml = meteo_xml_head + meteo_station_ID + meteo_xml_tail
# Output file
meteo_data_fn = "meteo_data_" + datetime.datetime.now().strftime("%y%m") + ".csv"
meteo_log = "meteo_data_" + datetime.datetime.now().strftime("%y%m") + ".log"
# Time zone
local_tz = pytz.timezone("Europe/Ljubljana")

# Open log file, all messages are written to log
log_file = open(meteo_log, "a")

print(
    "Meteo",
    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    sep=",",
    end=",",
    file=log_file,
)

# Read station data
meteo_xml_req = urllib.request.urlopen(meteo_xml)
if meteo_xml_req.code == 200:
    meteo_xml_data = meteo_xml_req.read()
else:
    print(0, "Wrong API response", sep=",", file=log_file)
    raise
# Parse XML
tree = ET.fromstring(meteo_xml_data)
# V metData poiščemo čase (tsValid_issued) in meritve (tavg, rr_val, pavg, ffavg_val_kmh)
meteo_data_elements = tree.findall("metData")
meteo_data = []
for data in meteo_data_elements:
    temp = float(data.find("tavg").text) if data.find("tavg").text != None else None
    perc = float(data.find("rr_val").text) if data.find("rr_val").text != None else None
    wind = (
        int(data.find("ffavg_val_kmh").text)
        if data.find("ffavg_val_kmh").text != None
        else None
    )
    pres = float(data.find("pavg").text) if data.find("pavg").text != None else None
    cond = (
        str(data.find("nn_icon-wwsyn_icon").text)
        if data.find("nn_icon-wwsyn_icon").text != None
        else np.nan
    )
    date_time = datetime.datetime.strptime(
        data.find("tsValid_issued_UTC").text, "%d.%m.%Y %H:%M %Z"
    )
    meteo_data.append([date_time, temp, perc, wind, pres, cond])
# Create dataframe
meteo_data_df = pd.DataFrame(meteo_data)
meteo_data_df.columns = ["DateTime", "Temp", "Perc", "Wind", "Pres", "Cond"]
meteo_data_df = meteo_data_df.set_index("DateTime")
meteo_data_df = meteo_data_df.drop_duplicates().sort_index()
# Data is in UTC, change to local time, than remove time zone info
meteo_data_df.index = (
    meteo_data_df.index.tz_localize(pytz.utc).tz_convert(local_tz).tz_localize(None)
)
# Add to file
try:
    meteo_data_full = pd.read_csv(meteo_data_fn, index_col="DateTime", parse_dates=True)
    len_before = len(meteo_data_full.index)
    meteo_data_full = (
        meteo_data_full.append(meteo_data_df).drop_duplicates().sort_index()
    )
    len_after = len(meteo_data_full.index)
    meteo_data_full.to_csv(meteo_data_fn, index=True)
    print(len_after - len_before, "Added", sep=",", file=log_file)
except:
    meteo_data_df.to_csv(meteo_data_fn, index=True)
    len_after = len(meteo_data_df.index)
    print(len_after, "Added", sep=",", file=log_file)
