# Mac OS X Memory Usage
#
# Compute total memory usage per app
#
# Krištof Oštir
# 2016-09-13

# Load libraries
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

# Memory dump
memory_copy = '''
 Google Chrome	148,6 MB	17,8 MB	42	569	3008	Kristof	0,7	2:50,43	1	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	No		0 bytes	No	Yes
 Google Chrome Helper	146,2 MB	0 bytes	18	145	4879	Kristof	2,0	3,24		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	143,5 MB	0 bytes	17	141	4887	Kristof	0,2	3,30		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	121,1 MB	0 bytes	18	136	4886	Kristof	0,2	3,52		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	116,5 MB	25,7 MB	16	152	3037	Kristof	0,1	8,85	2	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	109,4 MB	0 bytes	17	137	4882	Kristof	0,3	2,88		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	108,1 MB	0 bytes	17	137	4888	Kristof	0,2	1,48		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	94,9 MB	0 bytes	18	137	4889	Kristof	0,1	1,48		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	89,7 MB	0 bytes	18	135	4884	Kristof	0,2	2,28		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	83,7 MB	780 KB	17	123	3033	Kristof	0,4	38,17	0	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	77,2 MB	4,1 MB	19	149	3031	Kristof	0,2	11,03	1	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	76,3 MB	0 bytes	16	131	4883	Kristof	0,1	1,68		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	70,8 MB	0 bytes	19	137	4885	Kristof	0,1	1,79		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	70,2 MB	0 bytes	17	136	4881	Kristof	0,1	1,64		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	56,4 MB	12,2 MB	4	160	3020	Kristof	0,0	14,74	1	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	44,2 MB	0 bytes	15	122	4880	Kristof	0,1	0,73		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	27,3 MB	388 KB	14	116	3036	Kristof	0,0	2,37	0	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	26,5 MB	932 KB	11	110	3034	Kristof	0,0	0,93	0	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Google Chrome Helper	25,0 MB	0 bytes	11	111	3035	Kristof	0,0	0,65	0	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Firefox	980,5 MB	58,7 MB	63	356	3373	Kristof	9,6	4:49,13	6	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	No		0 bytes	No	No
 https://www.facebook.com	197,4 MB	0 bytes	23	228	4856	Kristof	0,7	2,74		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Safari	153,1 MB	13,2 MB	27	450	4061	Kristof	0,2	30,78	1	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	No		0 bytes	No	Yes
 https://www.dataquest.io	101,0 MB	0 bytes	13	211	4864	Kristof	0,1	2,40		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 https://www.kaggle.com	99,0 MB	0 bytes	14	260	4862	Kristof	0,1	2,10		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 http://lifehacker.com	89,6 MB	0 bytes	15	260	4865	Kristof	0,2	8,17		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 https://www.kaggle.com	86,4 MB	0 bytes	13	202	4860	Kristof	0,0	2,09		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 http://www.gcflearnfree.org	82,9 MB	0 bytes	21	270	4858	Kristof	0,1	2,05		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 http://data.worldbank.org	79,3 MB	0 bytes	13	204	4861	Kristof	0,0	1,08		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 https://www.kaggle.com	71,3 MB	0 bytes	14	206	4863	Kristof	0,0	1,11		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 http://www.makeuseof.com	46,3 MB	0 bytes	13	210	4866	Kristof	0,1	1,09		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 http://www.laptopmag.com	43,6 MB	0 bytes	13	205	4867	Kristof	0,1	1,41		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 http://pandas.pydata.org	32,4 MB	0 bytes	13	203	4857	Kristof	0,0	0,87		64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 Safari Networking	24,1 MB	4,3 MB	5	123	4063	Kristof	0,1	11,95	2	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	Yes		0 bytes	No	Yes
 com.apple.Safari.SafeBrowsing.Service	4,9 MB	464 KB	4	73	4068	Kristof	0,0	2,13	0	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	No	No		0 bytes	No	Yes
 com.apple.Safari.ImageDecoder	3,3 MB	1,7 MB	2	43	4073	Kristof	0,0	0,08	0	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	Yes	Yes		0 bytes	No	Yes
 com.apple.SafariServices	1,6 MB	1,2 MB	2	40	2267	Kristof	0,0	0,03	0	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	Yes	No		0 bytes	No	Yes
 SafariCloudHistoryPushAgent	1,4 MB	348 KB	4	49	386	Kristof	0,0	5,88	1	64 bit	0 bytes	0 bytes	0	0		-	No	No	0 bytes	0 bytes	0 bytes	0 bytes	0 bytes	Yes	No		0 bytes	No	Yes
'''

# Clean memory dump and make dataframe
memory_copy = memory_copy.replace(',', '.')
memory_copy = memory_copy.replace('\t', ',')
data_io = StringIO(memory_copy)
memory_df = pd.read_csv(data_io, header=None)
# Rename columns
memory_df = memory_df[memory_df.columns[0:2]]
memory_df.columns = ['Process', 'Memory']
# Strip process names
memory_df.Process = memory_df.Process.str.lstrip()
# Convert memory units
memory_df.Memory= memory_df.Memory.str.split()
memory_df['Size'] = memory_df.Memory.str[0].astype(float)
memory_df['Size KB'] = memory_df['Size'] * (memory_df.Memory.str[1] == 'KB') * 1
memory_df['Size MB'] =  memory_df['Size'] * (memory_df.Memory.str[1] == 'MB') * 1024
memory_df['Size GB'] = memory_df['Size'] * (memory_df.Memory.str[1] == 'GB') * 1024 * 1024
memory_df['Size'] = memory_df['Size KB'] + memory_df['Size MB'] + memory_df['Size GB']
memory_df = memory_df[['Process', 'Size']]
# Find browser, Chrome and Firefox are listed, everything else is Safari
memory_df['Browser'] = 'Safari'
memory_df.loc[memory_df['Process'].str.startswith('Google'),'Browser'] = 'Chrome'
memory_df.loc[memory_df['Process'].str.startswith('Firefox'),'Browser'] = 'Firefox'

# Memory usage by browser
print('Browser memory usage')
memory_browser_df = memory_df.groupby('Browser').sum()
print(memory_browser_df)

# Plot memory usage
memory_browser_df.plot(kind='bar')
plt.show()
