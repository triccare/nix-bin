"""Setup some basic shell command builtins"""

from itertools import zip_longest
from pathlib import Path
from shutil import get_terminal_size


def lsd(silent=False, width=None):
    """List folders in current working directory

    Parameters
    ----------
    silent: bool
        If true, do not print the list

    width: int or None
        The row length to use. If None, try
        to determine the width of the terminal.

    Returns
    -------
    dirs: [dir[,...]]
        The list of subfoders.
    """
    dirs = [
        file.stem
        for file in Path.cwd().iterdir()
        if file.is_dir()
    ]
    dirs.sort()

    if not silent:
        if width is None:
            width = get_terminal_size().columns
        max_name_len = len(max(dirs, key=len)) + 2
        ncols = width // max_name_len
        row_format = '{{:<{}}}'.format(max_name_len) * ncols
        for group in grouper(dirs, ncols, ''):
            print(row_format.format(*group))
    else:
        return dirs


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
