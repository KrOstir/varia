# %%
# Create senate metings calendar

# %%
import pandas as pd
import io
from datetime import datetime
from datetime import timedelta


# %%
# File names
txt_file_fn = "./data/fgg_senat.txt"
cal_file_fn = "./data/fgg_senat.csv"


# %%
buf = io.StringIO()
# Read and clean file
txt_file = open(txt_file_fn)
text = txt_file.read().splitlines()
txt_file.close()
text


# %%
for line in text:
    line = line.strip().replace(" ", "")
    if line.endswith('uri'):
        line = line.split("seja",1)[1]
        line = line.replace("ob", " ").replace("uri", "")
        print(line)
        buf.write(line + "\n")


# %%
buf.seek(0)
calendar = pd.read_csv(buf, header=None)


# %%
calendar


# %%
calendar["Start"] = pd.to_datetime(calendar[0], format = '%d.%m.%Y %H.%M')


# %%
calendar["End"] = calendar["Start"] + timedelta(hours=3)


# %%
calendar[0] = "Seja senata"
calendar.columns.values[0] = "Subject"
calendar


# %%
calendar['StartDate'] = calendar['Start'].apply(lambda x:x.date())
calendar['StartTime'] = calendar['Start'].apply(lambda x:x.time())
calendar['EndDate'] = calendar['End'].apply(lambda x:x.date())
calendar['EndTime'] = calendar['End'].apply(lambda x:x.time())


# %%
calendar


# %%
del calendar["Start"]
del calendar["End"]
calendar


# %%
cal_file = open(cal_file_fn, "w")
calendar.to_csv(cal_file)
cal_file.close()


# %%



