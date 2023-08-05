# coding=utf-8
"""
Tests path package
"""

from pathlib import Path

import pytest

import elib.path


def test_path():
    path_str = './test'
    path_test = Path('./test')
    assert elib.path.ensure_path(path_str, must_exist=False) == elib.path.ensure_path(path_test, must_exist=False)
    with pytest.raises(FileNotFoundError):
        elib.path.ensure_path(path_str)
    with pytest.raises(FileNotFoundError):
        elib.path.ensure_path(path_test)


def test_dir():
    test = Path('./test')
    assert isinstance(elib.path.ensure_dir(test, must_exist=False), Path)
    test.touch()
    with pytest.raises(TypeError):
        elib.path.ensure_dir(test)
    test.unlink()
    test.mkdir()
    assert isinstance(elib.path.ensure_dir(test), Path)


def test_file():
    test = Path('./test')
    assert isinstance(elib.path.ensure_file(test, must_exist=False), Path)
    test.mkdir()
    with pytest.raises(TypeError):
        elib.path.ensure_file(test)
    test.rmdir()
    test.touch()
    assert isinstance(elib.path.ensure_file(test), Path)
