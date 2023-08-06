"""Main script for SMILECTL."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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
flags.DEFINE_bool(
    "dry_run", False,
    "If this command is specified, instead of running the command, print out "
    "the entire job object.")

FLAGS = flags.FLAGS


def path_import_callback(dir_path, rel):
    """Path import callback function. Used for JSONNET evaluation."""
    full_path = libsm_abs_path(dir_path, rel)
    if full_path:
        with open(full_path, "r") as fobj:
            content = fobj.read()
        return full_path, content
    raise RuntimeError('File not found')


def parse_config_file(config_file):
    """Parse the smile configuration file into Python dictionory object."""
    json_result = _jsonnet.evaluate_file(
        config_file, import_callback=path_import_callback)
    jsonobj = json.loads(json_result)
    return jsonobj


def runlocal(jsonobj):
    """Bring up the given config file."""
    subprocess.Popen(jsonobj["cmd"], shell=True).wait()


def main(_):
    """Main entry function."""
    # Parse the smile configuration file.
    jsonobj = parse_config_file(FLAGS.config_file)
    if FLAGS.dry_run:
        # Pretty print the json object.
        print(json.dumps(
            jsonobj, sort_keys=True, indent=2, separators=(',', ': ')))
        return
    if FLAGS.command == "runlocal":
        runlocal(jsonobj)


def app_main():
    """The entry function of the script."""
    sm.app.run(main=main)
