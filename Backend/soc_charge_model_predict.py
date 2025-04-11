import pandas as pd
import numpy as np
from keras import models, layers
import joblib
import numpy as np
import pandas as pd

SOC_CHARGE_DIM = 6

def json2pandas(json_data):
    charge_data = []
    for i, cycle in enumerate(json_data):
        data_dict = cycle["data"]
        try:
            voltage = data_dict['Voltage_measured']
            current = data_dict['Current_measured']
            temperature = data_dict['Temperature_measured']
            current_charge = data_dict['Current_charge']
            voltage_charge = data_dict['Voltage_charge']
            time_array = data_dict['Time']

            for j in range(len(time_array)):
                charge_data.append({
                    'time': time_array[j],
                    'voltage_measured': voltage[j],
                    'current_measured': current[j],
                    'temperature_measured': temperature[j],
                    'current_charge': current_charge[j],
                    'voltage_charge': voltage_charge[j],
                })

        except Exception as e:
            print(f"⚠️ Skipped a cycle due to error: {e}")
            continue  # skip bad cycles

    df = pd.DataFrame(charge_data)
    return df

def preProcess(json_data):
   X = json2pandas(json_data)
   print(X)
   scaler = joblib.load('data/soc_charge_minmax_scaler.pkl')
   X_scaled = scaler.transform(X)
   X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
   print(X_scaled)
   return X_scaled

def getModel():
    model = models.Sequential([
        layers.InputLayer(input_shape=(SOC_CHARGE_DIM,)),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1)
    ])
    return model