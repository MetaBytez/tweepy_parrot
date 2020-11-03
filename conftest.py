import pytest

from tweepy_parrot import ParrotBot
from tweepy_parrot.models import ParrotData
from tweepy_parrot.parrots import JSONParrot


@pytest.fixture
def parrot_bot_factory(mocker):
    def _factory(listener=None, parrot=None):
        listener = listener or mocker.MagicMock()
        parrot = parrot or mocker.MagicMock()
        return ParrotBot(listener, parrot)
    return _factory


@pytest.fixture
def json_parrot_factory(tmp_path):
    def _factory(file_name='parrot_test.json'):
        test_file = tmp_path / file_name
        return JSONParrot(str(test_file.absolute()))
    return _factory


@pytest.fixture
def parrot_data_factory():
    def _factory(seen_tweets=None, markov_chain=None):
        seen_tweets = seen_tweets or set()
        markov_chain = markov_chain or {}
        return ParrotData(seen_tweets=seen_tweets, markov_chain=markov_chain)
    return _factory
