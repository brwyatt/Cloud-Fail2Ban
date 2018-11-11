import pytest

from F2B.jails.sshd import Sshd


def test_sshd():
    sshd = Sshd()

    assert sshd.name == 'sshd'
