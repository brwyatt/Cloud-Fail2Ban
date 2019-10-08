import json

from cloud_f2b import process_log_events, process_jails, send_bans
import cloud_f2b.filters.auth.sshd
import cloud_f2b.filters.syslog.dovecot
import cloud_f2b.filters.syslog.roundcube
import cloud_f2b.jails.dovecot
import cloud_f2b.jails.roundcube
import cloud_f2b.jails.sshd
from cloud_f2b.logging import setup_logging
from cloud_f2b.utils import decompress_cloudwatch_event


log = setup_logging()


logParsers = {
    'Auth': [
        cloud_f2b.filters.auth.sshd.Sshd,
    ],
    'Syslog': [
        cloud_f2b.filters.syslog.dovecot.Dovecot,
        cloud_f2b.filters.syslog.roundcube.Roundcube,
    ],
}

jails = [
    cloud_f2b.jails.dovecot.Dovecot,
    cloud_f2b.jails.roundcube.Roundcube,
    cloud_f2b.jails.sshd.Sshd,
]


def unpack_cloudwatch_event(event):
    event = decompress_cloudwatch_event(event)
    cw_event = event['awslogs']['data']

    return cw_event


def run_filters(cw_event):
    log.debug('Running filters')
    matches = False
    if cw_event['logGroup'] in logParsers:
        log.info('Running parsers for {0}'.format(cw_event['logGroup']))
        matches = process_log_events(cw_event['logEvents'],
                                     logParsers[cw_event['logGroup']],
                                     source=cw_event['logStream'])
    else:
        log.critical('Invalid logGroup "{0}"! No parsers available!'
                     .format(cw_event['logGroup']))

    log.debug('Matches: {0}'.format(matches))
    return matches


def run_jails(matches):
    # Run matches against jails
    bans = False
    if matches:
        bans = process_jails(matches, jails)
        log.debug('Banlist: {0}'.format(bans))

    # Send the bans
    if bans:
        send_bans(bans)
