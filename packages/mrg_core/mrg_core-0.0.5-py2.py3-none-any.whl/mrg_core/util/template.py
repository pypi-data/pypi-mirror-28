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
""" This module defines a templating class that translates a body of text with
placeholders and expressions that may be evaluated. """

from __future__ import print_function

import re
import os
import ctypes
import platform


class TemplateEngineException(Exception):
    """ Exception emanating from the TemplateEngine class. """


class TemplateEngine(object):
    """ A simple template engine that allows placeholder keys to be
    translated and placeholder expressions to be evaluated.

    Use [key] square brackets to translate this placeholder to a
    value defined in a parameters dictionary.

    Use the {} curly braces to translate placeholder expressions.

    Valid expressions are,

        * {extract://<file>|<sub-string-1>|<sub-string-2 default:LF>}
        * {size://<file or directory>}
        * {free://<drive example: C:>}
        * {count://<file>|<string>}
        * {file://<csv file>|<format-specifiers default: %s>}

    The `extract://` expression extracts the first string found surrounded
    by the specified sub-strings.

    The `size://` expression computes the size in MB of a file or a directory.

    The `free://` expression computes the disk space remaining for the
    specified drive.

    The `count://` expression counts the number of occurances of a
    specified word or sub-string.

    The `file://` expression inserts the content of the specified file into
    the translated body.

    The template file may contain a header which requires the following
    format,

        * key:value

    Whitespace around the key and value are stripped. The headers can then
    be passed to the consuming class, i.e. :class:`Notifier`; which can
    then set the subject heading or add file attachements to the email.
    """

    def __init__(self, parameters, template_file=None):
        self._parameters = {}
        self._headers = {}
        self._body = ''
        self._file = template_file
        if isinstance(parameters, dict):
            self._parameters = parameters

        elif isinstance(parameters, str):
            key_values = parameters.split(';')
            for key_value in key_values:
                key_value = key_value.strip()
                if len(key_value):
                    key, value = key_value.split('=', 1)
                    self._parameters[key] = value
    @staticmethod
    def get_free_space(dir_name):
        """ Return folder/drive free space (in bytes).

        Reference:
        http://stackoverflow.com/questions/51658/cross-platform-space-remaining-on-volume-using-python

        :param str dir_name: the drive name or path
        :return: the number of bytes
        :rtype: int
        """
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dir_name),
                                                       None,
                                                       None,
                                                       ctypes.pointer(free_bytes))
            return free_bytes.value
        else:
            if ':' in dir_name:
                # this is much too forgiving but for cross platform
                # unit-testing it's a must.
                # This assumes no 'c:' or 'd:' directories exist on Linux
                # platforms. This will be converted to a '/' root directory
                drive, rest = dir_name.split(':', 1)
                if len(drive) == 1 and len(rest) == 0:
                    dir_name = '/'

            # Using getattr instead of os.statvfs so to avoid the pylint error:
            # [E1101(no-member), get_free_space] Module 'os' has no 'statvfs' member
            stat = getattr(os, 'statvfs')(dir_name)
            return stat.f_bavail * stat.f_frsize

    @property
    def body(self):
        """ Return the translated body. """
        return self._body

    @property
    def headers(self):
        """ Return the translated headers.
        :return: a dictionary of lists
        :rtype: dict
        """
        return self._headers

    @property
    def parameters(self):
        """ Return the parameters used to do the translation.
        :return: the key value pairs
        :rtype: dict
        """
        return self._parameters

    @staticmethod
    def _get_expression(line):
        """ Extract the expression to evaluate.
        :param str line:
        :return: None or the expression between the { curly braces }
        :rtype: str
        """
        keys = re.findall(r'{([^}]+)}', line)
        if keys and len(keys):
            return keys[0]

    @staticmethod
    def _get_extract(expression):
        """ Extract the first occurrence in a file that matches the
        sub-string expression.

        :param str expression: <file>|<sub-string-1>|[sub-string-2 default:LF]
        :return: empty string if the criteria was not found, else the
            string between the sub-strings.
        :rtype: str
        :raises TemplateEngineException: if the /path/ expression
            does not exist on the file system, or the expression
            does not include a vertical line (|) separator.
        """
        if '|' not in expression:
            raise TemplateEngineException(
                'Missing | separator in `extract` expression: %s'
                % expression)

        parts = expression.split('|')
        path = parts[0]
        sub_str_1 = parts[1]
        sub_str_2 = '\n'
        if len(parts) >= 2:
            sub_str_2 = parts[2]

        if not os.path.exists(path):
            raise TemplateEngineException(
                'File `extract` expression error in line: %s. '
                'File does not exist: %s' % (expression, path))

        if not os.path.isfile(path):
            raise TemplateEngineException(
                'File `extract` expression error in line: %s. '
                'Path is not a file: %s' % (expression, path))

        with open(path) as file_object:
            lines = file_object.readlines()

        value = ''
        for _line in lines:
            pos_1 = _line.find(sub_str_1)
            pos_2 = _line.find(sub_str_2)
            if pos_1 != -1 and pos_2 != -1:
                if pos_2 < pos_1:
                    pos_2 = len(_line)
                value = _line[pos_1 + len(sub_str_1):pos_2].strip()
                break
        return value

    @staticmethod
    def _get_count_words(expression):
        """ Retrieve the number of occurrences of a sub-string in a file.

        :param str expression: <file>|<sub-string>
        :return: the occurrence count.
        :rtype: str
        :raises TemplateEngineException: if the /path/ expression
            does not exist on the file system, or the expression
            does not include a vertical line (|) separator.
        """
        if '|' not in expression:
            raise TemplateEngineException(
                'Missing | separator in `count` expression: ' % expression)

        file_path, expr = expression.split("|", 1)
        if not os.path.exists(file_path):
            raise TemplateEngineException(
                'File `count` expression error: %s. '
                'File does not exist: %s' % (expression, file_path))

        with open(file_path, 'r') as file_object:
            content = file_object.read()
            count = content.count(expr)
        return '%d' % count

    @staticmethod
    def _get_file_content(expression):
        """ Get the file content as a formatted string.

        :param str expression: <file>|[<format> default:%s]
        :return: the formatted file content.
        :rtype: str
        :raises TemplateEngineException: if the /path/ expression
            does not exist on the file system, or if
            a line cannot be properly formatted.
        """
        if '|' in expression:
            path, format_expr = expression.split("|", 1)
        else:
            path = expression
            format_expr = '%s'

        if not os.path.exists(path):
            raise TemplateEngineException(
                'File `file` expression error in line: %s. '
                'File does not exist: %s' % (expression, path))

        with open(path) as file_object:
            lines = file_object.readlines()
            if format_expr:
                try:
                    for i, row in enumerate(lines):
                        columns = tuple(row.split(','))
                        lines[i] = (format_expr % columns)
                except Exception as exc:
                    raise TemplateEngineException(
                        'Error formatting table in line %s. '
                        'Exception: %s' % (expression, str(exc)))
        return ''.join(lines)

    @staticmethod
    def _get_path_size(expression):
        """ Get the number of MB of a file or directory.

        :param str expression: file or directory
        :return: the formatted MB string
        :rtype: str
        :raises TemplateEngineException: error is raised if the /path/
            expression specified does not exist on the file system.

        """
        path = expression
        if not os.path.exists(path):
            raise TemplateEngineException(
                'Size expression error: %s. '
                'Directory does not exist: %s' % (expression, path))

        if os.path.isdir(path):
            value = sum([os.path.getsize(os.path.join(path, f)) for f in os.listdir(path)
                         if os.path.isfile(os.path.join(path, f))])
        else:
            value = os.path.getsize(path)
        return '%0.2f (MB)' % (value / (1024.0 * 1024.0))

    @staticmethod
    def _get_free(expression):
        """ Get the amount of free disk space for the specified drive.
        :param str expression: the drive, i.e. C: or D: etc
        :return: the formatted GB string
        :rtype: str
        """
        drive = expression
        free = TemplateEngine.get_free_space(drive) / (1024.0 * 1024.0 * 1024.0)
        return '%0.2f (GB)' % free

    def _translate_line(self, line):
        """ Translate the placeholder expressions in the specified string.

        :param str line: translate the [ square bracketed ]  placeholders
            using the mail translation dictionary.
        :return: the new translated line.
        :rtype: str
        """
        if not line:
            return line

        if len(self._parameters):
            # extract keys between [...] brackets
            keys = re.findall(r'\[([^\]]+)]', line)
            for key in keys:
                if key in self._parameters:
                    replace = '[%s]' % key
                    value = self._parameters[key]
                    line = line.replace(replace, value)
        return line

    def _load_template_file(self):
        """ Retrieve the translated template file content.
        """
        # print('Parameters:', self._parameters)
        if not self._file:
            raise TemplateEngineException('Email template file is missing')

        if not os.path.exists(self._file):
            raise TemplateEngineException(
                'Email template file does not exist: %s'
                % self._file)

        with open(self._file, 'r') as file_object:
            lines = file_object.readlines()
            # remove any empty lines from the header
            while len(lines) and not lines[0].strip():
                lines.pop(0)

        for i, line in enumerate(lines):
            lines[i] = self._translate_line(line)

        expression_func = {
            'count': self._get_count_words,
            'extract': self._get_extract,
            'file': self._get_file_content,
            'free': self._get_free,
            'size': self._get_path_size,
        }

        body = []
        in_header = True
        for i, line in enumerate(lines):
            if in_header and ':' in line:
                key, value = [part.strip() for part in line.split(':', 1)]
                if key not in self._headers:
                    self._headers[key] = []
                self._headers[key].append(value)
            elif in_header and not line.strip():
                pass  # skip empty lines after header
            else:
                in_header = False
                expression = self._get_expression(line)
                if expression:
                    try:
                        key, args = expression.split('://', 1)
                    except ValueError as exc:
                        msg = 'Invalid expression at line %d: %s\n  Exception: %s' \
                              % (i + 1, line, str(exc))
                        raise TemplateEngineException(msg)

                    if key not in expression_func:
                        raise TemplateEngineException('Invalid expression key: %s' % key)

                    value = expression_func[key](args)
                    line = line.replace('{%s}' % expression, value)
                body.append(line)

        self._body = ''.join(body)

    def run(self):
        """ Execute the template file translation. The results may be access
        by using the :func:`body` and :func:`headers` methods. """
        self._load_template_file()
