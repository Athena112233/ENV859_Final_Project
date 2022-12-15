# ENV859_Final_Project
In this final project, I created a blue rockfish habitat prediction tool using ArcGIS and Xgboost. The model can intake points containing enviornmental information, and predict if a blue rockfish is likely to exist in this point. This project is contained in both argis interface, python scripts, and jupyter notebook. The recommended way of running this project is to run the jupyter notebook located in the notebook folder, then add the final_predictions.shp feature class to ArcGIS. 

# Worksapce Setup Instruction
### Install Dependencies
The project depends on a ArcGIS environment. The user must have ArcGIS installed and have a valid license.
Other dependecies include:

pandas
xgboost
geopandas 
torch
simpledbf
scikit-learn

Please create a virutal environment with ArcGIS. Then, run 'pip install requirements.txt' to install dependencies at once.

### Required Input Files
1. brf_obs.shp: shape file containing points that a blue rockfish was observed.
2. rand_obs.shp: shape file containing randomly generated points across the region of analysis where blue rockfish was not observed. 
3. environmental raster layers of your choice.

This tool would accept up to 15 layers of environmental raster files. 

# Geospatial Tool
### User Manual
1. ArcGIS User Interface:
Ideally, the users can train and make predictions by running the tool "Select Model Training Files" and "Select Model Testing Files" lcoated in the ArcGIS toolbook. However, ArcGIS would crash when running the xgboost model. Thus, this is not the preferred way of running this project.

2. Python Scripts:
All training, testing, data preprocessing methods used in this project were functionalized. Users can feel free to call methods defined in the python files listed in the src folder and use them appropriately. 

3. Jupyter Notebook:
This notebook contains the completed training and prediction pipeline. Users can train and make predictions by running the training_pipeline.ipynb file located in notebook. Outputs will be saved to the scratch folder in your ArcGIS workspace. 

# Data Analytic Pipeline
This project follows this pipeline:
(obs_points, rnd_point, rasters) --> data preprocess --> build_model --> pre-trained model
(rasters, pre-trained model) --> data preprocess --> make_predictions --> final_predictions.shp

### Data Preprocessing
1. Data Preprocessing for Data Training
The pipeline preprocess the data by sampling the raster layers with the observed points and random points. For each point, we extracted the environmental information using Arcpy Sample. The samples points from observed and random will be combined into a single dataframe for model training.

2. Data Preprocessing for Predictions
The pipeline would randomly generated 300 points within the raster layer's boundary. Using the 300 newly genereted random points, we sample the input raster layers using Arcpy Sample again to extract environmetal information. Unfortunately, this tool cannot make prediction on the entire raster layer's region. However, if the user creates enough random datapoints that represent the overall raster region, the predictions could be insightful. 

### Training/Validating/Testing
### Model Packaging
### Output Results
