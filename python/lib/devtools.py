# devtools: shortcuts, etc., that are of interest.

# Environment setup
import inspect


# Examination/debugging


def what(obj):
    """
    Return the class tree of the specified thing.

    Basically a wrapper around the call inspect.getclasstree
    """

    # Internal call.
    def _what(obj):
        """
        Internal call to abstract out the wrapper.
        """

        return inspect.getclasstree(inspect.getmro(obj))

    if (inspect.isclass(obj)):
        return _what(obj)
    else:
        return _what(type(obj))


def pack_kwargs():
    '''Pack explicitly defined keyword arguments into a dict.'''
    calling_frame = inspect.getouterframes(inspect.currentframe())[1]
    arg_defs = inspect.getargspec(globals()[calling_frame[3]])
    arg_vals = inspect.getargvalues(calling_frame[0])
    kwargs = {arg: arg_vals[3][arg] for arg in arg_defs[0][-len(arg_defs[3]):]}
    return kwargs


def obj_search(needle, obj,
               respect_privacy=True,
               respect_system=True,
               _ids=None):
    '''Simple search of an object for all occurances of needle
    
    Parameters
    ==========
    needle: type or object
            The thing to search for.
            
    obj: object
         The object to look through.
         
    respect_privacy: bool
                     If True, ignore attributes that start with '_'
    
    respect_system: bool
                    If True, ignore attributes that start with '__'
                    
    Returns
    =======
    list: [obj,...]
          A list of objects found.
    '''
    
    result = []
    
    if not _ids:
        _ids = {}
        
    kwargs = pack_kwargs()
    
    # See if we've looked at this object already.
    obj_id = id(obj)
    if obj_id not in _ids:
        _ids[obj_id] = True
        
        # Is object the type we're looking for
        if isinstance(obj, needle):
            result.append(obj)
        
        # If iterable, go through all the items in the object.
        try:
            for itm in obj:
                result.extend(obj_search(needle, itm, **kwargs))
        except Exception:
            pass
        
        # Now go through all the attributes of the object, see what can be dug up
        for a in dir(obj):
            process = True
            if a.startswith('_'):
                if a.startswith('__'):
                    process = not respect_system
                else:
                    process = not respect_privacy
            if process:
                try:
                    result.extend(obj_search(needle, getattr(obj, a), **kwargs))
                except Exception:
                    pass

    return result
