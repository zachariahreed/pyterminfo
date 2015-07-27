from . constants import *
from . compile import *
from . utils import *

import locale
import os
import sys

__all__ = [
    'terminfo'
  ]

##################################################
#                                                #
##################################################
_default_encoding = locale.getpreferredencoding( False )

##################################################
#                                                #
##################################################
def _decode_latin1( b ) :
  return b.decode( 'latin1' )

def _ipad( it, fill ) :
  yield from it
  while True :
    yield fill

##################################################
#                                                #
##################################################
class TermInfo( object ) :

  def __init__( self, term, binary, encoding ) :

    path = '/usr/share/terminfo/%s/%s' % (term[0],term)
    if sys.platform == 'darwin' :
      path = '/usr/share/terminfo/%02X/%s' % (ord(term[0]),term)

    with open( path, 'rb' ) as f :

      def read( n ) :
        return f.read( n )

      def read_i16s( n ) :
        return memoryview(f.read( n*2 )).cast( 'h' )

      def read_bools( n ) :
        return memoryview(f.read( n )).cast( '?' )

      magic, = read_i16s(1)
      if magic != 0x011A : 
        raise Exception(
                  str.format(
                      '"{}" is not a valid compiled terminfo file'
                    , path
                    )
                )

      names_length   , \
      booleans_count , \
      numerics_count , \
      strings_count  , \
      table_length   = read_i16s(5)

      names          = read( names_length-1 ).split( b'|' )
      _              = read( 1 )
      booleans       = read_bools(  booleans_count )
      _              = read( f.tell()&1 )
      numerics       = read_i16s(  numerics_count )
      strings        = read_i16s( strings_count )
      tab            = read( table_length )

    self.path      = path
    self.names     = tuple_map( _decode_latin1, names )
    self.binary    = binary
    self.encoding  = encoding
    self.variables = [0] * 52

    for spec,value in zip( BOOLEAN_CAPABILITIES, _ipad(booleans,False) ) :
      self.__dict__.update( (k,value) for k in spec.split( ':' ) )

    for spec,value in zip( NUMERIC_CAPABILITIES, _ipad(numerics,-1) ) :
      if value > 0 :
        value = None
      self.__dict__.update( (k,value) for k in spec.split( ':' ) )

    for spec,idx in zip( STRING_CAPABILITIES, _ipad(strings,-1) ) :

      *spec,aritytag = spec.split( ':' )

      value = None
      if idx is not None and idx >= 0 :
        off = tab.find( b'\0', idx )
        if off < 0 :
          off = None
        value = tab[idx:off]

      if aritytag != '' :

        arity = None
        if aritytag != '*' :
          arity = int(aritytag)

        value = function_from_capability( 
                    spec[0]
                  , value
                  , declared_arity = arity
                  , index          = idx
                  , variables      = self.variables
                  , encoding       = encoding
                  , binary         = binary
                  )

      elif not binary and value is not None :
        value = _decode_latin1( value )

      self.__dict__.update( (k,value) for k in spec )


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

    info = TermInfo( term, binary, encoding )

    _cache[ (term,binary,encoding) ] = info
    _cache[ key ] = info

  return info


