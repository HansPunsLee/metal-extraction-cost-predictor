import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


st.title("🧪 Thermodynamic Assumptions & Chemistry Explained")

st.markdown("""
This page explains how the **chemical and thermodynamic properties** used in the extraction cost model affect real-world metallurgy and commodity pricing.

---

### 🔥 1. Temperature Dependence of ΔG

Gibbs Free Energy is temperature-dependent:

\\[
\\Delta G = \\Delta H - T\\Delta S
\\]

At high temperatures, reactions with positive enthalpy (ΔH) may still proceed due to entropy gains (ΔS).

---

### ⚡ 2. Electrode Potentials Are Not Fixed

Standard electrode potentials (E°) change with:

- Ion concentration
- pH of solution
- Temperature

They are governed by the Nernst equation:

\\[
E = E^\\circ - \\frac{0.0591}{n} \\log \\frac{[\\text{Red}]}{[\\text{Ox}]}
\\]

---

### 🪨 3. Ore Composition and Extraction Energy

The **form in which a metal is found** (oxide, sulfide, carbonate, etc.) greatly affects the energy required to extract it.

- Oxides: easier to reduce (e.g., Fe₂O₃)
- Sulfides: require roasting and extra steps (e.g., CuFeS₂)

---

### 📈 4. Real-World Cost ≠ Theoretical ΔG

While thermodynamics gives a baseline, actual costs depend on:

- Ore grade and impurities
- Environmental regulations
- Energy source (coal vs hydro)
- Scale of operation

This is why machine learning helps bridge the **gap between chemistry and economics**.

---

### 💡 Why This Matters

Understanding these principles helps explain **why metals like platinum or lithium** are expensive to extract — not just due to rarity, but **due to unfavorable reaction conditions or electrochemical instability**.
""")

st.title("🔺 ΔG vs Temperature Curve")

st.markdown("This plot shows how ΔG = ΔH - TΔS changes with temperature.")

# Constants for a mock metal oxide reduction
delta_H = 200  # kJ/mol
delta_S = 0.15  # kJ/mol·K

T = np.linspace(300, 2000, 500)
delta_G = delta_H - T * delta_S

# Plot
fig, ax = plt.subplots()
ax.plot(T, delta_G)
ax.axhline(0, color='red', linestyle='--')
ax.set_xlabel("Temperature (K)")
ax.set_ylabel("ΔG (kJ/mol)")
ax.set_title("ΔG vs T for a metal extraction reaction")

st.pyplot(fig)

delta_H = st.slider("ΔH (kJ/mol)", 50, 400, 200)
delta_S = st.slider("ΔS (kJ/mol·K)", 0.05, 0.3, 0.15)
