import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import requests
import pandas as pd
import time
import joblib
import plotly.graph_objects as go
import plotly.express as px

from src.data_simulator import generate_sensor_data
from src.anomaly import detect_anomaly
from src.logger import log_data, init_log

# --- Futuristic Neon UI Styling ---
st.set_page_config(layout="wide", page_title="DeepGuard Predictor V2.0")
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    h1, h2, h3 { color: #00FFCC !important; text-shadow: 0px 0px 10px #00FFCC; }
    .stMetric, .stAlert { border: 1px solid #B026FF; border-radius: 5px; box-shadow: 0 0 15px #B026FF; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ DEEP-GUARD: Telemetry & Analytics Engine")
st.markdown("**CSE-AIML Undergraduate Project | Dual-AI Real-Time Architecture**")

# Create our Main Navigation Tabs
tab_live, tab_analytics = st.tabs(["🚀 Live Command Center", "📊 V2.0 Data Science Analytics"])

# ==========================================
# TAB 2: DATA SCIENCE ANALYTICS (STATIC)
# ==========================================
with tab_analytics:
    st.subheader("🧠 Machine Learning Model Insights")
    st.write("Post-training analysis of the Random Forest and NASA CMAPSS Sensor relationships.")
    
    col_a, col_b = st.columns(2)
    
    try:
        # Load Model and Features
        rf_model = joblib.load("models/nasa_model.pkl")
        features_list = joblib.load("models/features.pkl")
        
        # 1. Feature Importance Chart
        importances = rf_model.feature_importances_
        df_imp = pd.DataFrame({"Sensor Feature": features_list, "Importance": importances}).sort_values(by="Importance", ascending=True)
        
        fig_imp = px.bar(df_imp, x="Importance", y="Sensor Feature", orientation='h', 
                         title="Random Forest Feature Importance",
                         color_discrete_sequence=["#B026FF"])
        fig_imp.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#00FFCC"))
        
        with col_a:
            st.plotly_chart(fig_imp, use_container_width=True)
            
        # 2. Sensor Correlation Heatmap
        col_names = ['id', 'cycle', 'setting1', 'setting2', 'setting3'] + [f's{i}' for i in range(1, 22)]
        df_train = pd.read_csv("data/train_FD001.txt", sep='\s+', header=None, names=col_names)
        corr_matrix = df_train[features_list].corr()
        
        fig_corr = px.imshow(corr_matrix, text_auto=False, aspect="auto", 
                             color_continuous_scale=[(0, "black"), (1, "#00FFCC")],
                             title="Sensor Correlation Heatmap")
        fig_corr.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#00FFCC"))
        
        with col_b:
            st.plotly_chart(fig_corr, use_container_width=True)
            
    except FileNotFoundError:
        st.error("⚠️ Models not found. Please run `python src/model_train.py` first.")

# ==========================================
# TAB 1: LIVE TELEMETRY SIMULATION
# ==========================================
with tab_live:
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
    tab_temp, tab_pres, tab_mech = st.tabs(["🔥 Compressors (Temperature)", "🌪️ Turbines (Pressure)", "⚙️ Mechanical (Vibration)"])
    
    with tab_temp: chart_temp = st.empty()
    with tab_pres: chart_pres = st.empty()
    with tab_mech: chart_mech = st.empty()

    alert_dispatched = False

    # Live Streaming Loop
    for _ in range(250):
        try:
            data = next(data_gen)
        except StopIteration:
            st.success("🏁 Simulation Complete.")
            break

        try:
            response = requests.post("http://127.0.0.1:5000/predict", json=data)
            result = response.json()
            pred, prob = result["prediction"], result["probability"]
        except:
            st.error("API Offline. Run `python api/app.py`")
            break

        anomaly = detect_anomaly(data)
        log_data(data, pred, prob, anomaly)

        data_placeholder.json({"Cycle": data["cycle"], "S2": data["s2"], "S3": data["s3"], "S4": data["s4"]})

        if anomaly == 1:
            alert_placeholder.error("🚨 UNKNOWN ANOMALY DETECTED IN TELEMETRY")
        elif pred == 1:
            alert_placeholder.warning("⚠️ HIGH RISK: PREDICTIVE FAILURE IMMINENT")
        else:
            alert_placeholder.success("🟢 SYSTEM STABLE")

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
        gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=300, margin=dict(l=20, r=20, t=30, b=20))
        gauge_placeholder.plotly_chart(gauge, use_container_width=True, key=f"gauge_{_}")

        new_row_dict = {"cycle": data["cycle"]}
        for f in features: new_row_dict[f] = data[f]
        
        new_row = pd.DataFrame([new_row_dict])
        chart_data = pd.concat([chart_data, new_row], ignore_index=True)

        chart_temp.line_chart(chart_data.set_index("cycle")[['s2', 's3', 's4']])
        chart_pres.line_chart(chart_data.set_index("cycle")[['s7', 's8', 's9', 's11', 's12']])
        chart_mech.line_chart(chart_data.set_index("cycle")[['s13', 's14', 's15', 's17', 's20', 's21']])

        time.sleep(0.8)