from cloud_f2b.filters import Filter


class Roundcube(Filter):
    subs = {
        '_daemon': 'roundcube',
    }

    failregexes = [
        '^%(__prefix_line)s\<\S+\> IMAP Error: Login failed for \S+ from %(host)s\. AUTHENTICATE \S*: Authentication failed\. .*$',
    ]
