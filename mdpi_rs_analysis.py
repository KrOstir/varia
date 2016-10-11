# MDPI Remote Sensing
#
# Analyse paper statistics, read paper rada from CSV
#
# Krištof Oštir
# 2016-10-08

# Load libraries
import pandas as pd
import numpy as np

# Input data
mdpi_file_stat = 'mdpi_rs_analysis.csv'
mdpi_file_out = 'mdpi_rs_analysis.xlsx'

print('Analyzing MDPI Remote Sensing')

# Read data
mdpi = pd.read_csv(mdpi_file_stat)
mdpi = mdpi.sort_values(by=['Volume', 'Issue', 'Paper'])
# mdpi['Pages'] = mdpi['Paper'].shift(-1).diff()
# mdpi['Pages'][mdpi['Pages'] <= 1] = np.nan

# mdpi = mdpi[mdpi.columns[0:3]]
# print(mdpi.head())

# Group by volume and issue, count papers
mdpi_gr_vi = pd.DataFrame(mdpi.groupby(['Volume', 'Issue'])['Paper'].count().reset_index(name = 'Papers'))
mdpi_gr_v = pd.DataFrame(mdpi.groupby(['Volume'])['Paper'].count().reset_index(name = 'Papers'))
# mdpi_gr_vp = pd.DataFrame(mdpi.groupby(['Volume'])['Pages'].mean().reset_index(name = 'Papers'))
# Average number of pages per volume
# print('Pages per paper', mdpi_gr_vp['Papers'][0:6].mean())

# Save statistics to Excel
writer = pd.ExcelWriter(mdpi_file_out, engine='xlsxwriter')
mdpi_gr_v.to_excel(writer, sheet_name='Volumes')
mdpi_gr_vi.to_excel(writer, sheet_name='Issues')
mdpi.to_excel(writer, sheet_name='Papers')
writer.save()
