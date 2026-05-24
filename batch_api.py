from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import joblib
import pandas as pd
import uvicorn

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


@app.post('/predict', response_model=BatchResponse)
def predict_batch(req: BatchRequest):
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
