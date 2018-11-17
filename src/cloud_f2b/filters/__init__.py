import logging
import re
from uuid import UUID, uuid5

from cloud_f2b.utils import compile_regex


class Filter():
    subs = {
        '__bsd_syslog_verbose': '(<[^.]+\.[^.]+>)',
        '_daemon': '\S*',
        '__daemon_combs_re': '(?:%(__pid_re)s?:\s+%(__daemon_re)s|%(__daemon_re)s%(__pid_re)s?:?)',
        '__daemon_extra_re': '(?:\[ID \d+ \S+\])',
        '__daemon_re': '[\[\(]?%(_daemon)s(?:\(\S+\))?[\]\)]?:?',
        '__date_re': '\S+ +\d+ +\d+:\d+:\d+',
        'host': '(?P<host>\d{1,3}(?:\.\d{1,3}){3})',
        '__hostname': '\S+',
        '__kernel_prefix': 'kernel: \[ *\d+\.\d+\]',
        '__pid_re': '(?:\[\d+\])',
        '__md5hex': '(?:[\da-f]{2}:){15}[\da-f]{2}',
        '__prefix_line': '%(__date_re)s %(__hostname)s %(_daemon)s%(__pid_re)s: ',
    }

    failregexes = []

    ttl = 86400  # 1 Day

    uuid = UUID('c1a820c0-5a1e-4d99-8234-1bdf71aec514')

    def __init__(self):
        self.log = logging.getLogger(self.__module__)
        if self.__class__.__name__ == 'Filter':
            self.subs = Filter.subs
            self.failregexes = Filter.failregexes
            self.uuid = Filter.uuid
        else:
            self.subs = {**Filter.subs, **self.__class__.subs}
            self.failregexes = list(set(Filter.failregexes +
                                    self.__class__.failregexes))
            self.uuid = uuid5(Filter.uuid, '{0}.{1}'.format(
                self.__module__, self.__class__.__name__))
        self.compile_failregexes()

    def compile_failregexes(self):
        self.log.debug('Compiling/resolving regular expression list')
        compiled_failregexes = []
        for failregex in self.failregexes:
            compiled_failregex = compile_regex(failregex, self.subs).strip()
            compiled_failregexes.append(compiled_failregex)
            self.log.debug('Compiled "{0}" to "{1}"'.format(
                failregex, compiled_failregex))

        self.failregexes = compiled_failregexes
        self.log.debug('Regex compile complete')

    def test_line(self, log_line):
        self.log.debug('Testing "{0}"'.format(log_line))
        log_line = log_line.strip()
        for failregex in self.failregexes:
            self.log.debug('Testing against "{0}"'.format(failregex))
            match = re.match(failregex, log_line)
            self.log.debug('match = {0}'.format(match))
            if match:
                self.log.debug('Found match against "{0}"'.format(failregex))
                return match.groupdict()

        return False
