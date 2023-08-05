import csft


def test_meta():
    assert csft.__author__
    assert csft.__copyright__
    assert csft.__email__
    assert csft.__license__
    assert csft.__url__
    assert csft.__version__


def test_csft2data():
    from inspect import isfunction
    assert isfunction(csft.csft2data)
