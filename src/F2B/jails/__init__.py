import logging
from time import time

from F2B.dynamo import get_match_count


class Jail():
    filters = []

    fail_limit = 3

    fail_window = 3600  # 1 hour

    def __init__(self):
        self.log = logging.getLogger(self.__module__)
        if self.__class__.__name__ == 'Jail':
            self.filters = Jail.filters
        else:
            self.filters = list(set(Jail.filters + self.__class__.filters))

    def check_bans(self, matches):
        self.log.info('Checking matches against jail "{0}"'.format(self.name))
        self.log.debug('Matches: {0}'.format(matches))
        bans = []
        hosts = []

        # Get all the matched IPs from the filters we care about
        for filter_name in self.filters:
            self.log.info('Collecting matches from filter "{0}"'
                          .format(filter_name))
            filter_hosts = [x['Host'] for x in matches.get(filter_name, [])]
            self.log.debug('Found hosts: {0}'.format(filter_hosts))
            hosts.extend(filter_hosts)

        # Remove duplicates
        hosts = list(set(hosts))
        self.log.debug('Final host list: {0}'.format(hosts))

        if self.fail_window:
            self.log.debug('fail_window is set, will filter search to window')
            since = int(time()) - self.fail_window
        else:
            self.log.debug('fail_window is no set, not filtering search window')
            since = None

        for host in hosts:
            self.log.debug('Checking host "{0}" for filter matches')
            match_count = get_match_count(host, self.filters, since=since)
            self.log.debug('Host "{0}" had {1} matches'.format(host,
                                                               match_count))
            if match_count >= self.fail_limit:
                self.log.info('{0} exceeded jail limit and will be banned!'
                              .format(host))
                bans.append(host)

        return bans

    @property
    def name(self):
        if hasattr(self, 'jail_name'):
            return self.jail_name.lower()
        else:
            return self.__class__.__name__.lower()
