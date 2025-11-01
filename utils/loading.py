import os 
import pandas as pd
import json

def load_data(csv_path):
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None

def load_json(json_path, lines=False):
    """Load and return JSON data from a file."""
    if os.path.exists(json_path):
       return pd.read_json(json_path, lines=lines)
    return None