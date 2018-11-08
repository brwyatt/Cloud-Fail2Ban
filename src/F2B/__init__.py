import logging
from uuid import uuid5

log = logging.getLogger()


def process_log_events(log_events, parsers):
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
                matches[parser_name].append({
                    'Host': resp['host'],
                    'EventID': event['id'],
                    'MatchID': uuid5(parser_instance.uuid, event['id']),
                    'timestamp': event['timestamp']
                })
            else:
                log.debug('No match!')
    return matches
