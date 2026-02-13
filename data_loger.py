import pandas as pd
import requests
import json

def load_csv(file_path):
    """Загрузка данных из CSV файла."""
    return pd.read_csv(file_path)

def load_json(file_path):
    """Загрузка данных из JSON файла."""
    with open(file_path) as json_file:
        return pd.json_normalize(json.load(json_file))

def load_api(url):
    """Загрузка данных из API."""
    response = requests.get(url)
    data = response.json()
    return pd.json_normalize(data)



    