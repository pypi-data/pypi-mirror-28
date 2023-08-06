#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import numpy as np
import pandas as pd

try:
    from .pkg import rolex
except: # pragma: no cover
    from convert2.pkg import rolex


class Anything2Datetime(object):

    """Parse anything to ``datetime.datetime``.

    The logic:

    - for int, it's the ``datetime.from_utctimestamp(value)``
    - for float, it's the ``datetime.from_utctimestamp(value)``
    - for str, try to parse ``datetime``
    - for datetime type, it's itself
    - for date type, it's the time at 00:00:00
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
                    return rolex.from_utctimestamp(int(value))
                except:
                    raise ValueError("%r is not datetime parsable!" % value)
        except:
            pass

        #--- float, np.float, np.float16, np.float32, np.float64 ---
        if type(value).__name__.startswith("float"):
            try:
                return rolex.from_utctimestamp(float(value))
            except:
                raise ValueError("%r is not datetime parsable!" % value)

        #--- np.datetime64, pd.Timestamp ---
        if isinstance(value, pd.Timestamp):
            try:
                return value.to_pydatetime()
            except:
                raise ValueError("%r is not datetime parsable!" % value)

        if isinstance(value, np.datetime64):
            try:
                return value.astype(datetime)
            except:
                raise ValueError("%r is not datetime parsable!" % value)

        # --- other type ---
        try:
            return rolex.parse_datetime(value)
        except:
            raise ValueError("%r is not datetime parsable!" % value)

any2datetime = Anything2Datetime()
