# coding: utf-8

# Create senate meetings calendar
# 
# Read and parse TXT, create CSV
#
# Krištof Oštir
# 2017-10-24

import pandas as pd
import io
from datetime import datetime
from datetime import timedelta

# File names
txt_file_fn = "D:/Kristof/Predavanja/urnik/fgg_senat.txt"
cal_file_fn = "D:/Kristof/Predavanja/urnik/fgg_senat.csv"

# Temporary string
buf = io.StringIO()
# Read and clean file
txt_file = open(txt_file_fn)
text = txt_file.read().splitlines()
for line in text:
    line = line.strip().replace(" ", "")
    if line.endswith('uri'):
        line = line.replace("ob", " ").replace("uri", "")
        buf.write(line + "\n")
txt_file.close()

# Read CSV to data frame
buf.seek(0)
calendar = pd.read_csv(buf, header=None)

# Parse date
calendar["Start"] = pd.to_datetime(calendar[0], format = '%d.%m.%Y %H.%M')

# Events take 3 hours
calendar["End"] = calendar["Start"] + timedelta(hours=3)
calendar[0] = "Seja senata"
calendar.columns.values[0] = "Subject"

# Outlook needs start and end date and time
calendar['StartDate'] = calendar['Start'].apply(lambda x:x.date())
calendar['StartTime'] = calendar['Start'].apply(lambda x:x.time())
calendar['EndDate'] = calendar['End'].apply(lambda x:x.date())
calendar['EndTime'] = calendar['End'].apply(lambda x:x.time())
del calendar["Start"]
del calendar["End"]

# Write file
cal_file = open(cal_file_fn, "w")
calendar.to_csv(cal_file)
cal_file.close()
