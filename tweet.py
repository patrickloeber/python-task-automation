# YOU NEED TO CREATE TWITTER AND GOOGLE CREDENTIALS FIRST
from os import environ
from datetime import datetime, timedelta

import tweepy
import gspread

from dotenv import load_dotenv
load_dotenv()

# SAVE THE json FROM GOOGLE DEVELOPER CONSOLER FIRST
gc = gspread.service_account(filename='googledrive_credentials.json')
sh = gc.open_by_key("your_sheet_key")
worksheet = sh.sheet1

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

tweet_api = tweepy.API(auth)

def get_now_time_normalized():
    return datetime.now()
    # modify if needed, e.g.:
    # return datetime.utcnow() + timedelta(hours=1)

def check_and_update_tweets():
    tweets = worksheet.get_all_records()
    for row_idx, tweet in enumerate(tweets, start=2):
        msg = tweet['message']
        time_str = tweet['time']
        done = tweet['done']
                
        post_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        if not done:
            now_time = get_now_time_normalized()
            if post_time < now_time:
                try:
                    tweet_api.update_status(msg)
                    worksheet.update_cell(row_idx, 3, 1)  # row, col, value
                except Exception as e:
                    print(f'exception during tweet! {e}')


if __name__ == '__main__':
    check_and_update_tweets()