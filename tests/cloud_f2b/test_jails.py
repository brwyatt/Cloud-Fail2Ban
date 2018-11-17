import pytest

import cloud_f2b.jails
from cloud_f2b.jails import Jail


def test_jail():
    jail = Jail()
    assert jail.filters == []
    assert jail.fail_limit == 3
    assert jail.fail_window == 3600
    assert jail.name == 'jail'

    class SimpleJail(Jail):
        filters = ['test']
        fail_limit = 1
        fail_window = False
        jail_name = 'TESTING'

    jail = SimpleJail()
    assert jail.filters == ['test']
    assert jail.fail_limit == 1
    assert jail.fail_window == False
    assert jail.name == 'testing'


@pytest.mark.parametrize(
    'filters,fail_limit,fail_window,matches,match_counts,result', [
        # One filter with one host match, with 3 strikes
        (['filter1'], 3, 3600, {
            'filter1': [{'Host': '0.0.0.0'}]
        }, {'0.0.0.0': 3}, ['0.0.0.0']),
        # One filter with one host match in different filter
        (['filter2'], 3, 3600, {
            'filter1': [{'Host': '0.0.0.0'}]
        }, {}, []),
        # One filter with one host match, with 2 strikes
        (['filter1'], 3, 3600, {
            'filter1': [{'Host': '0.0.0.0'}]
        }, {'0.0.0.0': 2}, []),
        # Two filters with the same one host match, with 3 strikes
        (['filter1', 'filter2'], 3, False, {
            'filter1': [{'Host': '0.0.0.0'}],
            'filter2': [{'Host': '0.0.0.0'}],
        }, {'0.0.0.0': 3}, ['0.0.0.0']),
        # Two filters with one different host match each, with 3 strikes
        (['filter1', 'filter2'], 3, False, {
            'filter1': [{'Host': '0.0.0.0'}],
            'filter2': [{'Host': '0.0.0.1'}],
        }, {'0.0.0.0': 3, '0.0.0.1': 3}, ['0.0.0.0', '0.0.0.1']),
        # Two filters with one different host match each, with 0 and 3 strikes
        (['filter1', 'filter2'], 3, False, {
            'filter1': [{'Host': '0.0.0.0'}],
            'filter2': [{'Host': '0.0.0.1'}],
        }, {'0.0.0.0': 0, '0.0.0.1': 3}, ['0.0.0.1']),
    ])
def test_jail_check_bans(monkeypatch, filters, fail_limit, fail_window, matches,
                         match_counts, result):
    jail = Jail()
    jail.filters = filters
    jail.fail_limit = fail_limit
    jail.fail_window = fail_window

    def mock(*args, **kwargs):
        if match_counts:
            return match_counts.get(args[0], 0)
        else:
            return 0

    monkeypatch.setattr(cloud_f2b.jails, 'get_match_count', mock)

    assert sorted(jail.check_bans(matches)) == sorted(result)
