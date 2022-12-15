import arcpy
import xgboost as xgb
import numpy as np
import geopadas as gpd
import pandas as pd
import sys, os
import preprocess_data


def model(files):
    """
    """
    obs_path, obs_label, rnd_path, rnd_label = preprocess_data(files)
    