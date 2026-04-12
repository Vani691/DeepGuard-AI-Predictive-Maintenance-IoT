import pandas as pd
import time
import joblib

def generate_sensor_data():
    col_names = ['id', 'cycle', 'setting1', 'setting2', 'setting3'] + [f's{i}' for i in range(1, 22)]
    
    # 🔥 CHANGE HERE: Switch to the train file to see the full lifecycle
    df = pd.read_csv("data/train_FD001.txt", sep='\s+', header=None, names=col_names)
    
    features = joblib.load("models/features.pkl")

    # Engine 1 in the train set runs for 192 cycles until failure
    engine_data = df[df['id'] == 1]

    for _, row in engine_data.iterrows():
        data_packet = row[features].to_dict()
        data_packet['cycle'] = int(row['cycle'])
        data_packet['id'] = int(row['id'])
        
        yield data_packet
        time.sleep(0.8)