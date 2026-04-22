import pandas as pd
import time

def generate_sensor_data():
    # NASA CMAPSS column names
    col_names = ['id', 'cycle', 'setting1', 'setting2', 'setting3'] + [f's{i}' for i in range(1, 22)]
    
    
    df = pd.read_csv("data/train_FD001.txt", sep='\s+', header=None, names=col_names)
    
    # Isolate Engine #1
    engine_data = df[df['id'] == 1]
    
    # Stream the data row by row
    for index, row in engine_data.iterrows():
        data_packet = row.to_dict()
        data_packet['cycle'] = int(row['cycle'])
        data_packet['id'] = int(row['id'])
        
        yield data_packet