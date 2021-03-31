#!/user/bin/env python

"""Update pip-only installed packages in a conda environment"""
import logging
from subprocess import run
import yaml


# configure logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def conda_pip_update():
    """Update pip-only installed packages in a conda environment"""

    # Get the package list
    result = run(['conda', 'env', 'export'], capture_output=True)
    if result.returncode:
        raise RuntimeError(
            'Update failed: {}'.format(result.stderr)
        )
    logger.debug('result.stdout = %s', result.stdout)

    # Convert from YAML to python structure
    dependencies = yaml.load(result.stdout)['dependencies']
    logger.debug('dependencies = %s', dependencies)

    # Find the pip-only dependencies
    for item in dependencies:
        if isinstance(item, dict) and 'pip' in item:
            pip_deps = item['pip']
            break
    else:
        logger.info('No pip dependencies found.')
        return True
    logger.debug('pip_deps = %s', pip_deps)

    # Separate out the package names and versions
    packages = {
        name: version
        for name, version in [
            item.split('==')
            for item in pip_deps
        ]
    }
    logger.debug('packages = %s', packages)

    # Now do the updating.
    for name in packages:
        logger.info('\nUpdate %s...', name)
        run(['pip', 'install', '-U', name])


# Main
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Update pip installed packages in a conda environment'
    )
    parser.add_argument(
        '-d', '--debug',
        help='Produce debugging output',
        action='store_const', dest='log_level', const=logging.DEBUG,
        default=logging.INFO
    )
    args = parser.parse_args()

    logger.setLevel(args.log_level)
    logger.addHandler(logging.StreamHandler())

    conda_pip_update()
