# %%
# Faktor vpliva za Geodetski vestnik
#
# Krištof Oštir
# (c) 2021
# %%
# Potrebne knjižnice
import pandas as pd
import matplotlib.pyplot as plt

# from dateutil import parser
from urllib.request import Request, urlopen

# %%
# Parameters
# IF URL
if_url = (
    "https://plus.si.cobiss.net/opac7/jcr?query=geodetski%20vestnik&max=100&sort=def"
)
# Where to put plots
plots_folder = "./figures/"

# %%
# Read webpage
req = Request(if_url, headers={"User-Agent": "Mozilla/5.0"})
webpage = urlopen(req).read()

# %%
# Read downloads
if_df = pd.read_html(webpage)[0]
if_df.head()

# %%
if_df = if_df.drop(["Št.", "Naslov serijske publikacije", "ISSN"], axis=1)
if_df = if_df.set_index("Leto")
if_df.sort_index(inplace=True)
if_df


# %%
plt.plot(if_df, marker="o")
plt.title("Geodetski vestnik IF")
# plt.show()
plt.savefig(plots_folder + "geodetski_vestnik_if.png", dpi=300)
# plt.show()
plt.close()

# %%
