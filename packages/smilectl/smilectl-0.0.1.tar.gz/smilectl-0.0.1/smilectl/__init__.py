"""Main script for SMILECTL."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__version__ = "0.0.1"

import subprocess

import simplejson as json
import smile as sm
from smile import flags
import _jsonnet

from .utils import libsm_abs_path

flags.DEFINE_string("config_file", "", "The config filename.", required=True)
flags.DEFINE_string(
    "command",
    "",
    "Command to be used, current only support up.",
    required=True)

FLAGS = flags.FLAGS


def path_import_callback(dir_path, rel):
    """Path import callback function. Used for JSONNET evaluation."""
    full_path = libsm_abs_path(dir_path, rel)
    if full_path:
        with open(full_path, "r") as fobj:
            content = fobj.read()
        return full_path, content
    raise RuntimeError('File not found')


def runlocal(config_file):
    """Bring up the given config file."""
    json_result = _jsonnet.evaluate_file(
        config_file, import_callback=path_import_callback)
    jsonobj = json.loads(json_result)
    subprocess.Popen(jsonobj["cmd"], shell=True)


def main(_):
    """Main entry function."""
    if FLAGS.command == "runlocal":
        runlocal(FLAGS.config_file)


def app_main():
    """The entry function of the script."""
    sm.app.run(main=main)
