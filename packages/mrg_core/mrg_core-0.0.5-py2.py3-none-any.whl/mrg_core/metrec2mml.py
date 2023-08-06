#   --------------------------------------------------------------------------
#   Copyright 2016 SRE-F, ESA (European Space Agency)
#       Hans Smit <Hans.Smit@esa.int>
#
#   This is restricted software and is only to be used with permission
#   from the author, or from ESA.
#
#   THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#   --------------------------------------------------------------------------
"""

The command line usages is::

    usage: matrec2mml.py [-h] [-f FILE] [-r REPORTER]

Examples::

    todo
"""
from __future__ import print_function

import os
import logging
import shlex
import argparse

from mrg_core.mml.mml import MML
from mrg_core.mml.validator import Validator


def main(cmdline=None):
    """ The main entry point for this script.

    :param str cmdline: if set, then this command line string will override
        the console command line input. Useful for debugging.
    """
    args = shlex.split(cmdline) if cmdline else None

    parser = argparse.ArgumentParser(description='METREC to MML converter',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('command', nargs='?',
                        choices=['json', 'xml', 'python', 'test', 'validate'])
    parser.add_argument('-i', '--ignore-errors', dest='ignoreErrors', action='store_true',
                        help='Ignore errors and keep processing.')
    parser.add_argument('-f', '--file', dest='file',
                        help='the metrec log file.')
    parser.add_argument('-d', '--directory', dest='directory',
                        help='the wildcard enabled directory.')
    parser.add_argument('-r', '--reporter', dest='reporter', default='ANON',
                        help='the reporter to associate with this conversion')
    parser.add_argument('-o', '--output', dest='output', default=None,
                        help='the output file (or directory) to save the json or xml output to. '
                             'If not specified, the output is sent to the stdout. '
                             'If no extension is found than a default file name is generated. '
                             'The directories will be auto-created.')
    parser.add_argument('-C', '--continue-from', dest='continueFromPath',
                        help='the path to continue processing from.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Log with verbosity.')
    opts = parser.parse_args(args)

    logging.basicConfig(level=100)
    # logging.basicConfig(level=[logging.INFO, logging.DEBUG][opts.verbose])

    # check that there is an input
    if opts.file or opts.directory:
        if opts.directory:
            night = os.path.basename(opts.directory)
            metrec_log = os.path.join(opts.directory, night + '.log')
            if os.path.exists(metrec_log):
                opts.file = metrec_log
                execute_command(opts)
            else:
                validator = Validator(opts.reporter, opts.continueFromPath, opts.ignoreErrors)
                validator.validate_directory(opts.directory)
        else:
            execute_command(opts)
    else:
        parser.print_help()


def execute_command(opts):
    """ Execute a command specified in the options. """

    if opts.command == 'validate':
        validator = Validator(opts.reporter, opts.continueFromPath,
                              opts.ignoreErrors, save_files=True, display_progress=False)
        validator.validate_session(opts.file)
        print('OK. Validated %s' % opts.file)
        return

    converter = MML(opts.file, opts.reporter)
    default_base_file_name = os.path.splitext(os.path.basename(opts.file))[0]
    if opts.command == 'json':
        output = converter.get_json_string()
        default_base_file_name += '.json'
    elif opts.command == 'xml':
        output = converter.get_xml_string()
        default_base_file_name += '.xml'
    elif opts.command == 'python':
        output = 'from collections import OrderedDict\n'
        output += repr(converter.get_json(True))
        default_base_file_name += '.py'
    else:
        converter.get_json(True)
        output = ''

    if opts.output:
        if not os.path.splitext(opts.output)[1]:
            try:
                os.makedirs(opts.output)
            except OSError:
                pass
            opts.output = os.path.join(opts.output, default_base_file_name)
        with open(opts.output, 'w') as file_obj:
            file_obj.write(output)
    else:
        print(output)

if __name__ == '__main__':
    main()
