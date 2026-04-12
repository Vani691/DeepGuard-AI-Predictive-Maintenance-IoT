import pandas as pd
import os

def load_and_clean_nasa_data(filepath):
    """Loads the raw NASA text file and applies proper column headers."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Error: Could not find {filepath}")

    # NASA CMAPSS FD001 Columns
    col_names = ['id', 'cycle', 'setting1', 'setting2', 'setting3'] + [f's{i}' for i in range(1, 22)]
    
    # Load data
    df = pd.read_csv(filepath, sep='\s+', header=None, names=col_names)
    
    # In a real messy industrial dataset, we would handle missing values (NaNs) right here
    # e.g., df.fillna(method='ffill', inplace=True)
    
    print(f"🧹 Preprocessing complete: Loaded {len(df)} rows.")
    return df