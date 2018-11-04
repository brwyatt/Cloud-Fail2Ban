import pytest

from F2B.filters import Filter


@pytest.mark.parametrize("test_data,result", [
    ('', False),
    ('This line should never match', False),
])
def test_filter(test_data, result):
    generic_filter = Filter()

    assert generic_filter.failregexes == []
    assert generic_filter.jails == []
    assert generic_filter.ttl == 3600
    assert generic_filter.max_fail_count == 3
    assert generic_filter.test_line(test_data) == result
