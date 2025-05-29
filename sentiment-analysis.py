import tweepy
import pandas as pd

# Wstaw tutaj swoje klucze
api_key = 'TWÓJ_API_KEY'
api_secret = 'TWÓJ_API_SECRET'
access_token = 'TWÓJ_ACCESS_TOKEN'
access_token_secret = 'TWÓJ_ACCESS_TOKEN_SECRET'

# Autoryzacja
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Pobierz 100 tweetów z wybranym hashtagiem (np. #Nike)
tweets = tweepy.Cursor(api.search_tweets, q="#Nike", lang="en", tweet_mode='extended').items(100)
data = [tweet.full_text for tweet in tweets]

# Zapisz do DataFrame
df = pd.DataFrame(data, columns=['tweet'])
df.to_csv('tweets.csv', index=False)
print("Pobrano i zapisano tweety.")
