# coding: utf-8

# # Create PhD metings calendar

# In[ ]:


import pandas as pd
import io
from datetime import datetime
from datetime import timedelta


# In[ ]:


# File names
txt_file_fn = "D:/Kristof/OneDrive - Univerza v Ljubljani/Lectures/Grajeno okolje/Seje/GO_seje.txt"
cal_file_fn = "D:/Kristof/OneDrive - Univerza v Ljubljani/Lectures/Grajeno okolje/Seje/GO_seje.csv"


# In[ ]:


buf = io.StringIO()
# Read and clean file
txt_file = open(txt_file_fn, encoding="utf-8")
text = txt_file.read().splitlines()

for line in text:
    line = (
        line.strip()
        .replace("Študijski odbor doktorskega študija\t", "")
        .replace(" ", "")
    )
    if line.endswith("uri"):
        line = line.replace("ob", " ").replace("uri", "")
        buf.write(line + "\n")
        print(line)
txt_file.close()


# In[ ]:


buf.seek(0)
calendar = pd.read_csv(buf, header=None)


# In[ ]:


calendar


# In[ ]:


calendar["Start"] = pd.to_datetime(calendar[0], format="%d.%m.%Y %H.")


# In[ ]:


calendar["End"] = calendar["Start"] + timedelta(hours=2)


# In[ ]:


calendar[0] = "Študijski odbor doktorskega študija"
calendar.columns.values[0] = "Subject"
calendar


# In[ ]:


calendar["StartDate"] = calendar["Start"].apply(lambda x: x.date())
calendar["StartTime"] = calendar["Start"].apply(lambda x: x.time())
calendar["EndDate"] = calendar["End"].apply(lambda x: x.date())
calendar["EndTime"] = calendar["End"].apply(lambda x: x.time())


# In[ ]:


del calendar["Start"]
del calendar["End"]
calendar


# In[ ]:


cal_file = open(cal_file_fn, "w")
calendar.to_csv(cal_file)
cal_file.close()
