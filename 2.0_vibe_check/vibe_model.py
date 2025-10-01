from transformers import pipeline

# Sentiment: CardiffNLP Twitter model (3 classes: Positive, Neutral, Negative)
sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

# Emotion classifier: multi-class emotions
emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

# Sarcasm detector
sarcasm_analyzer = pipeline("text-classification", model="mrm8488/t5-base-finetuned-sarcasm-twitter", top_k=None)

def analyze_vibes(text: str):
    """
    Analyze sentiment, emotion, and sarcasm for a given text.
    Returns clean labels only (no scores).
    """

    # Sentiment
    sentiment_result = sentiment_analyzer(text)[0]
    sentiment_label = sentiment_result["label"]

    # Emotion → pick strongest
    emotions = emotion_analyzer(text)
    emotions_sorted = sorted(emotions, key=lambda x: x["score"], reverse=True)
    emotion_label = emotions_sorted[0]["label"]

    # Sarcasm
    sarcasm_result = sarcasm_analyzer(text)[0]
    sarcasm_label = (
        "Sarcastic" if sarcasm_result["label"].lower() == "sarcasm" else "Not Sarcastic"
    )

    return {
        "sentiment": sentiment_label,
        "emotion": emotion_label,
        "sarcasm": sarcasm_label,
    }
