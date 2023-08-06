#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
try:
    from .pkg import rolex
    from .parse_datetime import any2datetime
except: # pragma: no cover
    from convert2.pkg.rolex import rolex
    from convert2.parse_datetime import any2datetime


class Anything2Date(object):

    """Parse anything to ``datetime.date``.

    The logic:

    - for int, it's the ``datetime.fromordinal(value)``
    - for float, it's a invalid input
    - for str, try to parse ``date``
    - for datetime type, it's the date part
    - for date type, it's itself
    """

    def __call__(self, value):
        #--- None ---
        if value is None:
            return None

        try:
            if np.isnan(value):
                return None
        except:
            pass

        #--- int, long, np.int, np.int8, np.int16, np.int32, np.int64 ---
        try:
            if int(value) == value:
                try:
                    return rolex.from_ordinal(value)
                except:
                    raise ValueError("%r is not date parsable!" % value)
        except:
            pass

        #--- float, np.float, np.float16, np.float32, np.float64 ---
        if type(value).__name__.startswith("float"):
            raise ValueError("%r is not date parsable!" % value)

        #--- np.datetime64, pd.Timestamp ---
        # --- other type ---
        try:
            return any2datetime(value).date()
        except:
            raise ValueError("%r is not date parsable!" % value)

any2date = Anything2Date()
