import streamlit as st
import requests
import math
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Statement Classifier",
    page_icon="🧭",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS (Animations + Icons)
# -----------------------------
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

<style>

body {
    background-color: #F5F7FA;
}

/* Fade-in animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Gauge needle animation */
@keyframes rotateNeedle {
    from {transform: rotate(-90deg);}
    to {transform: rotate(var(--needle-angle));}
}

/* Card styling */
.card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 25px;
    animation: fadeIn 0.6s ease-out;
}

.result-card {
    padding: 25px;
    border-radius: 16px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    animation: fadeIn 0.6s ease-out;
}

.explanation-card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    border-left: 6px solid #4A90E2;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-top: 20px;
    animation: fadeIn 0.8s ease-out;
}

/* Animated icon */
.animated-icon {
    font-size: 60px;
    margin-bottom: 10px;
    animation: fadeIn 0.8s ease-out;
}

/* Progress label */
.progress-label {
    font-weight: 600;
    margin-bottom: -8px;
}

/* Title */
.big-title {
    font-size: 42px;
    font-weight: 800;
    color: #2A4E9E;
    text-align: center;
    margin-bottom: -10px;
}

.subtitle {
    font-size: 20px;
    color: #4A4A4A;
    text-align: center;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<div class='big-title'>Statement Classifier</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analyze statements and visualize trustworthiness with animated confidence indicators</div>", unsafe_allow_html=True)

# -----------------------------
# INPUT SECTION
# -----------------------------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    statement = st.text_area("Statement", placeholder="Enter the statement to analyze...")
    speaker = st.text_input("Speaker", placeholder="Who said it?")
    context = st.text_input("Context", placeholder="Where was it said? (optional)")

    analyze = st.button("🔍 Run Analysis")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# API CALL
# -----------------------------
if analyze:
    if not statement.strip():
        st.error("Please enter a statement before running the analysis.")
    else:
        with st.spinner("Contacting API…"):

            # -----------------------------
            # YOUR CLASSIFICATION API CALL
            # -----------------------------
            api_url = "https://example.com/api/classify"
            payload = {
                "statement": statement,
                "speaker": speaker,
                "context": context
            }

            response = requests.post(api_url, json=payload)
            data = response.json()

            predicted_class = data["predicted_class"]
            probs = data["probabilities"]

        # -----------------------------
        # ICONS FOR CLASSES
        # -----------------------------
        icon_map = {
            "trustworthy": "<i class='fa-solid fa-circle-check'></i>",
            "questionable": "<i class='fa-solid fa-circle-exclamation'></i>",
            "unreliable": "<i class='fa-solid fa-circle-xmark'></i>"
        }

        # -----------------------------
        # COLOR MAPPING
        # -----------------------------
        color_map = {
            "trustworthy": "#2ECC71",
            "questionable": "#F5A623",
            "unreliable": "#D0021B"
        }

        main_color = color_map.get(predicted_class, "#4A90E2")
        icon_html = icon_map.get(predicted_class, "")

        # -----------------------------
        # RESULT CARD WITH ICON
        # -----------------------------
        st.markdown(f"""
        <div class='result-card' style='background:{main_color};'>
            <div class='animated-icon'>{icon_html}</div>
            <h2>Prediction: {predicted_class.title()}</h2>
        </div>
        """, unsafe_allow_html=True)

        # -----------------------------
        # CONFIDENCE GAUGE (Animated)
        # -----------------------------
        def gauge_html(value, label):
            angle = (value / 100) * 180 - 90  # -90° = left start
            return f"""
            <div style="text-align:center; margin-top:20px;">
                <svg width="260" height="140">
                    <path d="M20 120 A100 100 0 0 1 240 120" fill="none" stroke="#ddd" stroke-width="18"/>
                    <path d="M20 120 A100 100 0 0 1 240 120"
                          fill="none" stroke="{main_color}" stroke-width="18"
                          stroke-dasharray="314"
                          stroke-dashoffset="{314 - (value/100)*314}"
                          style="transition: stroke-dashoffset 1.2s ease-out;"/>
                    <g style="transform-origin:130px 120px; transform: rotate({angle}deg); transition: transform 1.2s ease-out;">
                        <rect x="128" y="20" width="4" height="100" fill="{main_color}" rx="2"/>
                    </g>
                </svg>
                <div style="font-size:22px; font-weight:700; color:#333;">{label}: {value:.1f}%</div>
            </div>
            """

        st.markdown(gauge_html(probs[predicted_class] * 100, predicted_class.title()), unsafe_allow_html=True)

        # -----------------------------
        # PROBABILITY BARS (Animated)
        # -----------------------------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Class Probabilities")

        for cls, val in probs.items():
            st.markdown(f"<div class='progress-label'>{cls.title()}</div>", unsafe_allow_html=True)
            st.progress(0)
            time.sleep(0.1)
            st.progress(val)

        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # SECOND API: EXPLANATION TEXT
        # -----------------------------
        st.subheader("Model Explanation")

        with st.spinner("Fetching explanation…"):

            explain_url = "https://example.com/api/explain"
            explain_payload = {"statement": statement}

            explain_response = requests.post(explain_url, json=explain_payload)
            explanation_text = explain_response.json().get("explanation", "")

        st.markdown(f"""
        <div class='explanation-card'>
            <h4><i class="fa-solid fa-lightbulb"></i> Explanation</h4>
            <p>{explanation_text}</p>
        </div>
        """, unsafe_allow_html=True)
