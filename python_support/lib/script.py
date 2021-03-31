"""Common command-line script setup"""
import sys

from  abc import ABC, abstractmethod
import argparse
import logging
import pdb

# Configure logging
script_logger = logging.getLogger(__name__)
script_logger.addHandler(logging.NullHandler())


class Script(ABC):
    """Provide generic usage of argparse.

    Parameters
    ----------
    argv : str or [str,[...]] or None
        The command line arguments.
        If None, `sys.argv` is used.

    logger : logging.getLogger or None
        Logger to use when setting verbosity.

    Attributes
    ----------
    args : Namespace
        The parsed arguments

    exit_status : obj
        Return from `main`

    parser : argparse.ArgumentParser
        The argument parser
    """

    LEVELS = [logging.WARNING, logging.INFO, logging.DEBUG]

    def __init__(self, argv=None, logger=None):
        if isinstance(argv, str):
            argv = argv.split()
        elif argv is None:
            argv = sys.argv
        self._argv = argv
        self.exit_status = None
        self.logger = logger if logger else script_logger

        # Parse the command-line arguments
        self.parser = argparse.ArgumentParser(prog=self._argv[0])
        self.add_args()
        self._predefined_args()
        self.args = self.parser.parse_args(self._argv[1:])

        # Finish configuration.
        self._log_config()

    @abstractmethod
    def add_args(self):
        """Add required command line arguments and options"""

    def add_argument(self, *parser_args, **parser_kwargs):
        """Add an argument definition to the parser"""
        return self.parser.add_argument(*parser_args, **parser_kwargs)

    @abstractmethod
    def main(self):
        """Method when the Script instance is called. All parameters are provided by Script.args"""

    def _log_config(self):
        """Configure logging based on the arguments"""
        nlevels = len(self.LEVELS)
        level = self.LEVELS[min(nlevels - 1, self.args.verbose)]
        self.logger.setLevel(level)

    def _main(self):
        """Execute the main method"""
        try:
            if self.args.pdb:
                self.exit_status = pdb.runeval("self.main()", globals(), locals())
            else:
                self.exit_status = self.main()
        except KeyboardInterrupt as exception:
            if self.args.pdb:
                raise
            else:
                raise KeyboardInterrupt('Interrupted. Shutting down...') from exception
        except Exception as exception:
            if self.args.post_mortem:
                pdb.post_mortem()
            else:
                raise

        return self.exit_status
    __call__ = _main

    def _predefined_args(self):
        """Standard options"""
        self.add_argument('--pdb',
                          action="store_true",
                          help="Run under pdb.")
        self.add_argument('--post-mortem',
                          action='store_true',
                          help='Drop into pdb if an exception occurs.')
        self.add_argument('-v', '--verbose',
                          action='count', default=0,
                          help='Increase verbosity. Repeat option for more verbosity.')
