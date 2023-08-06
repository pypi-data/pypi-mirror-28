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
Tool to manipulate images. Functions available are,

    * convert BND files to animated GIF
    * resizing images
    * enhanding contrast

The command line usages is::

    usage: imageproc.py [-h] [-i INPUT] [-o OUTPUT_DIR] [-C CONTRAST] [-S SCALE]
                        [-B] [-b] [-p] [-g] [-v]

    Metrec Image Manipulation and Processing

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            The bnd file path or directory. (default: None)
      -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                            The absolute output directory path or the output
                            directory relative to the bnd input file. It will be
                            auto created. (default: None)
      -C CONTRAST, --contrast CONTRAST
                            Enhance the contrast of the saved images. (default:
                            1.0)
      -S SCALE, --scale SCALE
                            Scale (resize) the saved images. (default: 1.0)
      -B, --background-full
                            Include the entire background bmp image. WARNING: this
                            will result in large output GIF (default: False)
      -b, --background      Include the background bmp image (default: False)
      -p, --save-png        Save the sum image as png (default: False)
      -g, --save-gif        Save the animated gif image (default: False)
      -v, --verbose         Log with verbosity (default: False)


"""
from __future__ import print_function

import os
import logging
import argparse
import glob

from mrg_core.util import imaging


def execute_command(opts):
    """ Execute the import command.

    :param Namespace opts: the option settings from argparse.
    """

    if os.path.isdir(opts.input):
        bnd_files = glob.glob(opts.input + '/*.bnd')
    else:
        bnd_files = [opts.input]

    for bnd_file in bnd_files:
        save_types = []
        if opts.save_png:
            save_types.append('png')
        if opts.save_gif:
            save_types.append('gif')
        background = None
        if opts.background:
            background = False
        elif opts.full_image:
            background = True

        bnd = imaging.BNDImages(bnd_file,
                                save_types=save_types,
                                background=background,
                                contrast=opts.contrast,
                                scale=opts.scale)
        bnd.save(opts.output_dir)


def main():
    """ Main entry point of script """
    parser = argparse.ArgumentParser(
        description='Metrec Image Manipulation and Processing',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--input', dest='input',
                        help='The bnd file path or directory.')

    parser.add_argument('-o', '--output-dir', dest='output_dir', default=None,
                        help='The absolute output directory path or the output '
                             'directory relative to the bnd input file. It will be auto '
                             'created.')

    parser.add_argument('-C', '--contrast', default=1.0, type=float, dest='contrast',
                        help='Enhance the contrast of the saved images.')

    parser.add_argument('-S', '--scale', default=1.0, type=float, dest='scale',
                        help='Scale (resize) the saved images.')

    parser.add_argument('-B', '--background-full', dest='full_image', action='store_true',
                        help='Include the entire background bmp image. WARNING: this will '
                             'result in large output GIF')

    parser.add_argument('-b', '--background', dest='background', action='store_true',
                        help='Include the background bmp image')

    parser.add_argument('-p', '--save-png', dest='save_png', action='store_true',
                        help='Save the sum image as png')

    parser.add_argument('-g', '--save-gif', dest='save_gif', action='store_true',
                        help='Save the animated gif image')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Log with verbosity')

    opts = parser.parse_args()

    format_str = '%(asctime)s %(levelname)-7s %(name)-30s %(thread)-8d %(message)s'
    logging.basicConfig(format=format_str,
                        level=[logging.INFO, logging.DEBUG][opts.verbose],
                        filename=None)

    execute_command(opts)

if __name__ == '__main__':
    main()
