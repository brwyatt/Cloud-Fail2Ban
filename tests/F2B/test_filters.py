import pytest
from uuid import UUID

from F2B.filters import Filter


@pytest.mark.parametrize("test_data,result", [
    ('', False),
    ('This line should never match', False),
])
def test_filter(test_data, result):
    generic_filter = Filter()

    assert generic_filter.failregexes == []
    assert generic_filter.ttl == 86400
    assert generic_filter.test_line(test_data) == result


def test_filter_uuid():
    assert Filter().uuid == UUID('c1a820c0-5a1e-4d99-8234-1bdf71aec514')
