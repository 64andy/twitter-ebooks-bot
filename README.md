# twitter-ebooks-bot
### ***Archival*** - *A Twitter ebooks bot using Markov Chains &amp; NLP.*

* Originally hosted on [replit](https://replit.com/@64andy2000/twitter-ebooks-bot)

---

This bot was created for a friend, as an "ebooks" style bot (takes source tweets, posts new tweets).
It uses Markov Chains (markovify) to generate the tweets, and NLP (nltk) so it understands the source sentence structure

This bot was discontinued in June 2021

### Setup:
1. The required packages are in `requirements.txt`, to install run `pip install -r requirements.txt`
2. Change the settings in `e_books/settings.py`, specifically the `user_handle`
3. Add your bot account's 4 API keys to a `.env` file (see the provided file)
4. Run the `main.py`

---

This bot used a repl.it hack with Flask to keep it constantly running.
Flask hack from [@GarethDwyer1](https://replit.com/@GarethDwyer1/discord-bot)