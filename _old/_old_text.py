"""Functions that work with text"""
import random
import re
from html import unescape
from .settings import target_length, min_group_len, max_group_len, fortnite_sucks

TWITTER_URL_REGEX = r"(https:\/\/t.co\/)\w+"    # Catches t.co links
HARD_LIMIT = 280            # The absolute maximum tweet length
TOO_LONG_APPEND = '…'       # If the tweet hits the hard limit, append it with this
REPLACEMENT_SYMBOLS = [
    '■', '□', '▢', '▣', '▤', '▥', '▦', '▧', '▨', '▩', '▪', '▫',
    '▬', '▭', '▮', '▯', '▰', '▱', '▲', '△', '▴', '▵', '▶',
    '▷', '▸', '▹', '►', '▻', '▼', '▽', '▾', '▿', '◀', '◁', '◂',
    '◃', '◄', '◅', '◆', '◇', '◈', '◉', '◊', '○', '◌', '◍', '◎',
    '●', '◐', '◑', '◒', '◓', '◔', '◕', '◖', '◗', '◘', '◙', '◚',
    '◛', '◜', '◝', '◞', '◟', '◠', '◡', '◢', '◣', '◤', '◥', '◦',
    '◧', '◨', '◩', '◪', '◫', '◬', '◭', '◮', '◯', '◰', '◱', '◲',
    '◳', '◴', '◵', '◶', '◷','◸', '◹', '◺', '◻', '◼', '◽', '◾', '◿']


def obfuscate_word(text: str, bad_word: str, symbols=REPLACEMENT_SYMBOLS) -> str:
    """Replaces every instance of `bad_word` in `text` with a random selection of symbols
    Example:
    ```python
    >>> text = "The way the sun shines"
    >>> bad_word = "the"
    >>> obfuscate_word(text, bad_word)
    '◟◌◵ way ▪▥▽ sun shines'
    """
    word_list = text.split()
    bad_word = bad_word.lower()
    for pos, word in enumerate(word_list):
        if word.lower() == bad_word:
            replacement_text = ''.join(random.choices(symbols, k=len(bad_word)))
            word_list[pos] = replacement_text
    return ' '.join(word_list)


def message_len(message_list: list) -> int:
    """Returns the length of a list of strings, as if they were concatenated into a string
    e.g. `["Hello", "There"]` -> "Hello There" -> 11 chars long
    Note: Calculating the length of the list and the length of each element, is 2x slower than generating a string. Don't know why"""
    return len(" ".join(message_list));


def grouped_words(text: str, min_len:int=min_group_len, max_len:int=max_group_len) -> list:
    r"""Generates a list of grouped words. Each group has a random amount of words between `min_len <= x <= max_len`
    A word is a group of characters seperated by whitespace i.e. spaces, tabs, newlines.
    e.g. "A B C D\nE F G" -> ["A B C D E", "F G"]
    Note that all whitespace will get replaced by a single space character. RIP newlines"""
    text = unescape(text)                               # "&lt;" => "<" etc.  
    text = re.sub(TWITTER_URL_REGEX, "", text)          # Removes t.co links
    text = text.split()                                 # Split into individual words
    grouped_words = []
    while text:
        number_of_words = random.randint(min_len, max_len)
        word_group = " ".join(text[:number_of_words])[:60]  #[:60] prevents 280 char long words messing everything up
        grouped_words.append(word_group)
        text = text[number_of_words:]                   # Remove the used words
    return grouped_words


def generate_ebook(word_list: list, target_len:int=target_length) -> str:
    """Takes a list of list of string (e.g. `[['Hi', 'There'],['Good', 'Day']]`), returns a string pieced together from said strings."""
    word_list = [word for word in word_list if word]  # Gets rid of all the tweets that don't contain text
    message_list = []                                   # Where the grouped words get stored before getting concatinated
    position = 0
    """Logic: The input is a bunch of tweets chopped into word groups ["I do not", "like", "red salmon fish"], ...
    Take a random tweet, grab its first word group, put that in the tweet.
    Take another random tweet, grab its second word group, so on and so forth.
    If the ebook's length is beyond the target_len, just stop generating and push it out the door
    If it indexes beyond a tweet's amount of word groups e.g. fifth word group of a 2 word group long tweet,
        grab that tweet's final element and stop processing
    The output is those word group pieced together in order. It's random, but structured so it's usually mostly coherent
    """
    while message_len(message_list) < target_len:       # If it starts getting too long, just stop
        word_group = random.choice(word_list)
        if len(word_group) <= position:                 # If indexing would raise an error
            message_list.append(word_group[-1])         # The ebook might read nicer if it ends with the end of an actual tweet
            break;                                      # Stop ebook generation, move along
        else:
            message_list.append(word_group[position])
            word_list.remove(word_group)
        position += 1

    message = " ".join(message_list)
    message = message.replace("@", "@.")   # Prevents @user from getting notification spam from mentions
    # Added this condition because the bot kept getting notifs
    # from Fortnite players liking any tweet mentioning "fortnite"
    # for some reason
    if fortnite_sucks:
        message = obfuscate_word(message, "fortnite")
    if len(message) > HARD_LIMIT:
        # If the message is too long, truncate it and add a '…'
        message = message[:HARD_LIMIT-len(TOO_LONG_APPEND)] + TOO_LONG_APPEND
    return message