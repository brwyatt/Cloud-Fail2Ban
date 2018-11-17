from cloud_f2b.jails import Jail


class Sshd_Ddos(Jail):
    filters = [
        'cloud_f2b.filters.auth.sshd_ddos.Sshd_Ddos',
    ]

    jail_name = 'sshd-ddos'
