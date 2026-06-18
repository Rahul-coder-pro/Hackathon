import streamlit as st
import alpha
import subprocess
import threading
import time
import speech_recognition as sr

# --- Auto-start local server for camera.html ---
def start_server():
    subprocess.run(["python", "-m", "http.server", "8000"])

threading.Thread(target=start_server, daemon=True).start()
time.sleep(2)  # give server a moment to start

# --- Streamlit UI setup ---
st.set_page_config(
    page_title="AlphaVision",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark neon futuristic CSS
st.markdown(
    """
    <style>
    body {
        background-color: #0d0d0d;
        color: #39ff14;
        font-family: 'Orbitron', sans-serif;
    }
    h1, h2, label, p {
        color: #00ffff !important;
        text-shadow: 0px 0px 15px #ff00ff;
    }
    .stTextInput>div>input {
        background-color: #1a1a1a;
        color: #39ff14;
        border: 2px solid #00ffff;
        border-radius: 8px;
        box-shadow: 0px 0px 15px #ff00ff;
    }
    img.logo {
        width: 90px;
        margin: 15px;
        transition: 0.3s;
        cursor: pointer;
        border-radius: 12px;
        box-shadow: 0px 0px 15px #00ffff;
    }
    img.logo:hover {
        transform: scale(1.2);
        box-shadow: 0px 0px 25px #00ffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 AlphaVision")
st.write("Created By Code Smashers Members")

# Global engine reference for stopping speech
engine = None

def stop_speech():
    global engine
    if engine is not None:
        engine.stop()
        st.warning("🛑 Alpha stopped speaking.")

# Tabs
tab1, tab2 = st.tabs(["🎙️ Alpha Assistant", "📷 AI Camera"])

# --- Tab 1: Alpha Assistant ---
with tab1:
    st.markdown(
        "<h2 style='color:#00ffff; text-shadow:0px 0px 20px #ff00ff;'>Alpha Assistant</h2>",
        unsafe_allow_html=True
    )

    command = st.text_input("Type your command:")

    # Clickable neon logos 
    st.markdown(
        """
        <div style="display:flex; justify-content:center; gap:50px; margin-top:20px;">
            <a href="https://google.com" target="_blank">
                <img src="http://localhost:8000/static/google.png" class="logo">
            </a>
            <a href="https://youtube.com" target="_blank">
                <img src="http://localhost:8000/static/youtube.png" class="logo">
            </a>
            <a href="https://timesofindia.indiatimes.com" target="_blank">
                <img src="http://localhost:8000/static/news.png" class="logo">
            </a>
            <a href="https://netflix.com" target="_blank">
                <img src="http://localhost:8000/static/netflix.png" class="logo">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    song = st.text_input("Enter song name to play:")
    if st.button("Play Song"):
        alpha.comm(f"play {song}")

    if st.button("Run Command"):
        try:
            with st.spinner("⚡ Processing your command..."):
                alpha.comm(command)
            st.success("Command executed successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    # NEW Stop Speaking button
    if st.button("Stop Speaking"):
        stop_speech()

    st.markdown("### 🎤 Voice Command")
    st.info("Voice input works via your microphone (requires Chrome/Edge).")
    if st.button("Activate Voice Command"):
        try:
            r = sr.Recognizer()
            with st.spinner("🎤 Listening..."):
                with sr.Microphone() as source:
                    audio = r.listen(source, timeout=3, phrase_time_limit=3)
            with st.spinner("🧠 Recognizing..."):
                voice_text = r.recognize_google(audio)
            st.write(f"You said: {voice_text}")
            alpha.comm(voice_text)
        except Exception as e:
            st.error(f"Voice command error: {e}")

# --- Tab 2: AI Camera ---
with tab2:
    st.header("AI Camera Assistant")
    st.write("Object detection + speech output using TensorFlow.js")

    st.markdown(
    """
    <a href="http://localhost:8000/camera.html" target="_blank"
       style="background:linear-gradient(90deg,#ff00ff,#00ffff);
              padding:12px 24px;
              border-radius:12px;
              color:white;
              text-decoration:none;
              font-weight:bold;
              box-shadow:0px 0px 15px #00ffff;">
       🚀 Launch AI Camera
    </a>
    """,
    unsafe_allow_html=True
)

