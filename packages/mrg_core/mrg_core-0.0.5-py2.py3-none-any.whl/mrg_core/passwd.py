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
WARNING: This script requires the password to be passed as plain text to the
decryption algorithm. If a hacker acquires this password, they can in theory
also acquire the plain-text of the encrypted file. The command-line options
will not display the key values, but only list the keys. However, if the hacker
has knowledge of Python, they could modify this script to print the key values
to the terminal. The encrpytion procedure used in this script is really meant
to hide information from a casual observers.

The command line usages is::

    usage: passwd.py [-h] [-f FILE] [-p PWD] [-K KEY] [-V VAL] [-I]
                     [{modify,delete,list}]

    Password encrypted storage manager

    positional arguments:
      {modify,delete,list}

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  file to output encrypted content to. (default: None)
      -p PWD, --password PWD
                            the password used for encryption/decrpytion (default:
                            None)
      -K KEY, --key KEY     the key to modify (default: None)
      -V VAL, --value VAL   the value to modify (default: None)
      -I, --interactive     the key to modify (default: False)

Examples::

    passwd.py modify -f c:/passwd.enc -p mypasswd -K smtp.xs4all.nl -V myuid:mypwd
    passwd.py delete -f c:/passwd.enc -p mypasswd -K smtp.xs4all.nl
    passwd.py list -f c:/passwd.enc -p mypasswd
"""
from __future__ import print_function

import getpass
import shlex
import argparse
import sys
import os

from mrg_core.util import crypt


def main(cmdline=None):
    """ The main entry point for this script.

    :param str cmdline: if set, then this command line string will override
        the console command line input. Useful for debugging.
    """

    args = shlex.split(cmdline) if cmdline else None

    parser = argparse.ArgumentParser(description='Password encrypted storage manager',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('command', nargs='?',
                        choices=['modify', 'delete', 'list'])

    parser.add_argument('-f', '--file', dest='file',
                        help='file to output encrypted content to.')
    parser.add_argument('-p', '--password', dest='pwd',
                        help='the password used for encryption/decrpytion')
    parser.add_argument('-K', '--key', dest='key',
                        help='the key to modify')
    parser.add_argument('-V', '--value', dest='val',
                        help='the value to modify')
    parser.add_argument('-I', '--interactive', dest='interactive', action='store_true',
                        help='the key to modify')

    opts = parser.parse_args(args)

    if opts.file:
        # the minimum requirement passes
        run(opts)
    else:
        # else print the usage and help text to console
        parser.print_help()


def execute_command(opts):
    """ Execute a command specified in the options. """
    key = opts.key
    val = opts.val
    cmd = opts.command
    # reset the options command in-case of interactive mode.
    opts.command = ''
    try:
        props = crypt.CryptPropertyFile(opts.file, opts.pwd)
        if not cmd:
            sys.stdout.write('Please enter a command: \n')
            sys.stdout.write('(m)modify, (d)delete, (l)list, (x)exit: ')
            cmd = sys.stdin.readline().strip()

        if cmd.startswith('m'):
            if not key:
                sys.stdout.write('Please enter a key  : ')
                key = sys.stdin.readline().strip()
            if not val:
                sys.stdout.write('Please enter a value: ')
                val = sys.stdin.readline().strip()
            if key:
                props[key] = val
                props.flush()

        elif cmd.startswith('d'):
            if not key:
                sys.stdout.write('Please enter a key: ')
                key = sys.stdin.readline().strip()
            del props[key]
            props.flush()

        elif cmd.startswith('l'):
            print('Keys defined in the file: ')
            for key in props:
                print('  * %s' % key)

        elif cmd.startswith('x'):
            print('Exiting...')
            opts.interactive = 0

        else:
            print('ERROR: invalid command')

    except crypt.IncorrectPassword as exc:
        print('ERROR: ' + str(exc))


def run(opts):
    """ Run the console interface application """
    if not opts.pwd:
        opts.pwd = getpass.getpass('Please enter your password:')

    if not os.path.exists(opts.file):
        with crypt.CryptPropertyFile(opts.file, opts.pwd, True):
            pass
        print('Created password file')

    if not os.path.getsize(opts.file):
        with crypt.CryptPropertyFile(opts.file, opts.pwd, True):
            pass
        print('Created password file')

    while True:
        execute_command(opts)
        if not opts.interactive:
            break

if __name__ == '__main__':
    # cmdline = '-f test2.pwd -p \'pass-word\' -c modify -k key1 -v \'some val\""
    # cmdline = '-f test2.pwd'
    # cmdline = None
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting (Ctrl+c)...')
