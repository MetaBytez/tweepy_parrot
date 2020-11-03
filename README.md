# Tweepy Parrot
A library built on top of [Tweepy](https://www.tweepy.org/), designed to auto generate tweets from data sourced from other users.

A bot made with this library, will stream unique tweets and retweets of the users it follows and/or is followed by. It cleans and parses the words from the tweet into a growing Markov chain, which is later used to generate tweets.


## Setup
---
```bash
pip install tweepy-parrot
```

To setup the bot, you must [setup a Twitter developer account](https://developer.twitter.com/en/apply-for-access), and then either add the following to a `.env` file in your project, or otherwise export them to the runtime environment.

```
TWITTER_API_KEY={YOUR_API_KEY}
TWITTER_API_SECRET={YOUR_API_SECRET}
TWITTER_ACCESS_TOKEN={BOT_ACCESS_TOKEN}
TWITTER_ACCESS_SECRET={BOT_ACCESS_SECRET}
```

Once done, you are ready to use the library.


## Examples
---
A simple example that will store data in a JSON format, and echo Squawks to your terminal, rather than Tweet them out.

```python
from time import sleep

from tweepy_parrot import JSONParrot, ParrotBot

my_parrot = JSONParrot('parrot.json')
my_bot = ParrotBot(my_parrot)

# Call start, to being listening to the data stream.
# follows=True will stream data from accounts the bot follows
# followers=True will stream data from accounts that follow the bot
my_bot.start(follows=False, followers=True)

while True:
    sleep(3600)  # One hour
    print(my_bot.squawk(post=False))
```