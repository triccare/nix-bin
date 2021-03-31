class Nascent(dict):

    # Make any item in the dict an attribute of the object
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

