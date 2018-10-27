import re

import F2B.filters.common as common
import F2B.utils as utils

subs = common.subs

failregex = [
    '^%(__prefix_line)sDid not receive identification string from %(host)s\s*$',
    '^%(__prefix_line)s(fatal: )?Unable to negotiate with %(host)s port .*: no matching key exchange method found\. .*$'
]


def test_logline(line):
    for r in failregex:
        r = utils.format_all(r, subs)
        match = re.match(r, line)
        if match:
            return match

    return False
