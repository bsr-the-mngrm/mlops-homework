from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

# 1️⃣ Töltsd be a pickled modellt
# Ha még nem mentetted, a notebook végén add hozzá:
#   import joblib
#   joblib.dump(model, "../models/final_model.pkl")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/final_model.pkl")
model = joblib.load(MODEL_PATH)

# 2️⃣ Definiáld a kérés sémáját
class PriceRequest(BaseModel):
    bedrooms: int
    bathrooms: float
    accommodates: int
    number_of_reviews: int

# 3️⃣ FastAPI app inicializálása
app = FastAPI(title="Airbnb Price Predictor")

@app.get("/")
def read_root():
    return {"message": "API él!"}

@app.post("/predict")
def predict(req: PriceRequest):
    features = [[
        req.bedrooms,
        req.bathrooms,
        req.accommodates,
        req.number_of_reviews
    ]]
    pred = model.predict(features)
    return {"predicted_price": float(pred[0])}