# ⚡ DeepGuard AI: Predictive Maintenance & Telemetry Engine

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange.svg)
![Flask](https://img.shields.io/badge/Flask-Microservice-lightgrey.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Dashboard-red.svg)

**DeepGuard** is an industry-grade, microservice-based AI pipeline designed to ingest real-time IoT sensor data, predict critical mechanical failures before they occur, and dispatch automated alerts. 

Built using the **NASA CMAPSS (Turbofan Engine Degradation)** dataset, this system transitions beyond basic binary classification by utilizing a dual-model ensemble to calculate Remaining Useful Life (RUL) and detect zero-day mechanical anomalies.

---

## 📸 Command Center Dashboard

*(Real-time probability tracking and automated dispatch status)*
![Dashboard Overview](images/dashboard_top.png)

*(Live multidimensional sensor degradation tracking)*
![Telemetry Charts](images/dashboard_charts.png)

---

## 🚀 Core Architecture Flow

This project is structured as a distributed microservice architecture, simulating a true enterprise production environment. The system diagram below illustrates the real-time data flow:

```mermaid
graph TD;
    A[IoT Simulator<br/>data_simulator.py] -->|1Hz JSON Stream| B(Flask API Microservice<br/>api/app.py)
    B --> C{Dual-AI Predictor}
    C -->|Random Forest| D[RUL Failure Prediction]
    C -->|Isolation Forest| E[Zero-Day Anomaly Detection]
    D --> F[Streamlit Command Center]
    E --> F
    D -->|If High Risk| G((Discord Webhook<br/>Alert Dispatch))
    E -->|If Anomaly| G
    
    style A fill:#0E1117,stroke:#00FFCC,stroke-width:2px,color:#fff
    style B fill:#0E1117,stroke:#B026FF,stroke-width:2px,color:#fff
    style C fill:#222,stroke:#fff,stroke-width:1px,color:#fff
    style F fill:#0E1117,stroke:#00FFCC,stroke-width:2px,color:#fff
    style G fill:#ff4b4b,stroke:#fff,stroke-width:2px,color:#fff

```
### 📂 Project Structure
``` text
AI-Predictive-Maintenance-IoT/
│
├── data/                   # NASA CMAPSS Dataset
├── models/                 # Serialized joblib assets (.pkl)
├── logs/                   # System and prediction logging
├── images/                 # Architecture and UI screenshots
│
├── src/
│   ├── preprocess.py       # Data cleaning and pipeline orchestration
│   ├── feature_engineering.py # RUL calculation and label generation
│   ├── model_train.py      # Dual-model training and scaling pipeline
│   ├── predictor.py        # Inference engine
│   ├── anomaly.py          # Isolation Forest handler
│   ├── alert_system.py     # Webhook dispatcher
│   ├── data_simulator.py   # IoT data stream generator
│   └── logger.py           # CSV system telemetry logging
│
├── api/
│   └── app.py              # Flask Microservice (Port 5000)
│
├── dashboard/
│   └── streamlit_app.py    # Live Streamlit UI (Port 8501)

```
### 🛠️ Quick Start & Execution
1. Install Dependencies

Bash
pip install pandas numpy scikit-learn flask streamlit plotly requests

2. Train the Pipeline
Ingest the NASA data, engineer the RUL features, and generate the models:

Bash
python src/model_train.py

3. Boot the Prediction API
Start the backend server to listen for incoming sensor telemetry:

Bash
python api/app.py

4. Launch the Live Dashboard
Open a new terminal and initialize the frontend visualizer:

Bash
streamlit run dashboard/streamlit_app.py


### 📊 Dataset Context

This system utilizes the widely recognized NASA CMAPSS (Commercial Modular Aero-Propulsion System Simulation) dataset. Rather than simple, synthetic "pass/fail" data, this involves run-to-failure trajectories. The models must identify subtle, multidimensional drift across 14 active sensors to predict the Remaining Useful Life (RUL) of the asset.

### Developer
Developed by Shravani Mane | Computer Science & Engineering (AIML)    