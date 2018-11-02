import base64
import gzip
import json
import logging
import os

from F2B.filters.auth.sshd import Sshd
from F2B.filters.auth.sshd_ddos import Sshd_Ddos


log = logging.getLogger()
try:
        log.setLevel(getattr(logging, os.environ['LOGLEVEL']))
        log.info('LogLevel set to {0} by environment variable'
                 .format(os.environ['LOGLEVEL']))
except:
        log.setLevel(logging.WARNING)

logParsers = {
    'Auth': [Sshd, Sshd_Ddos]
}


def handle_log_event(event, context):
        log_event_compressed = event['awslogs']['data']
        log_event = json.loads(str(gzip.decompress(base64.b64decode(
            log_event_compressed)), 'utf-8'))

        if log_event['logGroup'] in logParsers:
            log.info('Running parsers for {0}'.format(log_event['logGroup']))
            for parser in logParsers[log_event['logGroup']]:
                log.info('  Running parser "{0}"'.format(parser.__name__))
                parser_instance = parser()
                for event in log_event['logEvents']:
                    log.info('    Testing line: {0}'.format(event['message']))
                    resp = parser_instance.test_line(event['message'])
                    if resp and 'host' in resp.groupdict():
                        log.warning('      Found match! Host: {0}'.format(
                            resp.group('host')))
        else:
            log.critical('Invalid logGroup "{0}"! No parsers available!'
                         .format(log_event['logGroup']))


if __name__ == '__main__':
    with open('example_log_message.txt') as f:
        log_event_compressed = base64.b64encode(gzip.compress(
            bytes(f.read(), 'utf-8')))

    handle_log_event({
        'awslogs': {
            'data': log_event_compressed,
        }
    }, None)
