import sys
import os

# Tell Python to look in the root directory to find 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from src.predictor import predict
# If you haven't split alert_system out yet, you can comment this next line out:
# from src.alert_system import generate_alert 

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict_api():
    data = request.json

    pred, prob = predict(data)
    
    # Simple alert logic if you haven't created alert_system.py yet
    alert = "⚠️ HIGH RISK" if pred == 1 else "✅ NORMAL"

    return jsonify({
        "prediction": int(pred),
        "probability": float(prob),
        "alert": alert
    })

if __name__ == "__main__":
    app.run(debug=True)