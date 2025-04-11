import scipy.io
import numpy as np
import pandas as pd
import os
from datetime import datetime

def convert_to_time(hmm):
    return datetime(year=int(hmm[0]), month=int(hmm[1]), day=int(hmm[2]),
                    hour=int(hmm[3]), minute=int(hmm[4]), second=int(hmm[5]))

def load_charge_cycles(matfile):
    data = scipy.io.loadmat(matfile)
    filename = os.path.splitext(os.path.basename(matfile))[0]
    cycles = data[filename][0][0][0][0]

    battery_id = filename
    charge_data = []

    for i, cycle in enumerate(cycles):
        cycle_type = str(cycle[0][0])
        if cycle_type != 'charge':
            continue

        try:
            temp = int(cycle[1][0][0]) 
            data_dict = cycle[3][0][0]

            voltage = data_dict['Voltage_measured'][0]
            current = data_dict['Current_measured'][0]
            temperature = data_dict['Temperature_measured'][0]
            current_charge = data_dict['Current_charge'][0]
            voltage_charge = data_dict['Voltage_charge'][0]
            time_array = data_dict['Time'][0]

            # Δt calculation
            dt = np.diff(time_array, prepend=time_array[0])  # seconds

            # Coulomb counting (A * s) → Ah
            delta_Ah = current_charge * dt / 3600
            charged_Ah = np.cumsum(delta_Ah)

            # Normalize to max = 100%
            soc = (charged_Ah / charged_Ah[-1]) * 100

            for j in range(len(time_array)):
                charge_data.append({
                    'battery_id': battery_id,
                    'cycle': i,
                    'ambient_temperature': temp,
                    'time': time_array[j],
                    'voltage_measured': voltage[j],
                    'current_measured': current[j],
                    'temperature_measured': temperature[j],
                    'current_charge': current_charge[j],
                    'voltage_charge': voltage_charge[j],
                    'soc': soc[j]
                })

        except Exception as e:
            print(f"⚠️ Skipped a cycle due to error: {e}")
            continue

    return charge_data


# Process charge files
files = ["B0005.mat", "B0006.mat", "B0018.mat"]
all_charge = []

for file in files:
    all_charge.extend(load_charge_cycles(file))

# Create DataFrame
df_charge = pd.DataFrame(all_charge)

# Save to CSV
df_charge.to_csv("soc_charge_dataset.csv", index=False)
print("✅ soc_charge_dataset.csv created successfully!")