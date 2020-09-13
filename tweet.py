# Based on a template by Molly White, see:
# https://github.com/molly/twitterbot_framework

import os
import tweepy
from time import time, gmtime, strftime

from draw import draw_card


# ====== Individual bot configuration ==========================

bot_username = 'infinite_eno'
logfile_name = bot_username + ".log"

# ====== Schedule ==============================================

FILENAME = '20200913.txt'  # was: 20200713.txt
T_START = 1600021600  # was: 1595425964
INTERVAL_HRS = 16  # was: 1, must be int


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

    times = range(T_START, T_START + 3600 * INTERVAL_HRS * len(tweets), 3600 * INTERVAL_HRS)
    times = [strftime("%Y%m%d%H", gmtime(t)) for t in times]
    tweet_schedule = dict(zip(times, tweets))
    print(list(zip(times, tweets))[:30])

    return tweet_schedule


def normalize_text(s):

    return ''.join(filter(str.isalpha, s[:50].lower()))


def get_tweet_text(api, tweet):

    status = api.get_status(tweet.id, include_ext_alt_text=True)
    try:
        text = status.extended_entities['media'][0]['ext_alt_text']
    except AttributeError:
        text = tweet.text

    return text


def get_recent_tweets(api):

    return [normalize_text(get_tweet_text(api, tweet)) for tweet in api.user_timeline('infinite_eno')]


def get_tweet(tweet_schedule, recent_tweets):
    """Create the text of the tweet you want to send."""
    t = strftime("%Y%m%d%H", gmtime(time()))
    tweet = tweet_schedule[t]
    if normalize_text(tweet) not in recent_tweets:
        return tweet
    else:
        raise ValueError(f'ERROR: tweet found, but was already tweeted recently. Tweet: "{tweet}"')


def tweet(api, text):
    """Send out the text as a tweet."""
    try:
        # text = "Make an exhaustive list of everything you might do and do the last thing on the list"
        # text = "Make a sudden, destructive unpredictable action; incorporate"
        # text = "Remove specifics and convert to ambiguities"
        draw_card(text, out_path='card.jpg')
        media = api.media_upload('card.jpg')
        api.create_media_metadata(media.media_id, alt_text=text)
        api.update_status(None, media_ids=[media.media_id])
    except tweepy.error.TweepError as e:
        log(e.message)
        try:
            api.update_status(text)
        except tweepy.error.TweepError as e:
            log(e.message)
        else:
            log("Tweeted: " + text)
    else:
        log("Tweeted card with text: " + text)


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
