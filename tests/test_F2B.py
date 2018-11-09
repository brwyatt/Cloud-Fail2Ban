import pytest
from uuid import uuid5

from F2B import process_log_events
from F2B.filters import Filter


class SimpleTestFilter(Filter):
    failregexes = [
        'This Host Matches: %(host)s'
    ]


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
    assert process_log_events(test_data, filters) == result
