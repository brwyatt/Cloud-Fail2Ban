import json

from cloud_f2b import process_log_events, process_jails, send_bans
import cloud_f2b.filters.auth.sshd
import cloud_f2b.filters.auth.sshd_ddos
import cloud_f2b.jails.sshd
import cloud_f2b.jails.sshd_ddos
from cloud_f2b.logging import setup_logging
from cloud_f2b.utils import (decompress_cloudwatch_event,
                             dynamodb_event_to_matches)


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


def unpack_cloudwatch_event(event):
    log.debug('Received CloudWatch event: {0}'.format(json.dumps(event)))
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


def cloudwatch_run_filters(event, context):
    """
    Lambda function for receiving events from CloudWatch and checking against
    defined filters.

    This is the first phase of the 2-phase variant.
    """
    run_filters(unpack_cloudwatch_event(event))


def run_jails(matches):
    # Run matches against jails
    bans = False
    if matches:
        bans = process_jails(matches, jails)
        log.debug('Banlist: {0}'.format(bans))

    # Send the bans
    if bans:
        send_bans(bans)


def cloudwatch_run_filters_and_jails(event, context):
    """
    Lambda function for receiving events from CloudWatch and checking against
    defined filters and checking matches against the jails then sending ban
    alerts.

    This is the single-phase variant.
    """
    matches = run_filters(unpack_cloudwatch_event(event))
    run_jails(matches)


def dynamodb_run_jails(event, context):
    """
    Lambda function for receiving events from DynamoDB and checking against
    defined jails and sending ban alerts.

    This is the second phase of the 2-phase variant.
    """
    log.debug('Received DynamoDB event: {0}'.format(json.dumps(event)))
    matches = dynamodb_event_to_matches(event)
    run_jails(matches)
