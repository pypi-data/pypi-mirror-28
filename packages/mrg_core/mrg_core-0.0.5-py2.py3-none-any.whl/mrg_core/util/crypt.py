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
File encryption / decryption module based on xor encryption. It has a number of
limitations that can be reviewed in the reference below.

References::
    http://en.wikipedia.org/wiki/XOR_cipher
    http://www.evanfosmark.com/2008/06/xor-encryption-with-python


@todo: add checksum to header section of the encrypted file.
"""
import hashlib
from itertools import cycle

from future.utils import iteritems


class IncorrectPassword(Exception):
    """ incorrect password exception """

    def __init__(self, fname):
        super(IncorrectPassword, self).__init__()
        self._fname = fname

    def __str__(self):
        return 'Incorrect password for: %s' % self._fname


class CryptFile(object):
    """
    Handles encryption / decryption of files. The file i/o handling
    is not buffered, therefore, do not use this class with huge files.
    """

    def __init__(self, pwd_file, password, create=False):
        self.file = pwd_file
        self.data = ''
        self.password = hashlib.md5(password.encode('utf-8')).hexdigest()
        self.header = '#===='
        self._create = create
        if not self._create:
            self._open()

    def flush(self):
        """ Join the key value pairs and write them back to file.
        """
        data = ''.join(['%s=%s\n' % (k, v) for k, v in iteritems(self)])
        self.write(data)

    def __enter__(self):
        return self

    def __exit__(self, err_type, err_val, err_tb):
        self.flush()

    @staticmethod
    def __xor_crypt_string(data, key):
        """ simple xor encryption
        Reference: http://www.evanfosmark.com/2008/06/xor-encryption-with-python
        """
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        return ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(data, cycle(key)))

    def __authenticate(self):
        """ Test to determine whether or not the password used to decrypt the
        file starts with a valid header. This indicates that the passowrd used
        is correct.
        """
        lines = self.data.split('\n')
        if len(lines) and lines[0] == self.header:
            self.data = '\n'.join(lines[1:])
            return True
        else:
            return False

    def _open(self):
        """ Open the encrypted file and decode it.
        """
        # read to EOF, or if opened as a binary, to the last byte
        with open(self.file, 'rb') as file_obj:
            data_enc = file_obj.read()
        self.data = self.__xor_crypt_string(data_enc, self.password)
        if not self.__authenticate():
            raise IncorrectPassword(self.file)
        return self.data

    def write(self, data):
        """
        Encrypt the plain data input using xor encryption and write the
        encrypted result to the binary file.
        """
        data = self.header + '\n' + data
        data_enc = self.__xor_crypt_string(data, self.password)
        with open(self.file, 'wb') as file_object:
            file_object.write(data_enc.encode('utf-8'))
            file_object.close()


class CryptPropertyFile(CryptFile, dict):
    """ handles encryption / decryption of files """

    def __init__(self, pwd_file, password, create=False):
        super(CryptPropertyFile, self).__init__(pwd_file, password, create)

    def __setitem__(self, name, value):
        """ Modify a key value. If the key does not exist it is created."""
        dict.__setitem__(self, name, value)

    def _open(self):
        """ Override the open method and parse the decoded content as a key
        value list.
        """
        data = super(CryptPropertyFile, self)._open()
        for line in data.split('\n'):
            parts = line.split('=', 2)
            if len(parts) == 2:
                key = parts[0].strip()
                val = parts[1].strip()
                self[key] = val
