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
        # Check common label patterns
        if "LABEL_1" in label or "sarcastic" in label.lower():
            return "Sarcastic / Playful tone"
        else:
            return "Not sarcastic / Serious tone"
    return "Not sarcastic / Serious tone"

def generate_summary(results):
    """Produce a human-like summary based on sentiment, emotion, and sarcasm."""
    sentiment = results['sentiment']['label'].upper()
    emotion = results['emotion']['label'].lower()
    sarcasm = interpret_sarcasm(results['sarcasm'])

    if "Sarcastic" in sarcasm:
        return "The speaker is making a playful or teasing remark."
    if sentiment == "NEGATIVE" and emotion in ["sadness", "anger", "fear"]:
        return "The message expresses concern, frustration, or self-reflection."
    if sentiment == "POSITIVE" and emotion in ["joy", "surprise"]:
        return "The message is uplifting, lighthearted, or encouraging."
    if sentiment == "NEUTRAL" and emotion in ["neutral", "calm"]:
        return "The statement is reflective or matter-of-fact in tone."
    return "The message conveys a nuanced or balanced tone."

if st.button("Analyze"):
    if user_input.strip():
        with st.spinner("Analyzing vibes..."):
            results = analyze_vibes(user_input)

        # Interpret sentiment
        sentiment_map = {
            "POSITIVE": "Positive / Uplifting",
            "NEGATIVE": "Negative / Critical",
            "NEUTRAL": "Neutral / Matter-of-fact"
        }
        sentiment_text = sentiment_map.get(results['sentiment']['label'].upper(), results['sentiment']['label'])

        # Interpret sarcasm
        sarcasm_text = interpret_sarcasm(results['sarcasm'])

        # Interpret dominant emotion
        emotion_map = {
            "joy": "Lighthearted / Humorous",
            "anger": "Frustrated / Upset",
            "sadness": "Sad / Self-critical",
            "fear": "Anxious / Concerned",
            "disgust": "Disgust / Disapproval",
            "surprise": "Surprised / Shocked",
            "neutral": "Calm / Matter-of-fact"
        }
        emotion_text = emotion_map.get(results['emotion']['label'].lower(), results['emotion']['label'])

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
