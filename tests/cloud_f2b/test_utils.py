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
