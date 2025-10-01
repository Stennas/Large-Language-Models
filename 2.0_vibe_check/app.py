import streamlit as st
from vibe_model import analyze_vibes

st.set_page_config(page_title="Vibe Check 2.0", page_icon="✨", layout="centered")

st.title("✨ Vibe Check 2.0")
st.write("Drop in a line or two and let’s decode the vibes 👇")

user_input = st.text_area("Enter text:", placeholder="Type something here...")

if st.button("Analyze"):
    if user_input.strip():
        with st.spinner("Analyzing vibes..."):
            results = analyze_vibes(user_input)

        st.subheader("Results")
        st.write(f"**Sentiment:** {results['sentiment']}")
        st.write(f"**Sarcasm:** {results['sarcasm']}")
        st.write(f"**Dominant Emotion:** {results['dominant_emotion']}")
        st.write(f"**Summary:** {results['summary']}")
    else:
        st.warning("⚠️ Please enter some text before analyzing.")
