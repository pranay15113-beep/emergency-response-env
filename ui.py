import streamlit as st # type: ignore
from env.environment import EmergencyEnv
import time
import random

st.set_page_config(layout="wide")

# -------------------- CSS --------------------
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: url("https://images.unsplash.com/photo-1496588152823-86ff7695e68f") no-repeat center center fixed;
    background-size: cover;
}

/* DARK OVERLAY */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(5, 10, 20, 0.75);
    z-index: -1;
}

/* REMOVE HEADER */
[data-testid="stHeader"] {
    background: transparent;
}

/* GLASS PANEL */
.glass {
    background: rgba(0, 10, 25, 0.55);
    backdrop-filter: blur(15px);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #4cc9ff, #1a73e8);
    border-radius: 12px;
    border: none;
    color: white;
    font-size: 18px;
    padding: 10px 20px;
}

/* FADE */
.fade {
    animation: fadeIn 1s;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

</style>
""", unsafe_allow_html=True)

# -------------------- HERO (FIXED) --------------------
st.markdown("""
<div style="text-align:center; margin-top:60px;">
    <h1 style="
        color: #ffffff;
        font-size: 60px;
        font-weight: 900;
        text-shadow: 0px 5px 25px rgba(0,0,0,0.9),
                     0px 10px 12px rgba(0,180,255,0.7),
                     0px 10px 25px rgba(0,180,255,0.5);
                                  ">
        🚨 Emergency AI Command Center
    </h1>

   <p style="color:#e0e0e0; font-size:18px; margin-top:-10px; text-shadow:0px 3px 10px rgba(0,0,0,0.8),0px 10px 12px rgba(0,180,255,0.7),
                     0px 10px 25px rgba(0,180,255,0.5);">
        AI-powered crisis response simulation system
    </p>
</div>
""", unsafe_allow_html=True)
st.write("")

env = EmergencyEnv()

# -------------------- BUTTON --------------------
generate = st.button("⚡ Initiate Simulation")

if generate:
    with st.spinner("Initializing..."):
        time.sleep(1.2)
        obs = env.reset()

    st.markdown("<h2 class='fade'>📍 Active Incidents</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # INCIDENTS
    with col1:
        for i, incident in enumerate(obs):
            st.markdown(f"""
            <div class="glass fade">
            <h3>🔥 Incident {i+1}</h3>
            <p><b>Type:</b> {incident['incident_type']}</p>
            <p><b>Location:</b> {incident['location']}</p>
            <p><b>Severity:</b> {incident['severity']}</p>
            <p><b>Required:</b> {incident['required']}</p>
            </div>
            """, unsafe_allow_html=True)

    # AI RESPONSE
    with col2:
        st.markdown("<h2 class='fade'>🤖 AI Response</h2>", unsafe_allow_html=True)

        with st.spinner("AI analyzing..."):
            time.sleep(1.5)

        ai_actions = [i["required"] for i in obs]

        for i, act in enumerate(ai_actions):
            st.markdown(f"""
            <div class="glass fade">
            <h3>🚑 Response {i+1}</h3>
            <p>{act}</p>
            </div>
            """, unsafe_allow_html=True)

    # HUMAN SIMULATION
    human_actions = [
        {k: max(0, v + random.randint(-1, 1)) for k, v in i["required"].items()}
        for i in obs
    ]

    _, ai_reward, _, _ = env.step(ai_actions)
    _, human_reward, _, _ = env.step(human_actions)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🤖 AI Score")
        st.progress(ai_reward)

    with col4:
        st.markdown("### 🧑 Human Score")
        st.progress(human_reward)

    # FINAL RESULT
    st.markdown("## ⭐ System Performance")

    if ai_reward > 0.8:
        st.success(f"AI RESPONSE OPTIMAL — Score: {ai_reward:.2f}")
    elif ai_reward > 0.5:
        st.warning(f"AI RESPONSE MODERATE — Score: {ai_reward:.2f}")
    else:
        st.error(f"AI RESPONSE FAILED — Score: {ai_reward:.2f}")
        