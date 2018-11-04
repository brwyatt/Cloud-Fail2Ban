import pytest

import F2B.dynamo as dynamo


def test_add_fail():
    assert dynamo.add_fail('127.0.0.1', '1245456546541', 'sshd', 3600)


def test_check_ban():
    assert not dynamo.check_ban('127.0.0.1', 'sshd')
