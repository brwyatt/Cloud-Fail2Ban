from F2B.jails import Jail


class Sshd_Ddos(Jail):
    filters = [
        'F2B.filters.auth.sshd_ddos.Sshd_Ddos',
    ]

    jail_name = 'sshd-ddos'
