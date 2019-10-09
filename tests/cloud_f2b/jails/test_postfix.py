import pytest

from cloud_f2b.jails.postfix import Postfix


def test_postfix():
    postfix = Postfix()

    assert postfix.name == 'postfix'
