import pytest
from uuid import UUID

from cloud_f2b.filters.auth.sshd import Sshd


@pytest.mark.parametrize("test_data,result", [
    ('', False),
    ('This line should never match', False),
    ('Nov  3 18:55:57 localhost sshd[12345]: Invalid user test from '
     '111.222.123.213', {'host': '111.222.123.213'}),
    ('Jan  8 12:32:24 bastion sshd[393]: Invalid user badguy from '
     '11.252.23.135 port 21464', {'host': '11.252.23.135'}),
    ('Dec 13 11:04:35 somehost sshd[6382]: Invalid user admin from '
     '21.42.94.20', {'host': '21.42.94.20'}),
    ('Apr  3 01:44:26 sshserver sshd[347]: Invalid user mysql from '
     '35.51.65.41 port 64743', {'host': '35.51.65.41'}),
    ('Dec 13 11:04:35 somehost notsshdfail[6382]: Invalid user admin from '
     '21.42.94.20', False),
    ('Jun 25 05:39:22 someserver notsshdfail[11111]: Invalid user superuser '
     'from 61.36.192.120 port 4356', False),
])
def test_sshd_filters(test_data, result):
    sshd = Sshd()

    assert sshd.test_line(test_data) == result


def test_sshd_filter_uuid():
    assert Sshd().uuid == UUID('d758d7bb-b183-58e8-8119-5c8d27e2042b')
