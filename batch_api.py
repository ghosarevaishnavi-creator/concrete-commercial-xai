from fastapi import FastAPI, HTTPException, Request, Header
from pydantic import BaseModel
from typing import List, Dict, Optional
import joblib
import pandas as pd
import uvicorn
import time
import os

app = FastAPI(title="Concrete XAI Batch API")

# Load model at module import
_model = joblib.load('concrete_xgboost_model.pkl')

# Expected feature names (must match training names)
FEATURE_NAMES = [
    'Cement (component 1)(kg in a m^3 mixture)',
    'Blast Furnace Slag (component 2)(kg in a m^3 mixture)',
    'Fly Ash (component 3)(kg in a m^3 mixture)',
    'Water  (component 4)(kg in a m^3 mixture)',
    'Superplasticizer (component 5)(kg in a m^3 mixture)',
    'Coarse Aggregate  (component 6)(kg in a m^3 mixture)',
    'Fine Aggregate (component 7)(kg in a m^3 mixture)',
    'Age (day)'
]


class PredictionItem(BaseModel):
    data: Dict[str, float]


class BatchRequest(BaseModel):
    items: List[PredictionItem]


class BatchResponse(BaseModel):
    predictions: List[float]


# Simple in-memory rate limiter per API key (for demo only — not for production)
RATE_LIMIT_WINDOW = int(os.environ.get('RATE_LIMIT_WINDOW', '60'))  # seconds
RATE_LIMIT_MAX = int(os.environ.get('RATE_LIMIT_MAX', '60'))  # requests per window
_request_log: Dict[str, List[float]] = {}


def is_rate_limited(key: str) -> bool:
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW
    logs = _request_log.setdefault(key, [])
    # drop old
    while logs and logs[0] < window_start:
        logs.pop(0)
    if len(logs) >= RATE_LIMIT_MAX:
        return True
    logs.append(now)
    return False


def check_api_key(api_key: Optional[str]):
    expected = os.environ.get('API_KEY', 'CHANGE_ME')
    if not api_key or api_key != expected:
        raise HTTPException(status_code=401, detail='Invalid or missing API key')


@app.post('/predict', response_model=BatchResponse)
def predict_batch(req: BatchRequest, request: Request, x_api_key: Optional[str] = Header(None)):
    # API key auth
    check_api_key(x_api_key)
    # rate limit
    if is_rate_limited(x_api_key or request.client.host):
        raise HTTPException(status_code=429, detail='Rate limit exceeded')

    rows = []
    for it in req.items:
        row = []
        for fn in FEATURE_NAMES:
            if fn not in it.data:
                raise HTTPException(status_code=400, detail=f"Missing feature: {fn}")
            row.append(float(it.data[fn]))
        rows.append(row)
    df = pd.DataFrame(rows, columns=FEATURE_NAMES)
    preds = _model.predict(df)
    return BatchResponse(predictions=[float(x) for x in preds])


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
