import pandas as pd
import joblib

from models.simulation_engine import run_simulation


# Load ML model
model = joblib.load("models/scenario_model.pkl")

print("========================================")
print("   AI DEFENCE SCENARIO SIMULATION")
print("========================================")

# Get scenario inputs
weather = input(
    "Enter weather (Clear/Rain/Heavy Rain/Fog/Snow): "
)

terrain = input(
    "Enter terrain (Plain/Mountain/Desert/Forest): "
)

visibility = float(
    input("Enter visibility percentage (20-100): ")
)

equipment_readiness = float(
    input("Enter equipment readiness (40-100): ")
)

communication = float(
    input("Enter communication availability (40-100): ")
)

resource_availability = float(
    input("Enter resource availability (40-100): ")
)


# -----------------------------------------
# SIMULATION ENGINE
# -----------------------------------------

readiness, simulation_risk, outcome = run_simulation(
    weather,
    visibility,
    equipment_readiness,
    communication,
    resource_availability
)


# -----------------------------------------
# ML MODEL
# -----------------------------------------

new_scenario = pd.DataFrame({
    "weather": [weather],
    "visibility": [visibility],
    "equipment_readiness": [equipment_readiness],
    "communication": [communication],
    "resource_availability": [resource_availability],
    "terrain": [terrain]
})

prediction = model.predict(new_scenario)

probability = model.predict_proba(new_scenario)

ml_risk = prediction[0]

confidence = max(probability[0]) * 100


# -----------------------------------------
# FINAL RESULT
# -----------------------------------------

print("\n========================================")
print("          SIMULATION RESULT")
print("========================================")

print("Readiness Score:", readiness)
print("Simulation Risk:", simulation_risk)
print("Outcome:", outcome)

print("\nML Predicted Risk:", ml_risk)
print("ML Prediction Confidence:",
      round(confidence, 2), "%")

print("========================================")