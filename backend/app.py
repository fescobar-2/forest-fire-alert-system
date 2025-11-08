from flask import Flask, jsonify
import requests
import pandas as pd
from io import StringIO

app = Flask(__name__)

API_KEY = "cbae442f3a983932ea8938d9b2a76acc"
URL = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{API_KEY}/VIIRS_NOAA20_NRT/-62.65,-27.6,-54.25,-19.3/1"


@app.route("/data", methods=["GET"])
def get_fire_data():
    try:
        response = requests.get(URL)
        response.raise_for_status()

        # Handle empty or invalid CSVs
        if not response.text.strip():
            return jsonify([])

        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)

        if df.empty or "latitude" not in df.columns or "longitude" not in df.columns:
            return jsonify([])

        return jsonify(df.to_dict(orient="records"))

    except Exception as e:
        print("Error fetching FIRMS data:", e)
        return jsonify([])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
