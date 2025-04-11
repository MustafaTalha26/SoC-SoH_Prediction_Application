import streamlit as st
import requests
import json
from datetime import datetime

st.title("Battery Cycle Data Uploader")

API_BASE = "http://backend:5000"

def prepare_time_input(key_prefix=""):
    date = st.date_input("Tarih", key=f"{key_prefix}_date")
    time = st.time_input("Saat", key=f"{key_prefix}_time")
    dt = datetime.combine(date, time)
    return [dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second]

def prepare_soh_inputs(key_prefix=""):
    st.write("Örnek veri girişleri:")
    Voltage_measured = st.text_input("Voltage_measured (virgülle ayır)", "4.2, 4.0, 3.7, 3.4", key=f"{key_prefix}_Voltage")
    Current_measured = st.text_input("Current_measured (virgülle ayır)", "1.5, 1.4, 1.3, 1.2", key=f"{key_prefix}_Current")
    Temperature_measured = st.text_input("Temperature_measured (virgülle ayır)", "30, 31, 32, 33", key=f"{key_prefix}_Temp")
    Current_load = st.text_input("Current_load (virgülle ayır)", "0.5, 0.5, 0.5, 0.5", key=f"{key_prefix}_CLoad")
    Voltage_load = st.text_input("Voltage_load (virgülle ayır)", "4.2, 4.1, 4.0, 3.9", key=f"{key_prefix}_VLoad")
    Time_arr = st.text_input("Time (ms, virgülle ayır)", "0, 1000, 2000, 3000", key=f"{key_prefix}_Time")
    Capacity = st.number_input("Capacity (Ah)", value=2.4, key=f"{key_prefix}_Capacity")

    data = {
        "Voltage_measured": list(map(float, Voltage_measured.split(","))),
        "Current_measured": list(map(float, Current_measured.split(","))),
        "Temperature_measured": list(map(float, Temperature_measured.split(","))),
        "Current_load": list(map(float, Current_load.split(","))),
        "Voltage_load": list(map(float, Voltage_load.split(","))),
        "Time": list(map(int, Time_arr.split(","))),
        "Capacity": Capacity
    }
    return data

def prepare_soc_charge_inputs(key_prefix):
    st.write("Örnek veri girişleri:")
    Voltage_measured = st.text_input("Voltage_measured (virgülle ayır)", "4.0, 4.0, 4.0, 4.0", key=f"{key_prefix}_Voltage")
    Current_measured = st.text_input("Current_measured (virgülle ayır)", "1.5, 1.5, 1.5, 1.5", key=f"{key_prefix}_Current")
    Temperature_measured = st.text_input("Temperature_measured (virgülle ayır)", "24.5, 24.5, 24.5, 24.5", key=f"{key_prefix}_Temp")
    Current_load = st.text_input("Current_charge (virgülle ayır)", "1.5, 1.5, 1.5, 1.5", key=f"{key_prefix}_CLoad")
    Voltage_load = st.text_input("Voltage_charge (virgülle ayır)", "4.7, 4.7, 4.7, 4.7", key=f"{key_prefix}_VLoad")
    Time_arr = st.text_input("Time (ms, virgülle ayır)", "20, 50, 80, 110", key=f"{key_prefix}_Time")

    data = {
        "Voltage_measured": list(map(float, Voltage_measured.split(","))),
        "Current_measured": list(map(float, Current_measured.split(","))),
        "Temperature_measured": list(map(float, Temperature_measured.split(","))),
        "Current_charge": list(map(float, Current_load.split(","))),
        "Voltage_charge": list(map(float, Voltage_load.split(","))),
        "Time": list(map(int, Time_arr.split(","))),
    }
    return data

def prepare_soc_discharge_inputs(key_prefix):
    st.write("Örnek veri girişleri:")
    Voltage_measured = st.text_input("Voltage_measured (virgülle ayır)", "4.25, 4.24, 4.23, 4.22", key=f"{key_prefix}_Voltage")
    Current_measured = st.text_input("Current_measured (virgülle ayır)", "-1.8, -1.8, -1.8, -1.8", key=f"{key_prefix}_Current")
    Temperature_measured = st.text_input("Temperature_measured (virgülle ayır)", "25.0, 25.0, 25.0, 25.0", key=f"{key_prefix}_Temp")
    Current_load = st.text_input("Current_load (virgülle ayır)", "-1.9, -1.9, -1.9, -1.9", key=f"{key_prefix}_CLoad")
    Voltage_load = st.text_input("Voltage_load (virgülle ayır)", "3.0, 3.0, 3.0, 3.0", key=f"{key_prefix}_VLoad")
    Time_arr = st.text_input("Time (ms, virgülle ayır)", "0, 16, 35, 53", key=f"{key_prefix}_Time")
    Capacity = st.number_input("Capacity (Ah)", value=1.80, key=f"{key_prefix}_Capacity")

    data = {
        "Voltage_measured": list(map(float, Voltage_measured.split(","))),
        "Current_measured": list(map(float, Current_measured.split(","))),
        "Temperature_measured": list(map(float, Temperature_measured.split(","))),
        "Current_load": list(map(float, Current_load.split(","))),
        "Voltage_load": list(map(float, Voltage_load.split(","))),
        "Time": list(map(int, Time_arr.split(","))),
        "Capacity": Capacity
    }
    return data

def send_request(endpoint, payload):
    try:
        response = requests.post(f"{API_BASE}{endpoint}", json=payload)
        if response.status_code == 200:
            st.success("✅ Veri başarıyla gönderildi.")
            st.json(response.json())
        else:
            st.error(f"❌ Hata: {response.status_code}")
            st.text(response.text)
    except Exception as e:
        st.error(f"İstek gönderilirken hata oluştu: {e}")


if "soh_cycles" not in st.session_state:
    st.session_state["soh_cycles"] = []

# Sekmeler: SoH, SoC Charge, SoC Discharge
tab1, tab2, tab3 = st.tabs(["🔋 SoH Cycle", "🔌 SoC Charge Cycle", "🔻 SoC Discharge Cycle"])

with tab1:
    st.header("🔋 SoH Cycle Gönder")
    time = prepare_time_input("soh_discharge")
    data = prepare_soh_inputs("soh_discharge")

    if st.button("Gönder", key="soh"):
        payload = [{
            "type": "discharge",
            "date": time,
            "data": data
        }]
        send_request("/upload_soh_cycle", payload)

with tab2:
    st.header("🔌 SoC Charge Cycle Gönder")
    time = prepare_time_input("soc_charge")
    data = prepare_soc_charge_inputs("soc_charge")

    if st.button("Gönder", key="soc_charge"):
        payload = [{
            "type": "charge",
            "date": time,
            "data": data
        }]
        send_request("/upload_soc_charge_cycle", payload)

with tab3:
    st.header("🔻 SoC Discharge Cycle Gönder")
    time = prepare_time_input("soc_discharge")
    data = prepare_soc_discharge_inputs("soc_discharge")

    if st.button("Gönder", key="soc_discharge"):
        payload = [{
            "type": "discharge",
            "date": time,
            "data": data
        }]
        send_request("/upload_soc_discharge_cycle", payload)