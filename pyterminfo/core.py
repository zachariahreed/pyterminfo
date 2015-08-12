from . constants import *
from . compile import *
from . utils import *

import itertools
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
class TermInfo( object ) :

  def __init__( self, path, binary, encoding, names, attribs, present, variables ) :
    
    self.path      = path
    self.binary    = binary
    self.encoding  = encoding
    self.names     = names
    self.attribs   = attribs
    self.present   = present
    self.variables = variables

    self.__dict__.update( attribs )


##################################################
#                                                #
##################################################
def _decode_latin1( b ) :
  return b.decode( 'latin1' )

def _parse_bcap( keys, value ) :
  present = True
  if value < 0 :
    present = False
    value = False
  return keys, value, present
  
def _parse_ncap( keys, value ) :
  present = True
  if value < 0 :
    present = False
    value = None
  return keys, value, present

def _parse_scap( keys, idx, binary, encoding, tab, variables ) :

  *keys,aritytag = keys

  value = None
  if idx is not None and idx >= 0 :
    off = tab.find( b'\0', idx )
    if off < 0 :
      off = None
    value = tab[idx:off]

  present = (value is not None)

  if aritytag != '' :

    arity = None
    if aritytag != '*' :
      arity = int(aritytag)

    value = function_from_capability( 
                keys[0]
              , value
              , declared_arity = arity
              , index          = idx
              , variables      = variables
              , encoding       = encoding
              , binary         = binary
              )
  
  else :

    if value is None :
      value = b''

    if not binary :
      value = _decode_latin1( value )

  return keys, value, present

def _make_terminfo_from_entry( 
          path
        , binary
        , encoding
        , tab
        , names
        , booleans
        , numerics
        , strings 
        ) :

  attribs   = {}
  presence  = set()

  variables = [0] * 52
  strings_context = {
      'binary'    : binary
    , 'encoding'  : encoding
    , 'variables' : variables
    , 'tab'       : tab
    }

  grouped = (BOOLEAN_CAPABILITIES,booleans,_parse_bcap,{})            \
          , (NUMERIC_CAPABILITIES,numerics,_parse_ncap,{})            \
          , (STRING_CAPABILITIES,strings,_parse_scap,strings_context)

  for specs,values,fn,kwargs in grouped :

    values = itertools.chain( values, itertools.repeat(-1) )

    for spec,value in zip( specs, values ) :
      keys,value,present = fn( spec.split( ':' ), value, **kwargs )
      attribs.update( (k,value) for k in keys )
      if present :
        presence.update( keys )

  return TermInfo(
            path
          , binary
          , encoding
          , tuple_map( _decode_latin1, names )
          , FrozenDict( attribs )
          , frozenset( presence )
          , variables
          )

##################################################
#                                                #
##################################################
def _read_terminfo_entry( path ) :

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

  return tab, names, booleans, numerics, strings


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

      entry = _read_terminfo_entry( path )

    info = _make_terminfo_from_entry( path, binary, encoding, *entry )

    _cache[ (term,binary,encoding) ] = info
    _cache[ key ] = info

  return info



