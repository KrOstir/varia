# %%
# Relief Visualization Tool Download Statistics
#
# Krištof Oštir
# (c) 2021

# %%
# Imports
import pandas as pd
import glob

# %%
# Folders with Sentinel-1 images
s1_folders = [
    'H:/Sentinel-1/044_147_asc',
    'H:/Sentinel-1/022_440_desc'
]

# %%
# Folders with Sentinel-1 images
s1_import_folders = [
    'H:/Sentinel-1/import/044_147_asc',
    'H:/Sentinel-1/import/022_440_desc'
]

# File list
s1_list = 'G:/SARScape/s1_list.xlsx'
s1_import_list = 'G:/SARScape/s1_import_list.xlsx'

# %%
s1_df = pd.DataFrame()

# %%
# Check folder list
for folder in s1_folders:
    print(folder)

    df = pd.DataFrame(glob.glob1(folder, '*.zip'), columns=['Filename'])

    df['Folder'] = folder.split('/')[-1]

    df_a = df['Filename'].str.split('_', expand=True)

    df['Date'] = pd.to_datetime(df_a.iloc[:, 5].str.split('T', expand=True)[0])
    df['Sat'] = df_a.iloc[:, [0]]

    s1_df = s1_df.append(df)


# %%
print('Downloads')
for folder in s1_df['Folder'].unique():
    print(folder)
    df_s = s1_df[s1_df['Folder'] == folder]
    print(df_s['Date'].min())
    print(df_s['Date'].max())

# %%
s1_df.to_excel(s1_list, index=False)

# %%
s1_l_df = pd.DataFrame()

# %%
# Check folder list
for folder in s1_import_folders:
    print(folder)

    glob.glob1(folder, '*slc_list.sml')

    df = pd.DataFrame(glob.glob1(folder, '*slc_list.sml'), columns=['Filename'])

    df['Folder'] = folder.split('/')[-1]

    df_a = df['Filename'].str.split('_', expand=True)

    df_a.head()

    df['Date'] = pd.to_datetime(df_a.iloc[:, 2].str.split('T', expand=True)[0])

    s1_l_df = s1_l_df.append(df)

# %%
s1_l_df['Folder'].unique()

# %%
print('Imports')
for folder in s1_l_df['Folder'].unique():
    print(folder)
    df_s = s1_df[s1_df['Folder'] == folder]
    print(df_s['Date'].min())
    print(df_s['Date'].max())

# %%
s1_l_df.to_excel(s1_import_list, index=False)
# %%
