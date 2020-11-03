from os import getenv

from dotenv import load_dotenv

load_dotenv()


TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = getenv('TWITTER_API_SECRET')

TWITTER_ACCESS_TOKEN = getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = getenv('TWITTER_ACCESS_SECRET')
