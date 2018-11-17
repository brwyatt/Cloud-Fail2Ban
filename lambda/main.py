import json

from cloud_f2b import process_log_events, process_jails, send_bans
import cloud_f2b.filters.auth.sshd
import cloud_f2b.filters.auth.sshd_ddos
import cloud_f2b.jails.sshd
import cloud_f2b.jails.sshd_ddos
from cloud_f2b.logging import setup_logging
from cloud_f2b.utils import decompress_cloudwatch_event


log = setup_logging()


logParsers = {
    'Auth': [
        cloud_f2b.filters.auth.sshd.Sshd,
        cloud_f2b.filters.auth.sshd_ddos.Sshd_Ddos
    ]
}

jails = [
    cloud_f2b.jails.sshd.Sshd,
    cloud_f2b.jails.sshd_ddos.Sshd_Ddos
]


def handle_log_event(event, context):
    log.debug('Received CloudWatch event: {0}'.format(json.dumps(event)))
    event = decompress_cloudwatch_event(event)
    cw_event = event['awslogs']['data']

    # Run parsers on the logs
    matches = False
    if cw_event['logGroup'] in logParsers:
        log.info('Running parsers for {0}'.format(cw_event['logGroup']))
        matches = process_log_events(cw_event['logEvents'],
                                     logParsers[cw_event['logGroup']],
                                     source=cw_event['logStream'])
    else:
        log.critical('Invalid logGroup "{0}"! No parsers available!'
                     .format(cw_event['logGroup']))

    # Run matches against jails
    bans = False
    if matches:
        bans = process_jails(matches, jails)
        log.debug('Banlist: {0}'.format(bans))

    # Send the bans
    if bans:
        send_bans(bans)
