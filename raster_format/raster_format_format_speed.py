# Compare raster reading and processing speed
#
# GeoTIFF, JPEG2000 and Erdas Imagine file formats are processed.
# Image is opened, NDVI is computed and written to file.
#
# Kristof Ostir, 2017-01-13
# University of Ljubljana, Faculty of Civil and Geodetic Engeenering
# (c) 2017

from __future__ import print_function
import os
import numpy as np
from osgeo import gdal, gdal_array
from fnmatch import fnmatch
from glob import glob
import pandas as pd
import math
from scipy.ndimage.interpolation import zoom
from datetime import datetime

# Files
fn_geotiff_f = "D:/GeoData/Sentinel/format/S2A_OPER_MSI_L2A_20160107.tif"
fn_geotiff = "D:/GeoData/Sentinel/format/S2A_OPER_MSI_L2A_20160107_i.tif"
# JPEG2000 ni podprt v gdal.Open()
# fn_jpg2000 = "D:/GeoData/Sentinel/format/S2A_OPER_MSI_L2A_20160107_j.jp2"
fn_erdas = "D:/GeoData/Sentinel/format/S2A_OPER_MSI_L2A_20160107_e.img"
fn_erdas_f = "D:/GeoData/Sentinel/format/S2A_OPER_MSI_L2A_20160107_f.img"

files = [["GeoTIFF float", fn_geotiff_f],
         ["GeoTIFF int", fn_geotiff],
         ["GeoTIFF Erdas", fn_erdas],
         ["GeoTIFF Erdas float", fn_erdas_f]]

# Band numbers
b_red = 3
b_nir = 7

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


def save_geotiff(band, path, geo_info=None, proj_info=None, type="Byte", bits=None):
    """
    Wrapper function for saving geotiff images

    :param array: numpy array with image that will be written to disk
    :param path: destination + filename of the image
    :param geo_info: GeoTransform information about image
    :param proj_info: Projection information about the image
    :param type: pixel type of saved image
    :param bits: number of bits per image pixel
    :return: nothing
    """

    # Additional image creation options
    options = ["COMPRESS=LZW"]
    if bits > 0:
        options.extend(["NBITS="+str(bits)])
    gtif_out = gdal.GetDriverByName("GTiff").Create(path, band.shape[1], band.shape[0], 1, getattr(gdal, "GDT_"+type), options)
    gtif_out.GetRasterBand(1).WriteArray(band)  # can return "ERROR 1: TIFFReadDirectory:Cannot handle zero scanline size", but still works
    # OR version without any additional options
    # gtif_out = gdal_array.SaveArray(band, path, format="GTiff")

    # Add geolocation and projection information
    if geo_info is not None:
        gtif_out.SetGeoTransform(geo_info)
    if proj_info is not None:
        gtif_out.SetProjection(proj_info)
    # Close and save image
    gtif_out = None

# Main program
print("Compare raster reading and processing speed")

# Process files
for f in files:
    print("\nProcessing %s" % (f[0]))
    process_start = datetime.now()
    im_in = f[1]
    im_in_name = os.path.splitext(os.path.abspath(im_in))[0]
    im_file = gdal.Open(im_in)
    # Get geolocation of ul coordinate of ul pixel
    im_geoinfo = list(im_file.GetGeoTransform())  # convert returned tuple to list to be able to assign values to items
    #  Get image projection informations
    im_proj = im_file.GetProjection()
    print("Computing NDVI ...")
    im_red = np.array(im_file.GetRasterBand(b_red).ReadAsArray())
    im_nir = np.array(im_file.GetRasterBand(b_nir).ReadAsArray())
    im_ndvi = ndvi(im_nir, im_red)
    # Write output
    print("Writing results ...")
    im_out = im_in_name + "_ndvi.tif"
    save_geotiff(im_ndvi.astype(np.float), im_out, im_geoinfo, im_proj)
    process_time = datetime.now() - process_start
    print("Processing time: " + str(process_time))
