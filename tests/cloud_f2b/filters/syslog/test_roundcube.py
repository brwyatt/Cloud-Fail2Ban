import pytest
from uuid import UUID

from cloud_f2b.filters.syslog.roundcube import Roundcube


@pytest.mark.parametrize("test_data,result", [
    ('', False),
    ('This line should never match', False),
    ('Oct  7 16:24:08 somemailserver roundcube: <au74df2> IMAP Error: Login '
     'failed for user@mail.host from 123.111.64.12. AUTHENTICATE PLAIN: '
     'Authentication failed. in /opt/roundcube/install/roundcubemail-1.0.0/'
     'program/lib/Roundcube/rcube_imap.php on line 123 (POST '
     '/?_task=login&_action=login)', {'host': '123.111.64.12'}),
    ('Dec 17 17:03:22 othermailserver roundcube: <65gfds3> IMAP Error: Login '
     'failed for user@mail.host from 119.41.164.212. AUTHENTICATE CRAM-MD5: '
     'Authentication failed. in /opt/roundcube/install/roundcubemail-1.0.0/'
     'program/lib/Roundcube/rcube_imap.php on line 123 (POST '
     '/?_task=login&_action=login)', {'host': '119.41.164.212'}),
    ('Jan 25 01:15:43 somewhere sshd: <au74df2> IMAP Error: Login failed for '
     'user@mail.host from 123.111.64.12. AUTHENTICATE PLAIN: '
     'Authentication failed. in /opt/roundcube/install/roundcubemail-1.0.0/'
     'program/lib/Roundcube/rcube_imap.php on line 123 (POST '
     '/?_task=login&_action=login)', False),  # Wrong daemon name
    ('Feb 16 06:54:27 othermailserver roundcube: <sg7fds> DB Error: [0128] '
     'Unknown column \'oops\' in \'field list\' (SQL Query: UPDATE '
     '`users` SET `oops` = \'fail\' WHERE `user_id` = \'0\') in '
     '/opt/roundcube/install/roundcubemail-1.0.0/program/lib/Roundcube/'
     'rcube_db.php on line 321 (POST /?_task=login&_action=login)',
     False),  # Not an error we're looking for
])
def test_roundcube_filters(test_data, result):
    roundcube = Roundcube()

    assert roundcube.test_line(test_data) == result


def test_roundcube_filter_uuid():
    assert Roundcube().uuid == UUID('7951e432-57d5-5692-9173-1b4cdbb9e5ed')
