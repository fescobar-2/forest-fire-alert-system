from flask import Flask, jsonify
import requests
import pandas as pd
from io import StringIO

app = Flask(__name__)

API_KEY = "cbae442f3a983932ea8938d9b2a76acc"
URL = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{API_KEY}/VIIRS_NOAA20_NRT/-62.65,-27.6,-54.25,-19.3/1"

@app.route("/")
def home():
    return {"message": "Backend is running"}

@app.route("/fires", methods=["GET"])
def get_fires():
    try:
        response = requests.get(URL)
        response.raise_for_status()

        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)

        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify([])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
