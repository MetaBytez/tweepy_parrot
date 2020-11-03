from logging import getLogger
from pathlib import Path
from random import choice, choices

from .models import ParrotData

logger = getLogger(__name__)


class Parrot:
    def read_data(self) -> ParrotData:
        raise NotImplementedError

    def write_data(self, data: ParrotData) -> None:
        raise NotImplementedError

    def update_data(self, tweet_id: str, tweet_text: str) -> None:
        raise NotImplementedError

    def squawk(self, character_limit: int = 280) -> str:
        """
        Build a message from the data set with length less than character_limit
        """
        markov_chain = self.read_data().markov_chain
        prev_word = choice(list(markov_chain.keys()))
        squawk_parts = []
        squawk = ' '.join(squawk_parts)

        while len(squawk) < character_limit and markov_chain.get(prev_word, {}):
            squawk_parts.append(prev_word)
            squawk = ' '.join(squawk_parts)
            population, weights = zip(*markov_chain[prev_word].items())
            prev_word = choices(population, weights)[0]

        if len(squawk) > character_limit:
            squawk, __ = squawk.rsplit(maxsplit=1)

        return squawk.title()


class JSONParrot(Parrot):
    """
    An instance of the Parrot class, that uses a JSON as the storage medium
    fo the Markov Chain and Tweet ID data.

    Args:
        data_file_path (str):
            The path to the json file to use. If the path does not exist, it
            will be created.
    """
    def __init__(self, data_file_path: str):
        self.data_file_path = data_file_path
        if not Path(self.data_file_path).exists():
            empty_data = ParrotData(seen_tweets=set(), markov_chain={})
            with open(self.data_file_path, 'w+') as f:
                f.write(empty_data.json(sort_keys=True, indent=4))

    def read_data(self) -> ParrotData:
        return ParrotData.parse_file(self.data_file_path)

    def write_data(self, data: ParrotData) -> None:
        with open(self.data_file_path, 'w+') as f:
            f.write(data.json(sort_keys=True, indent=4))

    def update_data(self, tweet_id: str, tweet_text: str) -> None:
        current_data = self.read_data()
        if tweet_id in current_data.seen_tweets:
            logger.info('Seen Tweet, skipping update')
            return None

        words = tweet_text.split()
        word_chain = zip(words, words[1:])
        for anchor, follow in word_chain:
            anchor_node = current_data.markov_chain.setdefault(anchor, {})
            anchor_node[follow] = anchor_node.setdefault(follow, 0) + 1

        current_data.seen_tweets.add(tweet_id)
        self.write_data(current_data)
