from cloud_f2b.jails import Jail


class Sshd(Jail):
    filters = [
        'cloud_f2b.filters.auth.sshd.Sshd',
        'cloud_f2b.filters.auth.sshd_ddos.Sshd_Ddos',
    ]
