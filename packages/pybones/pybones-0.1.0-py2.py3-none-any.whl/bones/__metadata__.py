# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

__all__ = (
    '__name__', '__description__', '__version__', '__author__',
    '__author_email__', '__maintainer__', '__maintainer_email__',
    '__copyright_years__', '__license__', '__url__', '__ver__',
    '__classifiers__', '__keywords__', 'package_metadata',
)

# ----------------------------------------------------------------------
# Package Metadata
# ----------------------------------------------------------------------
__name__ = 'pybones'
__description__ = 'A python project creation toolkit'
__version__ = '0.1.0'

__author__ = 'Brian Bruggeman'
__author_email__ = 'brian.m.bruggeman@gmail.com'

__maintainer__ = 'Brian Bruggeman'
__maintainer_email__ = 'brian.m.bruggeman@gmail.com'

__copyright_years__ = '2017'
__license__ = 'Apache 2.0'
__url__ = 'https://github.com/brianbruggeman/bones'
__ver__ = tuple([int(ver_i.split('-')[0]) for ver_i in __version__.split('.')])

__classifiers__ = [
    'Programming Language :: Python',
    'Natural Language :: English',
    'Development Status :: 3 - Alpha',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3.6',
]

__keywords__ = ['bones', 'scaffold', 'template', 'project', 'package', 'tool']

# Package everything above into something nice and convenient for extracting
package_metadata = {
    k.strip('_'): v
    for k, v in locals().items()
    if k.startswith('__')
    if k.strip('_') not in ['all', 'copyright_years', 'ver']
}
