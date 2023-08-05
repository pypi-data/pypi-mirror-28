"""MongoDB shleem data sources."""

import sys

from .mongodb import (
    server,
    _add_servers_attr,
)

_add_servers_attr(sys.modules[__name__])

for name in [
        'sys', 'mongodb', '_add_servers_attr',
]:
    try:
        globals().pop(name)
    except KeyError:
        pass
try:
    del name  # pylint: disable=W0631
except NameError:
    pass
