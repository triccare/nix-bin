from __future__ import print_function
import logging
import re

from astropy.table import Table

from jwst_tools.associations.association import make_timestamp
from jwst_tools.associations.lib.rules_level3 import _DMS_POOLNAME_REGEX


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter('%(levelname)s:%(name)s: %(message)s')
)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def exam_program_pools(colname, program_path='.', latest=True):
    for pool in get_pools(program_path=program_path, latest=latest):
        logger.info('Pool="{}"'.format(pool))
        pool_exam(pool, colname)


def get_pools(program_path='.', latest=True):
    from glob import glob
    pools = glob(program_path + '/*_pool.csv')
    if latest:
        yield sorted(pools, reverse=True)[0]
    else:
        for pool in pools:
            yield pool


def pool_exam(pool, colname):
    """Show the column from the pool file for specified program"""
    tbl = Table.read(pool, format='ascii')
    try:
        logger.info(tbl[colname])
    except KeyError:
        logger.error('No column "{}" in pool "{}"'.format(colname, pool))


def all_programs(colname, path='.', latest=True):
    """Go through all programs in the specified directory
    Parameters
    ----------
    colname: str
        The column to list

    path: str
        The folder path to look for programs.
        This can be specified using local vernacular.
    """
    from os import listdir
    from os.path import isdir
    for fname in listdir(python_path(path)):
        if isdir(fname):
            logger.info('\n>>>> Program {}:'.format(fname))
            try:
                exam_program_pools(colname, program_path=fname, latest=latest)
            except IndexError:
                """No files, no matter"""
                pass


def python_path(path):
    from os.path import abspath, expanduser, expandvars
    return abspath(expanduser(expandvars(path)))


def pool_combine(program_path='.', seq='999'):
    """Combine pools into one

    This skips the header line of all the pool files, except the first.
    """
    from os.path import dirname
    from subprocess import call

    new_pool = None
    for pool in get_pools(program_path=program_path, latest=False):
        if new_pool is None:
            path = dirname(pool)
            new_pool = open('/'.join([path, make_poolname(pool, seq=seq)]), 'w')
            call(['head', '-n', '1', pool], stdout=new_pool)
        call(['tail', '-n', '+2', pool], stdout=new_pool)
    new_pool.close()


def make_poolname(existing_pool, seq='999'):
    parsed_name = re.search(_DMS_POOLNAME_REGEX, existing_pool)
    if parsed_name is None:
        raise RuntimeError('Existing pool cannot be parsed: "{}"'.format(existing_pool))
    if seq is None:
        seq = parsed_name.group(2)
    new_pool = '_'.join([
        'jw' + parsed_name.group(1),
        seq,
        make_timestamp(),
        'pool.csv'
    ])
    return new_pool
