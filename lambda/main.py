import base64
import json
import logging
import gzip


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()


def handle_log_event(event, context):
        log_event_compressed = event['awslogs']['data']
        log_event = gzip.decompress(base64.b64decode(log_event_compressed))
        log.critical('DECOMPRESSED: {}'.format(log_event))
