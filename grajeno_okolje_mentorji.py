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
# Filenames
# List of mentors 
mentors_in_fn = './data/go_seznam_mentorjev_2122.xlsx'
filename = os.path.splitext(mentors_in_fn)
mentors_out_fn = filename[0] + '_sicris' + filename[1]
mentors_out_fn

# %%
# Sicris parameters
mstid_url = 'https://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=rsrid,&country=SI_JSON&entity=RSR&methodCall=mstid='
bib_url = 'https://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&country=SI_JSON&entity=rsr&methodCall=id='

# %%
# Sicris score return fields
bib_fields = ['A1_Score',  'A11',  'A12',  'A3_Score',
              'AI',  'AII',  'CI_10',  'CI_Max',  'h-index',  'Z']

# %%
# Get recapitulazation data from Sicris
def sicris_get_info(mstid):
    """
    sicris_get_info Generate researches score from Sicris

    :param mstid: Sicris ID
    :type mstid: int
    :return: recapitalization
    :rtype: dict
    """
    mstid_url_r = mstid_url + str(mstid)
    r = requests.get(mstid_url_r)
    mstid_json = json.loads(r.text[1:-1])
    bib_url_r = bib_url + mstid_json['RSRID']
    r = requests.get(bib_url_r)
    bib_json = json.loads(r.text[1:-1])
    bib_r = {'MSTID': int(mstid)}
    for field in bib_fields:
        bib_r.update(
            {
                field:
                float(bib_json['RECAPITUALITION'][0][field].replace(',', '.'))
            }
        )
    return bib_r


# %%
# Sicris code
mstid = 15112

# %%
bib_recap = sicris_get_info(mstid)
bib_recap

# %%
# Read mentors
mentors_df = pd.read_excel(mentors_in_fn, dtype={'Sicris': 'Int64'})
mentors_df.head()

# %%
mentors_df = mentors_df[0:3]
mentors_df

# %%
mentors_df['recap'] = mentors_df.apply(lambda x: sicris_get_info(x['Sicris']), axis=1)


# %%
mentors_df['recap']
# %%
