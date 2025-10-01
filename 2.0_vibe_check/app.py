import streamlit as st
from vibe_model import analyze_vibes

# Streamlit UI
st.set_page_config(page_title="Vibe Check", page_icon="✨", layout="centered")
st.title("✨ Vibe Check App")
st.write("Paste a chat or message below to get a thoughtful vibe analysis 👇")

user_input = st.text_area("Enter your message:")

def interpret_sarcasm(label):
    """Map sarcasm model output to human-friendly text."""
    if isinstance(label, str):
        if "LABEL_1" in label or "sarcastic" in label.lower():
            return "Sarcastic"
        else:
            return "Not Sarcastic"
    return "Not Sarcastic"

def generate_summary(results):
    """Produce a human-like summary based on sentiment, emotion, and sarcasm."""
    sentiment = results['sentiment']['label']
    emotion = results['emotion']['label']
    sarcasm = interpret_sarcasm(results['sarcasm'])

    # Core summary logic
    if sentiment == "Negative" and emotion in ["Sadness", "Anger", "Fear"]:
        base_summary = "The message expresses concern, frustration, or self-reflection."
    elif sentiment == "Positive" and emotion in ["Joy", "Surprise"]:
        base_summary = "The message is uplifting, lighthearted, or encouraging."
    elif sentiment == "Neutral" and emotion in ["Calm", "Neutral"]:
        base_summary = "The statement is reflective or matter-of-fact in tone."
    else:
        base_summary = "The message conveys a nuanced or balanced tone."

    # Add sarcasm flavor (without overriding everything)
    if sarcasm == "Sarcastic":
        return base_summary + " However, it carries a sarcastic or playful undertone."
    return base_summary

if st.button("Analyze"):
    if user_input.strip():
        with st.spinner("Analyzing vibes..."):
            results = analyze_vibes(user_input)

        # Interpret sentiment
        sentiment_map = {
            "Positive": "Positive / Uplifting",
            "Negative": "Negative / Critical",
            "Neutral": "Neutral / Matter-of-fact"
        }
        sentiment_text = sentiment_map.get(results['sentiment']['label'], results['sentiment']['label'])

        # Interpret sarcasm
        sarcasm_text = interpret_sarcasm(results['sarcasm'])

        # Interpret dominant emotion
        emotion_map = {
            "Joy": "Lighthearted / Humorous",
            "Anger": "Frustrated / Upset",
            "Sadness": "Sad / Self-critical",
            "Fear": "Anxious / Concerned",
            "Disgust": "Disgust / Disapproval",
            "Surprise": "Surprised / Shocked",
            "Calm": "Calm / Matter-of-fact"
        }
        emotion_text = emotion_map.get(results['emotion']['label'], results['emotion']['label'])

        # Display results
        st.subheader("🎭 Vibe Analysis")
        st.write(f"**Sentiment:** {sentiment_text}")
        st.write(f"**Sarcasm:** {sarcasm_text}")
        st.write(f"**Dominant Emotion:** {emotion_text}")

        # Smart summary
        summary_text = generate_summary(results)
        st.markdown(
            f"<div style='background-color:#f0f2f6;padding:12px;border-radius:6px'><strong>Summary:</strong> {summary_text}</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Please enter some text first!")
