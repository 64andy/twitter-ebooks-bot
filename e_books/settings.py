"""
Settings used throughout this program.
`user_handle: str`      - The handle of the user whom we're getting tweets
                            from i.e. "wint"
`source_count: int`     - The number of tweets that'll be grabbed from the user's                                  timeline and pooled. It will usually grab more tweets than
                            source_count.
`exact_source_len: bool`- If you want to return exactly `source_count` number of 
                            tweets from get_tweets(). If false, get_tweets() will
                            most likely return more tweets than specifi
`tweet_interval: int`   - How frequently it'll post in seconds, e.g. 3600 = every hour
`min_length: int`       - The minimum tweet length
`max_length: int`       - The maximum tweet length
`banned_words: list`    - Replaces each banned word in the tweet with random Unicode
                            symbols. Created to stop Fortnite search-liking-bots

DEPRECATED:
`min_group_len: int` - The minimum number of words that can be in a source chunk
`max_group_len: int` - The maximum number of words that can be in a source chunk
"""

user_handle: str        = 'wint'
source_count: int       = 600
exact_source_len: bool  = False
tweet_interval: int     = 1800
min_length: int         = 12
max_length: int         = 90
banned_words: list      = ["fortnite"]


# Deprecated
min_group_len: int      = 1
max_group_len: int      = 4