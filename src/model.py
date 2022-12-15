import xgboost as xgb
from xgboost import XGBClassifier
import numpy as np
import pandas as pd
import sys, os
import preprocess_data
import pickle
import Dbf5

def build_model(files):
    """
    Description
    
    param files: 
    """
    # preprocess data
    obs_path, obs_label, rnd_path, rnd_label = preprocess_data.preprocess_train_data(files)
    
    # read training file
    obs_dbf = Dbf5(obs_path)
    rnd_dbf = Dbf5(rnd_path)
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
        'max_depth': range (2, 10),
        'n_estimators': range(60, 220, 40),
        'learning_rate': [0.1, 0.01, 0.05]
    }
    grid_search = GridSearchCV(
        estimator = clf,
        param_grid = parameters,
        scoring = 'roc_auc',
        n_jobs = 5,
        cv = 5,
        verbose = True)
    grid_search.fit(X, Y)
    
    model_path = "../../scratch/xgb_model.pkl"