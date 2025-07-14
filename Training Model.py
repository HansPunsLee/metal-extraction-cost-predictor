import pandas as pd

# Load your data
df = pd.read_csv(r"C:/Users\Admin\Desktop/Commodities ML/metal_properties.csv")

# Show the first few rows
print(df.head())
print("\nColumns:", df.columns.tolist())
print("\nMissing values:\n", df.isnull().sum())

# Simulate target variable (cost in $/ton) — dummy for now
# This is for demonstration; you’ll replace it with real data later

import numpy as np

# Simulated cost = weighted sum of enthalpy, ore grade, and electrode potential
df["Estimated Cost ($/ton)"] = (
    df["Enthalpy (kJ/mol)"] * 2 +
    (1 / df["Ore Grade (%)"]) * 500 +
    df["Electrode Potential (V)"].abs() * 100
) + np.random.normal(0, 100, size=len(df))  # adds some randomness

print("\nPreview of data with target column:")
print(df[["Metal", "Estimated Cost ($/ton)"]])

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Select numerical features
features = ["Delta G (kJ/mol)", "Electrode Potential (V)", "Enthalpy (kJ/mol)", "Ore Grade (%)", "Melting Point (C)", "Boiling Point (C)"]
X = df[features]
y = df["Estimated Cost ($/ton)"]

# Handle missing values (if any)
X = X.fillna(X.mean())

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"\nModel trained. Test MAE: ${mae:.2f}")

import joblib
joblib.dump(model, r"C:\Users\Admin\Desktop\Commodities ML\extraction_cost_model.pkl")
print("Model saved as extraction_cost_model.pkl")
