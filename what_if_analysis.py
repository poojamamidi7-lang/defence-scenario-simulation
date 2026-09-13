from models.simulation_engine import run_simulation


print("========================================")
print("          WHAT-IF ANALYSIS")
print("========================================")


# BASELINE SCENARIO
print("\nBASELINE SCENARIO")

weather = input("Enter weather: ")
visibility = float(input("Enter visibility: "))
equipment = float(input("Enter equipment readiness: "))
communication = float(input("Enter communication: "))
resources = float(input("Enter resource availability: "))

baseline_readiness, baseline_risk, baseline_outcome = run_simulation(
    weather,
    visibility,
    equipment,
    communication,
    resources
)


# WHAT-IF SCENARIO
print("\nWHAT-IF SCENARIO")
print("Change visibility only.")

new_visibility = float(
    input("Enter new visibility: ")
)

new_readiness, new_risk, new_outcome = run_simulation(
    weather,
    new_visibility,
    equipment,
    communication,
    resources
)


# COMPARISON
print("\n========================================")
print("             COMPARISON")
print("========================================")

print("\nBaseline:")
print("Readiness:", baseline_readiness)
print("Risk:", baseline_risk)
print("Outcome:", baseline_outcome)

print("\nWhat-If:")
print("Readiness:", new_readiness)
print("Risk:", new_risk)
print("Outcome:", new_outcome)

print("\nChange in Readiness:",
      round(new_readiness - baseline_readiness, 2))

print("========================================")