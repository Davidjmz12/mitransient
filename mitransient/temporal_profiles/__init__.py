# Import/re-import all files in this folder to register AD integrators
import importlib
import mitsuba as mi

if mi.variant() is not None and not mi.variant().startswith('scalar'):
    from . import common
    importlib.reload(common)
    from . import constant_profile
    importlib.reload(constant_profile)
    from . import constant_texture_profile
    importlib.reload(constant_texture_profile)
    from . import exponential_profile
    importlib.reload(exponential_profile)
    from . import gaussian_profile
    importlib.reload(gaussian_profile)
del importlib, mi
