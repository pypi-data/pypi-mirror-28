#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

try:
    from .pkg import chardet
    from .pkg.six import binary_type
except: # pragma: no cover
    from convert2.pkg import chardet
    from convert2.pkg.six import binary_type


class Anything2Str(object):
    """Parse anything to ``str``

    The logic:

    - bytes: auto detect encoding and then decode
    - other: stringlize it
    """

    def __call__(self, value):
        # --- None ---
        if value is None:
            return None

        try:
            if np.isnan(value):
                return None
        except:
            pass

        # --- bytes ---
        if isinstance(value, binary_type):
            result = chardet.detect(value)
            return value.decode(result["encoding"])

        # --- other type ---
        try:
            return str(value)
        except:
            raise ValueError("%r is not str parsable!" % value)


any2str = Anything2Str()
