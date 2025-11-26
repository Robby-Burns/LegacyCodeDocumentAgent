import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# --- LOAD DATA ---
# Assuming data export from SQL
df = pd.read_csv("customer_dump_final_v2.csv")

# --- CLEANING ---
# Drop rows with null IDs
df = df.dropna(subset=['cust_id'])

# Fill age with mean (maybe not best practice?)
df['age'] = df['age'].fillna(df['age'].mean())

# Map text columns
# 0 = No, 1 = Yes
df['is_active'] = df['status'].map({'Active': 1, 'Closed': 0})
df['has_credit_card'] = df['cc_flag'].apply(lambda x: 1 if x == 'Y' else 0)

# Feature Engineering
# Create tenure in years
df['tenure_years'] = df['tenure_months'] / 12.0

# --- MODELING ---
features = ['age', 'tenure_years', 'balance', 'num_products', 'has_credit_card', 'estimated_salary']
target = 'exited'

X = df[features]
y = df[target]

# 80/20 split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Init model
# n_estimators=100 is standard
clf = RandomForestClassifier(n_estimators=100, max_depth=10)
clf.fit(X_train, y_train)

# --- EVALUATION ---
preds = clf.predict(X_test)
acc = accuracy_score(y_test, preds)

print(f"Model Accuracy: {acc}")

# Important features
importances = clf.feature_importances_
print("Feature ranking:")
for i, v in enumerate(importances):
    print(f"{features[i]}: {v}")

# TODO: Save pickle file
