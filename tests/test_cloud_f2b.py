import pytest
from uuid import uuid5

from cloud_f2b import boto3, process_log_events, process_jails, send_bans
from cloud_f2b.filters import Filter
from cloud_f2b.jails import Jail


class SimpleTestFilter(Filter):
    failregexes = [
        'This Host Matches: %(host)s'
    ]


class SimpleTestJail(Jail):
    filters = [
        'tests.test_cloud_f2b.SimpleTestFilter',
    ]

    fail_limit = 0


@pytest.mark.parametrize("test_data,filters,result", [
    ([
        {
            'id': '12345',
            'timestamp': 1541698535000,
            'message': 'Test',
        }
     ],
     [Filter],
     {}),
    ([
        {
            'id': '12345',
            'timestamp': 1541698535000,
            'message': 'Test',
        },
        {
            'id': '21245',
            'timestamp': 1541698946000,
            'message': 'This Host Matches: 127.0.0.1',
        },
        {
            'id': '23345',
            'timestamp': 1541698946012,
            'message': 'This Host Matches: 127.0.0.2',
        }
     ],
     [SimpleTestFilter, Filter],
     {
         'tests.test_cloud_f2b.SimpleTestFilter': [
             {
                 'Host': '127.0.0.1',
                 'MatchID': uuid5(SimpleTestFilter().uuid, '21245'),
                 'Timestamp': 1541698946
             },
             {
                 'Host': '127.0.0.2',
                 'MatchID': uuid5(SimpleTestFilter().uuid, '23345'),
                 'Timestamp': 1541698946
             }
         ]
     }),
])
def test_process_log_events(test_data, filters, result):
    assert sorted(process_log_events(test_data, filters)) == sorted(result)


@pytest.mark.parametrize("test_data,jails,result", [
    ({},
     [Jail],
     {}),
    ({
        'tests.test_cloud_f2b.SimpleTestFilter': [],
     },
     [Jail],
     {}),
    ({
        'tests.test_cloud_f2b.SimpleTestFilter': [],
        'cloud_f2b.filters.Filter': []
     },
     [Jail, SimpleTestJail],
     {}),
    ({
        'cloud_f2b.filters.Filter': [
            {
                'Host': '127.0.0.1',
                'MatchID': uuid5(Filter().uuid, '21245'),
                'Timestamp': 1541698946
            },
            {
                'Host': '127.0.0.2',
                'MatchID': uuid5(Filter().uuid, '23345'),
                'Timestamp': 1541698946
            }
        ],
        'tests.test_cloud_f2b.SimpleTestFilter': [
            {
                'Host': '127.0.1.1',
                'MatchID': uuid5(SimpleTestFilter().uuid, '21245'),
                'Timestamp': 1541698946
            },
            {
                'Host': '127.0.1.2',
                'MatchID': uuid5(SimpleTestFilter().uuid, '23345'),
                'Timestamp': 1541698946
            }
        ]
     },
     [SimpleTestJail],
     {
         'simpletestjail': ['127.0.1.1', '127.0.1.2']
     }),
])
def test_process_jails(test_data, jails, result):
    assert sorted(process_jails(test_data, jails)) == sorted(result)


@pytest.mark.parametrize("test_data,result", [
    ({}, []),
    ({'jail1': []},
     [
         {'Message': '{"jail1": []}',
          'MessageAttributes': {'jail': {
              'DataType': 'String', 'StringValue': 'jail1'
          }}}
     ]),
    ({'jail1': ['127.0.1.1'], 'jail2': ['127.0.2.2']},
     [
         {'Message': '{"jail1": ["127.0.1.1"]}',
          'MessageAttributes': {'jail': {
              'DataType': 'String', 'StringValue': 'jail1'
          }}},
         {'Message': '{"jail2": ["127.0.2.2"]}',
          'MessageAttributes': {'jail': {
              'DataType': 'String', 'StringValue': 'jail2'
          }}}
     ]),
])
def test_send_bans(monkeypatch, test_data, result):
    class faketopic():
        def publish(self, *args, **kwargs):
            return True

    class fakesns():
        def create_topic(self, *args, **kwargs):
            return faketopic()

    monkeypatch.setattr(boto3, 'resource', lambda x: fakesns())

    assert sorted(send_bans(test_data), key=lambda k: k['Message']) == \
        sorted(result, key=lambda k: k['Message'])
