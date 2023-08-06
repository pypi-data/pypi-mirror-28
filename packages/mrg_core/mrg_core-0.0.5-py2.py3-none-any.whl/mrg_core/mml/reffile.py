#!/usr/bin/env python
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
"""
This module implements the METREC REF star position file parser.
"""
from mrg_core.util.fileparser import FileParser


class RefFile(FileParser):
    """ Parse a METREC reference `*`.ref file. A typical file is provided
    here::

        SiteCode 14260
        Longitude 10.858890
        Latitude 45.697498
        Altitude 1208
        OperationMode unguided
        ReferenceDate 2010 3 19
        ReferenceTime 22 35 0
        VideoBrightness 255
        VideoContrast 255
        CenterOfPlate  192  144
        OrderOfPlateConstants 3
        NumOfRefStars 42
        RefStar1  1.8  1.1   147  11.0620  61.7510 152.25  51.00
        RefStar2  1.8  0.0   252  12.9000  55.9600 226.50  67.25
        RefStar3  2.7  0.9    50  16.4000  61.5140 245.00 200.00
        RefStar4  2.2  0.1   180  13.3990  54.9250 244.00  80.50
    """

    def __init__(self, path):
        """
        :param str path: the hhmmss.inf astrometry file path.
        :raises IOError: if the INF path specified does not exist.
        """
        self._positions = []
        super(RefFile, self).__init__(path)

    def parse(self):
        """ Parse the entire REF astrometry file content."""
        in_header = True
        iterator = self._lines.__iter__()
        for line in iterator:
            line = line.strip()
            if line.startswith('RefStar1'):
                in_header = False

            if in_header:
                key, value = [part.strip() for part in line.split(' ', 1)]
                self._header[key] = value
            else:
                # NOTE: here is where the RefStar{#} would be parsed
                break
