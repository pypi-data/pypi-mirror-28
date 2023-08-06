""" The common library for all Meteor Research Group scripts. This
library includes all metrec data interfaces, common astronomical routines,
and utility classes. """

from ._version import get_versions

__version__ = get_versions()['version']
# __status__ = 'Release'
__status__ = '+++ Testing +++'

__pkgname__ = 'mrg_core'
__author__ = 'Hans Smit'
__email__ = 'jcsmit@xs4all.nl'
__docurl__ = 'https://mrg-tools.gitlab.io/mrg_core/'
__giturl__ = 'https://gitlab.com/mrg-tools/mrg_core'

del get_versions
