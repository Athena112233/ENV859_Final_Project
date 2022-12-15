import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
import geopandas as gpd
import numpy as np
import pandas as pd
import sys, os
import preprocess_data
import pickle
from simpledbf import Dbf5
import arcpy

def build_model(files):
    """
    Description
    
    param files: 
    """
    arcpy.env.workspace = 'sratch'
    arcpy.env.overwriteOutput = True
    save_path = 'scratch/'
    # preprocess data
    obs_path, obs_label, rnd_path, rnd_label = preprocess_data.preprocess_train_data(files)
    
    # read training file
    obs_dbf = Dbf5(save_path + obs_path)
    rnd_dbf = Dbf5(save_path + rnd_path)
    obs_df = obs_dbf.to_dataframe()
    rnd_df = rnd_dbf.to_dataframe()

    # prepare data for training
    obs_df = obs_df.drop(columns = ['brf_obs', 'X', 'Y'])
    rnd_df = rnd_df.drop(columns = ['rand_obs', 'X', 'Y'])
    obs_df['label'] = obs_label
    rnd_df['label'] = rnd_label
    data = pd.concat([obs_df, rnd_df])
    X = data.drop(columns = ['label'])
    Y = data['label']
    
    # build xgboost model
    clf = XGBClassifier(objective= 'binary:logistic')
    parameters = {
        'max_depth': range (2, 5),
        'n_estimators': [40, 60],
        'learning_rate': [0.1, 0.05]
    }
    grid_search = GridSearchCV(
        estimator = clf,
        param_grid = parameters,
        scoring = 'roc_auc',
        n_jobs = 5,
        cv = 5,
        verbose = True)
    
    grid_search.fit(X, Y)
    
    model_path = "xgb_model.pkl"
    pickle.dump(grid_search, open(model_path, "wb"))
    
    
def make_predictions(files):
    arcpy.env.workspace = 'sratch'
    arcpy.env.overwriteOutput = True
    
    # preprocess data
    data, label = preprocess_data.preprocess_eval_data(files)
    dbf = Dbf5(data)
    df = dbf.to_dataframe()
    print(df.columns)
    X = df.drop(columns = ['prediction', 'X', 'Y'])
    
    # load pre-trained model
    model = pickle.load(open('../../scratch/xgb_model.pkl', 'rb'))
    predictions = model.predict(X)
    
    # Set local variables
    df['habitat_prediction'] = predictions
    
    # convert pd to gdf
    final_gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.X, df.Y))
    
    # save gpd as shp
    final_gdf.to_file('final_predictions.shp')
    

files = ['V:\\ENV859_Final_Project_al512\\data\\bathy',
         'V:\\ENV859_Final_Project_al512\\data\\habras10_1', 
         'V:\\ENV859_Final_Project_al512\\data\\habras10_2', 
         'V:\\ENV859_Final_Project_al512\\data\\habras10_3', 
         'V:\\ENV859_Final_Project_al512\\data\\habras10_4', 
         'V:\\ENV859_Final_Project_al512\\data\\habras10_5',
         'V:\\ENV859_Final_Project_al512\\data\\habras10_6',
         'V:\\ENV859_Final_Project_al512\\data\\habras10_7',
         'V:\\ENV859_Final_Project_al512\\data\\habras10_8', 
         'V:\\ENV859_Final_Project_al512\\data\\dist_kelp', 
         'V:\\ENV859_Final_Project_al512\\data\\dist_100m', 
         'V:\\ENV859_Final_Project_al512\\data\\botc10_8ws', '#', '#']

make_predictions(files)
