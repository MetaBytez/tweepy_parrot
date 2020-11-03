from logging import getLogger
from typing import Type

from tweepy import API, OAuthHandler, Stream, Cursor

from .listener import ParrotListener
from .parrots import Parrot
from .settings import (
    TWITTER_ACCESS_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
)

logger = getLogger(__name__)
REQUIRED_FIELD_MAP = {
    'API Key': TWITTER_API_KEY,
    'API Secret': TWITTER_API_SECRET,
    'Access Token': TWITTER_ACCESS_TOKEN,
    'Access Secret': TWITTER_ACCESS_SECRET,
}


class ParrotBot:
    """
    Manager class for a ParrotBot. Given an instance of a Listener and Parrot,
    provides utilities for managing the bot.

    Args:
        Parrot (Parrot):
            The Parrot responsible for handling the data operations for the
            bot.
        Listener (Type[ParrotListener]):
            The Listener class used to pipe stream data into the bot. Defaults to
            tweepy_parrot.ParrotListener
    """
    def __init__(
        self,
        parrot: Parrot,
        listener_class: Type[ParrotListener] = ParrotListener,
    ) -> None:
        for field_name, val in REQUIRED_FIELD_MAP.items():
            if val is None:
                raise ValueError(f'Missing required environment variable for {field_name}')

        auth = OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
        api = API(auth)

        if not api.verify_credentials():
            raise ValueError('Failed to verify Twitter Credentials')

        self.parrot = parrot
        self.listener = listener_class(self.parrot)
        self._api = api
        self._stream = Stream(self._api.auth, self.listener, daemon=True)
        self._filter_params = (False, False)

    def start(self, follows: bool = True, followers: bool = False) -> None:
        self._filter_params = (follows, followers)
        self._stream.disconnect()
        filtered_user_ids = set()
        if follows:
            for follow in Cursor(self._api.friends).items():
                filtered_user_ids.add(str(follow.id))
        if followers:
            for follower in Cursor(self._api.followers).items():
                filtered_user_ids.add(str(follower.id))

        logger.info(f'Starting Parrot stream with filter IDs: {filtered_user_ids}')
        self._stream.filter(
            follow=filtered_user_ids,
            is_async=True,
            languages=['en']
        )

    def stop(self) -> None:
        self._stream.disconnect()

    def refresh(self) -> None:
        """Refreshes the Twitter stream sources, with the last called args"""
        self.start(*self._filter_params)

    def post(self, msg: str) -> None:
        """Post the given message to the Bot Twitter"""
        self._api.update_status(msg)

    def squawk(self, post=True, character_limit: int = 280) -> str:
        """
        Get a squawk from the managed Parrot instance. If post is True, will
        also post the squawk to the bot twitter. Always retursn the squawk.
        """
        squawk = self.parrot.squawk(character_limit)
        if post:
            self.post(squawk)
        return squawk
