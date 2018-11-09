import logging

import boto3
from boto3.dynamodb.conditions import Key


log = logging.getLogger()
table = boto3.resource('dynamodb', region_name='us-west-2').Table('F2B')


def add_match(host, matchid, filter_name, timestamp, ttl, source=None):
    item = {
        'Host': host,
        'MatchID': str(matchid),
        'Filter': filter_name,
        'Timestamp': timestamp,
        'TTL': timestamp+ttl
    }
    if source:
        item['Source'] = str(source)

    log.debug('Adding Match to DynamoDB: {0}'.format(item))
    try:
        resp = table.put_item(Item=item)
    except Exception as e:
        log.critical('Exception adding to DynamoDB: {0}: {1}'
                     .format(e.__class__.__name__, str(e)))
        return False
    else:
        if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            log.critical('Failed to add to DynamoDB: {0}'.format(resp))
            return False


def check_ban(ip, jail):
    return False
