import streamlit as st
from vibe_model import analyze_vibes

# Streamlit UI
st.set_page_config(page_title="Vibe Check", page_icon="✨", layout="centered")
st.title("✨ Vibe Check App")
st.write("Paste a chat or message below to get a meaningful vibe analysis 👇")

user_input = st.text_area("Enter your message:")

if st.button("Analyze"):
    if user_input.strip():
        with st.spinner("Analyzing vibes..."):
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
            tone_hint = "This message is friendly and playful."
        elif sentiment_text.startswith("Negative") and "Sad" in emotion_text:
            tone_hint = "The message contains self-critique or frustration."

        # --- Display results ---
        st.subheader("🎭 Vibe Analysis")
        st.write(f"**Sentiment:** {sentiment_text}")
        st.write(f"**Sarcasm:** {sarcasm_text}")
        st.write(f"**Dominant Emotion:** {emotion_text}")
        if tone_hint:
            st.write(f"**Tone Insight:** {tone_hint}")

        # --- Summary at the bottom with highlight ---
        summary_text = f"""
        This message can be understood as: **{sentiment_text.lower()}, {emotion_text.lower()}, {sarcasm_text.lower()}**.
        """
        st.markdown(f"<div style='background-color:#f0f0f0; padding:10px; border-radius:5px'>{summary_text}</div>", unsafe_allow_html=True)

    else:
        st.warning("Please enter some text first!")
