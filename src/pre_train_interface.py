import sys
import os
import arcpy
import arcpy
import model

# define env
arcpy.env.workspace = "../data"
arcpy.env.overwriteOutput = True

# allow up to 15 user inputs
file_paths = []

for i in range(17):
    # obs_shp, rnd_shp, raster1, raster2,...
    file_paths.append(sys.argv[i])
 
# dispaly message
arcpy.AddMessage(file_paths)
arcpy.AddMessage('Please take a screen shot of the message above. Habitat prediction \
                 generation requires input in the same order.')

# call model building
model(file_paths)
