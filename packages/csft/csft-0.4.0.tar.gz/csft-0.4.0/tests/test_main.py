# -*- coding:utf-8 -*-

import sys
from os.path import curdir, devnull
from subprocess import check_call

from pandas import DataFrame
from pytest import fixture, mark, raises

from csft import __main__ as main
from csft._csft import column


@fixture
def null():
    with open(devnull, 'w') as fobj:
        yield fobj


@fixture
def data():
    return DataFrame({
        column.TYPE: ('a', 'b', 'c'),
        column.SIZE: (3, 2, 1),
    })


def test_call(null):
    check_call(['python', '-m', 'csft', 'csft'], stdout=null, stderr=null)


@mark.parametrize('argv', [None, [], [''], ['csft'], ])
def test_main(argv, data, mocker, capsys):
    mocker.patch('sys.argv', ['csft'])
    csft2data = mocker.patch('csft.__main__.csft2data', return_value=data)

    assert 0 == main.main(argv=argv)

    if argv:
        csft2data.assert_called_once_with(main._dir(argv[0]))
    else:
        csft2data.assert_called_once_with(main._dir(curdir))

    out, err = capsys.readouterr()
    assert out
    assert not err


@mark.parametrize('path', ['path/not/exist', 'path/not/valid<?*>', 'LICENSE'])
def test_wrong_path(path, capsys):
    with raises(SystemExit):
        main.main(argv=[path])
    out, err = capsys.readouterr()
    assert not out
    assert err


def test_show_version(capsys):
    try:
        main.main(argv=['-V'])
    except SystemExit as err:
        assert 0 == err.code

    from csft import __version__
    if sys.version < '3.0':
        _, out = capsys.readouterr()
    else:
        out, _ = capsys.readouterr()
    assert __version__ == out.strip()


def test_arg_top(data, mocker, capsys):
    csft2data = mocker.patch('csft.__main__.csft2data', return_value=data)
    head = mocker.patch.object(data, 'head', return_value=data)

    assert 0 == main.main(argv=[curdir, '--top', '5'])

    csft2data.assert_called_once_with(main._dir(curdir))
    head.assert_called_once()
    out, err = capsys.readouterr()
    assert out
    assert not err


@mark.parametrize('top', ['not-a-number', '-1'])
def test_arg_top_err(top, mocker, capsys):
    csft2data = mocker.patch('csft.__main__.csft2data')

    with raises(SystemExit):
        main.main(argv=[curdir, '--top', top])

    csft2data.assert_not_called()
    out, err = capsys.readouterr()
    assert not out
    assert err


def test_arg_with_raw(data, mocker, capsys):
    csft2data = mocker.patch('csft.__main__.csft2data', return_value=data)

    assert 0 == main.main(argv=[curdir, '--with-raw'])

    csft2data.assert_called_once_with(main._dir(curdir))
    out, err = capsys.readouterr()
    assert out
    assert not err
