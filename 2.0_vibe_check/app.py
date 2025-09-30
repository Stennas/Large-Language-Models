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
        
        # Display results
        st.subheader("🎭 Vibe Results")
        st.write(f"**Sentiment:** {results['sentiment']['label']} (score: {results['sentiment']['score']:.2f})")
        st.write(f"**Sarcasm:** {results['sarcasm']}")
        st.write(f"**Dominant Emotion:** {results['emotion']['label']} (score: {results['emotion']['score']:.2f})")
        
        # Optional: emoji mapping for fun
        vibe_emojis = {
            "joy": "😂",
            "anger": "😡",
            "sadness": "😢",
            "fear": "😱",
            "disgust": "🤢",
            "surprise": "😲",
            "neutral": "😐"
        }
        st.write(f"**Emoji vibe:** {vibe_emojis.get(results['emotion']['label'].lower(), '✨')}")
    else:
        st.warning("Please enter some text first!")
