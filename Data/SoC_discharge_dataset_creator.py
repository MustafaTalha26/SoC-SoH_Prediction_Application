import scipy.io
import numpy as np
import pandas as pd
import os

def load_discharge_instances_with_soc(matfile):
    data = scipy.io.loadmat(matfile)
    filename = os.path.splitext(os.path.basename(matfile))[0]
    cycles = data[filename][0][0][0][0]

    battery_id = filename
    all_instances = []

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
            capacity = float(data_dict['Capacity'][0][0])  # Ahr
        except:
            continue  # skip bad cycles

        # Coulomb counting: SoC starts at 100%, decrease over time
        dt = np.diff(time_array, prepend=time_array[0])  # time steps (sec)
        current_abs = np.abs(current)  # ensure current is positive (discharge)
        delta_Ah = current_abs * dt / 3600  # current (A) * time (s) = charge (As) → convert to Ah
        used_capacity = np.cumsum(delta_Ah)
        soc = (1 - used_capacity / capacity) * 100  # in %

        for j in range(len(time_array)):
            all_instances.append({
                'battery_id': battery_id,
                'cycle': i,
                'instance': j,
                'time': time_array[j],
                'voltage': voltage[j],
                'current': current[j],
                'temperature': temperature[j],
                'voltage_load': voltage_load[j],
                'current_load':  current_load[j],
                'ambient_temperature': temp,
                'soc': soc[j]
            })

    return all_instances

# Load all files
files = ["B0005.mat", "B0006.mat", "B0018.mat"]
all_data = []

for file in files:
    all_data.extend(load_discharge_instances_with_soc(file))

# Create DataFrame
df_soc = pd.DataFrame(all_data)

# Save
df_soc.to_csv("soc_discharge_dataset.csv", index=False)
print("✅ soc_discharge_dataset.csv created with per-instance SoC values.")
