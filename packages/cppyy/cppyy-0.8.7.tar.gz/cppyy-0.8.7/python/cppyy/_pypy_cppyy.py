""" PyPy-specific touch-ups
"""

from . import _stdcpp_fix

import os, sys
from cppyy_backend import loader

__all__ = [
    'gbl',
    'addressof',
    'bind_object',
    'nullptr',
    ]

# first load the dependency libraries of the backend, then
# pull in the built-in low-level cppyy
c = loader.load_cpp_backend()
os.environ['CPPYY_BACKEND_LIBRARY'] = c._name

# for pypy5.9 we may need to move to the location of the backend, if '.' happens
# to be in LD_LIBRARY_PATH, but not the full directory

def py59_compat(c):
    olddir = os.getcwd()
    os.chdir(os.path.dirname(c._name))
    try:
        import _cppyy as _backend
    except ImportError:
        raise EnvironmentError('"%s" missing in LD_LIBRARY_PATH' % os.path.dirname(c._name))
    finally:
        os.chdir(olddir)
    _backend.nullptr = _backend.gbl.nullptr
 

if sys.pypy_version_info[0] == 5 and sys.pypy_version_info[1] == 9:
    py59_compat(c)

import _cppyy as _backend     # built-in module
_backend._cpp_backend = c


#- exports -------------------------------------------------------------------
import sys
_thismodule = sys.modules[__name__]
for name in __all__:
    setattr(_thismodule, name, getattr(_backend, name))
del name, sys
nullptr = _backend.nullptr

def load_reflection_info(name):
    sc = _backend.gbl.gSystem.Load(name)
    if sc == -1:
        raise RuntimeError("Unable to load reflection library "+name)

# add other exports to all
__all__.append('load_reflection_info')
__all__.append('_backend')
