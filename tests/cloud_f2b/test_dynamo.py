import pytest

import cloud_f2b.dynamo as dynamo


def test_add_match():
    assert dynamo.add_match('0.0.0.0', 'xxxxx', 'TEST', 12345, 30)
    assert dynamo.add_match('0.0.0.0', 'xxxxx', 'TEST', 12345, 30,
                            source='Somewhere', eventid='1234')


def test_add_match_exception(mock_dynamo_table_put_item_exception):
    assert not dynamo.add_match('0.0.0.0', 'xxxxx', 'TEST', 12345, 30)
    assert not dynamo.add_match('0.0.0.0', 'xxxxx', 'TEST', 12345, 30,
                                source='Somewhere', eventid='1234')


def test_add_match_http_error(mock_dynamo_table_put_item_http_error):
    assert not dynamo.add_match('0.0.0.0', 'xxxxx', 'TEST', 12345, 30)
    assert not dynamo.add_match('0.0.0.0', 'xxxxx', 'TEST', 12345, 30,
                                source='Somewhere', eventid='1234')


def test_get_match_count():
    assert dynamo.get_match_count('0.0.0.0', 'Filter1') == 0
    assert dynamo.get_match_count('0.0.0.0', ['Filter1']) == 0
    assert dynamo.get_match_count('0.0.0.0', ['Filter1', 'Filter2']) == 0
    assert dynamo.get_match_count('0.0.0.0', ['Filter1'], since=12345) == 0


def test_get_match_count_filter_type_error():
    with pytest.raises(TypeError):
        dynamo.get_match_count('0.0.0.0', 1234)

    with pytest.raises(TypeError):
        dynamo.get_match_count('0.0.0.0', [1234])


def test_get_match_count_since_type_error():
    with pytest.raises(TypeError):
        dynamo.get_match_count('0.0.0.0', ['Filter'], since='Fail')
