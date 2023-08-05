# coding=utf-8
"""
Path utilities
"""

import typing
from pathlib import Path


def ensure_path(path: typing.Union[str, Path], must_exist: bool = True) -> Path:
    """
    Ensure path is a Path instance

    Args:
        path: path
        must_exist: if True, raises FileNotFoundError when path does not exist

    Returns: Path instance
    """
    if isinstance(path, str):
        path = Path(path)
    if must_exist and not path.exists():
        raise FileNotFoundError(str(path.absolute()))
    return path.absolute()


def ensure_file(file_path: typing.Union[str, Path], must_exist: bool = True) -> Path:
    """
    Ensure path is a Path instance

    Args:
        file_path: path
        must_exist: if True, raises FileNotFoundError when path does not exist

    Returns: Path instance

    """
    file_path = ensure_path(file_path, must_exist=must_exist)
    if file_path.exists():
        if not file_path.is_file():
            raise TypeError(f'not a file: {str(file_path.absolute())}')
    return file_path


def ensure_dir(dir_path: typing.Union[str, Path], must_exist: bool = True, create=False) -> Path:
    """
    Ensure path is a Path instance

    Args:
        dir_path: path
        must_exist: if True, raises FileNotFoundError when path does not exist

    Returns: Path instance

    """
    dir_path = ensure_path(dir_path, must_exist=must_exist)
    if dir_path.exists():
        if not dir_path.is_dir():
            raise TypeError(f'not a file: {str(dir_path.absolute())}')
    else:
        if create:
            dir_path.mkdir(parents=True)
    return dir_path
