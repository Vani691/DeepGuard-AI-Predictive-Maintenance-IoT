import joblib
import numpy as np

# Load assets
model = joblib.load("models/nasa_model.pkl")
scaler = joblib.load("models/scaler.pkl")
features_list = joblib.load("models/features.pkl")

def predict(data):
    # Extract features in the correct order
    input_data = [data[f] for f in features_list]
    
    # Scale the input
    input_scaled = scaler.transform([input_data])
    
    pred = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    return pred, probability