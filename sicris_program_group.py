# %%
# Program gropup analysis
#
# Krištof Oštir
# (c) 2021

# %%
# Imports
import pandas as pd
import json

# %%
# Sicris URL
sicris_url = 'https://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&country=SI_JSON&entity=prg&methodCall=id=17645%20and%20lang=slv'

# %%
# Get JSON
r = requests.get(sicris_url)
sicris_json = json.loads(r.text[1:-1])

# %%
# Members
sicris_members_df = pd.DataFrame.from_dict(sicris_json['EMPLOY'])
sicris_members_df

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
