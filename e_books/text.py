import random
import re
from html import unescape
from typing import List

import twitter

from .settings import banned_words

REPLACEMENT_SYMBOLS = [
    '■', '□', '▢', '▣', '▤', '▥', '▦', '▧', '▨', '▩', '▪', '▫',
    '▬', '▭', '▮', '▯', '▰', '▱', '▲', '△', '▴', '▵', '▶',
    '▷', '▸', '▹', '►', '▻', '▼', '▽', '▾', '▿', '◀', '◁', '◂',
    '◃', '◄', '◅', '◆', '◇', '◈', '◉', '◊', '○', '◌', '◍', '◎',
    '●', '◐', '◑', '◒', '◓', '◔', '◕', '◖', '◗', '◘', '◙', '◚',
    '◛', '◜', '◝', '◞', '◟', '◠', '◡', '◢', '◣', '◤', '◥', '◦',
    '◧', '◨', '◩', '◪', '◫', '◬', '◭', '◮', '◯', '◰', '◱', '◲',
    '◳', '◴', '◵', '◶', '◷','◸', '◹', '◺', '◻', '◼', '◽', '◾', '◿']

TWITTER_URL_REGEX = r"(https:\/\/t\.co\/)\w+|(\B@\w+)"    # Catches t.co links AND @{user}s


def statuses_to_clean_texts(tweets: List[twitter.Status]) -> List[str]:
    """ Takes a list of twitter.Status objects, extracts their text,
    removes t.co links, removes @{user} mentions, and strips the tweet.
    Returns a list of each tweet's text, if this process didn't reduce to an 
    empty string.
    """
    clean_tweets = []
    for tweet in tweets:
        text = re.sub(TWITTER_URL_REGEX, "", tweet.full_text)   # Removes t.co links and @{user} mentions
        text = unescape(text.strip())    # " 1 &lt; 2 " -> "1 < 2"
        if len(text) > 0:
            clean_tweets.append(text)
    return clean_tweets



def clean_banned_words(tweet: str,
                        banned_words: List[str] = banned_words,
                        replacement_symbols: List[str] = REPLACEMENT_SYMBOLS
                        ) -> str:
                
    banned_pattern = '|'.join(banned_words)     # '|' to catch each banned word
    banned_pattern = re.compile(banned_pattern, flags=re.IGNORECASE)
    def _remove_words(match: re.Match) -> str:
        length = match.end() - match.start()
        replacement = random.choices(replacement_symbols, k=length)
        return ''.join(replacement)
    return re.sub(banned_pattern, _remove_words, tweet)

