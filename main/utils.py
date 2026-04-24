import pandas as pd

def compute_risk_scores(df):

    df['high_risk_hour'] = df['hour'].between(0, 8).astype(int)
    df['high_txn_velocity_1h'] = (df['txn_velocity_1h'] >= 3).astype(int)
    df['high_txn_velocity_24h'] = (df['txn_velocity_24h'] >= 5).astype(int)

    df['high_ip_risk'] = (df['ip_risk_score'] > 0.49).astype(int)
    df['low_device_trust'] = (df['device_trust_score'] < 0.52).astype(int)
    df['new_account'] = (df['account_age_days'] < 147).astype(int)

    df['behavioral_risk_score'] = df[
        ['high_txn_velocity_1h','high_txn_velocity_24h','new_account','high_ip_risk']
    ].sum(axis=1)

    df['normalized_behavioral_risk'] = df['behavioral_risk_score'] / 4

    return df


def engineer_features(df):

    df['txn_ratio_1h_24h'] = df['txn_velocity_1h'] / (df['txn_velocity_24h'] + 1)
    df['velocity_24h_amount_interaction'] = df['txn_velocity_24h'] * df['amount_usd']
    df['ip_device_interaction'] = df['high_ip_risk'] * df['low_device_trust']

    return df


def preprocess(df, scaler, encoders, feature_names):

    # ----------------------------------------
    # 1️⃣ Feature Engineering (same as training)
    # ----------------------------------------
    df = compute_risk_scores(df)
    df = engineer_features(df)

    # ----------------------------------------
    # 2️⃣ Align features with training
    # ----------------------------------------
    X = df.copy()

    # 🔥 CRITICAL FIX: ensure ALL features exist
    for col in feature_names:
        if col not in X.columns:
            X[col] = 0

    # Keep exact order
    X = X[feature_names]

    # ----------------------------------------
    # 3️⃣ Encoding (same encoders from training)
    # ----------------------------------------
    for col, le in encoders.items():
        if col in X.columns:
            try:
                X[col] = le.transform(X[col].astype(str))
            except:
                X[col] = 0  # unseen category fallback

    # ----------------------------------------
    # Scaling 
    # ----------------------------------------
    numeric_cols = [
        'customer_txn_count', 'customer_total_amount', 'customer_corridor_diversity',
        'customer_avg_amount', 'device_count_per_customer',
        'velocity_24h_amount_interaction', 'txn_ratio_1h_24h',
        'chargeback_amount_interaction', 'normalized_behavioral_risk'
    ]

    numeric_cols = [c for c in numeric_cols if c in X.columns]

    X[numeric_cols] = scaler.transform(X[numeric_cols])

    return X