import pytest

from cloud_f2b.jails.sshd import Sshd


def test_sshd():
    sshd = Sshd()

    assert sshd.name == 'sshd'
