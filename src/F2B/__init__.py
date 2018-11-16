import json
import logging
from uuid import uuid5

import boto3

from F2B.dynamo import add_match

log = logging.getLogger()


def process_log_events(log_events, parsers, source=None):
    matches = {}
    for parser in parsers:
        parser_name = '{0}.{1}'.format(parser.__module__, parser.__name__)
        log.info('Running parser "{0}"'.format(parser_name))
        parser_instance = parser()
        for event in log_events:
            resp = parser_instance.test_line(event['message'])
            log.debug('resp: {0}'.format(resp))
            if resp and 'host' in resp:
                log.info('Found match! Host: {0}'.format(resp['host']))
                if parser_name not in matches:
                    matches[parser_name] = []
                match = {
                    'Host': resp['host'],
                    'MatchID': uuid5(parser_instance.uuid, event['id']),
                    # Convert miliseconds
                    'Timestamp': int(event['timestamp']/1000)
                }
                log.debug('Match data: {0}'.format(match))
                add_match(match['Host'], match['MatchID'], parser_name,
                          match['Timestamp'], parser_instance.ttl,
                          source=source, eventid=event['id'])
                matches[parser_name].append(match)
            else:
                log.debug('No match!')
    return matches


def process_jails(matches, jails):
    bans = {}
    for jail in jails:
        jail_name = '{0}.{1}'.format(jail.__module__, jail.__name__)
        log.info('Running jail "{0}"'.format(jail_name))
        jail_instance = jail()
        jail_bans = jail_instance.check_bans(matches)
        if len(jail_bans) > 0:
            bans[jail_instance.name] = list(set(
                bans.get(jail_instance.name, []) + jail_bans))

    return bans


def send_bans(bans):
    sns = boto3.resource('sns')
    topic = sns.create_topic(Name='F2B')

    msgs = []

    for jail in bans:
        log.info('Publishing ban for "{0}": {1}'
                 .format(jail, bans[jail]))
        msg = json.dumps({jail: bans[jail]})
        msg_attr = {
            'jail': {
                'DataType': 'String',
                'StringValue': jail
            }
        }
        res = topic.publish(
            Message=msg,
            MessageAttributes=msg_attr
        )
        msgs.append({'Message': msg, 'MessageAttributes': msg_attr})

        log.debug('Publish result: {0}'.format(res))

    return msgs
