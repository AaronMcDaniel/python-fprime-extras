try:
    from .version import __branch__  # noqa: F401
    from .version import __version__
except Exception:
    __version__ = 'v0.0.0'

__author__ = 'Sterling Peet'
__author_email__ = 'sterling.peet@ae.gatech.edu'
__date__ = '10-14-2020'
