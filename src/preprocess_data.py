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
    arcpy.env.workspace = 'data'
    arcpy.env.overwriteOutput = True
    #save_path = '../scratch/'
    
    # gather the shape files
    files = np.array(files)
    obs = files[0]
    rnd = files[1]
    
    # gather the raster files
    rasters = files[2:]
    rasters = list(rasters[rasters != '#'])

    # sample rasters from observed points
    obs_table = 'observed_presence_sampled.dbf'
    obs_points = arcpy.sa.Sample(rasters, obs, obs_table)
    obs_count = int(arcpy.management.GetCount(obs_table)[0])
    obs_label = np.array([1]*obs_count)
    
    # sample rasters from absence points
    rnd_table = 'random_absence_sampled.dbf'
    rnd_points = arcpy.sa.Sample(rasters, rnd, rnd_table)
    rnd_count = int(arcpy.management.GetCount(rnd_table)[0])
    rnd_label = np.array([0]*rnd_count)

    return obs_table, obs_label, rnd_table, rnd_label


def preprocess_eval_data(files):
    # define env
    arcpy.env.workspace = 'scratch'
    arcpy.env.overwriteOutput = True
    
    # gather the raster files
    files = np.array(files)
    rasters = list(files[files != '#'])
    
    # create random points
    points = arcpy.management.CreateRandomPoints('../../scratch', 
                                        'prediction_points',  
                                        constraining_extent = rasters[0], 
                                        number_of_points_or_field = 300)
    
    out_table = '../../scratch/prediction_sampled.dbf'
    out_points = arcpy.sa.Sample(rasters, points, out_table)
    out_count = int(arcpy.management.GetCount(out_table)[0])
    out_label = np.array([1]*out_count)
    
    return out_table, out_label
