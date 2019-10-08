from cloud_f2b.jails import Jail


class Dovecot(Jail):
    filters = [
        'cloud_f2b.filters.syslog.dovecot.Dovecot',
    ]
