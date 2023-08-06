"""
.. py:module:: cmdline

Parser for single command-line or multiple command-line options.

The :py:mod:`cmdline` module extends the functionality of the standard python
library `argparse <https://docs.python.org/2.7/library/argparse.html>`_
making it easier to write single command line or multiple command line
interfaces.  The main script defines what commands requires and what arguments
are needed per command and this module will figure out how to parse those out
of sys.argv.  This module also generates help and usage messages and issues
errors when users give the program invalid arguments.

The module contains the following public classes:

   - :py:class:`.MultiCmdParser` --
     The main entry point for the multiple-command line parsing.  The
     :py:meth:`add_command() <MultiCmdParser.add_command>` method is used to
     populate the parser with command(s) and its arguments.  Then the
     :py:meth:`parse_args() <MultiCmdParser.add_command>` method is invoked to
     convert the arguments at the command-line into an object with attributes.

   - :py:class:`.SingleCmdParser` --
     The main entry point for the single-command line parsing.  Once the
     instance is constructed, the :py:meth:`parse_args` method is invoked to
     convert the arguments at the command-line into an object with attributes.

   - :py:class:`.Opts` --
     A namespace class for individual options for the parsers.

   - :py:class:`.Argument` --
     A class that support the creation of additional -- non-standard --
     argument options within a given program.  This class facilitates the
     creation of multiple-command line parsers where a non-standard argument
     option is required by multiple commands.

All other classes in this module are considered private and could be changed at any
time.

"""
from __future__ import print_function

import argparse
import os
import sys

import mrg_core.util.cmdline.action as action


class Argument(object):
    """Class to hold the contents of a given argument."""

    def __init__(self, *args, **kwargs):

        # If not positional arguments are supplied, there's an error as
        # there is no argument name or flag.
        if not args:
            raise ValueError('No argument flag or argument name supplied.')

        self._name = args
        self._config = kwargs

    @property
    def name(self):
        r"""List of flags or names given to the Argument instance, in the form
        required by the ArgumentParse add_argument method.  When invoking this
        method, this property should be preceded by \*.  Note that this
        property corresponds to the args in the method call."""
        return self._name

    @property
    def options(self):
        r"""List of configuration options for the Argument instance, in the
        form required by the ArgumentParse add_argument method.  When invoking
        this method, this property should be preceded by \**.  Note that this
        property corresponds to the kwargs in the method call."""
        return self._config


class MultiCmdParser(argparse.ArgumentParser):
    """
    Class for handling multiple commands argument parsing, i.e. argument
    parsers for several commands with multiple (different) arguments.
    """

    def __init__(self, description=None):
        self.program_name = os.path.basename(sys.argv[0])
        self._commands = {
            'help': SingleCmdParser(
                [],
                description='Get help on using {}.'.format(self.program_name))
        }

        super(MultiCmdParser, self).__init__(
            description=description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    def parse_args(self, argv=None, namespace=None):
        """Parsing of arguments"""

        if not argv:
            argv = sys.argv[1:]

        if not argv:
            self._help(topic='minimum_help')
            raise SystemExit

        command = argv[0]
        argv = argv[1:]
        parser = self._commands.get(command)
        if not parser:
            self._help("Unknown command: '%s'" % command)
            raise SystemExit

        options, args = parser.parse_known_args(argv, namespace)

        if command == 'help':
            if args:
                parser = self._commands.get(args[0])
                if parser:
                    self._help(parser=parser)
                else:
                    self._help("Unknown command: '%s'" % args[0])
            else:
                self._help(topic='help')
        elif options.help:
            self._help(parser=parser)
        elif args:
            self.program_name = '{} {}'.format(self.program_name, command)
            self._help("Unknown option: '%s'" % args[0])

        return options

    def add_command(self, command, arguments, description=None):
        """Method for adding a command to a MultiCmdParser instance"""
        self._commands[command] = SingleCmdParser(
            arguments=arguments,
            prog='{} {}'.format(self.program_name, command),
            description=description)

    def _help(self, error=None, topic=None, parser=None):
        """
        Display an error message, the requested topic or the help of the
        parser provided as input argument.
        """
        help_topics = {
            'minimum_help': '{description}.  Use "{program_name} help" for '
                            'help.\n',
            'help': self._make_help_message()
        }

        assert error or topic or parser
        if error:
            print(error)
            print("Use '%s help' for help." % (self.program_name,))
        elif parser:
            print(parser.format_help().strip())
        else:
            help_params = {'program_name': self.program_name,
                           'description': self.description}
            print(help_topics[topic].format(**help_params))

    def _make_help_message(self):
        """
        Return a help message listing all the different commands available
        within the current MultiCmdParser instance.

        :rtype str
        """
        help_msg = ['{program_name}, version TBD.',
                    '{description}',
                    '',
                    'usage: {program_name} <command> [options]',
                    '',
                    'Commands:']
        for name in sorted(self._commands):
            words = self._commands[name].description.split()
            description = '    {}'.format(name.ljust(11))
            for word in words:
                if len(description + word) > 79:
                    help_msg.append(description)
                    description = ' ' * 16 + word
                else:
                    description += ' {}'.format(word)
            help_msg.append(description)

        help_msg.append('')
        help_msg.append('Use "{program_name} help <command>" for detailed '
                        'help on any command.')

        return '\n'.join(help_msg)


class Opts(object):
    """
    A namespace class for individual options for the parsers.

    """

    begdate = Argument('-b', '--begdate', action=action.CheckDate,
                       required=True, type=str, dest='begdate',
                       help='Begin date for action, format YYYYMMDD')

    cam1 = Argument('-c1', '--cam1', default='ICC7',
                    required=False, type=str, dest='cam1',
                    help='Name of the camera 1, e.g. ICC7')

    cam2 = Argument('-c2', '--cam2', default='ICC7',
                    required=False, type=str, dest='cam2',
                    help='Name of the camera 2, e.g. ICC9')

    enddate = Argument('-e', '--enddate', action=action.CheckDate,
                       required=True, type=str, dest='enddate',
                       help='End date for action, format YYYYMMDD')

    outdir = Argument('-o', '--outdir', default='.', action=action.CheckDir,
                      required=False, type=str, dest='outdir',
                      help='Path to output directory')

    root = Argument('-r', '--root', default='.', action=action.CheckDir,
                    required=False, type=str, dest='root',
                    help='Root path containing the input data')

    verbose = Argument('-v', '--verbose', default='WARNING',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                'CRITICAL'],
                       required=False, type=str, dest='loglevel',
                       help='Logging level of verbosity')


class SingleCmdParser(argparse.ArgumentParser):
    """
    Class for handling single command argument parsers, i.e. standard command
    line.
    """

    def __init__(self, arguments, prog=None, description=None):
        super(SingleCmdParser, self).__init__(
            prog=prog,
            description=description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            conflict_handler='resolve',
            add_help=False
        )

        for argument in arguments:
            if not isinstance(argument, Argument):
                raise ValueError('Expected Argument type but got {} instead.',
                                 type(argument))

            self.add_argument(*argument.name, **argument.options)

        self.add_argument('-h', '--help', action='store_true',
                          help='show this help message and exit.')
