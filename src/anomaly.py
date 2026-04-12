import joblib

def detect_anomaly(data):
    try:
        model = joblib.load("models/anomaly.pkl")
        scaler = joblib.load("models/scaler.pkl")
        features_list = joblib.load("models/features.pkl")
    except FileNotFoundError:
        return 0

    # Extract and scale features just like the main model
    input_data = [data[f] for f in features_list]
    input_scaled = scaler.transform([input_data])
    
    pred = model.predict(input_scaled)
    return 1 if pred[0] == -1 else 0