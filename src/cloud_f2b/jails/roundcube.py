from cloud_f2b.jails import Jail


class Roundcube(Jail):
    filters = [
        'cloud_f2b.filters.syslog.roundcube.Roundcube',
    ]
