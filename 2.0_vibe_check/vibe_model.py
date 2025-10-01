from transformers import pipeline

# Load pre-trained models
sentiment = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
sarcasm = pipeline("text-classification", model="helinivan/english-sarcasm-detector", return_all_scores=False)
emotion = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def analyze_vibes(text):
    # --- Sentiment ---
    raw_sentiment = sentiment(text)[0]['label'].upper()
    sentiment_map = {
        "POSITIVE": "Positive",
        "NEGATIVE": "Negative",
        "NEUTRAL": "Neutral"
    }
    sentiment_label = sentiment_map.get(raw_sentiment, raw_sentiment)

    # --- Sarcasm ---
    raw_sarcasm = sarcasm(text)[0]['label']
    sarcasm_map = {
        "LABEL_0": "Not Sarcastic",
        "LABEL_1": "Sarcastic"
    }
    sarcasm_label = sarcasm_map.get(raw_sarcasm, raw_sarcasm)

    # --- Emotion ---
    emotion_results = emotion(text)[0]
    top_emotion = max(emotion_results, key=lambda x: x['score'])
    emotion_map = {
        "joy": "Joy",
        "anger": "Anger",
        "sadness": "Sadness",
        "fear": "Fear",
        "disgust": "Disgust",
        "surprise": "Surprise",
        "neutral": "Calm"
    }
    emotion_label = emotion_map.get(top_emotion['label'].lower(), top_emotion['label'])

    return {
        "sentiment": {"label": sentiment_label},
        "sarcasm": sarcasm_label,
        "emotion": {"label": emotion_label}
    }
