'''
E-Books algorithm and Tweet posting bot.
Created by @64andy2000
24/7 bot trick by @GarethDwyer1
Created on 20/12/18
V1 completed 23/12/18
V2: Now with Markov Chains and NLP
    completed 07/09/18
'''

import time
from datetime import datetime
from traceback import format_exc
from e_books import api, generate_markov
from e_books.settings import user_handle, tweet_interval
from keep_alive import keep_alive, errors


def post_ebook():
    e_book = generate_markov(user_handle)
    print(datetime.now(), e_book)
    if e_book is not None:      # Markovify returns None if it fails
        api.PostUpdate(e_book)
    else:
        raise Exception("Couldn't generate an ebook")


if __name__ == "__main__":
    keep_alive()
    while True:
        try:
            if (tweet_interval-1) < (time.time() % tweet_interval):      # If o'clock is a few seconds away
                post_ebook()
                time.sleep(4)
            time.sleep(1)
        except:
            errors.append(format_exc())
