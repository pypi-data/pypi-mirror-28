#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "1.1.3.3"

from define import SH, SZ, CFFEX, SHFE, DEC, CZCE, INE
from define import MS, S, M, H, D
from define import STOCK, FUTURE, OPTION, INDEX
from CoralDBClient import CoralDBClient
# from CoralParallelClient import CoralParallelClient

from times import rawDate, rawDateText, rawTime, rawTimeText, addRawTime, subRawTime
