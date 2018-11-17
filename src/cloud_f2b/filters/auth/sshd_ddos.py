from cloud_f2b.filters import Filter


class Sshd_Ddos(Filter):
    subs = {
        '_daemon': 'sshd',
    }

    failregexes = [
        '^%(__prefix_line)sDid not receive identification string from %(host)s\s*$',
        '^%(__prefix_line)s(?:fatal: )?Unable to negotiate with %(host)s port .*: no matching key exchange method found\. .*$'
    ]
