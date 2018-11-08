import pytest

from F2B.filters import Filter


@pytest.mark.parametrize("test_data,result", [
    ('', False),
    ('This line should never match', False),
])
def test_filter(test_data, result):
    generic_filter = Filter()

    assert generic_filter.failregexes == []
    assert generic_filter.test_line(test_data) == result
