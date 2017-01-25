# Prepare raster for processing speed comparision
#
# REad Sentinel-2 data, save in GeoTIFF, Erdas, JPEG 2000, ENVI as
# float and integer
#
# Kristof Ostir, 2017-01-24
# University of Ljubljana, Faculty of Civil and Geodetic Engineering
# (c) 2017

# Imports
import os

# Original file, GeoTIFF, float
raster_original = "D:/GeoData/Sentinel/s2/S2A_MSIL2A_V20160107T101243_20160107T200822_20m/S2A_OPER_MSI_L2A_20160107T200822_R122_V20160107T101243__ms_p2atm_gk.tif"
# Output
raster_conv = "D:/GeoData/Sentinel/format/"
raster_conv_name = raster_conv + "s2_20160107"
raster_conv_name_float = raster_conv_name + "_gtiff_float.tif"
raster_conv_name_int = raster_conv_name + "_gtiff_int.tif"
gdal_tr = "gdal_translate -a_srs EPSG:3912 -of %s %s %s"
gdal_tr_int = "gdal_translate -a_srs EPSG:3912 -ot Int16 -of %s %s %s"
gdal_calc = "gdal_calc -A %s --A_band=%s --outfile=%s --calc=\"A*1000\""

# Float
# Copy original GeoTiff
translate = gdal_tr % ("GTiff", raster_original, raster_conv_name_float)
os.system(translate)
# Create Erdas Imagine float
translate = gdal_tr % ("HFA", raster_original, raster_conv_name + "_img_float.img")
os.system(translate)
# Create ENVI float
translate = gdal_tr % ("ENVI", raster_original, raster_conv_name + "_envi_float")
os.system(translate)

# Convert to integer, multiply by 1000
results = []
for i in range(1, 11):
    print(i, end=".")
    out_fn = "D:/GeoData/Sentinel/format/" + "raster_%s.tif" % i
    results.append(out_fn)
    calc = gdal_calc % (raster_conv_name_float, i, out_fn)
    os.system(calc)
print()
# Merge
merge_fn = ' '.join(str(e) for e in results)
merge_result = "D:/GeoData/Sentinel/format/raster.tif"
gdal_merge = "gdal_merge -separate -of GTiff -o %s %s" % (merge_result, merge_fn)
os.system(gdal_merge)

# Copy int GeoTiff
translate = gdal_tr_int % ("GTiff", merge_result, raster_conv_name_int)
os.system(translate)

# Delete temp files
for fn in results:
    os.remove(fn)
os.remove(merge_result)

# Int
# Create Erdas Imagine int
translate = gdal_tr % ("HFA", raster_conv_name_int, raster_conv_name + "_img_int.img")
os.system(translate)
# Create ENVI int
translate = gdal_tr % ("ENVI", raster_conv_name_int, raster_conv_name + "_envi_int")
os.system(translate)
# Create JPEG2000 int
translate = gdal_tr % ("JP2OpenJPEG", raster_conv_name_int, raster_conv_name + "_jpeg2000_int.jp2")
os.system(translate)
