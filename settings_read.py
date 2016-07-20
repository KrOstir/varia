# Settings Read
#
# Read settings from text file and assign to variable names
#
#
# Krištof Oštir
# 2016-05-17


from __future__ import print_function

# Read settings file
path = "settings.txt"
try:
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
except:
    print("Missing settings file", path)
    raise

# List of parameters
params = ('d_root', 'd_dem', 'd_out')
# Required parameters
params_r = (True, True, False)

# Read settings file and find parameters
for i, line in enumerate(lines):
    if line[0] != "#":
        for p in params:
            if p in line:
                exec(line)

# Check if required parameters are present
for i, p in enumerate(params):
    try:
        exec(p)
    except NameError:
        if params_r[i]:
            print(params[i], 'not defined but required.')
            raise
        else:
            print(params[i], 'not defined, using "" instead.')
