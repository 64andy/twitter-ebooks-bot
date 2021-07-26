import twitter
import os
import re
from typing import List

import markovify
from nltk.tag import pos_tag
from .text import statuses_to_clean_texts, clean_banned_words
from .settings import source_count, exact_source_len, min_length, max_length

RATE_LIMIT_CODE = 88

# Making sure nltk's data has been installed
try:
    pos_tag(["testing"])
except LookupError:
    print("Downloading tagger...")
    import nltk
    nltk.download("averaged_perceptron_tagger")
    print("Done")

# https://github.com/jsvine/markovify/blob/master/README.md
class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


api: twitter.Api = twitter.Api(
            consumer_key        = os.environ.get("CONSUMER_PUBLIC_KEY"),
            consumer_secret     = os.environ.get("CONSUMER_SECRET_KEY"),
            access_token_key    = os.environ.get("ACCESS_PUBLIC"      ),
            access_token_secret = os.environ.get("ACCESS_SECRET"      ),
            tweet_mode          = 'extended'
        )


def get_tweets(user: str, n_tweets: int) -> List[str]:
    """
    Overcomes Twitter's 200 tweet fetch limit by
    iteratively asking for more tweets until there's enough.
    Returns each tweet as a string, cleaned up with `statuses_to_clean_texts()`
    so no t.co links, no @mentions, and no blank strings
    """
    args = {
        'screen_name'     : user,
        'count'           : 200,
        'include_rts'     : False,
        'exclude_replies' : True
        }
    output_tweets = []
    try:
        tweets = api.GetUserTimeline(**args)
        final_id = tweets[-1].id
        output_tweets = statuses_to_clean_texts(tweets)
        stuck_in_loop = False
        while len(output_tweets) < n_tweets or not stuck_in_loop:
            new_tweets = api.GetUserTimeline(max_id=final_id-1, **args)
            clean_tweets = statuses_to_clean_texts(new_tweets)
            if len(clean_tweets) > 0:
                final_id = new_tweets[-1].id
                output_tweets.extend(clean_tweets)
            else:
                stuck_in_loop = True
        if exact_source_len:
            output_tweets = output_tweets[:source_count]
    except twitter.error.TwitterError as e:
        print(e)
        if e.message[0]['code'] == RATE_LIMIT_CODE:
            print("RATE LIMITED - Returning what we've got so far")
            return output_tweets
        else:
            raise e
    return output_tweets


def generate_markov(user: str) -> str:
    """Returns a markov chained sentence from the given `user`'s twitter timeline"""
    tweets = get_tweets(user=user, n_tweets=source_count)
    if len(tweets) == 0:
        print("Something went wrong, the source tweet list is empty.")
    texts = [POSifiedText(tweet, well_formed=False)
                for tweet in tweets]
    model = markovify.combine(texts)
    tweet = model.make_short_sentence(max_length, min_length, tries=1_000)
    if tweet is None:
        return None
    return clean_banned_words(tweet)


