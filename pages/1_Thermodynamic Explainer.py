import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# -------------------------------
# Thermodynamic Data
# -------------------------------
metal_data = {
    "Fe₂O₃": {"ΔH": 824, "ΔS": 0.216, "cost": 120},
    "Al₂O₃": {"ΔH": 1676, "ΔS": 0.288, "cost": 1600},
    "CuO": {"ΔH": 155, "ΔS": 0.093, "cost": 3800},
    "ZnO": {"ΔH": 350, "ΔS": 0.115, "cost": 1800},
    "PbO": {"ΔH": 217, "ΔS": 0.125, "cost": 2100},
}

# -------------------------------
# Main Content
# -------------------------------
st.title("🧪 Thermodynamic Assumptions & Chemistry Explained")

st.markdown("""
This page explains how the **chemical and thermodynamic properties** used in the extraction cost model affect real-world metallurgy and commodity pricing.
""")

st.markdown("---")
st.markdown("### 🔥 1. Temperature Dependence of ΔG")
st.markdown("Gibbs Free Energy is temperature-dependent:")
st.latex(r"\Delta G = \Delta H - T\Delta S")
st.markdown("At high temperatures, reactions with positive enthalpy (ΔH) may still proceed due to entropy gains (ΔS).")

st.markdown("---")
st.markdown("### ⚡ 2. Electrode Potentials Are Not Fixed")
st.markdown("Standard electrode potentials ($E^\\circ$) change with:")
st.markdown("- Ion concentration  \n- pH of solution  \n- Temperature")
st.markdown("They are governed by the Nernst equation:")
st.latex(r"E = E^\circ - \frac{0.0591}{n} \log \frac{[\text{Red}]}{[\text{Ox}]}")

st.markdown("---")
st.markdown("### 🪨 3. Ore Composition and Extraction Energy")
st.markdown(
    "The **form in which a metal is found** (oxide, sulfide, carbonate, etc.) greatly affects the energy required to extract it.\n\n"
    "- **Oxides**: easier to reduce (e.g., Fe₂O₃)  \n"
    "- **Sulfides**: require roasting and extra steps (e.g., CuFeS₂)"
)

st.markdown("---")
st.markdown("### 📈 4. Real-World Cost ≠ Theoretical ΔG")
st.markdown(
    "While thermodynamics gives a baseline, actual costs depend on:\n\n"
    "- Ore grade and impurities  \n"
    "- Environmental regulations  \n"
    "- Energy source (coal vs hydro)  \n"
    "- Scale of operation"
)
st.markdown(
    "This is why machine learning helps bridge the **gap between chemistry and economics**."
)

st.markdown("---")
st.markdown("### 💡 Why This Matters")
st.markdown(
    "Understanding these principles helps explain **why metals like platinum or lithium** are expensive to extract — not just due to rarity, but **due to unfavorable reaction conditions or electrochemical instability**."
)

# -------------------------------
# Animated Plot Section
# -------------------------------
st.title("🔺 ΔG vs Temperature Curve Animation")

# Dropdown for metal selection
metal_choice = st.selectbox("Choose a metal oxide:", list(metal_data.keys()))
delta_H = metal_data[metal_choice]["ΔH"]
delta_S = metal_data[metal_choice]["ΔS"]

# Display current equation with values
st.latex(fr"\Delta G = {delta_H} - T \times {delta_S}")

# Animation trigger
if st.button("▶️ Animate Curve"):
    placeholder = st.empty()
    T = np.linspace(300, 2000, 500)

    for i in range(10, len(T), 10):
        temp_slice = T[:i]
        delta_G_slice = delta_H - temp_slice * delta_S

        fig, ax = plt.subplots()
        ax.plot(temp_slice, delta_G_slice, color='blue')
        ax.axhline(0, color='red', linestyle='--')
        ax.set_xlim(300, 2000)
        ax.set_ylim(min(delta_G_slice.min(), -300), max(delta_G_slice.max(), 300))
        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel("ΔG (kJ/mol)")
        ax.set_title(f"ΔG vs T for {metal_choice}")

        placeholder.pyplot(fig)
        time.sleep(0.05)

# ---------------------------------------
# Scatter Plot: ΔG₃₀₀K vs Cost
# ---------------------------------------
st.markdown("---")
st.title("📊 ΔG at 300K vs Extraction Cost")

st.markdown(
    "This chart shows how thermodynamic favorability (ΔG at 300 K) correlates with real-world metal extraction cost. "
    "**Lower ΔG doesn't always mean lower cost**, because industrial factors (e.g. ore quality, energy source) also matter."
)

# Prepare data
metal_names = []
g300_values = []
cost_values = []

for metal, data in metal_data.items():
    g_300 = data["ΔH"] - 300 * data["ΔS"]
    metal_names.append(metal)
    g300_values.append(g_300)
    cost_values.append(data["cost"])

# Plotting
fig, ax = plt.subplots()
ax.scatter(g300_values, cost_values)

# Annotate each point
for i, metal in enumerate(metal_names):
    ax.annotate(metal, (g300_values[i], cost_values[i]), textcoords="offset points", xytext=(5,5), ha='left')

ax.set_xlabel("ΔG at 300K (kJ/mol)")
ax.set_ylabel("Estimated Extraction Cost ($/ton)")
ax.set_title("ΔG₃₀₀K vs Extraction Cost for Metal Oxides")

st.pyplot(fig)
