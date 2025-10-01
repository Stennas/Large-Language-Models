import streamlit as st
import time
from vibe_model import analyze_vibes

# Streamlit UI setup
st.set_page_config(page_title="Vibe Check", page_icon="✨", layout="centered")
st.title("✨ Vibe Check App")
st.write("Paste a chat or message below to get an intelligent vibe analysis 👇")

user_input = st.text_area("Enter your message:")

def generate_summary(results):
    """Generate a smart narrative summary based on sentiment, sarcasm, and emotion."""
    sentiment = results['sentiment']['label']
    emotion = results['emotion']['label'].lower()
    sarcasm_label = results['sarcasm']

    summary_parts = []

    # Sarcasm insight
    if "LABEL_1" in sarcasm_label or "sarcastic" in sarcasm_label.lower():
        summary_parts.append("The message has a playful or teasing undertone.")
    
    # Sentiment + emotion insight
    if sentiment.upper() == "POSITIVE" and emotion in ["joy", "surprise"]:
        summary_parts.append("Overall, the text feels cheerful and encouraging.")
    elif sentiment.upper() == "NEGATIVE" and emotion in ["sadness", "anger", "fear"]:
        summary_parts.append("There’s concern, frustration, or disappointment expressed.")
    elif sentiment.upper() == "NEGATIVE" and emotion in ["joy", "surprise"]:
        summary_parts.append("Despite a critical tone, there’s a hint of lightheartedness.")
    else:
        summary_parts.append("The conversation feels balanced or neutral in tone.")
    
    return " ".join(summary_parts)

if st.button("Analyze"):
    if user_input.strip():
        with st.spinner("Analyzing vibes..."):
            time.sleep(0.8)  # slight delay for UX
            results = analyze_vibes(user_input)

        # --- Interpret sentiment ---
        sentiment_map = {
            "POSITIVE": "Positive / Uplifting",
            "NEGATIVE": "Negative / Critical",
            "NEUTRAL": "Neutral / Matter-of-fact"
        }
        sentiment_text = sentiment_map.get(results['sentiment']['label'].upper(), results['sentiment']['label'])

        # --- Interpret sarcasm ---
        sarcasm_label = results['sarcasm']
        if "LABEL_0" in sarcasm_label:
            sarcasm_text = "Not sarcastic"
        else:
            sarcasm_text = "Sarcastic / Playful tone"

        # --- Interpret dominant emotion ---
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

        # --- Optional tone hint ---
        tone_hint = ""
        if sentiment_text.startswith("Positive") and "Humorous" in emotion_text:
            tone_hint = "This message comes across as friendly and playful."
        elif sentiment_text.startswith("Negative") and "Sad" in emotion_text:
            tone_hint = "The message shows self-critique or mild frustration."

        # --- Display results ---
        st.subheader("🎭 Vibe Analysis")
        st.write(f"**Sentiment:** {sentiment_text}")
        st.write(f"**Sarcasm:** {sarcasm_text}")
        st.write(f"**Dominant Emotion:** {emotion_text}")
        if tone_hint:
            st.write(f"**Tone Insight:** {tone_hint}")

        # --- Smart summary ---
        summary_text = generate_summary(results)
        st.markdown(
            f"<div style='background-color:#f0f2f6;padding:12px;border-radius:6px'><strong>Summary:</strong> {summary_text}</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Please enter some text first!")
