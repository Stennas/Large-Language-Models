import streamlit as st
from vibe_model import analyze_vibes

# --- Streamlit configuration ---
st.set_page_config(page_title="Vibe Check", page_icon="✨", layout="centered")
st.title("✨ Vibe Check App")
st.write("Paste a chat or message below to get a meaningful vibe analysis 👇")

# --- Mode selection ---
mode = st.radio("Select analysis mode:", ["Single message", "Conversation"])

user_input = st.text_area("Enter your message(s):")

def generate_summary(results):
    """Generate a smart summary based on sentiment, emotion, and sarcasm."""
    sentiment = results['sentiment']['label']
    emotion = results['emotion']['label']
    sarcasm = results['sarcasm']

    if sarcasm.get('label') == "LABEL_1" or "sarcastic" in str(sarcasm).lower():
        return "This message seems playful or teasing."
    if sentiment.upper() == "NEGATIVE" and emotion.lower() in ["joy", "surprise"]:
        return "Despite a critical tone, there is an underlying sense of lightheartedness."
    if sentiment.upper() == "POSITIVE" and emotion.lower() in ["joy", "surprise"]:
        return "Overall, the message is cheerful and encouraging."
    if sentiment.upper() == "NEGATIVE":
        return "The message expresses concern or dissatisfaction."
    return "The conversation feels balanced with neutral undertones."

def display_results(results, label_prefix=""):
    """Helper to display vibe results nicely."""
    # Interpret sentiment
    sentiment_map = {
        "POSITIVE": "Positive / Uplifting",
        "NEGATIVE": "Negative / Critical",
        "NEUTRAL": "Neutral / Matter-of-fact"
    }
    sentiment_text = sentiment_map.get(results['sentiment']['label'].upper(), results['sentiment']['label'])

    # Interpret sarcasm
    sarcasm_label = results['sarcasm']
    if sarcasm_label.get('label') == "LABEL_0":
        sarcasm_text = "Not sarcastic"
    else:
        sarcasm_text = "Sarcastic / Playful tone"

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

    # Optional tone hint
    tone_hint = ""
    if sentiment_text.startswith("Positive") and "Humorous" in emotion_text:
        tone_hint = "This message is friendly and playful."
    elif sentiment_text.startswith("Negative") and "Sad" in emotion_text:
        tone_hint = "The message contains self-critique or frustration."

    # Display results
    st.write(f"**{label_prefix}Sentiment:** {sentiment_text}")
    st.write(f"**{label_prefix}Sarcasm:** {sarcasm_text}")
    st.write(f"**{label_prefix}Dominant Emotion:** {emotion_text}")
    if tone_hint:
        st.write(f"**{label_prefix}Tone Insight:** {tone_hint}")

# --- Analyze button ---
if st.button("Analyze"):
    if user_input.strip():
        with st.spinner("Analyzing vibes..."):
            if mode == "Single message":
                results = analyze_vibes(user_input)
                display_results(results)
                summary_text = generate_summary(results)
            else:  # Conversation mode
                lines = [line.strip() for line in user_input.split("\n") if line.strip()]
                conversation_results = []
                for idx, line in enumerate(lines, start=1):
                    res = analyze_vibes(line)
                    conversation_results.append(res)
                    display_results(res, label_prefix=f"Line {idx}: ")
                # Aggregate summary for conversation
                summary_texts = [generate_summary(r) for r in conversation_results]
                summary_text = " ".join(summary_texts)

        # Smart summary
        st.markdown(
            f"<div style='background-color:#f0f2f6;padding:12px;border-radius:6px'><strong>Summary:</strong> {summary_text}</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Please enter some text first!")
