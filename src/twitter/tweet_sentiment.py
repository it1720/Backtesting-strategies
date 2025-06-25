import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

# Load CSV (Update file path as needed)
file_path = "data/tweets.csv"  # Change to your actual file path
df = pd.read_csv(file_path)

# Convert Twitter's timestamp format to YYYY-MM-DD
def parse_twitter_timestamp(timestamp):
    return datetime.strptime(timestamp, "%a %b %d %H:%M:%S %z %Y").date()

df['date'] = df['Created'].apply(parse_twitter_timestamp)

# Filter tweets containing BTC/ETH-related keywords
crypto_keywords = [
    "bitcoin", "btc",  "buy btc", "sell btc", "bullish btc", "bearish btc",
    "btc pump", "btc dump", "btc breakout", "btc moon", "btc crash", "btc price",
    "ethereum", "eth", "buy eth", "sell eth", "bullish eth", "bearish eth",
    "eth pump", "eth dump", "eth moon", "eth crash", "eth price",
    "crypto market", "crypto crash", "crypto rally", "hodl", "bull market", "bear market"
]
df = df[df['Text'].str.contains('|'.join(crypto_keywords), case=False, na=False)]

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    """Returns sentiment score (-1 to 1) using VADER."""
    if pd.isna(text):
        return np.nan  # Handle missing values
    return analyzer.polarity_scores(text)['compound']

# Apply sentiment analysis
df['sentiment'] = df['Text'].astype(str).apply(get_sentiment)

# Aggregate daily sentiment statistics
daily_sentiment = df.groupby('date').agg(
    bullish_ratio=('sentiment', lambda x: (x > 0).sum() / len(x)),
    bearish_ratio=('sentiment', lambda x: (x < 0).sum() / len(x)),
    tweet_count=('sentiment', 'count')
).reset_index()

# Save processed data for backtesting
daily_sentiment.to_csv("daily_tweet_sentiment.csv", index=False)

print("BTC/ETH-specific sentiment analysis completed. Data saved to daily_tweet_sentiment.csv")
