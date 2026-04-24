import streamlit as st
import requests
import json

st.set_page_config(page_title="NovaPay Fraud Detection", layout="wide")

st.title("🚀 NovaPay Fraud Detection Dashboard")

st.markdown("Enter transaction details to assess fraud risk")

# ----------------------------------------
# INPUT FORM
# ----------------------------------------
with st.form("fraud_form"):

    col1, col2 = st.columns(2)

    with col1:
        amount_usd = st.number_input("Transaction Amount (USD)", value=100.0)
        txn_velocity_1h = st.number_input("Transactions (1h)", value=1)
        txn_velocity_24h = st.number_input("Transactions (24h)", value=2)
        hour = st.slider("Transaction Hour", 0, 23, 12)

    with col2:
        ip_risk_score = st.slider("IP Risk Score", 0.0, 1.0, 0.2)
        device_trust_score = st.slider("Device Trust Score", 0.0, 1.0, 0.8)
        account_age_days = st.number_input("Account Age (days)", value=200)

    submit = st.form_submit_button("🔍 Analyze Transaction")

# ----------------------------------------
# CALL API
# ----------------------------------------
if submit:

    input_data = {
        "amount_usd": amount_usd,
        "txn_velocity_1h": txn_velocity_1h,
        "txn_velocity_24h": txn_velocity_24h,
        "hour": hour,
        "ip_risk_score": ip_risk_score,
        "device_trust_score": device_trust_score,
        "account_age_days": account_age_days
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/explain",
            json=input_data
        )

        result = response.json()

        # ----------------------------------------
        # DISPLAY RESULTS
        # ----------------------------------------
        st.subheader("📊 Prediction Result")

        structured = result["structured_output"]

        col1, col2, col3 = st.columns(3)

        col1.metric("Prediction", structured["prediction"])
        col2.metric("Confidence", f"{structured['confidence']:.2%}")
        col3.metric("Risk Level", structured["risk_level"])

        # ----------------------------------------
        # 🚨 RISK ALERT (PUT HERE)
        # ----------------------------------------
        if structured["risk_level"] == "HIGH":
            st.error("🚨 High Risk Fraud Detected")
        elif structured["risk_level"] == "MEDIUM":
            st.warning("⚠️ Medium Risk Transaction")
        else:
            st.success("✅ Low Risk Transaction")
            
        # ----------------------------------------
        # REASON CODES
        # ----------------------------------------
        st.subheader("🧠 Reason Codes")

        for reason in structured["reason_codes"]:
            st.write(f"• {reason}")

        # ----------------------------------------
        # TOP RISK DRIVERS
        # ----------------------------------------
        st.subheader("⚠️ Top Risk Drivers")

        for item in structured["top_risk_drivers"]:
            st.write(f"{item['feature']} → Impact: {item['impact']:.4f}")

        # ----------------------------------------
        # PROTECTIVE FACTORS
        # ----------------------------------------
        st.subheader("🛡️ Protective Factors")

        for item in structured["protective_factors"]:
            st.write(f"{item['feature']} → Impact: {item['impact']:.4f}")

        # ----------------------------------------
        # FULL REPORT
        # ----------------------------------------
        with st.expander("📄 Full Fraud Report"):
            st.text(result["review_summary"])

    except Exception as e:
        st.error(f"Error: {e}")