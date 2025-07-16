import streamlit as st
import pandas as pd
import joblib
import numpy as np
import io

st.set_page_config(
    page_title="Metal Extraction Cost Calculator",
    page_icon="🧮",
    layout="wide"
)

st.title("🧮 Metal Extraction Cost Calculator")
st.caption("Estimate the extraction cost of metal oxides based on thermodynamic data and ML models.")


# Load trained model
model = joblib.load("extraction_cost_model.pkl")

# Assume MAE from your model training (adjust as needed)
MODEL_MAE = 120  # example MAE in $

st.set_page_config(page_title="Metal Extraction Cost Predictor", layout="wide")

# Custom CSS styling
st.markdown("""
<style>
body {
    background-color: #f0f2f6;
    color: #333333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1, h2, h3 {
    color: #2c3e50;
}
.sidebar .sidebar-content {
    background-image: linear-gradient(#4b6cb7,#182848);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Sidebar - About section
with st.sidebar.expander("About this project"):
    st.write("""
    This app estimates the **metal extraction cost** based on chemical and physical properties.
    \n\n
    It uses a linear regression model trained on simulated data using thermodynamic and material parameters.
    \n\n
    Built by **HansPunsLee** — final year Chemistry student with a passion for commodities and data science.
    \n\n
    [GitHub Repo](https://github.com/HansPunsLee/metal-extraction-cost-predictor)
    """)

st.title("🛠️ Metal Extraction Cost Predictor")

# Metal images hosted on GitHub or locally in repo folder 'images/'
#metal_images = {
 #   "Aluminum (Al)": "https://upload.wikimedia.org/wikipedia/commons/8/85/Aluminium_eloi.jpg",
  #  "Copper (Cu)": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Copper_ingots_Picryl.jpg",
   # "Lithium (Li)": "https://upload.wikimedia.org/wikipedia/commons/5/59/Lithium_in_oil.jpg",
    #"Nickel (Ni)": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Nickel_crystals.jpg",
    #"Zinc (Zn)": "https://upload.wikimedia.org/wikipedia/commons/5/57/Zinc_plates.jpg",
    #"Cobalt (Co)": "https://upload.wikimedia.org/wikipedia/commons/4/47/Cobalt_crystals.jpg",
    #"Platinum (Pt)": "https://upload.wikimedia.org/wikipedia/commons/5/52/Platinum_bar.jpg",
    #"Gold (Au)": "https://upload.wikimedia.org/wikipedia/commons/0/09/Gold_Nuggets.jpg"
#}


# Metal properties dictionary
metal_data = {
    "Aluminum (Al)": {
        "Delta G (kJ/mol)": 900,
        "Electrode Potential (V)": -1.66,
        "Enthalpy (kJ/mol)": 1170,
        "Ore Grade (%)": 40,
        "Melting Point (C)": 660,
        "Boiling Point (C)": 2519
    },
    "Copper (Cu)": {
        "Delta G (kJ/mol)": -146,
        "Electrode Potential (V)": 0.34,
        "Enthalpy (kJ/mol)": 219,
        "Ore Grade (%)": 1.2,
        "Melting Point (C)": 1085,
        "Boiling Point (C)": 2562
    },
    "Lithium (Li)": {
        "Delta G (kJ/mol)": 300,
        "Electrode Potential (V)": -3.04,
        "Enthalpy (kJ/mol)": 650,
        "Ore Grade (%)": 1.5,
        "Melting Point (C)": 180.5,
        "Boiling Point (C)": 1342
    },
    "Nickel (Ni)": {
        "Delta G (kJ/mol)": -50,
        "Electrode Potential (V)": -0.25,
        "Enthalpy (kJ/mol)": 400,
        "Ore Grade (%)": 2,
        "Melting Point (C)": 1455,
        "Boiling Point (C)": 2913
    },
    "Zinc (Zn)": {
        "Delta G (kJ/mol)": -230,
        "Electrode Potential (V)": -0.76,
        "Enthalpy (kJ/mol)": 348,
        "Ore Grade (%)": 8,
        "Melting Point (C)": 419.5,
        "Boiling Point (C)": 907
    },
    "Cobalt (Co)": {
        "Delta G (kJ/mol)": -225,
        "Electrode Potential (V)": -0.28,
        "Enthalpy (kJ/mol)": 375,
        "Ore Grade (%)": 0.5,
        "Melting Point (C)": 1495,
        "Boiling Point (C)": 2927
    },
    "Platinum (Pt)": {
        "Delta G (kJ/mol)": 0,  # Replace None with 0 for safety
        "Electrode Potential (V)": 1.18,
        "Enthalpy (kJ/mol)": 1000,
        "Ore Grade (%)": 0.001,
        "Melting Point (C)": 1768,
        "Boiling Point (C)": 3825
    },
    "Gold (Au)": {
        "Delta G (kJ/mol)": 0,
        "Electrode Potential (V)": 1.50,
        "Enthalpy (kJ/mol)": 800,
        "Ore Grade (%)": 0.0005,
        "Melting Point (C)": 1064,
        "Boiling Point (C)": 2856
    }
}

# Select metal
metal_choice = st.selectbox("Select Metal", list(metal_data.keys()), help="Choose a metal to predict its extraction cost.")

# Show metal image if available
#if metal_choice in metal_images:
    #st.image(metal_images[metal_choice], width=150, caption=metal_choice)

# Editable inputs with default values from dictionary
st.write("### Adjust Metal Properties (override if desired):")

cols = st.columns(2)
with cols[0]:
    delta_g = st.number_input("ΔG (kJ/mol)", value=float(metal_data[metal_choice]["Delta G (kJ/mol)"]), step=1.0, format="%.2f", help="Gibbs Free Energy change during extraction")
    electrode_potential = st.number_input("Electrode Potential (V)", value=float(metal_data[metal_choice]["Electrode Potential (V)"]), step=0.01, format="%.2f", help="Electrode potential relative to standard hydrogen electrode")
    enthalpy = st.number_input("Enthalpy (kJ/mol)", value=float(metal_data[metal_choice]["Enthalpy (kJ/mol)"]), step=1.0, format="%.2f", help="Enthalpy change during extraction")
with cols[1]:
    ore_grade = st.number_input("Ore Grade (%)", value=float(metal_data[metal_choice]["Ore Grade (%)"]), min_value=0.0001, max_value=100.0, step=0.01, format="%.4f", help="Percentage of metal in ore")
    melting_point = st.number_input("Melting Point (C)", value=float(metal_data[metal_choice]["Melting Point (C)"]), step=1.0, format="%.2f", help="Temperature at which metal melts")
    boiling_point = st.number_input("Boiling Point (C)", value=float(metal_data[metal_choice]["Boiling Point (C)"]), step=1.0, format="%.2f", help="Temperature at which metal boils")

# Reset button to reset inputs to default values
if st.button("Reset All Inputs"):
    st.session_state.clear()
    st.rerun()


# Prepare input dataframe
features = [
    "Delta G (kJ/mol)",
    "Electrode Potential (V)",
    "Enthalpy (kJ/mol)",
    "Ore Grade (%)",
    "Melting Point (C)",
    "Boiling Point (C)"
]

input_df = pd.DataFrame([{
    "Delta G (kJ/mol)": delta_g,
    "Electrode Potential (V)": electrode_potential,
    "Enthalpy (kJ/mol)": enthalpy,
    "Ore Grade (%)": ore_grade,
    "Melting Point (C)": melting_point,
    "Boiling Point (C)": boiling_point
}])[features]

# Predict button
if st.button("Predict Extraction Cost"):
    prediction = model.predict(input_df)[0]
    st.success(f"Estimated Extraction Cost: ${prediction:,.2f} per ton")
    st.info(f"Model Mean Absolute Error (MAE): ±${MODEL_MAE}")

    # Prepare CSV for download
    csv_buffer = io.StringIO()
    input_df["Estimated Extraction Cost ($/ton)"] = prediction
    input_df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    st.download_button(
        label="Download prediction report as CSV",
        data=csv_data,
        file_name=f"{metal_choice.replace(' ', '_')}_extraction_cost.csv",
        mime="text/csv"
    )
