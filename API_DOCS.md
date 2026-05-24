# Concrete XAI - API Documentation

## Batch Prediction API

Endpoint: `POST /predict`

Request body (application/json):

```
{
  "items": [
    {
      "data": {
        "Cement (component 1)(kg in a m^3 mixture)": 320,
        "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": 0,
        "Fly Ash (component 3)(kg in a m^3 mixture)": 50,
        "Water  (component 4)(kg in a m^3 mixture)": 175,
        "Superplasticizer (component 5)(kg in a m^3 mixture)": 6,
        "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": 960,
        "Fine Aggregate (component 7)(kg in a m^3 mixture)": 740,
        "Age (day)": 28
      }
    }
  ]
}
```

Response (application/json):

```
{
  "predictions": [43.44577]
}
```

Notes:
- Feature names must match the model's trained feature names exactly (including spacing/units) as shown above.
- Run the API locally with:

```bash
uvicorn batch_api:app --reload --port 8000
```

- Example curl:

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"items":[{"data": {"Cement (component 1)(kg in a m^3 mixture)":320, "Blast Furnace Slag (component 2)(kg in a m^3 mixture)":0, "Fly Ash (component 3)(kg in a m^3 mixture)":50, "Water  (component 4)(kg in a m^3 mixture)":175, "Superplasticizer (component 5)(kg in a m^3 mixture)":6, "Coarse Aggregate  (component 6)(kg in a m^3 mixture)":960, "Fine Aggregate (component 7)(kg in a m^3 mixture)":740, "Age (day)":28}}]}'
```

License and cautions:
- This endpoint uses the same in-repo `concrete_xgboost_model.pkl`. Do not expose this endpoint publicly without proper authentication and rate limiting.
