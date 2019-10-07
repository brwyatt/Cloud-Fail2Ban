import pytest

from cloud_f2b.jails.roundcube import Roundcube


def test_roundcube():
    roundcube = Roundcube()

    assert roundcube.name == 'roundcube'
