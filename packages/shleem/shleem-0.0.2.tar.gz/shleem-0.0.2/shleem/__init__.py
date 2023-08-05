"""Automate and version datasets generation from data sources."""
# pylint: disable=C0413,C0411

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

# === module imports

from .core import ( # noqa
    DataSource,
    DataTap,
)

import shleem.mongodb  # noqa: E402, F401

for name in ['shleem', 'core', 'shared']:
    try:
        globals().pop(name)
    except KeyError:
        pass
try:
    del name  # pylint: disable=W0631
except NameError:
    pass
