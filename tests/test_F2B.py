import pytest

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
            'timestamp': 1541698535,
            'message': 'Test',
        }
     ],
     [Filter],
     {}),
    ([
        {
            'id': '12345',
            'timestamp': 1541698535,
            'message': 'Test',
        },
        {
            'id': '21245',
            'timestamp': 1541698946,
            'message': 'This Host Matches: 127.0.0.1',
        }
     ],
     [SimpleTestFilter, Filter],
     {
         'tests.test_F2B.SimpleTestFilter': [
             {
                 'Host': '127.0.0.1',
                 'EventID': '21245',
                 'timestamp': 1541698946
             }
         ]
     }),
])
def test_process_log_events(test_data, filters, result):
    assert process_log_events(test_data, filters) == result
