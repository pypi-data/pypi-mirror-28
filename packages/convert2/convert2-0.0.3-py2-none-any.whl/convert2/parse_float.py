#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta

try:
    from .pkg import chardet
    from .pkg import rolex
    from .pkg.six import string_types, binary_type
    from .util import extract_number_from_string
except: # pragma: no cover
    from convert2.pkg import chardet
    from convert2.pkg.rolex import rolex
    from convert2.pkg.six import string_types, binary_type
    from convert2.util import extract_number_from_string


class Anything2Float(object):
    """Parse anything to float

    The logic:

    - for int:
    - for float:
    - for str:
    - for datetime: it's utc timestamp
    - for date: it's days from ordinary
    - for timedelta: its total seconds
    """
    EXTRACT_NUMBER_FROM_TEXT = True

    def __call__(self, value):
        # --- None ---
        if value is None:
            return None

        try:
            if np.isnan(value):
                return None
        except:
            pass

        # --- int, long, np.int, np.int8, np.int16, np.int32, np.int64 ---
        # --- float, np.float, np.float16, np.float32, np.float64 ---
        try:
            return float(value)
        except:
            pass

        # --- str, unicode, np.str ---
        if isinstance(value, string_types):
            # if a parsable float str, like "3.14"
            try:
                return float(value)
            except ValueError:
                pass

            # if a extractable parsable str, like "a 3.14 b"
            if self.EXTRACT_NUMBER_FROM_TEXT:
                result = extract_number_from_string(value)
                if len(result) == 1:
                    return float(result[0])
                else:
                    raise ValueError("%r is not float parsable!" % value)

        # --- datetime, np.datetime64, pd.Timestamp ---
        if isinstance(value, pd.Timestamp):
            try:
                return self((value - pd.Timestamp("1970-01-01 00:00:00Z"))
                            .total_seconds())
            except:
                raise ValueError("%r is not float parsable!" % value)

        if isinstance(value, np.datetime64):
            try:
                return self(rolex.to_utctimestamp(value.astype(datetime)))
            except:
                raise ValueError("%r is not float parsable!" % value)

        if isinstance(value, datetime):
            try:
                return self(rolex.to_utctimestamp(value))
            except:
                raise ValueError("%r is not float parsable!" % value)

        # --- date ---
        if isinstance(value, date):
            try:
                return float(rolex.to_ordinal(value))
            except Exception as e:
                raise ValueError("%r is not float parsable!" % value)

        # --- timedelta ---
        if isinstance(value, timedelta):
            try:
                return self(value.total_seconds())
            except Exception as e:
                raise ValueError("%r is not float parsable!" % value)

        # --- other type ---
        try:
            return int(value)
        except:
            raise ValueError("%r is not float parsable!" % value)


any2float = Anything2Float()
