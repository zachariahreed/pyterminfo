import sys
from setuptools import setup

__author__  = 'Zachariah Reed'
__version__ = '0.2'
__contact__ = 'zreed@fastmail.com'
__url__     = 'https://github.com/zachariahreed/pyterminfo'
__license__ = 'GPL'

# byteasm-0.2.0 and later requires python 3.6
if sys.version_info < (3,6) :
  raise NotImplementedError( 'pyterminfo requires Python 3.6+' )

setup(
    name              = 'pyterminfo'
  , version           = __version__
  , description       = 'a terminfo-to-python cross compiler'
  , author            = __author__
  , author_email      = __contact__
  , license           = __license__
  , url               = __url__
  , download_url      = 'https://github.com/zachariahreed/pyterminfo/tarball/' + __version__
  , packages          = ['pyterminfo']
  , platforms         = 'any'
  , install_requires  = ['byteasm >=0.2, <0.3']
  , extra_requires    = { 'visualization' : ['pygraphviz>=1.3'] }
  , classifiers       = [
                            'Development Status :: 4 - Beta'
                          , 'Intended Audience :: Developers'
                          , 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
                          , 'Environment :: Console'
                          , 'Operating System :: Unix'
                          , 'Programming Language :: Python :: 3 :: Only'
                          , 'Programming Language :: Python :: 3.6'
                          , 'Topic :: Terminals'
                          ]
  )
