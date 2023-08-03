import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

def get_sentiment_score(paragraph):
    # Initialize the VADER SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()

    # Calculate the sentiment score for the paragraph
    sentiment_score = sia.polarity_scores(paragraph)['compound']

    # Map the sentiment score to the desired range of 1 to 10
    sentiment_on_scale = (sentiment_score + 1) * 5

    # Clip the value to ensure it falls within the desired range
    sentiment_on_scale = min(max(sentiment_on_scale, 1), 10)

    return sentiment_on_scale

