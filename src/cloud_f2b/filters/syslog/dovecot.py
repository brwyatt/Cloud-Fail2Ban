from cloud_f2b.filters import Filter


class Dovecot(Filter):
    subs = {
        '_daemon': 'dovecot',
    }

    failregexes = [
        '^%(__prefix_line)s(?: pop3-login|imap-login): .*(?:Authentication failure|Aborted login \(auth failed|Aborted login \(tried to use disabled|Disconnected \((auth failed|no auth attempts)|Aborted login \(\d+ authentication attempts).*rip=%(host)s.*$'
    ]
