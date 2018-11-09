import json
import logging
import os

from F2B import process_log_events
from F2B.filters.auth.sshd import Sshd
from F2B.filters.auth.sshd_ddos import Sshd_Ddos
from F2B.utils import decompress_cloudwatch_event


logging.basicConfig()  # needed to run outside Lambda
log = logging.getLogger()

default_loglevel = 'INFO'
loglevel = os.environ.get('LOGLEVEL', default_loglevel)

try:
    log.setLevel(getattr(logging, loglevel))
    log.info('LogLevel set to "{0}"'.format(loglevel))
except:
    log.setLevel(getattr(logging, default_loglevel))
    log.warning('LogLevel could not be set to "{0}", using default "{1}" '
                'instead!'.format(loglevel, default_loglevel))

logParsers = {
    'Auth': [Sshd, Sshd_Ddos]
}


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
