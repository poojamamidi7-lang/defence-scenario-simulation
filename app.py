import streamlit as st
import pandas as pd
import joblib
import os
import sys
import plotly.express as px

# --------------------------------------------------
# PROJECT SETUP
# --------------------------------------------------

project_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_folder)

from simulation_engine import run_simulation

model_path = os.path.join(project_folder, "scenario_model.pkl")

model = joblib.load(model_path)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Defence Scenario Simulation",
    page_icon="🛡️",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-bottom: 15px;
    }

    .result-title {
        font-size: 16px;
        font-weight: 600;
    }

    .result-value {
        font-size: 28px;
        font-weight: 700;
    }

    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 15px;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🛡️ AI Defence Scenario Simulation Platform</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-based scenario simulation, readiness assessment and outcome prediction</div>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# SCENARIO CONFIGURATION
# --------------------------------------------------

st.subheader("⚙️ Scenario Configuration")

col1, col2 = st.columns(2)

with col1:

    weather = st.selectbox(
        "Weather Condition",
        [
            "Clear",
            "Rain",
            "Heavy Rain",
            "Fog",
            "Snow"
        ]
    )

    terrain = st.selectbox(
        "Terrain",
        [
            "Plain",
            "Mountain",
            "Desert",
            "Forest"
        ]
    )

    visibility = st.slider(
        "Visibility (%)",
        min_value=20,
        max_value=100,
        value=80
    )


with col2:

    equipment_readiness = st.slider(
        "Equipment Readiness (%)",
        min_value=40,
        max_value=100,
        value=70
    )

    communication = st.slider(
        "Communication Availability (%)",
        min_value=40,
        max_value=100,
        value=70
    )

    resource_availability = st.slider(
        "Resource Availability (%)",
        min_value=40,
        max_value=100,
        value=70
    )


st.write("")

run_button = st.button(
    "🚀 Run Simulation",
    use_container_width=True
)


# --------------------------------------------------
# RUN SIMULATION
# --------------------------------------------------

if run_button:

    # Simulation engine
    readiness, simulation_risk, outcome = run_simulation(
        weather,
        visibility,
        equipment_readiness,
        communication,
        resource_availability
    )

    # ML prediction
    input_data = pd.DataFrame(
        {
            "weather": [weather],
            "visibility": [visibility],
            "equipment_readiness": [equipment_readiness],
            "communication": [communication],
            "resource_availability": [resource_availability],
            "terrain": [terrain]
        }
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    confidence = max(probabilities) * 100


    # Store values
    st.session_state["readiness"] = readiness
    st.session_state["simulation_risk"] = simulation_risk
    st.session_state["outcome"] = outcome
    st.session_state["prediction"] = prediction
    st.session_state["confidence"] = confidence


    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    st.divider()

    st.subheader("📊 Simulation Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Readiness Score",
            f"{readiness:.2f}%"
        )

    with col2:

        st.metric(
            "Simulation Risk",
            simulation_risk
        )

    with col3:

        st.metric(
            "Outcome",
            outcome
        )

    with col4:

        st.metric(
            "ML Prediction",
            prediction
        )


    # --------------------------------------------------
    # ML CONFIDENCE
    # --------------------------------------------------

    st.subheader("🤖 AI Prediction")

    st.write(
        f"The machine-learning model predicts **{prediction} Risk** "
        f"with approximately **{confidence:.1f}% confidence**."
    )


    # --------------------------------------------------
    # SCENARIO SUMMARY
    # --------------------------------------------------

    st.subheader("📋 Scenario Summary")

    summary = pd.DataFrame(
        {
            "Parameter": [
                "Weather",
                "Terrain",
                "Visibility",
                "Equipment Readiness",
                "Communication",
                "Resource Availability"
            ],

            "Value": [
                weather,
                terrain,
                f"{visibility}%",
                f"{equipment_readiness}%",
                f"{communication}%",
                f"{resource_availability}%"
            ]
        }
    )

    st.table(summary)


    # --------------------------------------------------
    # READINESS CHART
    # --------------------------------------------------

    st.subheader("📈 Readiness Analysis")

    chart_data = pd.DataFrame(
        {
            "Parameter": [
                "Visibility",
                "Equipment",
                "Communication",
                "Resources"
            ],

            "Score": [
                visibility,
                equipment_readiness,
                communication,
                resource_availability
            ]
        }
    )

    fig = px.bar(
        chart_data,
        x="Parameter",
        y="Score",
        title="Scenario Readiness Factors",
        range_y=[0, 100]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# WHAT-IF ANALYSIS
# --------------------------------------------------

st.divider()

st.subheader("🔄 What-If Analysis")

st.write(
    "Change the visibility condition and compare the new "
    "readiness with the original scenario."
)

what_if_visibility = st.slider(
    "What-If Visibility (%)",
    min_value=20,
    max_value=100,
    value=50
)


if st.button(
    "🔍 Analyze What-If Scenario",
    use_container_width=True
):

    what_if_readiness, what_if_risk, what_if_outcome = run_simulation(
        weather,
        what_if_visibility,
        equipment_readiness,
        communication,
        resource_availability
    )

    if "readiness" in st.session_state:

        baseline = st.session_state["readiness"]

        change = what_if_readiness - baseline

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Baseline Readiness",
                f"{baseline:.2f}%"
            )

        with col2:

            st.metric(
                "What-If Readiness",
                f"{what_if_readiness:.2f}%"
            )

        with col3:

            st.metric(
                "Change",
                f"{change:+.2f}%"
            )


        st.write(
            f"**What-If Risk:** {what_if_risk}"
        )

        st.write(
            f"**What-If Outcome:** {what_if_outcome}"
        )

    else:

        st.info(
            "Run the main simulation first, then perform What-If Analysis."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div class="footer">
    Academic Prototype | AI-Based Defence Scenario Simulation<br>
    Uses simulated, non-sensitive data for educational purposes.
    </div>
    """,
    unsafe_allow_html=True
)
