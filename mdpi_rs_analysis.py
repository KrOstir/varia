# %%
# MDPI Remote Sensing
#
# Analyze paper statistics
# Read paper data from CSV produced by mdpi_rs_analysis_prepare.py
#
# Krištof Oštir
# 2021-06

# %%
# Load libraries
import pandas as pd
import matplotlib.pyplot as plt

# %%
# Input data
mdpi_file_stat = './data/mdpi_rs_analysis.csv'
mdpi_file_out = './data/mdpi_rs_analysis.xlsx'

# %%
print('Analyzing MDPI Remote Sensing')

# %%
# Read data
mdpi = pd.read_csv(mdpi_file_stat)
mdpi = mdpi.sort_values(by=['Volume', 'Issue', 'Paper'])
# Remove last year
l_v = mdpi['Volume'].max()
mdpi.drop(
    mdpi[mdpi['Volume'] == l_v].index,
    inplace=True)

# %%
# Group by volume and issue, count papers
mdpi_gr_vi = pd.DataFrame(mdpi.groupby(['Volume', 'Issue'])[
                          'Paper'].sum().reset_index(name='Papers'))
mdpi_gr_v = pd.DataFrame(mdpi.groupby(['Volume'])[
                         'Paper'].sum().reset_index(name='Papers'))

# Add years
mdpi_gr_v['Year'] = 2008 + mdpi_gr_v['Volume']
mdpi_gr_vi['Year'] = 2008 + mdpi_gr_vi['Volume']

# %%
# Change index
mdpi_gr_v.set_index('Year', inplace=True)
mdpi_gr_v.drop(['Volume'], inplace=True, axis=1)


# %%
# Change index
mdpi_gr_vi.set_index(['Year', 'Issue'], inplace=True)
mdpi_gr_vi.drop(['Volume'], inplace=True, axis=1)


# %%
# Per year
plt.figure()
mdpi_gr_v.plot(marker='o')
plt.legend(frameon=False)
plt.show()

# %%
# Per year and issue
plt.figure()
mdpi_gr_vi.plot()
plt.legend(frameon=False)
plt.show()

# %%
