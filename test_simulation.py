from simulation_engine import run_simulation
# Test scenario
readiness, risk, outcome = run_simulation(
    weather="Heavy Rain",
    visibility=35,
    equipment_readiness=70,
    communication=55,
    resource_availability=55
)

print("========================================")
print("       SIMULATION ENGINE TEST")
print("========================================")

print("Readiness Score:", readiness)
print("Risk Level:", risk)
print("Outcome:", outcome)

print("========================================")