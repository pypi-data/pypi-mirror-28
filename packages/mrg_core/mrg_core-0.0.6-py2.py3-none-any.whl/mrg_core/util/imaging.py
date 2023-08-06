#!/usr/bin/env python
#   --------------------------------------------------------------------------
#   Copyright 2015 SRE-F, ESA (European Space Agency)
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
"""
This module provides routines to convert a BND file to an animated GIF.
"""
from __future__ import print_function

import os
import sys
import struct
import logging

try:
    import numpy
except ImportError as _exc:
    numpy = None
    # print(_exc)
    # print('to install: pip install numpy')

try:
    from PIL import Image
    from PIL import ImageEnhance
    # from PIL import ImageOps
    from PIL import GifImagePlugin
except ImportError as _exc:
    print(_exc)
    print('to install: pip install pillow')
    sys.exit(-1)

try:
    from astropy.io import fits as pyfits
except ImportError as _exc:
    try:
        import pyfits
    except ImportError as _exc:
        print(_exc)
        print('to install: pip install astropy')
        pyfits = None


class Img2Gif(object):
    """ This class generates an animated GIF from a list of images. """

    def __init__(self, images=None):
        """
        :param list images: list of 2D numpy.ndarray images.
        """
        if images is None:
            images = []
        self._images = []
        self._duration = 0.04  # in seconds
        self._loop = 0  # forever
        for image in images:
            self.append(image)

    def close(self):
        """ Free all image resources and clear the image list. """
        for im in self._images:
            im.close()
        del self._images[:]

    def append(self, image):
        """ Append an image to the internal image list.

        :param object image: an /image-like/ object. Can
            be an :class:`Image.Image` or :class:`numpy.ndarray`
            type, or a :class:`str` path to an image file.
        :raises ValueError: if the image passed is of a unknown type.
        """
        dither = 1
        if isinstance(image, str):
            image = Image.open(image)

        if isinstance(image, Image.Image):
            to_append = image.convert('P', dither=dither)

        elif numpy and isinstance(image, numpy.ndarray):
            if image.dtype == numpy.uint8:
                pass
            elif image.dtype in [numpy.float32, numpy.float64]:
                image = (image*255).astype(numpy.uint8)
            else:
                image = image.astype(numpy.uint8)
            # convert
            if len(image.shape) == 3 and image.shape[2] == 3:
                to_append = Image.fromarray(image, 'RGB').convert('P', dither=dither)
            elif len(image.shape) == 2:
                to_append = Image.fromarray(image, 'L').convert('P', dither=dither)
            else:
                raise ValueError('Array has invalid shape to be an image.')

        else:
            raise ValueError('Unknown image type.')

        self._images.append(to_append)

    def write(self, file_obj):
        """ Save the internal image list to the specified file.
        """
        def int_to_bin(i):
            """ Integer to two bytes """
            # divide in two parts (bytes)
            i_lo = i % 256
            i_hi = int(i/256)
            return bytes(bytearray([i_lo, i_hi]))

        def get_header_anim(img):
            """ Animation header. To replace the getheader()[0] """
            out = b'GIF89a'
            out += int_to_bin(img.size[0])
            out += int_to_bin(img.size[1])
            out += b'\x87\x00\x00'
            return out

        def get_app_ext(loops):
            """ Application extention. Part that secifies amount of loops.
            if loops is 0, if goes on infinitely.
            """
            out = b'\x21\xFF\x0B'  # application extension
            out += b'NETSCAPE2.0'
            out += b'\x03\x01'
            if loops == 0:
                loops = 2**16-1
                out += int_to_bin(loops)
                out += b'\x00'  # end
            return out

        def get_graphics_control_ext(duration):
            """ Graphics Control Extension. A sort of header at the start of
            each image. Specifies transparancy and duration. """
            out = b'\x21\xF9\x04'
            out += b'\x08'  # no transparency
            out += int_to_bin(int(duration*100))  # in 100th of seconds
            out += b'\x00'  # no transparent color
            out += b'\x00'  # end
            return out

        image_0 = self._images[0]
        header = GifImagePlugin.getheader(image_0)
        palette = header[1]
        if palette is None:
            palette = header[0][3]

        header = get_header_anim(image_0)
        app_ext = get_app_ext(self._loop)

        # write global header
        file_obj.write(header)
        file_obj.write(palette)
        file_obj.write(app_ext)

        for image in self._images:
            # im = ImageOps.autocontrast(im, 2)
            graph_ext = get_graphics_control_ext(self._duration)
            data = GifImagePlugin.getdata(image)
            imdes, data = data[0], data[1:]

            # write image
            file_obj.write(graph_ext)
            file_obj.write(imdes)
            for data_byte in data:
                file_obj.write(data_byte)

        file_obj.write(b';')  # end gif

    def save(self, gif_path):
        """ Save the images to an animated GIF file.

        :param str gif_path: path to the newly created GIF file.
            If it already exists, then it will be overwritten.
        """
        if len(self._images):
            with open(gif_path, 'wb') as file_obj:
                self.write(file_obj)


class BNDImages(object):
    """ This class manages the loading and saving of BND
    image files to displayable images in various formats.
    Some enhancement utilities are also available such
    as contrast enhancement and image scaling (resizing).
    """

    def __init__(self,
                 bnd_file,
                 save_types=None,
                 background=None,
                 contrast=1.0,
                 scale=1.0):
        """
        :param str bnd_file:
        :param list save_types: list of image types to save. Expected
            values are: 'png' and 'gif'. This may also be passed as a
            string: 'png,gif' or as a list: ['png', 'gif', 'fit']
        :param bool background: this is a tri-state switch to indicate how the
            sum image should be used,
                * True: use entire sum image,
                * False: use sub-frame of sum image,
                * None: (default) do not super impose band images on sum image.
        :param float contrast: to increase the contrast of the image
            a value greater than 1.0 should be specified.
        :param float scale: to decrease the image size a value less than
            1.0 should be specified.
        """
        self._bnd_path = bnd_file
        self._save_types = save_types

        self._background = background
        self._contrast = contrast
        self._scale = scale

        self._frame = None
        self._images = []

        if self._save_types is None:
            self._save_types = []

        if os.path.exists(self._bnd_path):
            self._load()

    def close(self):
        """ Free the image resources and clear the image list. """
        for im in self._images:
            im.close()
        del self._images[:]

    @property
    def frame(self):
        """ Retrieve the background sum image.
        :return: 2D image 8-bit grayscale array
        :rtype: ndarray
        """
        return self._frame

    @property
    def images(self):
        """ Retrieve the images loaded.
        :return: the list of band images of PIL.Image.Image type.
        :rtype: list
        """
        return self._images

    def _get_output_file_path(self, output_dir, ext):
        """ Helper method to help build the image path based on
        the BND file name.

        :param str output_dir: if None, then the BND directory is used
            to save the images in.
        :param str ext: the extension to append to the bnd name.
            Example: '.png', '.gif' etc.
        :return: the new image path
        :rtype: str
        """
        out_dir = os.path.dirname(self._bnd_path)
        if output_dir:
            if output_dir[0] in r'\/' or output_dir[1] == ':':
                # absolute path
                out_dir = output_dir
            else:
                # relative path
                out_dir = os.path.join(out_dir, output_dir)

            out_dir = os.path.abspath(out_dir)
            if not os.path.exists(out_dir):
                logging.info('Creating output directory: %s', out_dir)
                os.makedirs(out_dir)

        name = os.path.basename(self._bnd_path)
        name = os.path.splitext(name)[0]

        file_path = os.path.join(out_dir, name) + ext
        return file_path

    def transform(self, img):
        """ Scale (resize) and enhance (contrast) the image passed.

        :param ndarray img: the 2D numpy array.
        :return: the new image if any enhancements were performed
            otherwise the passed image is returned.
        :rtype: ndarray.
        """
        if self._contrast != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(self._contrast)
            logging.debug('Contrast image : %f', self._contrast)

        if self._scale != 1.0:
            new_size = (int(img.size[0] * self._scale), int(img.size[1] * self._scale))
            img = img.resize(new_size)
            logging.debug('Scaling image : %f', self._scale)

        return img

    def save(self, output_dir=None):
        """ Save the loaded images to the file system. Image
        scaling and contrast enhancements are applied as well.

        :param str output_dir: the output directory to save the images
            to. If it is not specified, then the output directory will
            default to the directory of the BND file.
        """
        if 'fit' in self._save_types:
            new_path = self._get_output_file_path(output_dir, '.fit')
            logging.debug('Saving sub-image BMP file to: %s', new_path)
            data_cube = [numpy.flipud(self._frame)]
            for image in self._images:
                frame = numpy.array(image.getdata(), numpy.uint8)
                frame = frame.reshape(image.size[1], image.size[0])
                data_cube.append(numpy.flipud(frame))
            # data_cube.extend(self._images)
            img = pyfits.PrimaryHDU(data_cube)
            if os.path.exists(new_path):
                os.remove(new_path)
            img.writeto(new_path)

        if 'png' in self._save_types and self._frame is not None:
            new_path = self._get_output_file_path(output_dir, '.png')
            logging.debug('Saving sub-image BMP file to: %s', new_path)
            img = Image.fromarray(self._frame)
            img = self.transform(img)
            # img = ImageOps.autocontrast(img, 0.2)
            img.save(new_path)

        if 'gif' in self._save_types:
            if self._contrast != 1.0:
                for i, img in enumerate(self._images):
                    self._images[i] = self.transform(img)
            new_path = self._get_output_file_path(output_dir, '.gif')
            if len(self._images):
                logging.info('Saving %d frames to: %s', len(self._images), new_path)
                with open(new_path, 'wb') as file_obj:
                    Img2Gif(self._images).write(file_obj)
            else:
                logging.error('no GIF images to write. File not saved: %s.', new_path)

    def load_images(self, images):
        """
        :param list images:
        """
        for img_path in images:
            self._images.append(Image.open(img_path))

        bmp_path = os.path.splitext(self._bnd_path)[0] + '.bmp'
        if os.path.exists(bmp_path):
            logging.debug('Reading background image: %s', bmp_path)
            with Image.open(bmp_path) as bmp_img:
                bmp_data = numpy.array(bmp_img)

            if self._background:
                self._frame = bmp_data

    def _load(self):
        """ Load the BND files and create an internal image array. """
        logging.info('Loading bnd file: %s', self._bnd_path)
        with open(self._bnd_path, 'rb') as file_obj:
            num_bands, band_size, num_lines, y_min = struct.unpack('hHHH', file_obj.read(8))
            # y_max = y_min + num_lines
            # hires = num_bands < 0
            num_bands = abs(num_bands)

            # determine the rectangular region of interest bounds
            x_min = 1000
            x_max = 0
            lines = []
            for _ in range(num_lines):
                line = struct.unpack('HH', file_obj.read(4))  # line => (column, width)
                lines.append(line)

                if line[0] < x_min:
                    x_min = line[0]

                if line[0] + line[1] > x_max:
                    x_max = line[0] + line[1]

            offset_yx = self._load_background(x_min, x_max, y_min, y_min + num_lines)
            for i in range(num_bands):
                logging.debug('Reading BND band #%d', (i+1))
                bands = file_obj.read(band_size)
                data = self._read_band(bands, lines, offset_yx, x_min)
                self._images.append(Image.fromarray(data, 'L'))

    def _load_background(self, x_min, x_max, y_min, y_max):
        """
        :param int x_min:
        :param int x_max:
        :param int y_min:
        :param int y_max:
        :return: 2D tuple of x and y offset of meteor FOV relative to
            full frame boundary.
        :rtype: tuple
        """
        self._frame = numpy.zeros((y_max-y_min, x_max-x_min)).astype(numpy.uint8)
        offset_yx = (0, 0)
        if self._background is not None:  # tri-state bool
            # bmp_path = self._get_output_file_path('.bmp')
            bmp_path = os.path.splitext(self._bnd_path)[0] + '.bmp'
            logging.debug('Reading background image: %s', bmp_path)
            with open(bmp_path, 'rb') as bmp_file:
                with Image.open(bmp_file) as bmp_img:
                    bmp_data = numpy.asarray(bmp_img)
            if self._background:
                self._frame = bmp_data
                offset_yx = y_min, x_min
            else:
                sub_bmp = bmp_data[y_min:y_max, x_min:x_max]
                y_n, x_n = sub_bmp.shape
                self._frame[0:y_n, 0:x_n] = sub_bmp
        return offset_yx

    def _read_band(self, bands, positions, offset_yx, x_min):
        """ Read a single band and convert it to an 2D image.

        :param bytes bands:
        :param list positions: list of x-pos and length tuple pairs
        :param tuple offset_yx: 2D tuple of (ymin, xmin) meteor
            FOV offset relative to full image.
        :param int x_min: the left most position of the meteo FOV.
        :return: ndarray 8-bit image data of a single meteor band.
        :rtype: ndarray
        """
        band_index = 0
        y_size = self._frame.shape[0]
        data = numpy.array(self._frame)
        for j, (x_n, cnt) in enumerate(positions):
            y_n = offset_yx[0] + j
            x_n = offset_yx[1] + x_n
            to_set = [ord(char) if isinstance(char, str) else char for char in bands[band_index:band_index+cnt]]
            if y_n >= y_size:
                logging.warning('y out of range: %s >= %s', y_n, y_size)
                break
            if len(to_set) != cnt:
                logging.warning('x out of range, j=%d, len(to_set)=%d, cnt=%d', j, len(to_set), cnt)
            try:
                data[y_n:y_n+1, x_n-x_min:x_n-x_min+cnt] = to_set
            except ValueError as ex:
                logging.warning('%s frame=%d, j=%d', str(ex), len(self._images), j)
            band_index += cnt
        return data
