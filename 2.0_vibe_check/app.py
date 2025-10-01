import streamlit as st
from vibe_model import analyze_vibes
import time

# Streamlit UI setup
st.set_page_config(page_title="Vibe Check", page_icon="✨", layout="centered")

st.title("✨ Vibe Check App")
st.write("Paste a chat or message below to check the conversation vibe 👇")

# Session state to track button click
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

user_input = st.text_area("Enter your message:")

def get_summary(results):
    """Generate an intelligent summary based on sentiment, emotion, and sarcasm."""
    sentiment = results['sentiment']['label']
    emotion = results['emotion']['label']
    sarcasm = results['sarcasm']

    # Basic interpretive rules
    if "Sarcastic" in sarcasm:
        return "This message seems playful or teasing."
    if sentiment == "Negative" and emotion.lower() in ["joy", "surprise"]:
        return "Despite a critical tone, there is an underlying sense of lightheartedness."
    if sentiment == "Positive" and emotion.lower() in ["joy", "surprise"]:
        return "Overall, the message is cheerful and encouraging."
    if sentiment == "Negative":
        return "The message expresses concern or dissatisfaction."
    return "The conversation feels balanced with neutral undertones."

# Button with feedback
button_placeholder = st.empty()
analyze_clicked = button_placeholder.button(
    "Analyze the Vibe" if not st.session_state.analyzed else "Vibe Analyzed ✅"
)

if analyze_clicked and user_input.strip():
    st.session_state.analyzed = True
    with st.spinner("Analyzing vibes..."):
        time.sleep(0.8)  # Slight delay for effect
        results = analyze_vibes(user_input)

    # Display results
    st.subheader("🎭 Analysis Results")
    st.write(f"**Sentiment:** {results['sentiment']['label']}")
    st.write(f"**Sarcasm:** {results['sarcasm']}")
    st.write(f"**Dominant Emotion:** {results['emotion']['label']}")

    # Smart summary
    summary_text = get_summary(results)
    st.markdown(
        f"<div style='background-color:#f0f2f6;padding:12px;border-radius:6px'><strong>Summary:</strong> {summary_text}</div>",
        unsafe_allow_html=True
    )

elif analyze_clicked:
    st.warning("Please enter some text first!")
