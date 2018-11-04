import pytest

import F2B.utils as utils


@pytest.mark.parametrize("regex_str,subs,result", [
    ('', {}, ''),
    ('%(test)s', {}, '{test}'),  # Test default key
    ('%(test)s', {'test': 'success'}, 'success'),
    ('%(test)s', {'test': '%(test2)s', 'test2': 'Test Success'},
     'Test Success'),
])
def test_compile_regex(regex_str, subs, result):
    assert utils.compile_regex(regex_str, subs) == result
