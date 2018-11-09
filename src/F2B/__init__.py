import logging
from uuid import uuid5

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
                    'Timestamp': event['timestamp']
                }
                log.debug('Match data: {0}'.format(match))
                add_match(match['Host'], match['MatchID'], parser_name,
                          match['Timestamp'], parser_instance.ttl,
                          source=source, eventid=event['id'])
                matches[parser_name].append(match)
            else:
                log.debug('No match!')
    return matches
