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

print("Analyzing MDPI Remote Sensing")

# Read data
mdpi = pd.read_csv(mdpi_file_stat)
print(mdpi.head())