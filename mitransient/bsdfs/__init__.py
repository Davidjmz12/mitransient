# Import/re-import all files in this folder to register AD integrators
import importlib
import mitsuba as mi

if mi.variant() is not None and not mi.variant().startswith('scalar'):
    from . import separable_transient
    importlib.reload(separable_transient)

    from . import composed_transient
    importlib.reload(composed_transient)

del importlib, mi
