# %%
# Mentor analysis
# Built Environment
#
# Krištof Oštir
# (c) 2021

# %%
# Imports
import os
import pandas as pd
import requests
import json

# %%
# Filenames
# List of mentors
# mentors_in_fn = './data/go_seznam_mentorjev_2122.xlsx'
# mentors_in_fn = 'C:/Users/krost/OneDrive - Univerza v Ljubljani/Grajeno okolje/Dokumenti/go_seznam_mentorjev_2122.xlsx'
mentors_in_fn = 'C:/Users/krost/Univerza v Ljubljani/Golobar, Monika - Grajeno okolje/Študijski odbor/Evidenca mentorjev GO/go_seznam_mentorjev.xlsx'
filename = os.path.splitext(mentors_in_fn)
mentors_out_fn = filename[0] + '_sicris' + filename[1]

# %%
# Sicris parameters
mstid_url = 'https://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=rsrid,&country=SI_JSON&entity=RSR&methodCall=mstid='
bib_url = 'https://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&country=SI_JSON&entity=rsr&methodCall=id='
# sicris_url = 'https://www.sicris.si/public/jqm/rsr.aspx?lang=slv&opdescr=search&opt=2&subopt=300&code1=rsr&search_term='
sicris_url = 'https://www.sicris.si/public/jqm/search_basic/slv/2/300/search/rsr/'

# %%
# Sicris score return fields
# bib_fields = [
#         'A1_Score', 'A11', 'A12',
#     'A3_Score', 'AI', 'AII',
#     'CI_10', 'CI_Max',
#     'h-index', 'Z']
bib_fields = ['Z', 'A12', 'CI_10', 'h-index']
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
    mstid_str = str(mstid).zfill(5)
    mstid_url_r = mstid_url + mstid_str
    r = requests.get(mstid_url_r)
    mstid_json = json.loads(r.text[1:-1])
    bib_url_r = bib_url + mstid_json['RSRID']
    r = requests.get(bib_url_r)
    bib_json = json.loads(r.text[1:-1])
    bib_r = {}
    for field in bib_fields:
        bib_r.update(
            {
                field:
                float(bib_json['RECAPITUALITION'][0][field].replace(',', '.'))
            }
        )
    return bib_r

# %%
# Add English research fields

def research_field(field_si):
    """
    research_field Add English name for fied

    Parameters
    ----------
    field_si : str
        Field in Slovenina

    Returns
    -------
    str
        Field in English
    """
    fields = {
        'Geodezija': 'Geodesy',
        'Geologija': 'Geology',
        'Gradbeništvo': 'Civil Engineering',
        'Načrtovanje in urejanje prostora': 'Spatial Planning and Spatial Development'
    }
    field_en = fields[field_si]
    return field_en

# %%
# # Sicris code
# mstid = 15112
# bib_recap = sicris_get_info(mstid)
# bib_recap


# %%
# Read mentors
mentors_df = pd.read_excel(mentors_in_fn, dtype={'Sicris': 'Int64'})
mentors_df.head()

# %%
# Add English fields
mentors_df['Field'] = mentors_df.apply(
    lambda x: research_field(x['Smer']), axis=1)
# %%
# Add Sicris URL
mentors_df['Sicris_URL'] = mentors_df['Sicris'].apply(lambda x: "{}{}".format(sicris_url, str(x).zfill(5)))

# %%
# Get Sicris info
mentors_df['recap'] = mentors_df.apply(
    lambda x: sicris_get_info(x['Sicris']), axis=1)

# %%
# Join with DF
mentors_df = mentors_df.join(pd.json_normalize(mentors_df['recap']))

# %%
# Drop column
mentors_df.drop(columns=['recap'], inplace=True)

# %%
# Check mentor Z > 150 and A12 > 0
mentors_df['Mentor'] = (mentors_df['Z'] >= 150) & (mentors_df['A12'] > 0)


# %%
mentors_df.to_excel(mentors_out_fn, index=False)

# %%
