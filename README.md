# SoH-SoC_Prediction_Application

This is a demo application for SoH and SoC predictions. 
It contains: 
Flask API for backend.
Streamlit for frontend.
MongoDB for database.
And Machine Learning with neural networks.

### To retrain models (Optional):
Models are already trained but if you want to retrain them, you can use the steps below.
download .mat files. (5th title)
https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/

necessary .mat files:
- B0005.mat
- B0006.mat
- B0018.mat

Create .csv files with "Data/"

Transfer .csv files to "Models/"

Use models seperately to create .h5 and .pkl files.

Create "data" file inside "Backend/" after creating it will look like this = "Backend/data/"

Transfer .h5 and .pkl files to "Backend/data/"

### To use the application:

Make sure Docker and MongoDB is working.

go to compose.yaml folder and and use "docker-compose up" command in cmd or prefered terminal.

(http://localhost:8501/)
