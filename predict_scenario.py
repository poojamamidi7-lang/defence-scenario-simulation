import pandas as pd
import joblib

# Load trained model
model = joblib.load("models/scenario_model.pkl")

print("========================================")
print(" DEFENCE SCENARIO PREDICTION SYSTEM")
print("========================================")

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

# Create new scenario
new_scenario = pd.DataFrame({
    "weather": [weather],
    "visibility": [visibility],
    "equipment_readiness": [equipment_readiness],
    "communication": [communication],
    "resource_availability": [resource_availability],
    "terrain": [terrain]
})

# Predict risk
prediction = model.predict(new_scenario)

# Prediction probabilities
probability = model.predict_proba(new_scenario)

risk = prediction[0]

print("\n========================================")
print("           SIMULATION RESULT")
print("========================================")

print("Weather:", weather)
print("Terrain:", terrain)
print("Visibility:", visibility, "%")
print("Equipment Readiness:", equipment_readiness, "%")
print("Communication:", communication, "%")
print("Resource Availability:", resource_availability, "%")

print("\nPredicted Risk:", risk)

confidence = max(probability[0]) * 100

print("Prediction Confidence:", round(confidence, 2), "%")

print("========================================")