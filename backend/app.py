from flask import Flask, jsonify
import requests

app = Flask(__name__)

FIRMS_URL = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/viirs_snpp_global_24h.json"

@app.route('/fetch-firms', methods=['GET'])
def fetch_firms():
    try:
        response = requests.get(FIRMS_URL)
        data = response.json()

        # Extract more meaningful subset
        simplified_data = [
            {
                "latitude": entry["latitude"],
                "longitude": entry["longitude"],
                "brightness": entry["brightness"],
                "confidence": entry["confidence"]
            }
            for entry in data
        ]

        return jsonify({
            "count": len(simplified_data),
            "fires": simplified_data
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
