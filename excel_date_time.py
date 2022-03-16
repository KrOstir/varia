from __future__ import print_function
import pandas as pd
import time
from datetime import datetime

ctrl_initial = {
    "File": ["Filename"],
    "DateProc": [None],
    "Status": [None],
    "Action": [None],
    "SnowDetected": [True],
    "SnowMin": [None],
    "SnowPerc": [None],
    "ProcessTime": [None],
}

process = pd.DataFrame(ctrl_initial)

time_start = datetime.now()
time.sleep(5.1234)
process_time = datetime.now() - time_start
print("Total processing time: " + str(process_time))

position = len(process)

process.set_value(position, "File", "Test")
process.set_value(position, "DateProc", datetime.now().date())
process.set_value(position, "Status", "Finished")
process.set_value(position, "Action", "No")
process.set_value(
    position,
    "ProcessTime",
    process_time.seconds + int(process_time.microseconds / 1e4) / 100,
)

excel_fn = "excel_date_time.xlsx"
writer = pd.ExcelWriter(excel_fn, engine="xlsxwriter")
process.to_excel(writer, sheet_name="Test")
writer.save()
