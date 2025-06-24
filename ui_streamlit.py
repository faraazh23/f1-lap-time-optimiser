#UI
import streamlit as st
from utils import simulate_lap, export_telemetry
import pandas as pd

st.title("🏎️ F1 Lap Time Optimiser")

ers_energy = st.slider("ERS Energy Budget (MJ)", 1.0, 5.0, 4.0)
tyre_health = st.slider("Initial Tyre Health", 0.7, 1.0, 0.95)
drs_boost = st.slider("DRS Speed Boost (%)", 0.01, 5.0, 3.0) / 100.0

segments = [
    {"type": "straight", "base_time": 2.5, "drs_zone": True},
    {"type": "corner", "base_time": 3.2, "drs_zone": False},
    {"type": "straight", "base_time": 1.8, "drs_zone": True},
    {"type": "corner", "base_time": 2.9, "drs_zone": False},
    {"type": "straight", "base_time": 2.0, "drs_zone": False},
]

lap_data, total_time = simulate_lap(segments, ers_energy, tyre_health, drs_boost)
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"data/lap_telemetry_{timestamp}.csv"
export_telemetry(lap_data, filename)

st.metric(label="Total Lap Time", value=f"{total_time:.2f} seconds")

df = pd.DataFrame(lap_data)
st.dataframe(df)

st.line_chart(df.set_index("segment")["time"])