import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual theme
sns.set(style='whitegrid', palette='Set2')

# 1. Load Data
data = {
    "ClientID": [101, 102, 103, 104, 105, 106],
    "Segment": ["Medium Corporate", "Small Corporate", "Small Corporate", "Medium Corporate", "Medium Corporate", "Small Corporate"],
    "Industry": ["Transportation and Storage", "Transportation and Storage", "Manufacturing", "Construction", "Agriculture, Forestry and Fishing", "Transportation and Storage"],
    "Country": ["Lithuania", "Estonia", "Lithuania", "Lithuania", "Latvia", "Lithuania"],
    "Financed Amount": [405639, 19642, 167375, 239927, 221043, 3099],
    "CO2 (tons)": [3184, 562, 987, 1922, 998, 944],
    "Energy Consumption (MWh)": [4323, 1922, 2832, 4177, 4738, 1375],
    "Water Usage (thousand m3)": [3691, 1348, 6692, 10446, 13471, 979],
    "Water Stress": [0.76, 0.48, 0.47, 0.76, 0.38, 0.79],
    "Flood Risk": [0.47, 0.66, 0.43, 0.45, 0.56, 0.39],
    "Drought Risk": [0.65, 0.20, 0.67, 0.62, 0.59, 0.62],
    "Report_Date": ["03/2023"] * 6
}

df = pd.DataFrame(data)

# 2. Derived Columns
df["CO2 per €k"] = df["CO2 (tons)"] / (df["Financed Amount"] / 1000)
df["Energy per €k"] = df["Energy Consumption (MWh)"] / (df["Financed Amount"] / 1000)
df["Water per €k"] = df["Water Usage (thousand m3)"] / (df["Financed Amount"] / 1000)
df["Total Risk"] = df[["Water Stress", "Flood Risk", "Drought Risk"]].mean(axis=1)

# 3. Descriptive Statistics
print("Descriptive Statistics:")
print(df.describe(include='all'))

# 4. Visualizations Directory (optional)
import os
os.makedirs("plots", exist_ok=True)

# 5. Visualizations

# Barplot: Financed Amount by Country
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Country", y="Financed Amount", estimator=sum, ci=None)
plt.title("Total Financed Amount by Country")
plt.savefig("plots/financed_by_country.png")
plt.close()

# Boxplot: Water Stress by Segment
plt.figure(figsize=(7, 5))
sns.boxplot(data=df, x="Segment", y="Water Stress")
plt.title("Water Stress by Company Segment")
plt.savefig("plots/water_stress_segment.png")
plt.close()

# Barplot: Average CO2 by Industry
plt.figure(figsize=(10, 5))
sns.barplot(data=df, x="Industry", y="CO2 (tons)", estimator='mean')
plt.title("Average CO2 Emissions by Industry")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("plots/co2_by_industry.png")
plt.close()

# Scatter: Financed vs CO2
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Financed Amount", y="CO2 (tons)", hue="Segment", style="Country", s=100)
plt.title("Financed Amount vs CO2 Emissions")
plt.savefig("plots/financed_vs_co2.png")
plt.close()

# Heatmap: Correlation Matrix
plt.figure(figsize=(10, 6))
sns.heatmap(df.select_dtypes(include='number').corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.savefig("plots/correlation_matrix.png")
plt.close()

# Barplot: CO2 per €k by Client
plt.figure(figsize=(9, 5))
sns.barplot(data=df, x="ClientID", y="CO2 per €k", hue="Segment")
plt.title("CO2 Intensity per €k Financed")
plt.savefig("plots/co2_per_euro.png")
plt.close()

# Risk Radar (Spider Plot) by Client
import numpy as np

categories = ["Water Stress", "Flood Risk", "Drought Risk"]
N = len(categories)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # Close the loop

plt.figure(figsize=(8, 8))
for i, row in df.iterrows():
    values = row[categories].tolist()
    values += values[:1]
    plt.polar(angles, values, label=f"Client {row['ClientID']}")

plt.xticks(angles[:-1], categories)
plt.title("Risk Profile Radar Chart")
plt.legend(loc='upper right')
plt.savefig("plots/risk_radar_chart.png")
plt.close()

# Pairplot: Risks
sns.pairplot(df, vars=["Water Stress", "Flood Risk", "Drought Risk"], hue="Country")
plt.savefig("plots/risk_pairplot.png")
plt.close()

# Histogram: Total Risk Distribution
plt.figure(figsize=(6, 4))
sns.histplot(df["Total Risk"], bins=5, kde=True)
plt.title("Distribution of Total Environmental Risk")
plt.savefig("plots/total_risk_dist.png")
plt.close()

# Barplot: Energy Usage per €k
plt.figure(figsize=(9, 5))
sns.barplot(data=df, x="ClientID", y="Energy per €k", hue="Country")
plt.title("Energy Intensity per €k Financed")
plt.savefig("plots/energy_per_euro.png")
plt.close()

# 6. Export Cleaned Data
df.to_csv("cleaned_environmental_finance_data.csv", index=False)

# 7. Optional Summary Table
summary = df.groupby("Country")[["Financed Amount", "CO2 (tons)", "Water Usage (thousand m3)", "Energy Consumption (MWh)"]].sum()
summary.to_csv("country_summary.csv")

print("✅ Analysis complete. All plots saved in the 'plots' folder.")
