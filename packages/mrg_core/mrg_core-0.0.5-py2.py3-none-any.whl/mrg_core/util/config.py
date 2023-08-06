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
""" Utility script to load configuration files into memory. """
# disabling the 'use-of-eval' pylint warning
# pylint: disable=W0123
from __future__ import print_function

import logging
import argparse

from future.utils import iteritems

from mrg_core.util import crypt


PASSWORD_KEYS = {
    'ftp_pwd': '{ftp_usr}@{ftp_host}',
    'smtp_pwd': '{smtp_usr}@{smtp_host}',
}


def load_password_parameters(opts, password_keys=None):
    """ Load the password parameters: ftp_pwd and smtp_pwd, from the password file
    into the opts object.

    :param Namespace opts: the argparse namespace object.
    :param dict password_keys: a mapping of the settings password key to the
        encrypted password's key.
    :raises IOError: error is raised if the file cannot be opened.
    :raises IncorrectPassword: error is raised if the encrypted file
        cannot be decrypted with the specified password.
    :raises KeyError: error is raised if the password file does not contain an
        entry for the keys listed in the specified password_keys.
    """
    logging.debug('Loading password file: %s', opts.passwd_file)
    try:
        passwords = crypt.CryptPropertyFile(opts.passwd_file, opts.passwd_pwd)
    except IOError as exc:
        logging.error(str(exc))
        raise
    except crypt.IncorrectPassword as exc:
        logging.error(str(exc))
        raise

    if password_keys is None:
        password_keys = PASSWORD_KEYS

    for opts_key, enc_key in iteritems(password_keys):
        if opts_key in opts.__dict__:
            opts_key_val = opts.__dict__[opts_key]
            if not opts_key_val:
                enc_key = enc_key.format(**opts.__dict__)
                if enc_key not in passwords:
                    err_msg = 'could not locate password key for: %s' % enc_key
                    logging.error(err_msg)
                    raise KeyError(err_msg)
                else:
                    setattr(opts, opts_key, passwords[enc_key])
                    # opts.__dict__[opts_key] = passwords[enc_key]


def get_file_settings(file_path, settings=None):
    """ Retrieve the key=value pairs from the specified file.
    The expected format of the file must be valid Python code
    since each key value will be evaluated to convert from
    a string to the primitive type.

    The allowed directives are::

        include("settings.py")

    This will recursively include the template settings file.

    :param str file_path: the settings file.
    :param dict settings: the dictionary to append new settings
        to, if None then a new dictionary will be returned.
    :return: the settings dictionary with primitive value types
    :rtype: dict
    """

    if settings is None:
        settings = {}

    in_comment = False
    with open(file_path) as file_obj:
        for line in file_obj:
            line = line.strip()
            # check for module comment
            if line.startswith('"""') or line.endswith('"""'):
                in_comment = not in_comment
            if in_comment:
                continue
            # check for include statements
            if line.startswith('include('):
                include = line.split('include(', 1)[1].strip(')').strip("'").strip('"')
                get_file_settings(include, settings)

            if line and not line.startswith('#') and '=' in line:
                key, val = [part.strip() for part in line.split('=', 1)]
                settings[key] = eval(val)

    return settings


def get_settings(file_path, opts=None, parser=None):
    """ Retrieve the configuration parameters for the application
    using the following precedence scheme,

        1. cmd line arguments
        2. user-defined settings file
        3. template settings file
        4. default command line argument value

    :param str file_path:
    :param Namespace opts:
    :param ArgumentParser parser:
    :return: the opts object specified in the argument list
        or a new :class:`argparse.Namespace` object.
    :rtype: Namespace
    """
    if opts is None:
        opts = argparse.Namespace()

    if not file_path:
        return opts

    cmdline_defaults = {}
    cmdline_arguments = {}
    if opts:
        for key in list(opts.__dict__.keys()):
            if parser:
                default_value = parser.get_default(key)
            else:
                default_value = None
            cmdline_defaults[key] = default_value
            if default_value != getattr(opts, key):
                cmdline_arguments[key] = getattr(opts, key)

    settings = get_file_settings(file_path)

    for key in cmdline_arguments:
        # add any settings that do not already exist
        settings[key] = cmdline_arguments[key]

    for key in cmdline_defaults:
        if key not in settings:
            # add any remaining settings that do not already exist
            settings[key] = cmdline_defaults[key]

    for key in settings:
        setattr(opts, key, settings[key])

    return opts
