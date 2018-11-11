from F2B.jails import Jail


class Sshd(Jail):
    filters = [
        'F2B.filters.auth.sshd.Sshd',
    ]
