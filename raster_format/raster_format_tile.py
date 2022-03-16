# Create tiles from raster image
#
# Determine dimension of a raster and create n by m tiles
#
# Kristof Ostir, 2016-12-12
# University of Ljubljana, Faculty of Civil and Geodetic Engeenering
# (c) 2016

# Imports
from __future__ import print_function
import os
from datetime import datetime

from osgeo import gdal

# Parameters
tile_size = 3000  # tile size in pixels

# Infile
# raster_file = "/Users/Kristof/Documents/Zacasno/SatelliteData/Sentinel/S2A_MSIL2A_V20160206T100203_20160206T202544_20m/S2A_OPER_MSI_L2A_20160206T202544_R122_V20160206T100203__ms_p2atm_gk.tif"
raster_file = "D:/GeoData/Sentinel/s2/S2A_MSIL2A_V20160107T101243_20160107T200822_20m/S2A_OPER_MSI_L2A_20160107T200822_R122_V20160107T101243__ms_p2atm_gk.tif"
raster_tiles = "D:/GeoData/Sentinel/tiles/"
# raster_tiles = "/Users/Kristof/Documents/Zacasno/SatelliteData/Sentinel/tiles/"

# Start processing
total_start = datetime.now()
print("Creating tiles")
raster_file_name = raster_file.split("/")[-1]
print(raster_file_name)

# Read raster
raster = gdal.Open(raster_file)

# File parameters
cols = raster.RasterXSize
rows = raster.RasterYSize
geoinformation = raster.GetGeoTransform()

top_left_x = geoinformation[0]
top_left_y = geoinformation[3]
res = geoinformation[1]

# Tile parameters
tiles_x = range(0, cols, tile_size)
tiles_y = range(0, rows, tile_size)

# Tile root filename
tile_file_root = raster_tiles + raster_file_name[:-4]

# Tile file
for i, x in enumerate(tiles_x):
    for j, y in enumerate(tiles_y):
        tile_file = tile_file_root + "_" + str(i) + "_" + str(j) + ".tif"
        print("Creating tile: %s %s" % (i, j))
        x_min = i * tile_size
        y_min = j * tile_size
        x_tile = tile_size if x_min + tile_size < cols else cols - x_min
        y_tile = tile_size if y_min + tile_size < rows else rows - y_min
        translate = "gdal_translate -srcwin %s %s %s %s %s %s" % (
            x_min,
            y_min,
            x_tile,
            y_tile,
            raster_file,
            tile_file,
        )
        os.system(translate)

raster = None
raster_tile = None

# End processing
total_time = datetime.now() - total_start
print("\nTotal processing time: " + str(total_time))
