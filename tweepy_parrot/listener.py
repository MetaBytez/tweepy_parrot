import re
from logging import getLogger

from tweepy import StreamListener

from .data import BANNED_WORDS
from .parrots import Parrot

logger = getLogger(__name__)


class ParrotListener(StreamListener):
    RT_REGEX = re.compile(r'rt @\w*: ')
    URL_REGEX = re.compile(r'https?:\/\/\S*')
    MIXED_DIGITS_REGEX = re.compile(r'\w*\d+\w*')
    ALPHA_ONLY_REGEX = re.compile(r'[^a-z\s]')
    REPEAT_SPACE_REGEX = re.compile(r'\s+')

    CLEANERS = [
        RT_REGEX,
        URL_REGEX,
        MIXED_DIGITS_REGEX,
        ALPHA_ONLY_REGEX,
    ]

    def __init__(self, parrot: Parrot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parrot = parrot

    def _clean_text(self, text):
        cleaned_text = text.lower()
        if any([
            banned_word in cleaned_text
            for banned_word in BANNED_WORDS
        ]):
            return ''

        for cleaner in self.CLEANERS:
            cleaned_text = cleaner.sub('', cleaned_text)

        cleaned_text = self.REPEAT_SPACE_REGEX.sub(' ', cleaned_text)

        return cleaned_text.strip().lower()

    def on_status(self, status):
        try:
            extended_tweet = getattr(status, 'extended_tweet', {})
            cleaned_text = extended_tweet.get('full_text', status.text)

            cleaned_text = self._clean_text(cleaned_text)

            if not cleaned_text:
                logger.info('Cleaned Text is Empty')
                return None

            logger.info(f'Adding Tweet to data set: {status.id}')

            self.parrot.update_data(str(status.id), cleaned_text)

        except Exception as e:
            logger.exception('Exception enountered in on_status: ' + str(e))

    def on_error(self, status_code):
        logger.error(f'Error in Listener: {status_code}')
