import pandas as pd
import numpy as np

def engineer_features(df):
    """Calculates RUL, creates the target label, and selects features."""
    # 1. Calculate Remaining Useful Life (RUL)
    id_max_cycle = df.groupby('id')['cycle'].max().reset_index()
    id_max_cycle.columns = ['id', 'max_cycle']
    
    df = df.merge(id_max_cycle, on='id', how='left')
    df['rul'] = df['max_cycle'] - df['cycle']

    # 2. Create Binary Label (Failure within 30 cycles)
    df['failure'] = np.where(df['rul'] <= 30, 1, 0)

    # 3. Feature Selection (Selecting only the important sensors for FD001)
    features = ['s2', 's3', 's4', 's7', 's8', 's9', 's11', 's12', 's13', 's14', 's15', 's17', 's20', 's21']
    
    X = df[features]
    y = df['failure']
    
    print("⚙️ Feature Engineering complete: RUL calculated and target labels created.")
    return X, y, features