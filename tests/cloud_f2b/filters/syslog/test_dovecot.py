import pytest
from uuid import UUID

from cloud_f2b.filters.syslog.dovecot import Dovecot


@pytest.mark.parametrize("test_data,result", [
    ('', False),
    ('This line should never match', False),
    # No login attempts, just a poke
    ('Oct  7 15:16:52 somemx dovecot: imap-login: Disconnected (no auth '
     'attempts in 2 secs): user=<>, rip=101.112.21.68, lip=192.168.0.12, TLS '
     'handshaking: SSL_accept() syscall failed: Success, '
     'session=<7g6ds0higfad873>', {'host': '101.112.21.68'}),
    # Failed login attempt
    ('Dec 17 10:23:19 somemx dovecot: imap-login: Disconnected (auth failed, '
     '1 attempts in 2 secs): user=<some-user>, method=PLAIN, '
     'rip=45.16.128.57, lip=192.168.1.33, TLS: Disconnected, '
     'session=<fgd6gfds786s>', {'host': '45.16.128.57'}),
    # Successful login, don't ban!
    ('Oct  8 06:23:20 mx01 dovecot: imap-login: Login: user=<someone>, '
     'method=PLAIN, rip=54.23.167.124, lip=192.168.0.47, mpid=26058, TLS, '
     'session=<fdghsuidyg78y>', False),
])
def test_dovecot_filters(test_data, result):
    dovecot = Dovecot()

    assert dovecot.test_line(test_data) == result


def test_dovecot_filter_uuid():
    assert Dovecot().uuid == UUID('f456ab4d-74df-56df-8d23-4d0b33f47ae7')
