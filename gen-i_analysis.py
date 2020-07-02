# %%
# Analyse electricity usage from Gen-i

# %%
# Libraries
import glob

import matplotlib.pyplot as plt
import pandas as pd

# %%
# Path to data
geni_path = './data/geni/'
# %%
# All files
fd_files = glob.glob(geni_path + "/*.xlsx")


# %%
def data_replace(data):
    str_repl = [
        ['JAN ', '01-'],
        ['FEB ', '02-'],
        ['MAR ', '03-'],
        ['APR ', '04-'],
        ['MAJ ', '05-'],
        ['JUN ', '06-'],
        ['JUL ', '07-'],
        ['AVG ', '08-'],
        ['SEP ', '09-'],
        ['OKT ', '10-'],
        ['NOV ', '11-'],
        ['DEC ', '12-']
    ]

    for pair in str_repl:
        data = data.replace(pair[0], pair[1])

    return data


# %%
# Read DFs
li = []
for filename in fd_files:
    print(filename)
    df = pd.read_excel(filename)

    li.append(df)
# %%
# Joind DFs
geni_df = pd.concat(li, axis=0, ignore_index=True)

# %%
geni_df.columns

# %%
# Drop unnecessary columns
geni_df.drop(['Merilno mesto', 'ET'], axis=1, inplace=True)

# %%
# Replace month names with numbers
geni_df['Mesec'] = geni_df['Mesec'].apply(data_replace)

# %%
# Convert MM-YY to datetime
geni_df['Mesec'] = pd.to_datetime(geni_df['Mesec'], format='%m-%y')

# %%
# Set index
geni_df.set_index('Mesec', inplace=True)

# %%
# Delete rows with 0
geni_df = geni_df[geni_df['VT'] != 0]
geni_df = geni_df[geni_df['MT'] != 0]

# %%
plt.plot(geni_df)
plt.show()

# %%
# Agregate by year
geni_df_year = geni_df.groupby(geni_df.index.year).mean()

# %%
plt.plot(geni_df_year)
plt.show()

# %%
# Agregate by month
geni_df_month = geni_df.groupby(geni_df.index.month).mean()

# %%
plt.plot(geni_df_month)
plt.show()
