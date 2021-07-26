"""
Bot settings
"""

'''The handle of the user we're getting tweets from e.g. "wint"'''
user_handle: str        = 'wint'
'''Number of tweets fetched from timeline and trained off
(note, might fetch more)'''
source_count: int       = 600

'''True if you want `source_count` to return
exactly as many specified.
Note, it can still overfetch the API'''
exact_source_len: bool  = False

''' How frequently it'll post in seconds
e.g. 1200 = 3 times an hour'''
tweet_interval: int     = 1800

'''Minimum output tweet length'''
min_length: int         = 12

''' Maximum output tweet length'''
max_length: int         = 90

'''Replaces any occuring words with garbage.
# Created to stop Fortnite search-liking-bots'''
banned_words: list      = ["fortnite"]



# Deprecated:
# These are relics from before Markov, when it just randomly grabbed
# groups of words from random tweets and strung them together

'''The minimum number of words in a "group" grabbed from a tweet'''
min_group_len: int      = 1

'''The maximum number of words in a "group" grabbed from a tweet'''
max_group_len: int      = 4