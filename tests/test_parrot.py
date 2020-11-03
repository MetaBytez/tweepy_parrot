import pytest


def test_parrot_initializes_file(tmp_path, json_parrot_factory, parrot_data_factory):
    file_path = tmp_path / 'init.json'
    assert file_path.exists() is False

    empty_data = parrot_data_factory()
    jp = json_parrot_factory('init.json')

    assert file_path.exists() is True
    assert jp.read_data() == empty_data


def test_repeat_tweets_ignored(json_parrot_factory):
    jp = json_parrot_factory()

    jp.update_data('1234', 'Test Potato')
    initial_data = jp.read_data()
    jp.update_data('1234', 'Test Tomato')
    updated_data = jp.read_data()

    assert initial_data == updated_data


@pytest.mark.parametrize(
    'character_limit,',
    (
        280,
        140,
        20
    )
)
def test_squawk(json_parrot_factory, parrot_data_factory, character_limit):
    jp = json_parrot_factory()
    looping_data = parrot_data_factory(
        markov_chain={
            'apple': {
                'banana': 1
            },
            'banana': {
                'apple': 1
            }
        }
    )
    jp.write_data(looping_data)

    squawk = jp.squawk(character_limit)

    assert len(squawk) < character_limit
    assert set(squawk.split()).issubset({'Apple', 'Banana'})
