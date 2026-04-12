from src.data_simulator import generate_sensor_data
from src.predictor import predict
from src.alert_system import generate_alert

for data in generate_sensor_data():
    pred, prob = predict(data)
    alert = generate_alert(pred, prob)

    print(data, alert)