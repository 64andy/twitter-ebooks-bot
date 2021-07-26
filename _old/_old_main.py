'''
Very simple E-Books algorithm and Tweet posting bot.
Created by @64andy2000
24/7 bot trick by @GarethDwyer1
Created on 20/12/18
V1 completed 23/12/18'''

import os
import time
from datetime import datetime
import twitter
from e_books.text import generate_ebook, grouped_words
from e_books.settings import user_handle, source_count, tweet_interval
from keep_alive import keep_alive, errors


api = twitter.Api(
            consumer_key        = os.environ.get("CONSUMER_PUBLIC_KEY"),
            consumer_secret     = os.environ.get("CONSUMER_SECRET_KEY"),
            access_token_key    = os.environ.get("ACCESS_PUBLIC"      ),
            access_token_secret = os.environ.get("ACCESS_SECRET"      ),
            tweet_mode          = 'extended'
        )


def post_ebook() -> None:
    tweets = api.GetUserTimeline(screen_name=user_handle, count=source_count, include_rts=False, exclude_replies=True)
    messages = [grouped_words(tweet.full_text) for tweet in tweets]
    e_book = generate_ebook(messages)
    print(datetime.now(), e_book)
    api.PostUpdate(e_book)


if __name__ == "__main__":
    keep_alive()
    while True:
        try:
            if (tweet_interval-1) < (time.time() % tweet_interval):      # If o'clock is a few seconds away
                post_ebook()
                time.sleep(10)
            time.sleep(1)
        except Exception as e:
            errors.append(e)





