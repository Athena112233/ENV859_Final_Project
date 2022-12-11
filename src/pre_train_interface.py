import sys
import os
import arcpy
import arcpy
# import model building file

# define env
arcpy.env.workspace = "../data"
arcpy.env.overwriteOutput = True

# allow up to 15 user inputs
file_paths = []

target = sys.argv[1]
file_paths.append(target)

for i in range(2, 16):
    file_paths.append(sys.argv[i])
 
# dispaly message
arcpy.AddMessage(file_paths)
arcpy.AddMessage('Please take a screen shot of the message above. Habitat prediction \
                 generation requires input in the same order.')

# call model building
