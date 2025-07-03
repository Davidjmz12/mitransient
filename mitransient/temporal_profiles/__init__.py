# Import/re-import all files in this folder to register AD integrators
import importlib
import mitsuba as mi

if mi.variant() is not None and not mi.variant().startswith('scalar'):
    from . import constant_profile
    importlib.reload(constant_profile)
    from . import exponential_profile
    importlib.reload(exponential_profile)
    from . import positive_epan
    importlib.reload(positive_epan)
del importlib, mi
