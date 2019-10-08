import pytest

from cloud_f2b.jails.dovecot import Dovecot


def test_dovecot():
    dovecot = Dovecot()

    assert dovecot.name == 'dovecot'
