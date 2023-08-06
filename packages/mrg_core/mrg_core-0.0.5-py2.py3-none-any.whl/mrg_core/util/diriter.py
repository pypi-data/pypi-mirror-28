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
""" This module provides routines to navigate a directory structure. It makes
extensive use of glob patterns to match directory with wildcard expressions.

Reference:
    https://en.wikipedia.org/wiki/Glob_(programming)
"""
# disabling the 'unused-import' pylint warning wrt scandir
# pylint: disable=W0611
from __future__ import print_function

import glob
import re
import sys
import time
import os

try:
    from os import scandir  # this will fail for Python < 3.5
    from os import walk
except ImportError:
    try:
        from scandir import scandir
        from scandir import walk
    except ImportError as _exc:
        print('WARNING: pip install scandir')
        print(str(_exc))
        # ok import the slow 'walk' variant
        from os import walk


class DirectoryIterator(object):
    """ This class acts as an iterator to the 'leaf' directories
    that match a directory expression. """

    def __init__(self, input_dir, ignore_case=True, walk_dir=True, display_progress=False):
        """

        :param str input_dir:
        :param bool ignore_case: True if the /last/ directory is
            to be matched using case-insensitive pattern rules.
        :param bool walk_dir: True if matched directories are to be
            navigated into using the scandir and walk methods.
        :param bool display_progress: show progress bar when iterating
            over directories.
        """
        self._display_progress = display_progress
        self._input_dir = input_dir
        if ignore_case:
            input_dir = DirectoryIterator.get_ignore_case_pattern(input_dir)
        self._input_dir_expr = input_dir
        self._paths = []
        self._sub_dirs = []
        self._sub_dir_index = -1
        self._walk = walk_dir
        self._progress = {'time_0': 0.0, 'counter': 0}
        self.reset()

    @staticmethod
    def get_ignore_case_pattern(pattern):
        """ Converts the base directory (or file) to an
        none case sensitive patten for use with the glob module.
        """

        def either(char_in):
            """ Translate character to case-insensitive wildcard
            expression. Example: 'a' => '[aA]'
            :param str char_in:
            :return: the 4 character wild card expression.
            :rtype: str
            """
            chars_case = '[%s%s]' % (char_in.lower(), char_in.upper())
            return chars_case if char_in.isalpha() else char_in

        root_dir, dir_name = os.path.split(pattern)
        dir_name = ''.join([either(char) for char in dir_name])
        pattern = os.path.join(root_dir, dir_name)
        return pattern

    @property
    def template(self):
        """ Retrieve the input directory expression.

        :return: the input directory glob expression.
        :rtype: str
        """
        if self._input_dir_expr != self._input_dir:
            return self._input_dir_expr
        else:
            return self._input_dir

    def reset(self):
        """ Reset the iterator back to the starting entry.
         :return: self
         :rtype: DirectoryIterator
        """
        # test = glob.glob(self._input_dir_expr)
        self._paths = glob.iglob(self._input_dir_expr)
        self._sub_dirs = []
        self._sub_dir_index = -1
        return self

    def sorted(self):
        """ Retrieve all entries as a path-sorted list.

        WARNING: For large directory structures this may be a performance
        bottle neck.
        """
        entries = list(self)
        entries = sorted(entries)
        return entries

    def __iter__(self):
        """ Start the iteration. """
        self._progress['time_0'] = time.time()
        return self

    def print_progress(self):
        """ Print the progress to the stdout as::

            <dir count> (<scan rate>)
        """
        if not self._display_progress:
            return
        self._progress['counter'] += 1
        d_time = time.time() - self._progress['time_0']
        rate = 0.0
        if d_time > 0:
            rate = self._progress['counter'] / d_time
        msg = '%05d (%0.1f dir/sec)' % (self._progress['counter'], rate)
        sys.stdout.write(msg + '\b' * len(msg))

    def __next__(self):
        """ Python 3 compatibility fix for iterator class """
        return self.next()

    def next(self):
        """ Retrieve the next entry.
        :return: the next path
        :rtype: str
        """
        if self._walk:
            # check if there are sub-directories to return
            if self._sub_dir_index >= 0:
                self._sub_dir_index += 1
                if self._sub_dir_index < len(self._sub_dirs):
                    return self._sub_dirs[self._sub_dir_index]

        # else get the next entry from the glob iterator
        path = next(self._paths)

        if self._walk:
            # check if there are sub-directories
            if os.path.isdir(path):
                # self._sub_dirs = os.listdir(path)
                self._sub_dirs = [sub_dir[0] for sub_dir in walk(path)]
                self._sub_dir_index = 0
                return self._sub_dirs[0]

        return path


class SystemSessionIterator(DirectoryIterator):
    """ The class iterates over either an CILBO or IMO directory structure.

    The VMO structure is defined as::

        */<yyyy>/<yyyymmdd>/<system code>

    While the MRG directory strucuture is defined as::

        */<system code>/<yyyymmdd>

    This iterator returns the following tuple::

        (path, yyyy, yyyymmdd, sys_code)

    Each tuple entry is a string type and the system code is upper case.
    """

    def __init__(self, input_dir, display_progress=False):
        super(SystemSessionIterator, self).__init__(input_dir,
                                                    ignore_case=True,
                                                    walk_dir=True,
                                                    display_progress=display_progress)
        # /media/FREECOM HDD/IMO Network Database/[YYYY]/[YYYYMMDD]/[SYSTEM_CODE]
        self._re_imo = re.compile(r'^.*/(\d{4})/(\d{8})/([a-zA-Z]{2}\w*)$')

        # /media/FREECOM HDD/MRG/[SYSTEM_CODE]/[YYYYMMDD]
        self._re_mrg = re.compile(r'^.*/([a-zA-Z]{2}\w*)/(\d{8})$')

    def sorted(self):
        """ Retrieve all entries as a path-sorted list.

        WARNING: For large directory structures this may be a performance
        bottle neck.
        """
        entries = list(self)
        entries = sorted(entries, key=lambda entry: entry[0])
        return entries

    def next(self):
        while True:
            path = super(SystemSessionIterator, self).next()
            self.print_progress()
            norm_path = path.replace('\\', '/')
            result = self._re_imo.findall(norm_path)
            year, night, sys_code = None, None, None
            if len(result):
                year, night, sys_code = result[0]
            else:
                result = self._re_mrg.findall(norm_path)
                if len(result):
                    sys_code, night = result[0]
                    year = night[0:4]
            if len(result):
                return str(path), \
                       str(year), \
                       str(night), \
                       str(sys_code).upper()


class SystemSessionYearIterator(object):
    """ The class iterates over a IMO directory structure. """

    def __init__(self, input_year_dir,
                 continue_from_yyyymmdd=None,
                 display_progress=False):

        # /media/FREECOM HDD/IMO Network Database/[YYYY]/[YYYYMMDD]/[SYSTEM_CODE]
        self._re_imo = re.compile(r'^.*/(\d{4})/(\d{8})/([a-zA-Z]{2}\w*)$')
        self._year = int(os.path.basename(input_year_dir))
        self._month = 0
        self._date = '??'
        self._camera = ''
        self._input_dir = os.path.join(input_year_dir, '%04d%02d??')
        self._iterator = None
        self._display_progress = display_progress
        self._continue_from_yyyymmdd = continue_from_yyyymmdd

    def __iter__(self):
        """ Start the iteration and locate the *continue from* entry
        if this is specified in the constructor.

        :return: self
        :rtype: SystemSessionYearIterator
        """
        self._month = 0
        self._iterator = None
        short_date_reg_ex = re.compile(r'^(\d{4})(\d{2})(\d{2}).*')
        if isinstance(self._continue_from_yyyymmdd, str):
            parts = short_date_reg_ex.findall(self._continue_from_yyyymmdd)
            if len(parts):
                _, month, date = [int(val) for val in parts[0]]
                self._month = month-1  # it will be incremented on the next call
                self._date = '%02d' % date
                self._camera = self._continue_from_yyyymmdd[9:].upper()
        return self

    def _new_iterator(self):
        """ Increments the month and creates a sorted directory
        session iterator.
        """
        self._month += 1
        input_month_dir = self._input_dir % (self._year, self._month)
        sess_iter = SystemSessionIterator(input_month_dir,
                                          display_progress=self._display_progress)
        sess_list = sess_iter.sorted()
        if self._camera:
            for i, sess_entry in enumerate(sess_list):
                if sess_entry[2].endswith(self._date) and sess_entry[3] == self._camera:
                    sess_list = sess_list[i:]
                    break
        self._iterator = iter(sess_list)
        self._date = '??'
        self._camera = ''

    def next(self):
        """ Retrieve the next entry.
        :return: the next path
        :rtype: str
        :raises StopIteration:
        """
        if self._iterator is None:
            self._new_iterator()

        try:
            return next(self._iterator)
        except StopIteration:
            self._iterator = None
            if self._month == 12:
                raise
            else:
                # NOTE: this uses recursion. Try and find
                # a better implementation that does not use recursion.
                return self.next()  # get next month
