import base64
import json
import logging
import gzip

from F2B.filters.auth.sshd import Sshd
from F2B.filters.auth.sshd_ddos import Sshd_Ddos


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

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
