from cloud_f2b.jails import Jail


class Postfix(Jail):
    filters = [
        'cloud_f2b.filters.syslog.postfix.Postfix',
    ]
