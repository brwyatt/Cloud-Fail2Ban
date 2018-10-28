import re

from F2B.utils import compile_regex


class Filter():
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
        '__prefix_line': '%(__date_re)s %(__hostname)s %(_daemon)s%(__pid_re)s: ',
    }

    failregexes = []

    def __init__(self):
        if self.__class__.__name__ == 'Filter':
            self.subs = Filter.subs
            self.failregexes = Filter.failregexes
        else:
            self.subs = {**Filter.subs, **self.__class__.subs}
            self.failregexes = list(set(Filter.failregexes +
                                    self.__class__.failregexes))
        self.compile_failregexes()

    def compile_failregexes(self):
        compiled_failregexes = []
        for failregex in self.failregexes:
            compiled_failregexes.append(compile_regex(failregex, self.subs))

        self.failregexes = compiled_failregexes

    def test_line(self, log_line):
        for failregex in self.failregexes:
            match = re.match(failregex, log_line)
            if match:
                return match

        return False
