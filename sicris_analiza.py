# coding: utf-8
# Analiza podatkov o raziskovalcih in skupinah na področju geodezija

# Imports
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# plt.rcParams['figure.figsize'] = (10, 10)
plt.style.use('ggplot')

# Sicris URL za dostop do podatkov
url_zaposleni_raziskovalci = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&fields=mstid,rsrid,fname,lname,type,typedescr,abbrev,science,field,subfield,sci_descr,fil_descr,sub_descr&country=SI_JSON&entity=RSR&methodCall=rolecode=[RYE][SNX][RGP]%20and%20lang=slv"
# url_mentorji_mladim_raziskovalcem
# url_aktivni_pri_projektih_programih
# url_zaposleni_univerze_v_ljubljani
# url_zaposleni_univerze_v_mariboru
# url_zaposleni_univerze_na_primorskem
# url_zaposleni_univerze_v_novi_gorici
url_zaposleni_na_univerzah = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&fields=mstid,rsrid,fname,lname,type,typedescr,abbrev,science,field,subfield,sci_descr,fil_descr,sub_descr&country=SI_JSON&entity=RSR&methodCall=organization=Univerza%%20and%20lang=slv"
# url_raziskovalne_organizacije = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&country=SI_JSON&entity=ORG&methodCall=mstid=%%20and%20lang=slv"
# url_raziskovalne_skupine = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&country=SI_JSON&entity=GRP&methodCall=mstid=%%20and%20lang=slv"
# url_projekti = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&country=SI_JSON&entity=PRJ&methodCall=mstid=%%20and%20lang=slv"
# url_programi = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&country=SI_JSON&entity=PRG&methodCall=mstid=%%20and%20lang=slv"
# url_aktivni_projekti = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&country=SI_JSON&entity=PRJ_ACTIVE&methodCall=mstid=%%20and%20lang=slv"
# url_aktivni_programi = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=&country=SI_JSON&entity=PRG_ACTIVE&methodCall=mstid=%%20and%20lang=slv"
# url_raziskovalna_oprema

# Plot v PDF
pp = PdfPages('sicris_analiza.pdf')

# Zaposleni raziskovalci
zaposleni_raziskovalci = pd.read_json(url_zaposleni_raziskovalci)
zaposleni_raziskovalci_geo = zaposleni_raziskovalci.loc[zaposleni_raziskovalci['FIL_DESCR'].isin(["Geodezija", "Geologija"])]

# Na univerzah
zaposleni_raziskovalci_uni = pd.read_json(url_zaposleni_na_univerzah)
print(zaposleni_raziskovalci_uni.head())
zaposleni_raziskovalci_uni_geo = zaposleni_raziskovalci_uni.loc[zaposleni_raziskovalci_uni['FIL_DESCR'].isin(["Geodezija", "Geologija"])]
zaposleni_raziskovalci_uni_geo.head()

# Vsi
# Izloči tehnike, grupiraj po področju in MR ali raziskovalec
zaposleni_raziskovalci_geo = zaposleni_raziskovalci_geo[zaposleni_raziskovalci_geo['TYPEDESCR'] != "Tehnik"]
zaposleni_raziskovalci_geo = zaposleni_raziskovalci_geo.groupby(['FIL_DESCR', 'TYPEDESCR'])['TYPEDESCR'].count()

fig, ax = plt.subplots()
ax = zaposleni_raziskovalci_geo.plot(kind='bar', title ="Zaposleni raziskovalci",figsize=(15,10), legend=False, fontsize=14)
for i, v in enumerate(zaposleni_raziskovalci_geo):
    ax.text(i, v+0.5, str(v))
ax.xaxis.label.set_visible(False)
plt.savefig(pp, format='pdf', bbox_inches='tight', pad_inches=0.5)

# Univerze
# Izloči tehnike, gruporaj po področju in MR ali raziskovalec
zaposleni_raziskovalci_uni_geo = zaposleni_raziskovalci_uni_geo[zaposleni_raziskovalci_uni_geo['TYPEDESCR'] != "Tehnik"]
zaposleni_raziskovalci_uni_geo = zaposleni_raziskovalci_uni_geo.groupby(['FIL_DESCR', 'TYPEDESCR'])['TYPEDESCR'].count()

fig, ax = plt.subplots()
ax = zaposleni_raziskovalci_uni_geo.plot(kind='bar', title ="Zaposleni raziskovalci na univerzah",figsize=(15,10),legend=False, fontsize=14)
for i, v in enumerate(zaposleni_raziskovalci_uni_geo):
    ax.text(i, v+0.1, str(v), fontsize=12)
ax.xaxis.label.set_visible(False)
plt.savefig(pp, format='pdf', bbox_inches='tight', pad_inches=0.5)

# Raziskovalne skupine
url_raziskovalne_skupine_geod = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=mstid,grp_name,org_name,city,lname,fname,rsr_mstid,rsrid,grpid,orgid&country=SI_JSON&entity=GRP&methodCall=nameadvanced=name=%20and%20sci=2%20and%20fil=17%20and%20sub=%20and%20lang=slv"
url_raziskovalne_skupine_geol = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=mstid,grp_name,org_name,city,lname,fname,rsr_mstid,rsrid,grpid,orgid&country=SI_JSON&entity=GRP&methodCall=nameadvanced=name=%20and%20sci=1%20and%20fil=06%20and%20sub=%20and%20lang=slv"
raziskovalne_skupine_geod = pd.read_json(url_raziskovalne_skupine_geod)
raziskovalne_skupine_geod["FIL_DESCR"] = "Geodezija"
raziskovalne_skupine_geol = pd.read_json(url_raziskovalne_skupine_geol)
raziskovalne_skupine_geol["FIL_DESCR"] = "Geologija"
raziskovalne_skupine_geo = raziskovalne_skupine_geod.append(raziskovalne_skupine_geol)
raziskovalne_skupine_geo.head()
raziskovalne_skupine_geo = raziskovalne_skupine_geo.groupby(['FIL_DESCR'])['GRPID'].count()

fig, ax = plt.subplots()

ax = raziskovalne_skupine_geo.plot(kind='bar', title ="Raziskovalne skupine",figsize=(15,10),legend=False, fontsize=14)
for i, v in enumerate(raziskovalne_skupine_geo):
    ax.text(i, v+.1, str(v), fontsize=12)
ax.xaxis.label.set_visible(False)
plt.savefig(pp, format='pdf', bbox_inches='tight', pad_inches=0.5)

# Raziskovalni projekti
url_raziskovalni_projekti_geod = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=mstid_prg,mstid_science,mstid_contr,title,prjid,startdate,enddate,lname,fname,rsr_mstid&country=SI_JSON&entity=PRJ&methodCall=nameadvanced=name=%20and%20sci=2%20and%20fil=17%20and%20sub=%20and%20duration=0%20and%20prj_type=%20and%20lang=slv"
url_raziskovalni_projekti_geol = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=mstid_prg,mstid_science,mstid_contr,title,prjid,startdate,enddate,lname,fname,rsr_mstid&country=SI_JSON&entity=PRJ&methodCall=nameadvanced=name=%20and%20sci=1%20and%20fil=06%20and%20sub=%20and%20duration=0%20and%20prj_type=%20and%20lang=slv"
raziskovalni_projekti_geod = pd.read_json(url_raziskovalni_projekti_geod)
raziskovalni_projekti_geod["FIL_DESCR"] = "Geodezija"
raziskovalni_projekti_geol = pd.read_json(url_raziskovalni_projekti_geol)
raziskovalni_projekti_geol["FIL_DESCR"] = "Geologija"
raziskovalni_projekti_geo = raziskovalni_projekti_geod.append(raziskovalni_projekti_geol)
raziskovalni_projekti_geo["MSTID_PRG"] = raziskovalni_projekti_geo["MSTID_PRG"].map({'L': 'aplikativni', 'J': 'temeljni', 'V': 'ciljni', 'M': 'ciljni',
'Z': 'podoktorski', 'N': 'evropski', 'R': 'razvojni raziskovalni'})
raziskovalni_projekti_geo.head()
raziskovalni_projekti_geo = raziskovalni_projekti_geo.groupby(['FIL_DESCR', 'MSTID_PRG'])['FIL_DESCR'].count()

fig, ax = plt.subplots()
ax = raziskovalni_projekti_geo.plot(kind='bar', title ="Raziskovalni projekti",figsize=(15,10),legend=False, fontsize=14)
for i, v in enumerate(raziskovalni_projekti_geo):
    ax.text(i, v+.1, str(v), fontsize=12)
ax.xaxis.label.set_visible(False)
plt.savefig(pp, format='pdf', bbox_inches='tight', pad_inches=0.5)

# Aktivni
url_raziskovalni_projekti_akt_geod = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=mstid_prg,mstid_science,mstid_contr,title,prjid,startdate,enddate,lname,fname,rsr_mstid&country=SI_JSON&entity=PRJ&methodCall=nameadvanced=name=%20and%20sci=2%20and%20fil=17%20and%20sub=%20and%20duration=1%20and%20prj_type=%20and%20lang=slv"
url_raziskovalni_projekti_akt_geol = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=mstid_prg,mstid_science,mstid_contr,title,prjid,startdate,enddate,lname,fname,rsr_mstid&country=SI_JSON&entity=PRJ&methodCall=nameadvanced=name=%20and%20sci=1%20and%20fil=06%20and%20sub=%20and%20duration=1%20and%20prj_type=%20and%20lang=slv"
raziskovalni_projekti_akt_geod = pd.read_json(url_raziskovalni_projekti_akt_geod)
raziskovalni_projekti_akt_geod["FIL_DESCR"] = "Geodezija"
raziskovalni_projekti_akt_geol = pd.read_json(url_raziskovalni_projekti_akt_geol)
raziskovalni_projekti_akt_geol["FIL_DESCR"] = "Geologija"
raziskovalni_projekti_akt_geo = raziskovalni_projekti_akt_geod.append(raziskovalni_projekti_akt_geol)
raziskovalni_projekti_akt_geo["MSTID_PRG"] = raziskovalni_projekti_akt_geo["MSTID_PRG"].map({'L': 'aplikativni', 'J': 'temeljni', 'V': 'ciljni', 'M': 'ciljni',
'Z': 'podoktorski', 'N': 'evropski', 'R': 'razvojni raziskovalni'})
raziskovalni_projekti_akt_geo.head()
raziskovalni_projekti_akt_geo = raziskovalni_projekti_akt_geo.groupby(['FIL_DESCR', 'MSTID_PRG'])['FIL_DESCR'].count()
raziskovalni_projekti_akt_geo

fig, ax = plt.subplots()
ax = raziskovalni_projekti_akt_geo.plot(kind='bar', title ="Aktivni raziskovalni projekti",figsize=(15,10),legend=False, fontsize=14)
for i, v in enumerate(raziskovalni_projekti_akt_geo):
    ax.text(i, v+.02, str(v), fontsize=12)
ax.xaxis.label.set_visible(False)
plt.savefig(pp, format='pdf', bbox_inches='tight', pad_inches=0.5)

# Aktivni raziskovalni programi
url_raziskovalni_programi_geod = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=mstid_prg,mstid_science,mstid_contr,title,prjid,startdate,enddate,lname,fname,rsr_mstid&country=SI_JSON&entity=PRG&methodCall=nameadvanced=name=%20and%20sci=2%20and%20fil=17%20and%20sub=%20and%20duration=1%20and%20prg_type=%20and%20lang=slv"
url_raziskovalni_programi_geol = "http://www.sicris.si/Common/rest.aspx?sessionID=1234CRIS12002B01B01A03IZUMBFICDOSKJHS588Nn44131&fields=mstid_prg,mstid_science,mstid_contr,title,prjid,startdate,enddate,lname,fname,rsr_mstid&country=SI_JSON&entity=PRG&methodCall=nameadvanced=name=%20and%20sci=1%20and%20fil=06%20and%20sub=%20and%20duration=1%20and%20prg_type=%20and%20lang=slv"
raziskovalni_programi_geod = pd.read_json(url_raziskovalni_programi_geod)
raziskovalni_programi_geod["FIL_DESCR"] = "Geodezija"
raziskovalni_programi_geol = pd.read_json(url_raziskovalni_programi_geol)
raziskovalni_programi_geol["FIL_DESCR"] = "Geologija"
raziskovalni_programi_geo = raziskovalni_programi_geod.append(raziskovalni_programi_geol)
raziskovalni_programi_geo["MSTID_PRG"] = raziskovalni_programi_geo["MSTID_PRG"].map({'P': 'programi', 'I': 'infrastrukturni programi'})
raziskovalni_programi_geo["MSTID_SCIENCE"] = raziskovalni_programi_geo["MSTID_SCIENCE"].map({1: 'Naravoslovje', 2: 'Tehnika', 3: 'Medicina', 4: 'Biotehnika', 5: 'Družboslovje', 6: 'Humanistika', 7: "Interdisciplinarne raziskave"})
raziskovalni_programi_geo.head()
raziskovalni_programi_geo = raziskovalni_programi_geo.groupby(['FIL_DESCR', 'MSTID_SCIENCE'])['FIL_DESCR'].count()

fig, ax = plt.subplots()
ax = raziskovalni_programi_geo.plot(kind='bar', title ="Raziskovalni programi",figsize=(15,10), legend=False, fontsize=14)
for i, v in enumerate(raziskovalni_programi_geo):
    ax.text(i, v+.02, str(v), fontsize=12)
ax.xaxis.label.set_visible(False)
plt.savefig(pp, format='pdf', bbox_inches='tight', pad_inches=0.5)

# Zapri PDF
pp.close()