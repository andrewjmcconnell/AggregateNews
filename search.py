#!/usr/bin/python3
from secrets import *
import tweepy
import re
from TwitterSearch import *

# connect to twitter
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)

# list worldwide trends
trends = api.trends_place(1)[0].get('trends')
query = trends[1].get('name')
query = re.sub('[!@#$]', '', query)
print(query)

# search trends for tweets
try:
    tso = TwitterSearchOrder()
    tso.set_keywords([query])
    tso.set_language('en')
    tso.set_include_entities(False)

    ts = TwitterSearch(
        consumer_key = C_KEY,
        consumer_secret = C_SECRET,
        access_token = A_TOKEN,
        access_token_secret = A_TOKEN_SECRET,
    )
    with open("trend_outputs/"+query+".txt", "w") as f:
        for tweet in ts.search_tweets_iterable(tso):
            tweet = re.sub(r"RT @.*: ", '', str(tweet['text'])) # remove retweet marks
            tweet = re.sub(r"http\S+", '', tweet) # remove URLs
            print(tweet)
            print()
            f.write(tweet)
except TwitterSearchException as e:
    print(e)