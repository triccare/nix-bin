# devtools: shortcuts, etc., that are of interest.

# Environment setup
import inspect


# Examination/debugging


def what(object):
    """
    Return the class tree of the specified thing.

    Basically a wrapper around the call inspect.getclasstree
    """

    # Internal call.
    def _what(object):
        """
        Internal call to abstract out the wrapper.
        """

        return inspect.getclasstree(inspect.getmro(object))

    if (inspect.isclass(object)):
        return _what(object)
    else:
        return _what(type(object))
