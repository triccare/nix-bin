"""Determine frequency of dates under a path"""
import argparse
from collections import Counter
from datetime import date
import logging
from os import walk
from os import path as op
from pathlib import Path


# Configure logging
logger = logging.getLogger('date_spread')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def date_spread(path='.'):
    """Determine frequency of dates under a path

    Parameters
    ----------
    path: str
        The path to start at

    Returns
    -------
    dates: dict(date: count)
        A dict keyed by date of the count of the number of files
        found for that date.
    """
    dates = Counter()
    for root, dirs, files in walk(path):
        for fname in files:
            mtime = date.fromtimestamp(op.getmtime(op.join(root, fname)))
            dates[mtime] += 1
    return dates

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Determine file dates at a path'
    )
    parser.add_argument(
        'path', type=str,
        help='Path to start recursively searching dates of files'
    )
    args = parser.parse_args()
    dates = date_spread(args.path)
    logger.info('Dats are:')
    logger.info(dates)
