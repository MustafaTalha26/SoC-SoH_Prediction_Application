import pandas as pd
import numpy as np
from keras import models, layers
import joblib
import numpy as np
import pandas as pd

SOH_DIM = 14

def summarize(arr):
    return {
        'mean': np.mean(arr),
        'std': np.std(arr),
        'min': np.min(arr),
        'max': np.max(arr)
    }

def json2pandas(json_data):
    discharge_data = []
    for i, cycle in enumerate(json_data):
        data_dict = cycle["data"]
        try:
            voltage = data_dict['Voltage_measured']
            current = data_dict['Current_measured']
            temperature = data_dict['Temperature_measured']
            current_load = data_dict['Current_load']
            voltage_load = data_dict['Voltage_load']
            time_array = data_dict['Time']
            capacity = float(data_dict['Capacity'])
        except:
            continue  # skip bad cycles

        voltage_stats = summarize(voltage)
        current_stats = summarize(current)
        temp_stats = summarize(temperature)
        charge_current_stats = summarize(current_load)
        charge_voltage_stats = summarize(voltage_load)
        duration = time_array[-1] - time_array[0]
        discharge_data.append({
            'voltage_mean': voltage_stats['mean'],
            'voltage_std': voltage_stats['std'],
            'voltage_min': voltage_stats['min'],
            'voltage_max': voltage_stats['max'],
            'current_mean': current_stats['mean'],
            'current_std': current_stats['std'],
            'current_min': current_stats['min'],
            'current_max': current_stats['max'],
            'temperature_mean': temp_stats['mean'],
            'temperature_std': temp_stats['std'],
            'current_charge_mean': charge_current_stats['mean'],
            'voltage_charge_mean': charge_voltage_stats['mean'],
            'duration': duration,
            'capacity': capacity
        })
    
    df = pd.DataFrame(discharge_data)
    return df

def preProcess(json_data):
   X = json2pandas(json_data)
   print(X)
   scaler = joblib.load('data/soh_minmax_scaler.pkl')
   X_scaled = scaler.transform(X)
   X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
   print(X_scaled)
   return X_scaled

def getModel():
    model = models.Sequential([
        layers.InputLayer(input_shape=(SOH_DIM,)),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1)
    ])
    return model