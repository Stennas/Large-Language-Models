import streamlit as st
from vibe_model import analyze_vibes

st.set_page_config(page_title="Vibe Check App", page_icon="✨", layout="centered")

st.title("✨ Vibe Check App")
st.write("Paste a sentence or chat below to analyze its vibe.")

# User input
user_input = st.text_area("Enter text:", height=120)

# Badge colors
badge_colors = {
    "Positive": "green",
    "Neutral": "gray",
    "Negative": "red",
    "Joy": "orange",
    "Anger": "red",
    "Sadness": "blue",
    "Fear": "purple",
    "Disgust": "brown",
    "Surprise": "pink",
    "Calm": "teal",
    "Sarcastic": "orange",
    "Not Sarcastic": "gray",
}

# Generate summary
def generate_summary(results):
    sentiment = results["sentiment"]
    emotion = results["emotion"]
    sarcasm = results["sarcasm"]

    if sarcasm == "Sarcastic":
        return f"The text has a **{sentiment.lower()}** tone, leans towards **{emotion.lower()}**, and carries a **sarcastic undertone**."
    else:
        return f"The text has a **{sentiment.lower()}** tone, with a dominant feeling of **{emotion.lower()}**, and is expressed in a straightforward way."

# Analyze button
if st.button("Analyze ✨"):
    if user_input.strip():
        with st.spinner("Analyzing vibes..."):
            results = analyze_vibes(user_input)

        # Show badges
        st.subheader("Vibe Badges")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"<span style='background-color:{badge_colors.get(results['sentiment'], 'gray')}; "
                f"padding:6px 12px; border-radius:12px; color:white;'>Sentiment: {results['sentiment']}</span>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"<span style='background-color:{badge_colors.get(results['emotion'], 'gray')}; "
                f"padding:6px 12px; border-radius:12px; color:white;'>Emotion: {results['emotion']}</span>",
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f"<span style='background-color:{badge_colors.get(results['sarcasm'], 'gray')}; "
                f"padding:6px 12px; border-radius:12px; color:white;'>Sarcasm: {results['sarcasm']}</span>",
                unsafe_allow_html=True,
            )

        # Show refined summary
        st.subheader("Refined Summary")
        st.info(generate_summary(results))
    else:
        st.warning("⚠️ Please enter some text first.")
