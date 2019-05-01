from __future__ import print_function

import json


def to_dynamic(json_string):
    try:
        from types import SimpleNamespace as Namespace
    except ImportError:
        # Python 2.x fallback
        from argparse import Namespace

    x = json.loads(json_string, object_hook=lambda d: Namespace(**d))
    return x


def update_exist_props(full_object, not_full_object):
    for attOfFull in dir(full_object):
        for attOfNotGull in dir(not_full_object):
            if str(attOfNotGull) == str(attOfFull) and "__" not in str(attOfNotGull):
                setattr(full_object, attOfFull, getattr(not_full_object, attOfNotGull))

    return full_object
