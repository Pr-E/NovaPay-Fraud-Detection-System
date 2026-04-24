from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

from main.utils import preprocess
from main.explain import explain_transaction

# --------------------------------------------------
# 🚀 FastAPI App
# --------------------------------------------------
app = FastAPI(title="NovaPay Fraud Detection API")

# --------------------------------------------------
# 📦 Load Artifacts
# --------------------------------------------------
model = joblib.load("artifacts/lgb_model.pkl")
scaler = joblib.load("artifacts/scaler.pkl")
encoders = joblib.load("artifacts/encoders.pkl")
features = joblib.load("artifacts/features.pkl")
explainer = joblib.load("artifacts/shap_explainer.pkl")

# --------------------------------------------------
# 📥 Input Schema (FIXES YOUR ERROR)
# --------------------------------------------------
class TransactionInput(BaseModel):
    hour: int
    amount_usd: float
    txn_velocity_1h: int
    txn_velocity_24h: int
    ip_risk_score: float
    device_trust_score: float
    account_age_days: int


# --------------------------------------------------
# 🏠 Health Check
# --------------------------------------------------
@app.get("/")
def home():
    return {"message": "NovaPay Fraud API is running 🚀"}


# --------------------------------------------------
# 🔍 Prediction Endpoint
# --------------------------------------------------
@app.post("/predict")
def predict(data: TransactionInput):

    # Convert input to DataFrame
    df = pd.DataFrame([data.dict()])

    # Apply full preprocessing pipeline
    X = preprocess(df, scaler, encoders, features)

    # Predict
    prob = model.predict_proba(X)[0][1]
    prediction = "FRAUD" if prob >= 0.5 else "LEGITIMATE"

    return {
        "prediction": prediction,
        "fraud_probability": float(prob)
    }


# --------------------------------------------------
# 🧠 Explainability Endpoint (SHAP)
# --------------------------------------------------


@app.post("/explain")
def explain(data: TransactionInput):

    df = pd.DataFrame([data.dict()])
    X = preprocess(df, scaler, encoders, features)

    response, report = explain_transaction(
        model=model,
        explainer=explainer,
        X=X,
        feature_names=features
    )

    return {
        "structured_output": response,
        "review_summary": report
    }