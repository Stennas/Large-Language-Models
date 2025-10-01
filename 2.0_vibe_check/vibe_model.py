from transformers import pipeline

# Load pre-trained models
sentiment = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
sarcasm = pipeline("text-classification", model="helinivan/english-sarcasm-detector", return_all_scores=False)
emotion = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def analyze_vibes(text):
    # Sentiment
    sentiment_result = sentiment(text)[0]

    # Sarcasm 
    sarcasm_result = sarcasm(text)[0]

    # Emotion
    emotion_results = emotion(text)[0]
    top_emotion = max(emotion_results, key=lambda x: x['score'])

    return {
        "sentiment": sentiment_result,
        "sarcasm": sarcasm_result,
        "emotion": top_emotion
    }