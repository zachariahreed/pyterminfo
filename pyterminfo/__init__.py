from . core import *

import locale
import os
import posixpath
import sys

__all__ = [
    'terminfo'
  ]


##################################################
#                                                #
##################################################
_default_encoding = locale.getpreferredencoding( False )
_null_entry = b'',(b'null',),(),(),()

##################################################
#                                                #
##################################################
_cache = {}

def terminfo( term=None, binary=False, encoding=None ) :

  """
    Returns a TermInfo structure for the terminal specified.
    The `binary` parameter controls whether the resulting object 
    has its capabilities represented as latin1-encoded `bytes`
    objects or as `str` objects. The former is strictly more 
    correct, but can be a bit painful to use. A few terminfo 
    entries representing more obscure hardware can cause utf 
    encoding errors in the `binary=False` mode, but modern stuff
    is generally fine. The `encoding` parameter is used for
    handling of string parameters in processing of format-string 
    capabilities.
  """

  key = (term,binary,encoding)
  info = _cache.get( key )
  if info is None :

    if term is None :
      term = os.environ[ 'TERM' ]

    if encoding is None :
      encoding = _default_encoding

    path = None
    entry = _null_entry
    if term != 'null' :

      suffix = term[0]
      if sys.platform == 'darwin' :
        suffix = '%02X' % ord( suffix )
      suffix += '/' + term

      path = posixpath.expanduser( '~/.terminfo/' + suffix )
      if not os.path.exists( path ) :
        path = '/usr/share/terminfo/' + suffix 

    info = make_terminfo_from_path( path, binary, encoding )

    _cache[ (term,binary,encoding) ] = info
    _cache[ key ] = info

  return info



