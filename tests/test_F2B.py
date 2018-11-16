import pytest
from uuid import uuid5

from F2B import process_log_events, process_jails
from F2B.filters import Filter
from F2B.jails import Jail


class SimpleTestFilter(Filter):
    failregexes = [
        'This Host Matches: %(host)s'
    ]


class SimpleTestJail(Jail):
    filters = [
        'tests.test_F2B.SimpleTestFilter',
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
         'tests.test_F2B.SimpleTestFilter': [
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
        'tests.test_F2B.SimpleTestFilter': [],
     },
     [Jail],
     {}),
    ({
        'tests.test_F2B.SimpleTestFilter': [],
        'F2B.filters.Filter': []
     },
     [Jail, SimpleTestJail],
     {}),
    ({
        'F2B.filters.Filter': [
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
        'tests.test_F2B.SimpleTestFilter': [
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
