import soh_model_predict
import soc_charge_model_predict
import soc_discharge_model_predict

from flask import app, render_template, Flask, request, jsonify

from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://mongodb:27017/")
db = client["battery_db"]  
soh_collection = db["soh_discharge"]
soc_charge_collection = db["soc_charge"]
soc_discharge_collection = db["soc_discharge"]


app = Flask(__name__)

soh_model = soh_model_predict.getModel()
soc_charge_model = soc_charge_model_predict.getModel()
soc_discharge_model = soc_discharge_model_predict.getModel()

@app.route('/')
def index():
    return "Battery Cycle Processor API"

@app.route('/upload_soh_cycle', methods=['POST'])
def upload_discharge_soh():
    try:
        data = request.get_json()

        # Filter only discharge cycles
        discharge_cycles = [cycle for cycle in data if cycle.get("type") == "discharge"]
        X_ready = soh_model_predict.preProcess(discharge_cycles)
        predictions = soh_model.predict(X_ready)

        soh_collection.insert_one({
            "input": discharge_cycles,
            "predictions": predictions.tolist()
        })

        return jsonify({
            "message": "Discharge data predicted successfully",
            "predictions": predictions.tolist()
        })

    except Exception as e:
        return jsonify({"Error: ": str(e)}), 500
    
@app.route('/upload_soc_charge_cycle', methods=['POST'])
def upload_charge_soc():
    try:
        data = request.get_json()

        # Filter only charge cycles
        charge_cycles = [cycle for cycle in data if cycle.get("type") == "charge"]
        X_ready = soc_charge_model_predict.preProcess(charge_cycles)
        predictions = soc_charge_model.predict(X_ready)

        soc_charge_collection.insert_one({
            "input": charge_cycles,
            "predictions": predictions.tolist()
        })

        return jsonify({
            "message": "SoC scores",
            "predictions": predictions.tolist()
        })

    except Exception as e:
        return jsonify({"Error: ": str(e)}), 500
    
@app.route('/upload_soc_discharge_cycle', methods=['POST'])
def upload_discharge_soc():
    try:
        data = request.get_json()

        # Filter only charge cycles
        discharge_cycles = [cycle for cycle in data if cycle.get("type") == "discharge"]
        X_ready = soc_discharge_model_predict.preProcess(discharge_cycles)
        predictions = soc_discharge_model.predict(X_ready)

        soc_discharge_collection.insert_one({
            "input": discharge_cycles,
            "predictions": predictions.tolist()
        })

        return jsonify({
            "message": "SoC scores",
            "predictions": predictions.tolist()
        })

    except Exception as e:
        return jsonify({"Error: ": str(e)}), 500
    
if __name__ == "__main__":
    soh_model.load_weights('data/soh_weights.h5')
    print("SoH model loaded")
    soc_charge_model.load_weights('data/soc_charge_weights.h5')
    print("SoC Charge model loaded")
    soc_discharge_model.load_weights('data/soc_discharge_weights.h5')
    print("SoC Discharge model loaded")
    app.run(debug=True, host="0.0.0.0", port=5000)