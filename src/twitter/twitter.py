from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio

MINIMUM_TWEETS = 60000
QUERY = '(from:elonmusk OR from:saylor OR from:binance OR from:federalreserve OR from:lookonchain) lang:en since:2021-01-01 until:2024-12-31 -filter:replies'

config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

with open('tweets.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Tweet_count', 'Username', 'Text', 'Created', 'Retweets', 'Likes'])

async def log():
    client = Client(language='en-US')
    await client.login(auth_info_1=username,auth_info_2=email,password=password)
    client.save_cookies('cookies.json')

#asyncio.run(log())
client = Client(language='en-US')
client.load_cookies('cookies.json' )

async def get_tweets(tweets):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Latest')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting more tweets after {wait_time} seconds...')
        time.sleep(wait_time)
        tweets = await tweets.next()

    return tweets

async def tweet():
    tweet_count = 0
    tweets = None
    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(tweets)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            time.sleep(wait_time.total_seconds())
            continue
        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
        for tweet in tweets:
            
            tweet_count += 1
            tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
            with open('tweets.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)
    
    print(f'{datetime.now()} - {tweet_count} tweets found')
    
asyncio.run(tweet())
