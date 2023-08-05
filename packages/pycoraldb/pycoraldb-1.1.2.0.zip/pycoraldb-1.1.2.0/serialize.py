#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import base64

try:
    import dill as pickle
except ImportError:
    import pickle


def loads(b64):
    return pickle.loads(base64.b64decode(b64))


def dumps(obj):
    return base64.b64encode(pickle.dumps(obj, recurse=True, ))

def load_json(s):
    # import simplejson
    pass

def dump_json(s):
    pass
