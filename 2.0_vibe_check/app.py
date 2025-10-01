import streamlit as st
from vibe_model import analyze_vibes

# Streamlit UI
st.set_page_config(page_title="Vibe Check", page_icon="✨", layout="centered")

st.title("✨ Vibe Check App")
st.write("Paste a chat or message below to check the pulse of your conversations! 👇")

user_input = st.text_area("Enter your message:")

if st.button("Check the Vibes"):
    if user_input.strip():
        with st.spinner("Analyzing vibes..."):
            results = analyze_vibes(user_input)
        
        # Map sarcasm labels to user-friendly text
        sarcasm_label = results['sarcasm']['label']
        if sarcasm_label == "LABEL_0":
            sarcasm_text = "Not Sarcastic 😐"
        else:
            sarcasm_text = "Sarcastic 😏"

        # Map sentiment to emojis
        sentiment_emoji = {
            "negative": "😔",
            "neutral": "😐",
            "positive": "😄"
        }.get(results['sentiment']['label'].lower(), "✨")

        # Map emotion to emojis
        vibe_emojis = {
            "joy": "😂",
            "anger": "😡",
            "sadness": "😢",
            "fear": "😱",
            "disgust": "🤢",
            "surprise": "😲",
            "neutral": "😐"
        }
        emotion_emoji = vibe_emojis.get(results['emotion']['label'].lower(), "✨")
        
        # Generate summary sentence
        summary = (
            f"This message feels {results['sentiment']['label'].lower()} {sentiment_emoji}, "
            f"the dominant emotion is {results['emotion']['label'].lower()} {emotion_emoji}, "
            f"and it is {sarcasm_text.lower()}."
        )
        
        # Display results
        st.subheader("🎭 Vibe Results")
        st.write(f"**Summary:** {summary}\n")
        st.write(f"**Sentiment:** {results['sentiment']['label'].capitalize()} {sentiment_emoji} (score: {results['sentiment']['score']:.2f})")
        st.write(f"**Sarcasm:** {sarcasm_text} (score: {results['sarcasm']['score']:.2f})")
        st.write(f"**Dominant Emotion:** {results['emotion']['label'].capitalize()} {emotion_emoji} (score: {results['emotion']['score']:.2f})")
        
    else:
        st.warning("Please enter some text first!")
