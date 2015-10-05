from . constants import *
from . compile import *
from . utils import *

from itertools import count

import os

__all__ = [
    'make_terminfo_from_path'
  ]

##################################################
#                                                #
##################################################
@singleton
def EMPTY_ATTRIBUTES() :
  result = {}
  for k,v in CAPABILITY_VARNAMES.items() :
    result[k] = None
    result[v] = None
  return result

##################################################
#                                                #
##################################################
class TermInfo( object ) :
  pass

##################################################
#                                                #
##################################################
def _decode_string( b ) :
  return b.decode( 'latin1' )

##################################################
#                                                #
##################################################
class CapGroup( object ) :

  def __init__( self ) :
    self.vals_std = None
    self.caps_ext = None
    self.vals_ext = None

  def iter( self, caps_std ) :

    for cap,val,idx in zip( caps_std, iextend(self.vals_std,-1), count() ) :
      yield cap, val, idx

    if self.caps_ext is not None :

      for cap,val in zip( self.caps_ext, iextend(self.vals_ext,-1) ) :
        yield _decode_string(cap), val, None


##
class RawTermInfo( object ) :

  def __init__( self, path ) :

    self.path     = path
    self.names    = None
    self.booleans = CapGroup()
    self.numerics = CapGroup()
    self.strings  = CapGroup()

    with open( path, 'rb' ) as f :

      def read( n ) :
        return f.read( n )

      def read_i16s( n ) :
        return memoryview(f.read( n*2 )).cast( 'h' )

      def read_bools( n ) :
        return memoryview(f.read( n )).cast( '?' )

      def lookup( tab, indices, off=0 ) :

        def impl( idx ) :
          idx += off
          if not (0 <= idx < len(tab)) :
            return -1
          end = tab.find( b'\0', idx )
          if end < 0 :
            end = None
          return tab[ idx:end ]

        return tuple_map( impl, indices )

      magic, = read_i16s(1)
      if magic != 0x011A : 
        raise Exception(
                  str.format(
                      '"{}" is not a valid compiled terminfo file'
                    , path
                    )
                )

      names_length           , \
      booleans_count         , \
      numerics_count         , \
      strings_count          , \
      table_length           = read_i16s(5)

      self.names             = read( names_length-1 ).split( b'|' )
      _                      = read( 1 )
      self.booleans.vals_std = read_bools(  booleans_count )
      _                      = read( f.tell()&1 )
      self.numerics.vals_std = read_i16s(  numerics_count )
      string_indices         = read_i16s( strings_count )
      tab                    = read( table_length )
      self.strings.vals_std  = lookup( tab, string_indices )
      
      if f.tell() < os.stat( f.fileno() ).st_size  :

        read( f.tell() & 1 )

        booleans_count         , \
        numerics_count         , \
        strings_count          , \
        _                      , \
        table_length           = read_i16s(5)

        self.booleans.vals_ext = read_bools( booleans_count )
        _                      = read( f.tell() & 1 )
        self.numerics.vals_ext = read_i16s( numerics_count )
        string_indices         = read_i16s( strings_count )
        boolean_caps           = read_i16s( booleans_count )
        numeric_caps           = read_i16s( numerics_count )
        string_caps            = read_i16s( strings_count )
        tab                    = read( table_length )
        self.strings.vals_ext  = lookup( tab, string_indices )

        idx = 0
        if string_indices :
          idx = max( string_indices ) + 1
          if idx :
            idx = tab.find( b'\0', idx ) + 1
            if not idx :
              return

        self.booleans.caps_ext  = lookup( tab, boolean_caps, off=idx )
        self.numerics.caps_ext  = lookup( tab, numeric_caps, off=idx )
        self.strings.caps_ext   = lookup( tab, string_caps, off=idx )


##################################################
#                                                #
##################################################
def make_terminfo_from_raw( raw, binary, encoding ) :

  def parser_b( cap, val, idx ) :
    if val is not None : return bool(val)

  def parser_n( cap, val, idx ) :
    return val

  def parser_s( cap, val, idx ) :

    if cap in CAPABILITY_ARITY :
      return function_from_capability( 
                  CAPABILITY_VARNAMES.get( cap, cap )
                , val
                , index          = idx
                , declared_arity = CAPABILITY_ARITY[ cap ]
                , variables      = variables
                , encoding       = encoding
                , binary         = binary
                )

    if val is None :
      val = b''

    if not binary :
      val = _decode_string( val )

    return val


  ##
  attribs   = EMPTY_ATTRIBUTES.copy()
  present   = set()
  extended  = set()
  variables = [0] * 52

  groups    = ( BOOLEAN_CAPABILITIES, raw.booleans, parser_b )  \
            , ( NUMERIC_CAPABILITIES, raw.numerics, parser_n )  \
            , ( STRING_CAPABILITIES, raw.strings, parser_s )

  for caps_std, group, parser in groups :
    for cap,val,idx in group.iter( caps_std ) :

      keys = { cap, CAPABILITY_VARNAMES.get( cap, cap ) }

      if val in (-1,-2) :
        val = None

      new = parser( cap, val, idx )
      for k in keys :
        attribs[k] = new

      if val is not None :
        present.update( keys )
        if idx is None :
          extended.update( keys )

  
  info           = TermInfo()

  info.names     = tuple_map( _decode_string, raw.names )
  info.attribs   = FrozenDict( attribs )
  info.present   = frozenset( present )
  info.extended  = frozenset( extended )
  info.variables = variables
  info.path      = raw.path
  info.binary    = binary
  info.encoding  = encoding

  info.__dict__.update( attribs )

  return info

def make_terminfo_from_path( path, binary, encoding ) :
  return make_terminfo_from_raw( RawTermInfo(path), binary, encoding )


