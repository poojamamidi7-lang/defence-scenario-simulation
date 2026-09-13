import streamlit as st

st.title("AI Defence Scenario Simulation Platform")

st.write("Welcome to the simulation platform!")

st.success("Website interface is working!")
import streamlit as st
import pandas as pd
import joblib
import sys
import os
import plotly.express as px


# =====================================================
# PROJECT PATH
# =====================================================

project_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, project_folder)

from models.simulation_engine import run_simulation


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Defence Scenario Simulation",
    page_icon="🎯",
    layout="wide"
)


# =====================================================
# CUSTOM STYLE
# =====================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #9aa0a6;
    margin-bottom: 25px;
}

.section-title {
    font-size: 26px;
    font-weight: 600;
    margin-top: 20px;
}

.result-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #1f2937;
    text-align: center;
    border: 1px solid #374151;
}

.result-value {
    font-size: 28px;
    font-weight: 700;
}

.result-label {
    font-size: 15px;
    color: #9ca3af;
}

.footer {
    text-align: center;
    color: #8b949e;
    margin-top: 40px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD MODEL
# =====================================================

model_path = os.path.join(
    project_folder,
    "models",
    "scenario_model.pkl"
)

model = joblib.load(model_path)





# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div class="main-title">🎯 AI Defence Scenario Simulation Platform</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Scenario Analysis • Readiness Assessment • ML Risk Prediction'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =====================================================
# SCENARIO INPUT
# =====================================================

st.markdown(
    '<div class="section-title">📋 Scenario Configuration</div>',
    unsafe_allow_html=True
)

st.write(
    "Configure the simulated scenario parameters below."
)

col1, col2 = st.columns(2)


with col1:

    weather = st.selectbox(
        "🌦️ Weather",
        ["Clear", "Rain", "Heavy Rain", "Fog", "Snow"]
    )

    visibility = st.slider(
        "👁️ Visibility (%)",
        min_value=20,
        max_value=100,
        value=60
    )

    equipment = st.slider(
        "⚙️ Equipment Readiness (%)",
        min_value=40,
        max_value=100,
        value=70
    )


with col2:

    terrain = st.selectbox(
        "🏔️ Terrain",
        ["Plain", "Mountain", "Desert", "Forest"]
    )

    communication = st.slider(
        "📡 Communication Availability (%)",
        min_value=40,
        max_value=100,
        value=70
    )

    resources = st.slider(
        "📦 Resource Availability (%)",
        min_value=40,
        max_value=100,
        value=70
    )


st.write("")

run_button = st.button(
    "▶️  RUN SIMULATION",
    type="primary",
    use_container_width=True
)


# =====================================================
# RUN SIMULATION
# =====================================================

if run_button:

    # Simulation engine
    readiness, simulation_risk, outcome = run_simulation(
        weather,
        visibility,
        equipment,
        communication,
        resources
    )


    # ML scenario
    scenario = pd.DataFrame({
        "weather": [weather],
        "visibility": [visibility],
        "equipment_readiness": [equipment],
        "communication": [communication],
        "resource_availability": [resources],
        "terrain": [terrain]
    })


    # ML prediction
    prediction = model.predict(scenario)

    probability = model.predict_proba(scenario)

    ml_risk = prediction[0]

    confidence = max(probability[0]) * 100


    # Save results
    st.session_state.baseline = {
        "readiness": readiness,
        "risk": simulation_risk,
        "outcome": outcome,
        "ml_risk": ml_risk,
        "confidence": confidence,
        "visibility": visibility,
        "weather": weather,
        "terrain": terrain,
        "equipment": equipment,
        "communication": communication,
        "resources": resources
    }


# =====================================================
# RESULTS
# =====================================================

if "baseline" in st.session_state:

    result = st.session_state.baseline

    st.divider()

    st.markdown(
        '<div class="section-title">📊 Simulation Results</div>',
        unsafe_allow_html=True
    )


    # Result cards
    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">READINESS SCORE</div>
                <div class="result-value">
                    {result["readiness"]}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">SIMULATION RISK</div>
                <div class="result-value">
                    {result["risk"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">OUTCOME</div>
                <div class="result-value">
                    {result["outcome"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.write("")


    # ML results
    col1, col2 = st.columns(2)


    with col1:

        st.subheader("🤖 ML Risk Prediction")

        st.info(
            f"Predicted Risk: **{result['ml_risk']}**"
        )


    with col2:

        st.subheader("🎯 Prediction Confidence")

        st.info(
            f"{result['confidence']:.2f}%"
        )


    # =================================================
    # SCENARIO SUMMARY
    # =================================================

    st.divider()

    st.subheader("📝 Scenario Summary")

    summary_col1, summary_col2 = st.columns(2)


    with summary_col1:

        st.write(
            f"**Weather:** {result['weather']}"
        )

        st.write(
            f"**Terrain:** {result['terrain']}"
        )

        st.write(
            f"**Visibility:** {result['visibility']}%"
        )


    with summary_col2:

        st.write(
            f"**Equipment Readiness:** "
            f"{result['equipment']}%"
        )

        st.write(
            f"**Communication:** "
            f"{result['communication']}%"
        )

        st.write(
            f"**Resource Availability:** "
            f"{result['resources']}%"
        )


    # =================================================
    # WHAT-IF ANALYSIS
    # =================================================

    st.divider()

    st.markdown(
        '<div class="section-title">🔄 What-If Analysis</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Change visibility and compare the modified "
        "scenario with the baseline."
    )


    new_visibility = st.slider(
        "Change Visibility (%)",
        min_value=20,
        max_value=100,
        value=result["visibility"],
        key="what_if_visibility"
    )


    if st.button(
        "🔍 ANALYZE WHAT-IF SCENARIO",
        use_container_width=True
    ):

        # Modified simulation
        new_readiness, new_risk, new_outcome = run_simulation(
            result["weather"],
            new_visibility,
            result["equipment"],
            result["communication"],
            result["resources"]
        )


        # Modified ML scenario
        new_scenario = pd.DataFrame({
            "weather": [result["weather"]],
            "visibility": [new_visibility],
            "equipment_readiness": [result["equipment"]],
            "communication": [result["communication"]],
            "resource_availability": [result["resources"]],
            "terrain": [result["terrain"]]
        })


        new_prediction = model.predict(new_scenario)

        new_probability = model.predict_proba(new_scenario)

        new_ml_risk = new_prediction[0]

        new_confidence = max(new_probability[0]) * 100


        # =============================================
        # COMPARISON
        # =============================================

        st.subheader("📈 Baseline vs What-If")


        col1, col2 = st.columns(2)


        with col1:

            st.markdown("### Baseline")

            st.metric(
                "Visibility",
                f"{result['visibility']}%"
            )

            st.metric(
                "Readiness",
                f"{result['readiness']}%"
            )

            st.write(
                f"Risk: **{result['risk']}**"
            )

            st.write(
                f"Outcome: **{result['outcome']}**"
            )


        with col2:

            st.markdown("### What-If")

            st.metric(
                "Visibility",
                f"{new_visibility}%"
            )

            st.metric(
                "Readiness",
                f"{new_readiness}%"
            )

            st.write(
                f"Risk: **{new_risk}**"
            )

            st.write(
                f"Outcome: **{new_outcome}**"
            )


        # Change
        change = round(
            new_readiness - result["readiness"],
            2
        )


        st.divider()

        st.metric(
            "Change in Readiness",
            f"{change:+.2f}%"
        )


        # =============================================
        # CHART
        # =============================================

        chart_data = pd.DataFrame({
            "Scenario": [
                "Baseline",
                "What-If"
            ],
            "Readiness": [
                result["readiness"],
                new_readiness
            ]
        })


        fig = px.bar(
            chart_data,
            x="Scenario",
            y="Readiness",
            text="Readiness",
            title="Readiness Comparison",
            range_y=[0, 100]
        )


        fig.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )


        fig.update_layout(
            height=450
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # =============================================
        # WHAT-IF ML RESULT
        # =============================================

        st.subheader("🤖 What-If ML Prediction")

        col1, col2 = st.columns(2)


        with col1:

            st.info(
                f"Predicted Risk: **{new_ml_risk}**"
            )


        with col2:

            st.info(
                f"Confidence: **{new_confidence:.2f}%**"
            )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    '<div class="footer">'
    'AI Defence Scenario Simulation Platform | '
    'Academic Software Prototype | '
    'Simulated Non-Sensitive Data'
    '</div>',
    unsafe_allow_html=True
)
