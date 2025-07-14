import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load the trained model
model = joblib.load("extraction_cost_model.pkl")

st.title("Metal Extraction Cost Predictor")

st.write("""
Enter the chemical and physical properties of a metal to estimate its extraction cost.
""")

# User inputs
delta_g = st.number_input("ΔG (kJ/mol)", value=0.0)
electrode_potential = st.number_input("Electrode Potential (V)", value=0.0)
enthalpy = st.number_input("Enthalpy (kJ/mol)", value=0.0)
ore_grade = st.number_input("Ore Grade (%)", min_value=0.0, max_value=100.0, value=1.0)
melting_point = st.number_input("Melting Point (°C)", value=0.0)
boiling_point = st.number_input("Boiling Point (°C)", value=0.0)

# Prepare input features as a dataframe (1 row)
input_features = pd.DataFrame(
    [[delta_g, electrode_potential, enthalpy, ore_grade, melting_point, boiling_point]],
    columns=["Delta G (kJ/mol)", "Electrode Potential (V)", "Enthalpy (kJ/mol)", "Ore Grade (%)", "Melting Point (C)", "Boiling Point (C)"]
)

if st.button("Predict Extraction Cost"):
    prediction = model.predict(input_features)[0]
    st.success(f"Estimated Extraction Cost: ${prediction:.2f} per ton")
