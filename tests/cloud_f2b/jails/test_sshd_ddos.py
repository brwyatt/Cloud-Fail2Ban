import pytest

from cloud_f2b.jails.sshd_ddos import Sshd_Ddos


def test_sshd_ddos():
    sshd_ddos = Sshd_Ddos()

    assert sshd_ddos.name == 'sshd-ddos'
