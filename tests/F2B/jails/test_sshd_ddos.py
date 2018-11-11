import pytest

from F2B.jails.sshd_ddos import Sshd_Ddos


def test_sshd_ddos():
    sshd_ddos = Sshd_Ddos()

    assert sshd_ddos.name == 'sshd-ddos'
