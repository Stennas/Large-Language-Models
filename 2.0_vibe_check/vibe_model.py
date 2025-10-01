from transformers import pipeline

# Load pre-trained models
sentiment = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
sarcasm = pipeline("text2text-generation", model="mrm8488/t5-base-finetuned-sarcasm-twitter", use_fast=False )
emotion = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def analyze_vibes(text):
    # Sentiment
    sentiment_result = sentiment(text)[0]

    # Sarcasm (T5 expects a Q&A prompt)
    sarcasm_result = sarcasm(f"Does this sentence contain sarcasm? {text}")
    sarcasm_text = sarcasm_result[0]['generated_text']

    # Emotion
    emotion_results = emotion(text)[0]
    top_emotion = max(emotion_results, key=lambda x: x['score'])

    return {
        "sentiment": sentiment_result,
        "sarcasm": sarcasm_text,
        "emotion": top_emotion
    }