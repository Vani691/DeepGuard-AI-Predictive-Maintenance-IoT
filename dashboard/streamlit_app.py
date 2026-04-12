import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import requests
import pandas as pd
import time
import plotly.graph_objects as go
from src.data_simulator import generate_sensor_data
from src.anomaly import detect_anomaly
from src.logger import log_data, init_log
from src.alert_system import send_discord_alert
# --- Futuristic Neon UI Styling ---
st.set_page_config(layout="wide", page_title="DeepGuard Predictor")
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    h1, h2, h3 { color: #00FFCC !important; text-shadow: 0px 0px 10px #00FFCC; }
    .stMetric, .stAlert { border: 1px solid #B026FF; border-radius: 5px; box-shadow: 0 0 15px #B026FF; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ DEEP-GUARD: Jet Engine Telemetry")

init_log()
data_gen = generate_sensor_data()
features = ['s2', 's3', 's4', 's7', 's8', 's9', 's11', 's12', 's13', 's14', 's15', 's17', 's20', 's21']
chart_data = pd.DataFrame(columns=["cycle"] + features)
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📡 Live Stream")
    data_placeholder = st.empty()
    alert_placeholder = st.empty()

with col2:
    st.subheader("🧠 Risk Assessment")
    gauge_placeholder = st.empty()

st.subheader("📉 Advanced Engine Telemetry")

# Create Interactive Tabs
tab1, tab2, tab3 = st.tabs(["🔥 Compressors (Temperature)", "🌪️ Turbines (Pressure)", "⚙️ Mechanical (Vibration & Speed)"])

with tab1:
    chart_temp = st.empty()
with tab2:
    chart_pres = st.empty()
with tab3:
    chart_mech = st.empty()

alert_dispatched = False  # Anti-spam flag

for _ in range(250):
    try:
        data = next(data_gen)
    except StopIteration:
        break

    # Fetch Predictions
    try:
        response = requests.post("http://127.0.0.1:5000/predict", json=data)
        result = response.json()
        pred, prob = result["prediction"], result["probability"]
    except:
        st.error("API Offline. Run `python api/app.py`")
        break

    anomaly = detect_anomaly(data)
    log_data(data, pred, prob, anomaly)

    # UI Updates (Showing just a few key ones in the JSON to keep it clean)
    data_placeholder.json({"Cycle": data["cycle"], "S2": data["s2"], "S3": data["s3"], "S4": data["s4"]})

    if anomaly == 1:
        alert_placeholder.error("🚨 UNKNOWN ANOMALY DETECTED IN TELEMETRY")
        if not alert_dispatched:
            send_discord_alert(data["id"], data["cycle"], "ISOLATION FOREST ANOMALY", prob)
            alert_dispatched = True
            
    elif pred == 1:
        alert_placeholder.warning("⚠️ HIGH RISK: PREDICTIVE FAILURE IMMINENT")
        if not alert_dispatched:
            send_discord_alert(data["id"], data["cycle"], "RANDOM FOREST PREDICTION", prob)
            alert_dispatched = True
            
    else:
        alert_placeholder.success("🟢 SYSTEM STABLE")

    # Neon Plotly Gauge
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        number={'suffix': "%", 'font': {'color': "#00FFCC"}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "#00FFCC"},
            'bar': {'color': "#B026FF"},
            'bgcolor': "black",
            'borderwidth': 2,
            'bordercolor': "#00FFCC",
        }
    ))
    gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=300)
    gauge_placeholder.plotly_chart(gauge, use_container_width=True, key=f"gauge_{_}")

    # Build the new row dynamically for all 14 features
    new_row_dict = {"cycle": data["cycle"]}
    for f in features:
        new_row_dict[f] = data[f]
        
    new_row = pd.DataFrame([new_row_dict])
    chart_data = pd.concat([chart_data, new_row], ignore_index=True)

    # Split the sensors by their physical meanings so the scales look good!
    # Compressors
    chart_temp.line_chart(chart_data.set_index("cycle")[['s2', 's3', 's4']])
    # Turbines
    chart_pres.line_chart(chart_data.set_index("cycle")[['s7', 's8', 's9', 's11', 's12']])
    # Mechanical Speeds
    chart_mech.line_chart(chart_data.set_index("cycle")[['s13', 's14', 's15', 's17', 's20', 's21']])

    time.sleep(0.8)