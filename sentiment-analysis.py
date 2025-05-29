import re
import tweepy
import pandas as pd
import os
from dotenv import load_dotenv
from textblob import TextBlob
import matplotlib.pyplot as plt

load_dotenv()
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
client = tweepy.Client(bearer_token=BEARER_TOKEN)

response = client.search_recent_tweets(
    query="#Nike lang:en",
    max_results=20,
    tweet_fields=['text']
)

if response.data is None:
    print("Nie znaleziono tweetów. Zmień zapytanie lub spróbuj później.")
    exit()

data = [tweet.text for tweet in response.data]
df = pd.DataFrame(data, columns=['tweet'])

def clean_tweet(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"[^A-Za-z\s]", "", text)
    text = text.lower()
    return text.strip()

df['cleaned'] = df['tweet'].apply(clean_tweet)

def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return 'Positive'
    elif polarity < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

df['sentiment'] = df['cleaned'].apply(get_sentiment)
df.to_csv('tweets_sentiment.csv', index=False)
print("Dodano analizę sentymentu i zapisano w tweets_sentiment.csv.")

sentiment_counts = df['sentiment'].value_counts()
labels = sentiment_counts.index
sizes = sentiment_counts.values

plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['green', 'red', 'gray'])
plt.title('Rozkład sentymentów dla #Nike')
plt.show()



