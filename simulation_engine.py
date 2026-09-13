def calculate_readiness(
    visibility,
    equipment_readiness,
    communication,
    resource_availability,
    weather
):
    # Calculate basic readiness
    score = (
        visibility * 0.20
        + equipment_readiness * 0.35
        + communication * 0.20
        + resource_availability * 0.25
    )

    # Weather effect
    weather_effect = {
        "Clear": 5,
        "Rain": 0,
        "Heavy Rain": -8,
        "Fog": -10,
        "Snow": -7
    }

    score = score + weather_effect.get(weather, 0)

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    return round(score, 2)


def determine_risk(readiness_score):

    if readiness_score >= 75:
        return "Low"

    elif readiness_score >= 55:
        return "Medium"

    else:
        return "High"


def determine_outcome(risk):

    if risk == "Low":
        return "Favourable"

    elif risk == "Medium":
        return "At Risk"

    else:
        return "High Risk"


def run_simulation(
    weather,
    visibility,
    equipment_readiness,
    communication,
    resource_availability
):

    readiness = calculate_readiness(
        visibility,
        equipment_readiness,
        communication,
        resource_availability,
        weather
    )

    risk = determine_risk(readiness)

    outcome = determine_outcome(risk)

    return readiness, risk, outcome