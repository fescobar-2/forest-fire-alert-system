import streamlit as st
import requests
import pandas as pd
from io import StringIO
import pydeck as pdk

# CONFIG
API_KEY = "cbae442f3a983932ea8938d9b2a76acc"  # Replace with your actual MAP_KEY
SENSOR = "ALL"          # Can be changed by dropdown
# URL = f"https://firms.modaps.eosdis.nasa.gov/api/data_availability/csv/{API_KEY}/{SENSOR}"
URL = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{API_KEY}/VIIRS_NOAA20_NRT/-62.65,-27.6,-54.25,-19.3/1"
# URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/{API_KEY}/VIIRS_NOAA20_NRT/Paraguay/1"

st.title("🔥 FIRMS Data Availability Viewer")
st.write(f"Sensor selected: **{SENSOR}**")

# Fetch the CSV data
try:
    response = requests.get(URL)
    response.raise_for_status()

    # Parse CSV into DataFrame
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)

    st.success("Data fetched successfully!")
    st.write("### Available Data by Country and Date")
    st.dataframe(df)
    st.subheader("🔥 Fire Intensity Map (by Brightness)")

    if not df.empty:
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state=pdk.ViewState(
                latitude=df["latitude"].mean(),
                longitude=df["longitude"].mean(),
                zoom=5,
                pitch=40,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position='[longitude, latitude]',
                    get_fill_color='[255, brightness - 250, 0, 160]',
                    get_radius=10000,
                    pickable=True,
                ),
            ],
        ))


except requests.HTTPError as err:
    st.error(f"HTTP Error: {err}")
except Exception as e:
    st.error(f"Something went wrong: {e}")
