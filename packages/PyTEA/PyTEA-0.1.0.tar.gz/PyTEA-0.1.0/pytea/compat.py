# -*- coding: utf-8 -*-

"""
pytea.compat
~~~~~~~~~~~~~~~
This module handles import compatibility issues between Python 2 and
Python 3.
"""

import sys
import binascii

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 3.x?
is_py3 = (_ver[0] == 3)

#: Python 2.x?
is_py2 = (_ver[0] == 2)

if is_py3:
    bytes = bytes
elif is_py2:
    bytes = str


def bytes_to_int(b):
    if is_py3:
        return int.from_bytes(b, 'big')
    else:
        return int(binascii.hexlify(b), 16)
