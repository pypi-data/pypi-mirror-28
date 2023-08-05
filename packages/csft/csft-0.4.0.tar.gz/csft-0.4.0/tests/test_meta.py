from pkg_resources import DistributionNotFound
from pytest import fixture, mark

from csft import _meta as meta


def test_meta():
    assert meta.__author__
    assert meta.__copyright__
    assert meta.__email__
    assert meta.__license__
    assert meta.__url__
    assert meta.__version__


@fixture
def mock_pkg_resources():
    import sys
    bak = sys.modules['pkg_resources']
    sys.modules['pkg_resources'] = __import__('mock')
    yield bak
    sys.modules['pkg_resources'] = bak


@mark.usefixtures(mock_pkg_resources.__name__)
def test_get_version_import_error():
    assert 'x.x.x.dev' == meta._get_version()

    default = 'xxx'
    assert default == meta._get_version(default=default)


@mark.parametrize('err', [DistributionNotFound, ValueError, TypeError])
def test_get_version_with_err(mocker, err):
    dist = mocker.patch('pkg_resources.get_distribution')
    dist.side_effect = err
    assert 'x.x.x.dev' == meta._get_version()
    dist.assert_called_once()
