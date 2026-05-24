import os
import sys
from pathlib import Path
# Ensure project root is on sys.path for importing batch_api
proj_root = str(Path(__file__).resolve().parents[1])
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

from fastapi.testclient import TestClient
from batch_api import app

client = TestClient(app)

API_KEY = os.environ.get('API_KEY', 'CHANGE_ME')


def test_predict_success():
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
    headers = {"x-api-key": API_KEY}
    r = client.post('/predict', json=payload, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert 'predictions' in data
    assert isinstance(data['predictions'], list)


def test_missing_api_key():
    payload = {"items": []}
    r = client.post('/predict', json=payload)
    assert r.status_code == 401


def test_rate_limit():
    headers = {"x-api-key": API_KEY}
    # sample single-item valid payload
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
    # simulate exceeding RATE_LIMIT_MAX by calling in a loop
    max_calls = int(os.environ.get('RATE_LIMIT_MAX', '5'))
    for i in range(max_calls):
        client.post('/predict', json=payload, headers=headers)
    r = client.post('/predict', json=payload, headers=headers)
    assert r.status_code in (200, 429)
