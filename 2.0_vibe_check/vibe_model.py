from transformers import pipeline

# Load pre-trained models
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

def detect_sarcasm(text, sentiment_label):
    """
    Simple heuristic sarcasm detector:
    - Looks for irony markers in text.
    - Detects mismatched signals (positive words + negative emotion).
    """
    text_lower = text.lower()
    sarcasm_markers = ["oh sure", "yeah right", "as if", "obviously", "totally", "brilliant idea"]
    
    if any(marker in text_lower for marker in sarcasm_markers):
        return "Sarcastic"
    
    # If sentiment is positive but top emotion is negative, assume sarcasm
    if sentiment_label == "Positive" and any(word in text_lower for word in ["fail", "waste", "useless", "never"]):
        return "Sarcastic"
    
    return "Not Sarcastic"

def generate_summary(sentiment, sarcasm, emotion):
    """
    Create a more natural summary from detected labels.
    """
    if sarcasm == "Sarcastic":
        return f"The message expresses {sentiment.lower()} sentiment with a sarcastic undertone."
    
    if sentiment == "Positive":
        return f"The speaker sounds genuinely {emotion.lower()} and optimistic."
    elif sentiment == "Negative":
        return f"The message conveys {emotion.lower()} and disapproval."
    elif sentiment == "Neutral":
        return f"The speaker maintains a calm and balanced tone."
    
    return "The message expresses a mixed or complex vibe."

def analyze_vibes(text):
    # Sentiment
    sentiment_result = sentiment_pipeline(text)[0]
    sentiment_label = sentiment_result["label"]
    if sentiment_label == "LABEL_0":
        sentiment = "Negative"
    elif sentiment_label == "LABEL_1":
        sentiment = "Neutral"
    else:
        sentiment = "Positive"
    
    # Emotions
    emotions = emotion_pipeline(text)
    emotions_sorted = sorted(emotions[0], key=lambda x: x["score"], reverse=True)
    dominant_emotion = emotions_sorted[0]["label"]
    
    # Sarcasm
    sarcasm = detect_sarcasm(text, sentiment)
    
    # Summary
    summary = generate_summary(sentiment, sarcasm, dominant_emotion)
    
    return {
        "sentiment": sentiment,
        "sarcasm": sarcasm,
        "dominant_emotion": dominant_emotion,
        "summary": summary
    }
