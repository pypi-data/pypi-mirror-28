#   --------------------------------------------------------------------------
#   Copyright 2016 SRE-F, ESA (European Space Agency)
#       Hans Smit <Hans.Smit@esa.int>
#
#   This is restricted software and is only to be used with permission
#   from the author, or from ESA.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#   --------------------------------------------------------------------------
""" New MRG data archive transferring tool. Functions available are,

    1. email notification using a template file
    2. compress night session data directories (``*``.zip)
    3. upload night session archive file (``*``.zip) to FTP server
    4. download archive (``*``.zip) night sessions from FTP server
    5. decompress night session (``*``.zip) files onto local filesystem
    6. email alert using only subject heading

The above functions can be chained and are executed in the order above.
This means you can compress and upload the night directory in one go and
optionally send an email alert when completed. Or you may download and
upack the archive in one-go.

Using wildcard(s) in the `--night` parameter enables **batch** execution
of commands.

The command line usages is::

    usage: archive.py [-h] [-r RETRIES] [-i] [-v] [-d] [-u] [-n] [-a] [-U] [-P]
                      [-y] [-o LOG] [-c CONFIG] [-C CAMERA] [-N NIGHT]

    MRG batch transfer program

    optional arguments:
      -h, --help            show this help message and exit
      -r RETRIES, --retries RETRIES
                            the number of SFTP retries after download failure.
                            (default: 0)
      -i, --ignore-errors   Ignore errors and keep processing. (default: False)
      -v, --verbose         Log with verbosity. (default: False)
      -d, --download        Download. (default: False)
      -u, --upload          Upload. (default: False)
      -n, --notify          Email notification when observation completed.
                            (default: False)
      -a, --alert           Send email alert when FTP upload complete. (default:
                            False)
      -U, --unpack          Unpack downloaded zip files. (default: False)
      -P, --pack            Pack directory into a compressed file. (default:
                            False)
      -y, --overwrite       automatically overwrite existing files. (default:
                            False)
      -o LOG, --log-output LOG
                            Log output to file. (default: None)
      -c CONFIG, --config-file CONFIG
                            the configuration file (default: settings.py)
      -C CAMERA, --camera CAMERA
                            the camera directory name to process (default: None)
      -N NIGHT, --night NIGHT
                            the night directory name to process. (default: None)

Examples
--------

Download and unpack archive::

    python archive.py -c settings.py -C ICC9 -N 201607?? -dUyv -r 3

"""
from __future__ import print_function

import argparse
import logging

from mrg_core.transfer import transfer
from mrg_core.util import config

LOGGER = logging


def run_commands(opts):
    """ Execute the command line switches that process.

    :param Namespace opts:
    """
    if opts.notify:
        LOGGER.info('Running email notification')
        assert opts.night, '-N/--night argument empty'
        assert opts.camera, '-C/--camera argument empty'
        assert opts.email_translation, 'missing "email_translation" setting'
        assert '?' not in opts.night and '*' not in opts.night, \
            'notify action -N/--night argument may not contain wild cards characters'
        opts.email_translation = opts.email_translation.format(**opts.__dict__)
        transfer.Notifier(opts).run()

    if opts.pack:
        LOGGER.info('Running archive pack')
        assert opts.night, '-N/--night argument empty'
        assert opts.camera, '-C/--camera argument empty'
        transfer.Compressor(opts).run()

    if opts.upload:
        LOGGER.info('Running upload directory')
        assert opts.night, '-N/--night argument empty'
        assert opts.camera, '-C/--camera argument empty'
        transfer.Uploader(opts).run()

    if opts.download:
        LOGGER.info('Running download archive')
        assert opts.night, '-N/--night argument empty'
        assert opts.camera, '-C/--camera argument empty'
        transfer.Downloader(opts).run()

    if opts.unpack:
        LOGGER.info('Running unpack archive')
        assert opts.night, '-N/--night argument empty'
        assert opts.camera, '-C/--camera argument empty'
        transfer.Decompressor(opts).run()

    if opts.alert:
        LOGGER.info('Running email alert notification')
        assert opts.night, '-N/--night argument empty'
        assert opts.camera, '-C/--camera argument empty'
        assert '?' not in opts.night and '*' not in opts.night, \
            'alert action -N/--night argument may not contain wild cards characters'
        opts.email_translation = opts.email_translation.format(**opts.__dict__)
        transfer.Notifier(opts).run()


def main():
    """ Main entry point of script. """
    parser = argparse.ArgumentParser(description='MRG batch transfer program',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-r', '--retries', dest='retries', type=int, default=0,
                        help='the number of SFTP retries after download failure.')

    parser.add_argument('-i', '--ignore-errors', dest='ignoreErrors', action='store_true',
                        help='Ignore errors and keep processing.')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Log with verbosity.')

    parser.add_argument('-d', '--download', dest='download', action='store_true',
                        help='Download.')

    parser.add_argument('-u', '--upload', dest='upload', action='store_true',
                        help='Upload.')

    parser.add_argument('-n', '--notify', dest='notify', action='store_true',
                        help='Email notification when observation completed.')

    parser.add_argument('-a', '--alert', dest='alert', action='store_true',
                        help='Send email alert when FTP upload complete.')

    parser.add_argument('-U', '--unpack', dest='unpack', action='store_true',
                        help='Unpack downloaded  zip files.')

    parser.add_argument('-P', '--pack', dest='pack', action='store_true',
                        help='Pack directory into a compressed file.')

    parser.add_argument('-y', '--overwrite', dest='overwrite', action='store_true',
                        help='automatically overwrite existing files.')

    parser.add_argument('-o', '--output', dest='log', default=None,
                        help='Log output to file.')

    parser.add_argument('-c', '--config-file', dest='config', default='settings.py',
                        help='the configuration file')

    parser.add_argument('-C', '--camera', dest='camera',
                        help='the camera directory name to process')

    parser.add_argument('-N', '--night', dest='night',
                        help='the night directory name to process.')

    opts = parser.parse_args()

    format_str = '%(asctime)s %(levelname)-7s %(name)-30s %(thread)-8d %(message)s'
    logging.basicConfig(format=format_str,
                        level=[logging.INFO, logging.DEBUG][opts.verbose],
                        filename=opts.log)

    config.get_settings(opts.config, opts, parser)
    config.load_password_parameters(opts)

    # with open(opts.config) as file_obj:
    #     for line in file_obj:
    #         line = line.strip()
    #         if line and not line.startswith('#') and '=' in line:
    #             key, val = [part.strip() for part in line.split('=', 1)]
    #             setattr(opts, key, eval(val))
    #
    # transfer.load_password_parameters(opts)
    try:
        run_commands(opts)
    except KeyboardInterrupt:
        LOGGER.info('Caught CTRL+C. Exiting program.')

if __name__ == '__main__':
    main()
