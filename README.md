# NovaPay-Fraud-Detection-System
# 🚀 NovaPay Fraud Detection System

An end-to-end machine learning project designed to detect fraudulent transactions in a highly imbalanced financial dataset, with a strong focus on **performance, interpretability, and real-world usability**.

---

## 📌 Project Overview

Fraud detection is a critical challenge in fintech, where fraudulent transactions are rare but highly impactful. In this project, we built a robust and interpretable fraud detection system for NovaPay that:

- Accurately identifies fraudulent transactions  
- Handles severe class imbalance (<10% fraud rate)  
- Provides transparent, audit-ready explanations for each prediction  

---

## ⚙️ Key Features

- ✅ Behavioural risk scoring system  
- ✅ Advanced feature engineering (velocity, anomaly, interaction features)  
- ✅ Time-based model validation (prevents data leakage)  
- ✅ LightGBM & XGBoost model comparison  
- ✅ Imbalance handling (SMOTE, class weights, undersampling)  
- ✅ SHAP-based explainability  
- ✅ Fraud review template with reason codes  
- ✅ Deployment-ready (FastAPI + Docker)  

---

## 📊 Model Performance

| Metric    | Score        |
|----------|-------------|
| Accuracy | ~98%         |
| ROC-AUC  | ~0.97–0.98   |
| F1-score | ~0.95        |

👉 **Final model:** LightGBM (Baseline)

- Best balance between precision and recall  
- Stable without heavy rebalancing  

---

## 🧠 Approach

### 1. Exploratory Data Analysis
Identified key fraud patterns:
- High transaction velocity  
- Risky IP/device behaviour  
- New accounts  

---

### 2. Risk Scoring
- Built a behavioural risk score using domain-driven rules  
- Normalized into interpretable risk levels  

---

### 3. Feature Engineering

**Customer behaviour:**
- Transaction frequency, averages, totals  

**Anomaly detection:**
- Velocity ratios, deviations  

**Interaction features:**
- IP × device risk  
- Velocity × amount  

---

### 4. Model Training

**Models used:**
- LightGBM  
- XGBoost  

**Techniques tested:**
- SMOTE  
- Class weighting  
- Undersampling  

---

### 5. Explainability (SHAP)

Implemented SHAP for:

- Global feature importance  
- Transaction-level explanations  

Each prediction includes:

- Prediction (Fraud / Legitimate)  
- Confidence score  
- Risk level (Low / Medium / High)  
- Top risk drivers  
- Protective factors  
- Business-friendly **reason codes**

---

## 🔍 Example Output

Prediction: FRAUD  
Confidence: 100%

Top Risk Drivers:
- High behavioural risk score
- New account
- High transaction velocity
- Suspicious IP/device interaction

---

## 🖥️ Interactive Dashboard (Streamlit)

A user-friendly interface allows stakeholders to:

- Input transaction details  
- View fraud prediction instantly  
- See:
  - Risk level (colour-coded)
  - Reason codes
  - Full fraud review summary  

👉 Transforms model output into **actionable insights**

---

## 🏗️ Deployment

The model is production-ready and deployed using:

FastAPI → REST API for predictions
Docker → Containerized deployment

---

## Project Structure

nova-fraud-api/
│
├── app/
│   ├── main.py
│   ├── utils.py
│
├── artifacts/
│   ├── lgb_model.pkl
│   ├── scaler.pkl
│   ├── encoders.pkl
│   ├── features.pkl
│   ├── shap_explainer.pkl
├── notebooks/
├── requirements.txt
├── Dockerfile

---

## 💡 Key Insights

- Feature engineering had the biggest impact on performance
- LightGBM handled imbalance effectively without heavy resampling
- Fraud detection requires balancing:
    - Recall (catch fraud)
    - Precision (avoid false alarms)
- Explainability is critical for:
    - Trust
    - Regulatory Compliance
    - Analyst decision-making
 
---

## 🚀 Future Improvements

- Real-time streaming fraud detection  
- Threshold optimisation for business strategies  
- Hybrid system (rules + ML)  
- Model monitoring & drift detection  
- Integration with transaction systems  

---

## 👩‍💻 Author

Priscillia Ejiro
Data Scientist | Machine Learning | Fraud Analytics
