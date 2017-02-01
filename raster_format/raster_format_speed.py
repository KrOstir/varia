# Compare raster reading and processing speed
#
# GeoTIFF, JPEG2000, ENVI and Erdas Imagine file formats are processed.
# Image is opened and NDVI is computed.
#
# Kristof Ostir, 2017-01-13
# University of Ljubljana, Faculty of Civil and Geodetic Engeenering
# (c) 2017

import os
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from osgeo import gdal, gdal_array
from datetime import datetime

# Files to process
files = [
    ["D:/GeoData/Sentinel/format/S2A_20160107_envi_float", 3, 7],
    ["D:/GeoData/Sentinel/format/S2A_20160107_envi_int", 3, 7],
    ["D:/GeoData/Sentinel/format/S2A_20160107_gtiff_float.tif", 3, 7],
    ["D:/GeoData/Sentinel/format/S2A_20160107_gtiff_int.tif", 3, 7],
    ["D:/GeoData/Sentinel/format/S2A_20160107_img_float.img", 3, 7],
    ["D:/GeoData/Sentinel/format/S2A_20160107_img_int.img", 3, 7],
    ["D:/GeoData/Sentinel/format/S2A_20160107_jpeg2000_int.jp2", 3, 7],
    ["D:/GeoData/Sentinel/format/S2A_20160814_envi_float", 3, 4],
    ["D:/GeoData/Sentinel/format/S2A_20160814_envi_int", 3, 4],
    ["D:/GeoData/Sentinel/format/S2A_20160814_gtiff_float.tif", 3, 4],
    ["D:/GeoData/Sentinel/format/S2A_20160814_gtiff_int.tif", 3, 4],
    ["D:/GeoData/Sentinel/format/S2A_20160814_img_float.img", 3, 4],
    ["D:/GeoData/Sentinel/format/S2A_20160814_img_int.img", 3, 4],
    ["D:/GeoData/Sentinel/format/S2A_20160814_jpeg2000_int.jp2", 3, 4]
]

# Compute NDVI
def ndvi(nir, red):
    """
    Compute Normalized Differential Vegetation Index

    :param nir: nir band
    :param red: red band
    :return: NDVI
    """
    result = (nir - red) / (nir + red)
    result[~ np.isfinite(result)] = -1.0
    return result


# Main program
print("Compare raster reading and processing speed")

# Process files
for im_in in files:
    name = im_in[0].split("_")
    process_start = datetime.now()
    im_in_name = os.path.splitext(os.path.abspath(im_in[0]))[0]
    if not os.path.exists(im_in[0]):
        print("%s does not exist." % (im_in[0]))
        continue
    im_file = gdal.Open(im_in[0])
    im_proj = im_file.GetProjection()
    im_red = np.array(im_file.GetRasterBand(im_in[1]).ReadAsArray())
    im_nir = np.array(im_file.GetRasterBand(im_in[2]).ReadAsArray())
    im_ndvi = ndvi(im_nir, im_red)
    process_time = datetime.now() - process_start
    print("%s, %s, %s, %s" % (im_in_name, name[-2], name[-1].split(".")[0], str(process_time)))
