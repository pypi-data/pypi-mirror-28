"""
   Interface module version 2.0 aiming at modifying the way files are parsed.
"""
# The following lines will make the main interface classes available through
# the standard import mechanism, e.g.:
#
#    import mrg_core.util.interfaces as interfaces
#
#    inf_file = interfaces.MetRecInfFile('my/path/to/the/file.inf')
#
from mrg_core.util.interfaces.daffile import DafFile
from mrg_core.util.interfaces.kml import MeteorKML
from mrg_core.util.interfaces.metrecinf import MetRecInfFile
from mrg_core.util.interfaces.metreclog import MetRecLogFile
from mrg_core.util.interfaces.metrecref import RefStarsFile
from mrg_core.util.interfaces.mk import MKFile
__all__ = ['DafFile', 'MeteorKML', 'MetRecInfFile', 'MetRecLogFile', 'MKFile',
           'RefStarsFile']
