# %%
# Analiza predlaganih mentorjev
# Grajeno okolje
#
# Krištof Oštir
# (c) 2021

# %%
# Imports
import pandas as pd
import requests
import json

# %%
# List
menthors_fn = './data/go_seznam_mentorjev_2122.xlsx'

# %%
# Sicris parameters
mstid_url = 'https://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=rsrid,&country=SI_JSON&entity=RSR&methodCall=mstid='
bib_url = 'https://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&country=SI_JSON&entity=rsr&methodCall=id='


# %%
# Sicris code
mstid = 15112

# %%
mstid_url_r = mstid_url + str(mstid)
r = requests.get(mstid_url_r)
r.text

# %%
mstid_json = json.loads(r.text[1:-1])

# %%
type(mstid_json)
mstid_json['RSRID']

# %%
bib_url_r = bib_url + mstid_json['RSRID']
r = requests.get(bib_url_r)
r.text

# %%
# %%
bib_json = json.loads(r.text[1:-1])

# %%
bib_json_recap = json.dumps(bib_json['RECAPITUALITION'])

# %%
# bib_josn_recap['Z']
bib_josn_recap
# %%
# %%





# %%
# Read
menthors_df = pd.read_excel(menthors_fn)

# %%
menthors_df.head()
# %%
