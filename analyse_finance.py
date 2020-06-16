# %%
# Analyse financial data
# Import data from Gorenjska banka and perform financial analysis.

# %%
# Libraries
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import glob

# %%
# Path
fd_path = './data/finance/'

# %%
# All files
fd_files = glob.glob(fd_path + "/promet_izvoz_*.txt")

# %%
def data_replace(data):
    str_repl = [
        ['GEODEZIJO;', 'GEODEZIJO-'],
        ['SCA;YYR', 'SCA-YYR'],
        [';INSU', '-INSU'],
        ['ZRC SAZU;', 'ZRC SAZU-'],
        ['S.P.A.;', 'S.P.A.-'],
        ['FURS;', 'FURS-'],
        [';OTHR', '-OTHR'],
        ['EUROPEAN COMMISSION;', 'EUROPEAN COMMISSION-']
    ]

    for pair in str_repl:
        data = data.replace(pair[0], pair[1])

    return data

# %%
# Read DFs
li = []
for filename in fd_files:
    print(filename)
    with open(filename, "r", encoding="utf-8") as myfile:
        data = myfile.read()
    data = data_replace(data)

    df = pd.read_csv(StringIO(data), delimiter=';', decimal=',', thousands='.')
    li.append(df)

# %%
# Joind DFs
fd_df = pd.concat(li, axis=0, ignore_index=True)

# %%
# print(fd_df.columns)
fd_df.columns

# %%
fd_df.drop(['Ime in priimek', 'Račun', 'Valuta'], inplace=True, axis=1)

    # %%
    plt.plot(fd_df['V dobro'])
    plt.show()

# %%
plt.plot(fd_df['V breme'])
plt.show()

#%%
fd_df['InOut'] = fd_df['V dobro'] - fd_df['V breme']

# %%
plt.plot(fd_df['InOut'])
plt.show()

# %%
plt.plot(fd_df['V dobro'])
plt.plot(-fd_df['V breme'])
plt.show()

