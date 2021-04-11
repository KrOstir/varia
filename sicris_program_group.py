# %%
# Program gropup analysis
#
# Krištof Oštir
# (c) 2021

# %%
# Imports
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json

# %%
# Sicris URL
sicris_url = 'https://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&country=SI_JSON&entity=prg&methodCall=id=17645%20and%20lang=slv'
# API reference
# https://www.sicris.si/public/jqm/memo.aspx?lang=slv&opdescr=faq&source=faq.inc&opt=5&subopt=2#8


# %%
# Files
ps_members = './data/ps_clani.xlsx'

# %%
# Get JSON
r = requests.get(sicris_url)
sicris_json = json.loads(r.text[1:-1])
sicris_json

# %%
# Members
sicris_members_df = pd.DataFrame.from_dict(sicris_json['EMPLOY'])
sicris_members_df.columns

# %%
# Save to Excel
sicris_members_df.to_excel(ps_members)

# %%
# Plot sicences of research
sicris_members_df['NAME'].value_counts().plot(kind='pie')

# %%
# Plot sicences of research
sicris_members_df['SCI_DESCR'].value_counts().plot(kind='pie')

# %%
# Plot fields of research
sicris_members_df['FIL_DESCR'].value_counts().plot(kind='pie')

# %%
# Plot types
sicris_members_df['TYPE'].value_counts().plot(kind='pie')

# %%
# Plot types
sicris_members_df['ROLECODE'].value_counts().plot(kind='pie')

# %%
# Recapitualtion
sicris_json['RECAPITUALITION']

# %%
# Citations
sicris_json['CITATIONS']

# %%
# Citations
sicris_json['PERIODS']

# %%
