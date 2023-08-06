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
""" This module implements an abstract class that may be used by sub-classes
to implement a file parsing mechanism.
"""
import os
import time
import logging
from collections import OrderedDict
from io import open


class FileParser(object):
    """ Abstract class to parse a textual based file. """

    def __init__(self, path):

        self._path = path
        self._lines = []  # NOTE: the lines are appended with '\n'
        self._header = OrderedDict()

        if path:
            if os.path.exists(path):
                self.load(path)
            else:
                raise IOError('%s does not exist.' % path)

    def parse(self):
        """ Parse the entire file content and creates an in-memory version
        of the data. This is to be implemented by the sub-class.
        """
        raise NotImplementedError

    @property
    def path(self):
        """ Retrieve the absolute path to the parsed file. """
        return os.path.realpath(self._path)

    @property
    def header(self):
        """ Retrieve the headers in the REF file. The header keys are vary
        with the metrec version.,

        :return: the ordered-dictionary of parsed key value INF header pairs.
        :rtype: OrderedDict
        """
        return self._header

    def load(self, path):
        """ Load the entire INF file into memory and parse it.

        :param str path: the METREC INF astrometry file.
        """
        t_0 = time.time()
        if not path:
            path = self._path
        self._path = path

        # with open(self._path, 'rb') as file_obj:
        #     body = file_obj.read()
        #     body = body.replace(b'\xf8', b'd')
        #     body = body.replace(b'\xe5', b'snr')
        #     body = body.replace(b'\xe4', b'#')  # V2.1
        #     body = body.replace(b'\xed', b'b')  # V2.1
        #     body = body.replace(b'\r', b'')
        #     body = str(body.decode('utf-8'))
        #     self._lines = body.split('\n')
        #     # self._lines = file_obj.readlines()
        with open(self._path, 'r', encoding='iso-8859-1') as file_obj:
            self._lines = file_obj.readlines()

        self.parse()
        logging.debug('Timed: %0.2fs, Parsed: %s', time.time() - t_0, self._path)
