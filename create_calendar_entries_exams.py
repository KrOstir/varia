# %%
# Create exams meetings calendar
#
# Krištof Oštir
# (c) 2021

# %%
# Imports
import pandas as pd
import io
from datetime import datetime
from datetime import timedelta

# %%
# File names
exam_file_fn = "D:/Kristof/OneDrive - Univerza v Ljubljani/Predavanja/izpiti/izpiti_202122_letni.xlsx"
cal_file_fn = "./data/" + exam_file_fn.split("/")[-1].split(".")[0] + ".csv"

# %%
# Read list of exams
# calendar = pd.read_excel(exam_file_fn, sep=';', dtype={'Opombe': 'str'})
calendar = pd.read_excel(exam_file_fn)

# %%
calendar.columns

# %%
calendar = calendar[["Datum roka", "Ura", "Predmet", "Predavalnica", "Opombe"]].dropna(
    subset=["Predmet"]
)

# %%
calendar["Subject"] = "Izpit - " + calendar["Predmet"]
del calendar["Predmet"]

# %%
calendar["AllDay"] = calendar["Ura"].apply(lambda x: x in ["00:00:00", "00:01:00"])

# %%
calendar.loc[calendar["Predavalnica"] == ".", "Predavalnica"] = ""

# %%
calendar.loc[calendar["Opombe"].isnull(), "Opombe"] = ""

# %%
calendar.columns = [
    "Start Date",
    "Start Time",
    "Location",
    "Description",
    "Subject",
    "All day event",
]

# %%
calendar

# %%
cal_file = open(cal_file_fn, "w", encoding="utf-8")
calendar.to_csv(cal_file, header=True, index=False, encoding="utf-8")
cal_file.close()

# %%
