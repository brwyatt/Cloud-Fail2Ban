import pytest
from uuid import UUID

from cloud_f2b.filters.syslog.postfix import Postfix


@pytest.mark.parametrize("test_data,result", [
    ('', False),
    ('This line should never match', False),
    # Some known logs we want to ban for
    ('Oct 13 12:23:28 someserver postfix/smtpd[2197]: NOQUEUE: reject: RCPT '
     'from some1.something.net[64.58.127.123]: 454 4.7.1 '
     '<someone@somewhere.com>: Relay access denied; '
     'from=<someoneelse@somewhereelse.net> to=<someone@somewhere.com> '
     'proto=ESMTP helo=<test>', {'host': '64.58.127.123'}),
    ('Apr  7 17:33:20 someserver postfix/smtpd[645]: warning: '
     'unknown[75.68.251.15]: SASL LOGIN authentication failed: Invalid '
     'authentication mechanism', {'host': '75.68.251.15'}),
    ('Feb 12 11:54:33 someserver postfix/smtpd[7354]: warning: '
     'unknown[28.74.222.62]: SASL PLAIN authentication failed:',
     {'host': '28.74.222.62'}),
    ('Dec 26 01:27:12 someserver postfix/smtpd[84]: NOQUEUE: reject: RCPT from '
     'unknown[129.129.54.7]: 554 5.7.1 <some1@somewhere.net>: Relay access '
     'denied; from=<some1else@somewhereesle.com> to=<some1@somewhere.net> '
     'proto=ESMTP helo=<example.net>', {'host': '129.129.54.7'}),
    ('Nov 15 08:06:07 someserver postfix/smtpd[9842]: NOQUEUE: reject: RCPT '
     'from ahost.1net.eu[84.236.187.129]: 554 5.7.1 '
     '<recipient@otherdomain.org>: Relay access denied; '
     'from=<sender@domain.net> to=<recipient@otherdomain.org> proto=SMTP '
     'helo=<blahblah>', {'host': '84.236.187.129'}),
    ('Oct 21 12:39:34 someserver postfix/smtpd[775]: too many errors after '
     'RCPT from unknown[65.64.87.19]', {'host': '65.64.87.19'}),
    ('Jun 30 07:19:09 someserver postfix/smtpd[6548]: warning: '
     'somehost.somewhere.com[47.58.101.54]: SASL LOGIN authentication failed: '
     'Invalid authentication mechanism', {'host': '47.58.101.54'}),
    ('Aug  8 12:25:14 someserver postfix/smtpd[1287]: 3DB2B41A4A: reject: RCPT '
     'from unknown[111.57.64.47]: 550 5.1.1 <someone@somewhere.com>: Recipient '
     'address rejected: User unknown in virtual mailbox table; '
     'from=<some1else@some-domain.ru> to=<some1@somewhere.com> proto=ESMTP '
     'helo=<[121.219.14.24]>', {'host': '111.57.64.47'}),
    ('May  6 13:08:34 someserver postfix/smtpd[168]: NOQUEUE: reject: RCPT '
     'from unknown[52.212.87.45]: 550 5.1.1 <noone@nowhere.net>: Recipient '
     'address rejected: User unknown in virtual mailbox table; '
     'from=<hacker@hackers.net> to=<noone@nowhere.net> proto=ESMTP '
     'helo=<harckers.org>', {'host': '52.212.87.45'}),
    # Some logs we DON'T want to ban for
    ('Oct  2 20:07:04 somemx postfix/smtpd[3415]: connect from '
     'unknown[13.57.129.211]', False),
    ('Sep 12 12:25:15 someserver postfix/smtpd[2359]: disconnect from '
     'unknown[43.10.182.154] ehlo=1 auth=0/1 quit=1 commands=2/3', False),
    ('Jan  2 09:18:21 somehost postfix/smtp[14110]: 2BE0747C9D: '
     'to=<someone@somewhere.net>, relay=otherhost.somwhere.net'
     '[24.38.20.99]:587, delay=0.22, delays=0.02/0/0.08/0.11, dsn=2.0.0, '
     'status=sent (250 2.0.0 Ok: queued as AB4C9D088E)', False),
    ('Feb 13 13:26:14 somewhere postfix/smtp[850]: connect to '
     'someother.host.com[1406:e9c5:51e2:4f8::2c]:25: Network is unreachable',
     False),
    ('Oct 13 07:19:21 somehost postfix/smtp[182]: 1FD11A50B9: '
     'to=<someone@somewhere.net>, relay=none, delay=0.22, '
     'delays=0.01/0.12/0.21/0, dsn=4.4.1, status=deferred (connect to '
     'othermx.somewhere.com[3214:22c9:a11f:2ac::51f]:25: Network is '
     'unreachable)', False),
    ('Mar 25 21:19:42 somewhere postfix/smtp[31419]: 8F42BB2CA8: Server '
     'certificate not verified', False),
    ('Jul 24 11:40:52 somehost postfix/smtpd[4439]: lost connection after '
     'CONNECT from unknown[187.68.54.72]', False),
])
def test_postfix_filters(test_data, result):
    postfix = Postfix()

    assert postfix.test_line(test_data) == result


def test_postfix_filter_uuid():
    assert Postfix().uuid == UUID('7fb12b93-a76f-5651-acf5-421b0ee73b64')
