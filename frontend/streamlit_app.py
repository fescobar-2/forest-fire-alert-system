import streamlit as st
import requests

st.title("🌲 Forest Fire Alert Dashboard")

url = "http://127.0.0.1:5000/fetch-firms"

st.write("Fetching data from backend...")

try:
    response = requests.get(url)
    data = response.json()

    if "error" in data:
        st.error(f"Error from backend: {data['error']}")
    else:
        st.success(f"Fetched {data['count']} fire points")
        st.json(data["sample"])

except Exception as e:
    st.error(f"Failed to fetch data: {e}")
