# Copyright (c) 2015–2016 Molly White
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import tweepy
from time import time, gmtime, strftime


# ====== Individual bot configuration ==========================

bot_username = 'infinite_eno'
logfile_name = bot_username + ".log"

# ====== Schedule ==============================================

FILENAME = '20200713.txt'
T_START = 1594594800
INTERVAL_HRS = 1  # must be int


def authenticate():

    C_KEY = os.environ['C_KEY']
    C_SECRET = os.environ['C_SECRET']
    A_TOKEN = os.environ['A_TOKEN']
    A_TOKEN_SECRET = os.environ['A_TOKEN_SECRET']

    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    return api


def get_tweet_schedule():

    with open(FILENAME, 'r') as f:
        tweets = f.readlines()
    tweets = [s.strip('\n') for s in tweets]

    times = range(T_START, T_START + 3600 * INTERVAL_HRS * len(tweets), 3600 * INTERVAL)
    times = [strftime("%Y%m%d%H", gmtime(t)) for t in times]
    tweet_schedule = dict(zip(times, tweets))

    return tweet_schedule


def normalize_tweet(s):

    return ''.join(filter(str.isalpha, s[:50].lower()))


def get_recent_tweets(api):

    return [normalize_tweet(tweet.text) for tweet in api.user_timeline('infinite_eno')]


def get_tweet(tweet_schedule, recent_tweets):
    """Create the text of the tweet you want to send."""
    t = strftime("%Y%m%d%H", gmtime(time()))
    tweet = tweet_schedule[t]
    if normalize_tweet(tweet) not in recent_tweets:
        return tweet
    else:
        raise ValueError(f'ERROR: tweet found, but was already tweeted recently. Tweet: "{tweet}"')


def tweet(api, text):
    """Send out the text as a tweet."""
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted: " + text)


def log(message):
    """Log message to logfile."""
    print(message)
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


if __name__ == "__main__":
    
    api = authenticate()
    tweet_schedule = get_tweet_schedule()
    recent_tweets = get_recent_tweets(api)
    try:
        tweet_text = get_tweet(tweet_schedule, recent_tweets)
        tweet(api, tweet_text)
    except ValueError as e:
        log(str(e))
