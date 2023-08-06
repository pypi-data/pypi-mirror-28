#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.3"
__short_description__ = "Convert anything to any type."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .parse_int import any2int
    from .parse_float import any2float
    from .parse_str import any2str
    from .parse_datetime import any2datetime
    from .parse_date import any2date
except ImportError: # pragma: no cover
    pass
