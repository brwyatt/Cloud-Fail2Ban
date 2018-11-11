import logging

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr


log = logging.getLogger()
table = boto3.resource('dynamodb', region_name='us-west-2').Table('F2B')


def add_match(host, matchid, filter_name, timestamp, ttl, source=None,
              eventid=None):
    item = {
        'Host': host,
        'MatchID': str(matchid),
        'Filter': filter_name,
        'Timestamp': timestamp,
        'TTL': timestamp+ttl
    }
    if source:
        item['Source'] = str(source)

    if eventid:
        item['EventID'] = str(eventid)

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


def get_match_count(host, filters, since=None):
    if type(filters) is str:
        filters = [filters]
    elif type(filters) is not list or type(filters[0]) is not str:
        raise TypeError('"filters" must be a list of strings or a string')

    filter_expression = Attr('Filter').is_in(filters)

    if since:
        if type(since) is int:
            filter_expression = filter_expression & Attr('Timestamp').gt(since)
        else:
            raise TypeError('"since" should be an int or None')

    response = table.query(
        KeyConditionExpression=Key('Host').eq(host),
        FilterExpression=filter_expression
    )

    return len(response['Items'])
