import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

API_URL = "https://forest-fire-alert-system-v3wp.onrender.com"  # Change this to your Render backend URL when deployed

st.title("Visualizador de datos del satélite FIRMS")

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    df = pd.DataFrame(response.json())

    st.success("Datos obtenidos correctamente desde el backend!")
    st.dataframe(df)
    st.subheader("Mapa de intensidad lumínica (por medida de brillo)")

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

except requests.exceptions.RequestException as err:
    st.error(f"Error al conectarse al backend: {err}")
except Exception as e:
    st.error(f"Ocurrió un error: {e}")
