# Import/re-import all files in this folder to register AD integrators
import importlib
import mitsuba as mi

if mi.variant() is not None and not mi.variant().startswith('scalar'):
    from . import transient_bsdf
    importlib.reload(transient_bsdf)

    from . import chlorophyll_bsdf
    importlib.reload(chlorophyll_bsdf)
del importlib, mi
