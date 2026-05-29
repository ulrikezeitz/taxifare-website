import streamlit as st
import requests
from streamlit_folium import st_folium
import folium
from datetime import datetime
import time


# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Taxi Fare Predictor",
    page_icon="🚕",
    layout="centered"
)

# --- INSTAGRAM STYLE ---
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #fdf497 0%, #fdf497 5%, #fd5949 45%, #d6249f 60%, #285AEB 90%);
    color: white;
}
div.stButton > button {
    background-color: #d6249f;
    color: white;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    border: none;
    font-weight: bold;
}
div.stButton > button:hover {
    background-color: #fd5949;
}
.block-container {
    backdrop-filter: blur(12px);
    background: rgba(255,255,255,0.15);
    padding: 2rem;
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.markdown("<h1 style='text-align:center; color:white;'>🚕 Taxi Fare Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Im Instagram‑Look mit interaktiver Karten‑Auswahl</p>", unsafe_allow_html=True)

# --- DATE & TIME ---
ride_datetime = st.datetime_input("📅 Datum & Uhrzeit der Fahrt", datetime.now())

# --- MAPS ---
st.subheader("📍 Pickup & Dropoff auswählen")

# Default NYC center
m = folium.Map(location=[40.75, -73.98], zoom_start=12)

# Add markers dynamically
pickup_marker = folium.Marker(
    location=[40.75, -73.98],
    popup="Pickup",
    draggable=True,
    icon=folium.Icon(color="green", icon="play", prefix="fa")
)

dropoff_marker = folium.Marker(
    location=[40.76, -73.99],
    popup="Dropoff",
    draggable=True,
    icon=folium.Icon(color="red", icon="flag-checkered", prefix="fa")
)


pickup_marker.add_to(m)
dropoff_marker.add_to(m)

map_data = st_folium(m, height=400, width=700)

# Extract coordinates
pickup_lat = map_data["last_object_clicked"]["lat"] if map_data["last_object_clicked"] else 40.75
pickup_lon = map_data["last_object_clicked"]["lng"] if map_data["last_object_clicked"] else -73.98

dropoff_lat = map_data["last_object_clicked"]["lat"] if map_data["last_object_clicked"] else 40.76
dropoff_lon = map_data["last_object_clicked"]["lng"] if map_data["last_object_clicked"] else -73.99

# --- PASSENGERS ---
passenger_count = st.slider("👥 Anzahl Passagiere", 1, 6, 1)

# --- API CALL ---
if st.button("💸 Vorhersage berechnen"):
    progress = st.progress(0)
    status = st.empty()
    status.write("Starte Anfrage...")

    for i in range(30):
        progress.progress(i / 30)
        time.sleep(0.05)
    progress.progress(1.0)          # Balken auf 100%
    status.write("Anfrage beendet") # Text aktualisieren

    url = "https://taxifareapi-1091606282523.europe-west1.run.app/predict"

    params = {
        "pickup_datetime": ride_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passenger_count
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        prediction = response.json().get("fare", "Keine Vorhersage erhalten")
        st.success(f"💰 Geschätzter Fahrpreis: **${prediction:.2f}**")
    else:
        st.error("❌ Fehler beim Abrufen der Vorhersage")
