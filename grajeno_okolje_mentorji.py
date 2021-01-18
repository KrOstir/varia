# %%
# Analiza predlaganih mentorjev
# Grajeno okolje
#
# Krištof Oštir
# (c) 2021

# %%
# Imports
import pandas as pd

# %%
# List
menthors_fn = 'd:/Kristof'
menthors_fn = 'D:/Kristof/OneDrive - Univerza v Ljubljani/Grajeno okolje/Dokumenti/go_seznam_mentorjev_2122.xlsx'

# %%
# Read
menthors_df = pd.read_excel(menthors_fn)

# %%
menthors_df.head()
# %%
