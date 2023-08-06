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


class RoundMethod:
    round = "round"
    floor = "floor"
    ceiling = "ceiling"


class Anything2Int(object):
    """Parse anything to ``int``.

    The logic:

    - for int: force to be generic int type.
    - for float: round.
    - for str: extract int from string, for exmplae: "you have 5 dollar" -> 5
        if there is more than 1 integer, "You got 3, he got 4", raise ValueError
    - for datetime: it's utc timestamp. Ignore milliseconds.
    - for date: it's days from ordinary.
    - for timedelta: its total seconds, Ignore milliseconds.
    """
    ROUND_FLOAT_METHOD = RoundMethod.round # could be one of 'floor', 'ceiling', 'round'
    EXTRACT_NUMBER_FROM_TEXT = True

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
                return int(value)
        except:
            pass

        #--- float, np.float, np.float16, np.float32, np.float64 ---
        if type(value).__name__.startswith("float"):
            return int(round(value))

        #--- str, unicode, np.str ---
        if isinstance(value, string_types):
            # if a parsable int str, like "123"
            try:
                return int(value)
            except ValueError:
                pass

            # if a parsable float str, like "3.14"
            try:
                float_ = float(value)
                return self(float_)
            except ValueError:
                pass

            # if a extractable parsable str, like "a 3.14 b"
            if self.EXTRACT_NUMBER_FROM_TEXT:
                result = extract_number_from_string(value)
                if len(result) == 1:
                    return self(float(result[0]))
                else:
                    raise ValueError("%r is not int parsable!" % value)

        #--- datetime, np.datetime64, pd.Timestamp ---
        if isinstance(value, pd.Timestamp):
            try:
                return self((value - pd.Timestamp("1970-01-01 00:00:00Z"))
                            .total_seconds())
            except:
                raise ValueError("%r is not int parsable!" % value)

        if isinstance(value, np.datetime64):
            try:
                return self(rolex.to_utctimestamp(value.astype(datetime)))
            except:
                raise ValueError("%r is not int parsable!" % value)

        if isinstance(value, datetime):
            try:
                return self(rolex.to_utctimestamp(value))
            except:
                raise ValueError("%r is not int parsable!" % value)

        #--- date ---
        if isinstance(value, date):
            try:
                return rolex.to_ordinal(value)
            except Exception as e:
                raise ValueError("%r is not int parsable!" % value)

        #--- timedelta ---
        if isinstance(value, timedelta):
            try:
                return self(value.total_seconds())
            except Exception as e:
                raise ValueError("%r is not int parsable!" % value)

        #--- other type ---
        try:
            return int(value)
        except:
            raise ValueError("%r is not int parsable!" % value)


any2int = Anything2Int()
