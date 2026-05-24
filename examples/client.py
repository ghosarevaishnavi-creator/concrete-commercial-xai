import requests
import os

API_URL = os.environ.get('API_URL', 'http://localhost:8000/predict')
API_KEY = os.environ.get('API_KEY', 'CHANGE_ME')

payload = {
    "items": [
        {"data": {
            'Cement (component 1)(kg in a m^3 mixture)': 320,
            'Blast Furnace Slag (component 2)(kg in a m^3 mixture)': 0,
            'Fly Ash (component 3)(kg in a m^3 mixture)': 50,
            'Water  (component 4)(kg in a m^3 mixture)': 175,
            'Superplasticizer (component 5)(kg in a m^3 mixture)': 6,
            'Coarse Aggregate  (component 6)(kg in a m^3 mixture)': 960,
            'Fine Aggregate (component 7)(kg in a m^3 mixture)': 740,
            'Age (day)': 28
        }}
    ]
}

r = requests.post(API_URL, json=payload, headers={'x-api-key': API_KEY})
print('Status', r.status_code)
print(r.json())
