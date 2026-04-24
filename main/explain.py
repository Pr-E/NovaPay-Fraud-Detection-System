# ----------------------------------------
# ✅ REASON CODE MAP (GLOBAL - TOP LEVEL)
# ----------------------------------------
reason_code_map = {
    "normalized_behavioral_risk": "High behavioural risk score",
    "high_txn_velocity_1h": "High transaction velocity (1 hour)",
    "high_txn_velocity_24h": "High transaction velocity (24 hours)",
    "velocity_24h_amount_interaction": "Unusual transaction volume and value pattern",
    "ip_device_interaction": "Suspicious device and IP combination",
    "customer_txn_count": "Unusual transaction frequency",
    "customer_total_amount": "High total transaction value",
    "customer_avg_amount": "Abnormal transaction size",
    "chargeback_amount_interaction": "Chargeback-related risk pattern",
    "txn_ratio_1h_24h": "Transaction velocity imbalance",
    "new_corridor_flag": "New transaction corridor detected",
    "device_count_per_customer": "Multiple devices used",
    "high_ip_risk": "High-risk IP address",
    "new_account": "Recently created account",
    "high_risk_score": "Elevated composite risk score",
    "high_risk_hour": "Transaction at high-risk time"
}


# ----------------------------------------
# ✅ EXPLAIN FUNCTION
# ----------------------------------------
def explain_transaction(model, explainer, X, feature_names, threshold=0.5):

    pred_proba = model.predict_proba(X)[0, 1]
    prediction = "FRAUD" if pred_proba >= threshold else "LEGITIMATE"

    # Risk level
    if pred_proba >= 0.8:
        risk_level = "HIGH"
    elif pred_proba >= 0.5:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # ----------------------------------------
    # SHAP VALUES (SAFE HANDLING)
    # ----------------------------------------
    shap_vals = explainer.shap_values(X)

    if isinstance(shap_vals, list):
        shap_vals = shap_vals[1][0]   # binary classification
    else:
        shap_vals = shap_vals[0]

    feature_vals = X.iloc[0].values

    contributions = list(zip(feature_names, feature_vals, shap_vals))
    contributions.sort(key=lambda x: abs(x[2]), reverse=True)

    risk_factors = [c for c in contributions if c[2] > 0][:5]
    protective_factors = [c for c in contributions if c[2] < 0][:5]

    # ----------------------------------------
    # ✅ REASON CODES (CLEAN)
    # ----------------------------------------
    reason_codes = [
        reason_code_map.get(feat, feat)
        for feat, _, _ in risk_factors
    ]

    # ----------------------------------------
    # ✅ STRUCTURED RESPONSE (API)
    # ----------------------------------------
    response = {
        "prediction": prediction,
        "confidence": float(pred_proba),
        "risk_level": risk_level,
        "reason_codes": reason_codes,
        "top_risk_drivers": [
            {
                "feature": feat,
                "value": float(val),
                "impact": float(shap_val)
            }
            for feat, val, shap_val in risk_factors
        ],
        "protective_factors": [
            {
                "feature": feat,
                "value": float(val),
                "impact": float(shap_val)
            }
            for feat, val, shap_val in protective_factors
        ]
    }

    # ----------------------------------------
    # ✅ HUMAN-READABLE REPORT
    # ----------------------------------------
    report = f"""
===============================
 FRAUD REVIEW SUMMARY
===============================

Prediction: {prediction}
Confidence: {pred_proba:.2%}
Risk Level: {risk_level}

-------------------------------
 REASON CODES
-------------------------------
"""

    for r in reason_codes:
        report += f" - {r}\n"

    report += "\n-------------------------------\n TOP DRIVERS\n-------------------------------\n"

    for feat, val, shap_val in risk_factors:
        report += f" - {feat}: {val:.4f} (Impact: +{shap_val:.4f})\n"

    report += "\n-------------------------------\n PROTECTIVE FACTORS\n-------------------------------\n"

    for feat, val, shap_val in protective_factors:
        report += f" - {feat}: {val:.4f} (Impact: {shap_val:.4f})\n"

    return response, report



