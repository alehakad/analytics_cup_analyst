import os 
import pandas as pd

def load_data(csv_path):
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None