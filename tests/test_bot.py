import pytest

from tweepy_parrot.bot import REQUIRED_FIELD_MAP


@pytest.mark.parametrize(
    'field_key,',
    (
        'API Key',
        'API Secret',
        'Access Token',
        'Access Secret',
    )
)
def test_missing_required_fields(mocker, parrot_bot_factory, field_key):
    old_val = REQUIRED_FIELD_MAP[field_key]
    REQUIRED_FIELD_MAP[field_key] = None
    with pytest.raises(ValueError, match=f'Missing required environment variable for {field_key}'):
        parrot_bot_factory()
    REQUIRED_FIELD_MAP[field_key] = old_val


def test_credential_verification_fail(mocker, parrot_bot_factory):
    mocker.patch('tweepy.API.verify_credentials', return_value=False)
    with pytest.raises(ValueError, match='Failed to verify Twitter Credentials'):
        parrot_bot_factory()


@pytest.mark.twitter
def test_credential_verification(parrot_bot_factory):
    parrot_bot_factory()
