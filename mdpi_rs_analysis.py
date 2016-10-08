# MDPI Remote Sensing
#
# Analyse paper statistics, read paper rada from CSV
#
# Krištof Oštir
# 2016-10-08

# Load libraries
import pandas as pd

# Input data
mdpi_file_stat = "mdpi_rs_analysis.csv"
mdpi_file_out = "mdpi_rs_analysis.xlsx"

print("Analyzing MDPI Remote Sensing")

# Read data
mdpi = pd.read_csv(mdpi_file_stat)
mdpi = mdpi[mdpi.columns[0:3]]
# print(mdpi.head())

# Group by volume and issue, count papers
mdpi_gr_vi = pd.DataFrame(mdpi.groupby(['Volume', 'Issue'])['Paper'].count().reset_index(name = "Papers"))
mdpi_gr_v = pd.DataFrame(mdpi.groupby(['Volume'])['Paper'].count().reset_index(name = "Papers"))
print(mdpi_gr_v)

# Save statistics to Excel
writer = pd.ExcelWriter(mdpi_file_out, engine='xlsxwriter')
mdpi_gr_v.to_excel(writer, sheet_name='Volumes')
mdpi_gr_vi.to_excel(writer, sheet_name='Issues')
writer.save()
