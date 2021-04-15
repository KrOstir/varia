# %%
# Program group analysis
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
# Abbreviate names

def organization_field(id):

    names = {
        '0618': 'ZRC SAZU',
        '0792': 'UL FGG'
    }
    organization = names[id]
    return organization


# %%
# Files
ps_members = './data/ps_clani.xlsx'
# Where to put plots
ps_plots = './data/'

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
# Add English fields
sicris_members_df['ORG_NAME'] = sicris_members_df.apply(
    lambda x: organization_field(x['ORG_MSTID']), axis=1)
    
# %%
# Save to Excel
sicris_members_df.to_excel(ps_members, index=False)

# %%
# Plot organizations of research
fig, ax = plt.subplots()
sicris_members_df['ORG_NAME'].value_counts().plot(kind='pie')
plt.savefig(ps_plots + 'ps_organizations.png', dpi=300)
plt.close()

# %%
# Plot sciences of research
fig, ax = plt.subplots(figsize=(8, 8))
sicris_members_df['SCI_DESCR'].value_counts().plot(kind='pie')
plt.savefig(ps_plots + 'ps_sciences.png', dpi=300)
plt.close()

# %%
# Plot fields of research
fig, ax = plt.subplots(figsize=(8, 8))
sicris_members_df['FIL_DESCR'].value_counts().plot(kind='pie')
plt.savefig(ps_plots + 'ps_fields.png', dpi=300)
plt.close()


# %%
# Plot types
fig, ax = plt.subplots(figsize=(8, 8))
sicris_members_df['TYPE'].value_counts().plot(kind='pie')
plt.savefig(ps_plots + 'ps_type.png', dpi=300)
plt.close()

# %%
# Plot types
fig, ax = plt.subplots(figsize=(8, 8))
sicris_members_df['ROLECODE'].value_counts().plot(kind='pie')
plt.savefig(ps_plots + 'ps_role.png', dpi=300)
plt.close()

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
