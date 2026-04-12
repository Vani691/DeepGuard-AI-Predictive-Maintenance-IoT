import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
from src.preprocess import load_and_clean_nasa_data
from src.feature_engineering import engineer_features

def train_nasa_model():
    print("🚀 Starting Dual-Model Training Pipeline...")
    df_clean = load_and_clean_nasa_data("data/train_FD001.txt")
    X, y, features_list = engineer_features(df_clean)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("🧠 Training Random Forest (Failure Prediction)...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_scaled, y)

    print("🕵️ Training Isolation Forest (Anomaly Detection)...")
    iso_model = IsolationForest(contamination=0.05, random_state=42)
    iso_model.fit(X_scaled) # Unsupervised, doesn't need 'y'

    os.makedirs("models", exist_ok=True)
    joblib.dump(rf_model, "models/nasa_model.pkl")
    joblib.dump(iso_model, "models/anomaly.pkl")
    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(features_list, "models/features.pkl")
    print("✅ Pipeline Finished! Models saved.")

if __name__ == "__main__":
    train_nasa_model()