import pytest

import F2B.dynamo as dynamo


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


def test_check_ban():
    assert not dynamo.check_ban('127.0.0.1', 'sshd')
