import pandas as pd
import numpy as np

# Make the results reproducible
np.random.seed(42)

# Number of simulated scenarios
number_of_scenarios = 1000

# Generate scenario data
data = {
    "weather": np.random.choice(
        ["Clear", "Rain", "Heavy Rain", "Fog", "Snow"],
        number_of_scenarios
    ),

    "visibility": np.random.randint(
        20, 101, number_of_scenarios
    ),

    "equipment_readiness": np.random.randint(
        40, 101, number_of_scenarios
    ),

    "communication": np.random.randint(
        40, 101, number_of_scenarios
    ),

    "resource_availability": np.random.randint(
        40, 101, number_of_scenarios
    ),

    "terrain": np.random.choice(
        ["Plain", "Mountain", "Desert", "Forest"],
        number_of_scenarios
    )
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate a simulated readiness score
df["readiness_score"] = (
    df["visibility"] * 0.20
    + df["equipment_readiness"] * 0.35
    + df["communication"] * 0.20
    + df["resource_availability"] * 0.25
)

# Add weather effect
weather_effect = {
    "Clear": 5,
    "Rain": 0,
    "Heavy Rain": -8,
    "Fog": -10,
    "Snow": -7
}

df["readiness_score"] = (
    df["readiness_score"]
    + df["weather"].map(weather_effect)
)

# Keep score between 0 and 100
df["readiness_score"] = df["readiness_score"].clip(0, 100)

# Create risk level
def calculate_risk(score):
    if score >= 75:
        return "Low"
    elif score >= 55:
        return "Medium"
    else:
        return "High"

df["scenario_risk"] = df["readiness_score"].apply(calculate_risk)

# Create simulated outcome
def calculate_outcome(risk):
    if risk == "Low":
        return "Favourable"
    elif risk == "Medium":
        return "At Risk"
    else:
        return "High Risk"

df["outcome"] = df["scenario_risk"].apply(calculate_outcome)

# Save dataset
df.to_csv(
    "data/defence_scenario_data.csv",
    index=False
)

print("Dataset created successfully!")
print("Number of scenarios:", len(df))
print("\nFirst 5 scenarios:")
print(df.head())