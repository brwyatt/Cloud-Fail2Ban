subs = {
    '__bsd_syslog_verbose': '(<[^.]+\.[^.]+>)',
    '_daemon': '\S*',
    '__daemon_combs_re': '(?:%(__pid_re)s?:\s+%(__daemon_re)s|%(__daemon_re)s%(__pid_re)s?:?)',
    '__daemon_extra_re': '(?:\[ID \d+ \S+\])',
    '__daemon_re': '[\[\(]?%(_daemon)s(?:\(\S+\))?[\]\)]?:?',
    '__date_re': '\S+ \d+ \d+:\d+:\d+',
    'host': '(?P<host>\d{1,3}(?:\.\d{1,3}){3})',
    '__hostname': '\S+',
    '__kernel_prefix': 'kernel: \[ *\d+\.\d+\]',
    '__pid_re': '(?:\[\d+\])',
    '__md5hex': '(?:[\da-f]{2}:){15}[\da-f]{2}',
    '__prefix_line': '\s*%(__bsd_syslog_verbose)s?\s*(?:%(__hostname)s )?(?:%(__kernel_prefix)s )?(?:@vserver_\S+ )?%(__daemon_combs_re)s?\s%(__daemon_extra_re)s?\s*',
}
