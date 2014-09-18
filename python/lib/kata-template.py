'''
Abstract
========
General title and description

Scenario
========
Describe the environment to be created.

Requirements
============
Describe the actions and outputs required.
'''
import sys
import nose


# Tests
def test():
    assert False

if __name__ == '__main__':
    nose.run(
        argv = [sys.argv[0],
                sys.modules[__name__].__file__,
                '-v']
    )
