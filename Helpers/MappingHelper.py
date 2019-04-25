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
