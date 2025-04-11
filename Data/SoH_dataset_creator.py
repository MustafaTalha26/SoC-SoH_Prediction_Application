import scipy.io
import numpy as np
import pandas as pd
from datetime import datetime
import os

def convert_to_time(hmm):
    return datetime(year=int(hmm[0]), month=int(hmm[1]), day=int(hmm[2]),
                    hour=int(hmm[3]), minute=int(hmm[4]), second=int(hmm[5]))

def summarize(arr):
    return {
        'mean': np.mean(arr),
        'std': np.std(arr),
        'min': np.min(arr),
        'max': np.max(arr)
    }

def load_discharge_cycles(matfile):
    data = scipy.io.loadmat(matfile)

    filename = os.path.splitext(os.path.basename(matfile))[0]
    cycles = data[filename][0][0][0][0]

    battery_id = filename
    discharge_data = []

    for i, cycle in enumerate(cycles):
        cycle_type = str(cycle[0][0])
        if cycle_type != 'discharge':
            continue
        
        temp = int(cycle[1][0][0]) 
        data_dict = cycle[3][0][0]

        try:
            voltage = data_dict['Voltage_measured'][0]
            current = data_dict['Current_measured'][0]
            temperature = data_dict['Temperature_measured'][0]
            current_load = data_dict['Current_load'][0]
            voltage_load = data_dict['Voltage_load'][0]
            time_array = data_dict['Time'][0]
            capacity = float(data_dict['Capacity'][0][0])
        except:
            continue  # skip bad cycles

        voltage_stats = summarize(voltage)
        current_stats = summarize(current)
        temp_stats = summarize(temperature)
        charge_current_stats = summarize(current_load)
        charge_voltage_stats = summarize(voltage_load)
        duration = time_array[-1] - time_array[0]

        discharge_data.append({
            'battery_id': battery_id,
            'cycle': i,
            'ambient_temperature': temp,
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
            'capacity': capacity,
        })
    return discharge_data


# Process files
files = ["B0005.mat", "B0006.mat", "B0018.mat"]
all_discharge = []

for file in files:
    all_discharge.extend(load_discharge_cycles(file))

# Create DataFrame
df = pd.DataFrame(all_discharge)

# Print DataFrame to ensure 'battery_id' is present
print("DataFrame before sorting:")
print(df.head())

# Check if 'battery_id' column exists
if 'battery_id' not in df.columns:
    print("ERROR: 'battery_id' column is missing!")
else:
    # Sort by 'battery_id' and 'cycle'
    df.sort_values(by=['battery_id', 'cycle'], inplace=True)

    # Compute SoH
    initial_capacities = df.groupby('battery_id')['capacity'].first().to_dict()
    df['soh'] = df.apply(lambda row: (row['capacity'] / initial_capacities[row['battery_id']]) * 100, axis=1)

    # Save to CSV
    df.to_csv("soh_dataset.csv", index=False)
    print("✅ soh_dataset.csv created with additional features.")