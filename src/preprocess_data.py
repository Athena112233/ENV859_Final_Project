import arcpy
import numpy as np
import sys, os
import json
 
def preprocess_train_data(files):
    """
    
    description
    
    param files: 
    """
    
    # set up env
    arcpy.env.workspace = '../../data'
    arcpy.env.overwriteOutput = True
    save_path = '../../scratch/'
    
    # gather the shape files
    files = np.array(files)
    obs = files[0]
    rnd = files[1]
    
    # gather the raster files
    rasters = files[2:]
    rasters = list(rasters[rasters != '#'])

    # sample rasters from observed points
    obs_table = save_path + 'observed_presence_sampled.shp'
    obs_points = arcpy.sa.Sample(rasters, obs, obs_table)
    obs_count = int(arcpy.management.GetCount(obs_table)[0])
    obs_label = np.array([1]*obs_count)
    
    # sample rasters from absence points
    rnd_table = save_path + 'random_absence_sampled.shp'
    rnd_points = arcpy.sa.Sample(rasters, rnd, rnd_table)
    rnd_count = int(arcpy.management.GetCount(rnd_table)[0])
    rnd_label = np.array([0]*rnd_count)

    return obs_table, obs_label, rnd_table, rnd_label


preprocess_train_data(['V:\\ENV859_Final_Project_al512\\data\\brf_obs.shp', 'V:\\ENV859_Final_Project_al512\\data\\rand_obs.shp', 'V:\\ENV859_Final_Project_al512\\data\\bathy', 'V:\\ENV859_Final_Project_al512\\data\\habras10_1', 'V:\\ENV859_Final_Project_al512\\data\\habras10_2', 'V:\\ENV859_Final_Project_al512\\data\\habras10_3', 'V:\\ENV859_Final_Project_al512\\data\\habras10_4', 'V:\\ENV859_Final_Project_al512\\data\\habras10_5', 'V:\\ENV859_Final_Project_al512\\data\\habras10_6', 'V:\\ENV859_Final_Project_al512\\data\\habras10_7', 'V:\\ENV859_Final_Project_al512\\data\\habras10_8', 'V:\\ENV859_Final_Project_al512\\data\\dist_kelp', 'V:\\ENV859_Final_Project_al512\\data\\dist_100m', 'V:\\ENV859_Final_Project_al512\\data\\botc10_8ws', '#', '#'])