import pandas as pd

data = {
    "Metal": ["Aluminum", "Copper", "Lithium", "Nickel", "Zinc", "Cobalt", "Platinum", "Gold"],
    "Extraction_Method": ["Electrolysis", "Pyrometallurgy", "Hydrometallurgy", "Combo", "Roast+Electro", "Combo", "Smelting", "Cyanidation"],
    "Delta G (kJ/mol)": [900, -146, 300, -50, -230, -225, None, None],
    "Electrode Potential (V)": [-1.66, 0.34, -3.04, -0.25, -0.76, -0.28, 1.18, 1.50],
    "Enthalpy (kJ/mol)": [1170, 219, 650, 400, 348, 375, 1000, 800],
    "Ore Grade (%)": [40, 1.2, 1.5, 2, 8, 0.5, 0.001, 0.0005],
    "Melting Point (C)": [660, 1085, 180.5, 1455, 419.5, 1495, 1768, 1064],
    "Boiling Point (C)": [2519, 2562, 1342, 2913, 907, 2927, 3825, 2856]
}

df = pd.DataFrame(data)
df.to_csv("C:\\Users\\Admin\\Desktop\\Commodities ML\\metal_properties.csv", index=False)
print("CSV file generated as 'metal_properties.csv'")

import os
print("Current working directory:", os.getcwd())
