import base64
import json
import logging
import gzip

import boto3
from boto3.dynamodb.conditions import Key


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

table = boto3.resource('dynamodb', region_name='us-west-2').Table('F2B')


def handle_log_event(event, context):
        log_event_compressed = event['awslogs']['data']
        log_event = gzip.decompress(base64.b64decode(log_event_compressed))
        log.critical('DECOMPRESSED: {}'.format(log_event))
