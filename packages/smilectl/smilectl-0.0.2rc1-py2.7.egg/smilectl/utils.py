"""Utility module for smilectl."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os


def libsm_abs_path(dir_path, rel):
    """Parse the libsm file full path."""
    lib_path = os.path.join(os.path.dirname(__file__), "lib")
    test_paths = [
        os.path.join(base_path, rel) for base_path in [dir_path, lib_path]
    ]
    return next((test_path for test_path in test_paths
                 if os.path.exists(test_path)), None)
