import base64
import gzip
import json
import pytest

import cloud_f2b.utils as utils


@pytest.mark.parametrize("regex_str,subs,result", [
    ('', {}, ''),
    ('%(test)s', {}, '{test}'),  # Test default key
    ('%(test)s', {'test': 'success'}, 'success'),
    ('%(test)s', {'test': '%(test2)s', 'test2': 'Test Success'},
     'Test Success'),
])
def test_compile_regex(regex_str, subs, result):
    assert utils.compile_regex(regex_str, subs) == result


@pytest.mark.parametrize('test_data', [
    {},
    {'test1': 'value1', 'test2': 'value2'},
    {'logEvents': [
        {'id': '32569', 'timestamp': 1540662758000, 'message': 'testtesttest'},
        {'id': '32597', 'timestamp': 1540662758000, 'message': 'test222222'},
    ]}
])
def test_decompress_cloudwatch_event(test_data):
    assert {'awslogs': {'data': test_data}} == \
        utils.decompress_cloudwatch_event(
            {'awslogs': {'data': str(
                base64.b64encode(gzip.compress(bytes(json.dumps(test_data),
                                                     'utf-8'))), 'utf-8'
            )}})


@pytest.mark.parametrize('test_data,result', [
    ({}, {}),
    (  # Test single INSERT
        {
            'Records': [
                {
                    'eventID': 'g247h8ohgiugsdfh',
                    'eventName': 'INSERT',
                    'eventVersion': '1.1',
                    'eventSource': 'aws:dynamodb',
                    'awsRegion': 'us-test-1',
                    'dynamodb': {
                        'ApproximateCreationDateTime': 1543169340,
                        'Keys': {
                            'MatchID': {
                                'S': '6fb63653-eee5-50d9-97fa-0a75545ab61e'
                            },
                            'Host': {
                                'S': '127.0.0.1'
                            }
                        },
                        'NewImage': {
                            'Filter': {
                                'S': 'cloud_f2b.filters.auth.sshd.Sshd'
                            },
                            'MatchID': {
                                'S': '6fb63653-eee5-50d9-97fa-0a75545ab61e'
                            },
                            'EventID': {
                                'S': '4646816316581646456'
                            },
                            'Host': {
                                'S': '127.0.0.1'
                            },
                            'TTL': {
                                'N': '1543255747'
                            },
                            'Timestamp': {
                                'N': '1543169347'
                            },
                            'Source': {
                                'S': 'some_host'
                            }
                        },
                        'SequenceNumber': '11111111111',
                        'SizeBytes': 11,
                        'StreamViewType': 'NEW_AND_OLD_IMAGES'
                    },
                    'eventSourceARN': 'arn:aws:dynamodb:us-test-1:1111:'
                                      'table/F2B/stream/2011-11-11'
                }
            ]
        },
        {
            'cloud_f2b.filters.auth.sshd.Sshd': [
                {
                    'Host': '127.0.0.1',
                    'MatchID': '6fb63653-eee5-50d9-97fa-0a75545ab61e',
                    'Timestamp': 1543169347
                }
            ]
        }
    ),
    (  # Test that we ignore REMOVE events
        {
            'Records': [
                {
                    'eventID': 'g247h8ohgiugsdfh',
                    'eventName': 'REMOVE',
                    'eventVersion': '1.1',
                    'eventSource': 'aws:dynamodb',
                    'awsRegion': 'us-test-1',
                    'dynamodb': {
                        'ApproximateCreationDateTime': 1543169340,
                        'Keys': {
                            'MatchID': {
                                'S': '6fb63653-eee5-50d9-97fa-0a75545ab61e'
                            },
                            'Host': {
                                'S': '127.0.0.1'
                            }
                        },
                        'NewImage': {
                            'Filter': {
                                'S': 'cloud_f2b.filters.auth.sshd.Sshd'
                            },
                            'MatchID': {
                                'S': '6fb63653-eee5-50d9-97fa-0a75545ab61e'
                            },
                            'EventID': {
                                'S': '4646816316581646456'
                            },
                            'Host': {
                                'S': '127.0.0.1'
                            },
                            'TTL': {
                                'N': '1543255747'
                            },
                            'Timestamp': {
                                'N': '1543169347'
                            },
                            'Source': {
                                'S': 'some_host'
                            }
                        },
                        'SequenceNumber': '11111111111',
                        'SizeBytes': 11,
                        'StreamViewType': 'NEW_AND_OLD_IMAGES'
                    },
                    'eventSourceARN': 'arn:aws:dynamodb:us-test-1:1111:'
                                      'table/F2B/stream/2011-11-11'
                }
            ]
        },
        {}
    )
])
def test_dynamodb_event_to_matches(test_data, result):
    assert utils.dynamodb_event_to_matches(test_data) == result
