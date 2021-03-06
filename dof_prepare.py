# Select DOF images from list QGIS Virtual Raster
#
# Query VRT file, find all images, copy images to folder
#
# Krištof Oštir
# 2016-08-26

# Load libraries
import os
import fnmatch
import time
from shutil import copy2

# Find all images to be processed
def dof_querry_vrt(vrt_file):
    fhand = open(vrt_file)
    dofs = list()
    for line in fhand:
        line = line.strip()
        if not line.startswith(vrt_tag):
            continue
        dof_num = line[len(vrt_tag) : len(vrt_tag) + 5]
        dofs.append(dof_num)
    return dofs


# Find all availabe images
def dof_querry(dof_folder):
    dofs_all = list()
    for root, dirnames, filenames in os.walk(dof_folder):
        for filename in fnmatch.filter(filenames, "*.tif"):
            dofs_all.append(os.path.join(root, filename))
    return dofs_all


# Start processing images
start = time.time()
print("\nSelect DOF images from list QGIS Virtual Raster")

# Processing parameters
# VRT file
vrt_fn = "/Users/Kristof/Documents/Python/Varia/dof_prepare.vrt"
# Filename location
vrt_tag = '<SourceFilename relativeToVRT="1">'
# Original file location
# dof_orig = '/Volumes/arhiv_gurs/DOF/DOF_2015_050/'
dof_orig = "/Volumes/arhiv_gurs/DOF/DOF_2015_050_IR/"
# Resulting file location
# dof_res = '/Users/Kristof/Documents/Zacasno/QGISTraining/data_slo/DOF'
dof_res = "/Users/Kristof/Documents/Zacasno/QGISTraining/data_slo/DOF_IR"

# Find list of files to be processed
dof_to_list = dof_querry_vrt(vrt_fn)
dof_to_list_len = len(dof_to_list)
print("%d DOFs to be extracted" % dof_to_list_len)

# Find list of available files
dof_list = dof_querry(dof_orig)

for idx, dof in enumerate(dof_to_list):
    print("Processing %d/%d: %s" % (idx + 1, dof_to_list_len, dof))
    found = False
    for i in dof_list:
        if dof in i:
            copy2(i, dof_res)
            copy2(os.path.splitext(i)[0] + ".tfw", dof_res)
            found = True
    if not found:
        print(dof, "not available in", dof_orig)

# End
print("\nFinished")
end = time.time()
time_min = (end - start) // 60
time_sec = (end - start) % 60
print("Time elapsed      : %i:%02i" % (time_min, time_sec))
