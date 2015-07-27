from . ast import *
from . ops import *
from . utils import *

__all__ = [
    'parse'
  ]

##################################################
#                                                #
##################################################
class ParseError( Exception ) :
  pass


##################################################
#                                                #
##################################################
DIGITS  = b'0123456789'
LOWER   = b'abcdefghijklmnopqrstuvwxyz'
UPPER   = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

##################################################
#                                                #
##################################################
class FormatSpec( object ) :

  def __init__( self, flags, width, precision, conversion ) :
    self.flags      = flags
    self.width      = width
    self.precision  = precision
    self.conversion = conversion

  def __str__( self ) :

    parts = ['%']
    if self.flags is not None :
      parts.append( self.flags )
    if self.width is not None :
      parts.append( str(self.width) )
    if self.precision is not None :
      parts.append( '.' + str(self.precision) )
    parts.append( self.conversion ) 

    return ''.join(parts)

  def __bytes__( self ) :
    return str(self).encode( 'latin1' )


##
class CharacterConstant( int ) :

  def __repr__( self ) :
    return repr( chr(self) )


##################################################
#                                                #
##################################################
def _decode_latin1( b ) :
  return b.decode( 'latin1' )

##################################################
#                                                #
##################################################
def _make_add() :
  return Add()

def _make_bitwise_and() :
  return BitwiseAnd()

def _make_bitwise_not() :
  assert BitwiseNot()

def _make_bitwise_or() :
  return BitwiseOr()

def _make_bitwise_xor() :
  return BitwiseXor()

def _make_block( items ) :
  return items

def _make_character( what ) :
  return Const(CharacterConstant(ord(what)))

def _make_compare_eq() :
  return CompareEQ()

def _make_compare_gt() :
  return CompareGT()

def _make_compare_lt() :
  return CompareLT()

def _make_conditional( *args ) :
  return Conditional( *args )

def _make_div() :
  return Div()

def _make_get( name ) :
  return Get( _decode_latin1(name) )

def _make_inc() :
  return Inc()

def _make_integer( what ) :
  return Const(what)

def _make_length() :
  return Length()

def _make_logical_and() :
  return BitwiseAnd()

def _make_logical_not() :
  return Not()

def _make_logical_or() :
  return BitwiseOr()

def _make_mod() :
  return Mod()

def _make_mul() :
  return Mul()

def _make_output_char() :
  return Write(ToChar())

def _make_output_formatted( flags, width, precision, conversion ) :

  conversion = _decode_latin1( conversion )
  if flags is not None :
    flags = _decode_latin1(flags)
  spec = FormatSpec( flags, width, precision, conversion )

  inner = None
  if spec.conversion == 's' :
    inner = EnsureStringLike()

  if str(spec) != '%s' :
    inner = Format( spec, inner )

  return Write( inner )

def _make_push( idx ) :
  return Push( Arg(idx) )

def _make_put( name ) :
  return Put( _decode_latin1(name) )

def _make_sub() :
  return Sub()

def _make_write( what ) :
  return Write(Const(what))


##################################################
#                                                #
##################################################
class Buffer( object ) :

  def __init__( self, data, idx=0 ) :
    self._data = data
    self._idx = 0
    self._end = len(data)

  def __bool__( self ) :
    return self._idx < self._end

  def __len__( self ) :
    return self._end - self._idx

  def __repr__( self ) :
    n = self._end - self._idx
    if n < 50 :
      return repr( self._data[self._idx:] )
    return repr( self._data[self._idx:self._idx+47] + b'...' )

  def match_until( self, what ) :
    idx = self._data.find( what, self._idx )
    if idx < 0 :
      idx = self._end
    result = self._data[self._idx:idx]
    self._idx = idx
    return result

  def optional( self, what ) :
    if self._data.startswith( what, self._idx ) :
      self._idx += len(what)
      return what

  def match( self, what ) :
    if self.optional( what ) is None :
      self.raise_error( '{!r}', what )

  def peek_at( self, idx ) :
    idx += self._idx
    if idx < self._end :
      return self._data[idx:idx+1]

  def advance( self, n=1 ) :
    self._idx += n

  def choose( self, chars, min=1, max=1 ) :

    idx = self._idx

    end = idx + max
    if end > self._end :
      end = self._end

    while idx < end and self._data[idx] in chars :
      idx += 1

    n = idx - self._idx

    if n < min or n > max :
      self.raise_error( 
          'between {} and {} char(s) from the set {!r}'
        , min
        , max
        , chars  
        )

    result = self._data[self._idx:idx]
    self._idx = idx

    if result :
      return result

  def anychar( self ) :
    if self._idx >= self._end :
      raise 

    result = self._data[self._idx:self._idx+1]
    self._idx += 1
    return result

  def _make_integer( self, max=99 ) :
    return int( self.choose( DIGITS, max=max ) )

  def optional_integer( self, max=99 ) :
    text = self.choose( DIGITS, min=0, max=max )
    if text :
      return int(text)

  def end( self ) :
    if self._idx < self._end :
      self.raise_error( 'end of input' )

  def raise_error( self, fmt, *args ) :
    
    # FIXME - this can report bad positions sometimes.
    #         hopefully everything in the terminfo db
    #         is well formed though.

    head = self._data[self._idx:]
    if not head :
      head = 'EOS'
    else :
      head = repr(head)
      if len(head) > 50 :
        head = head[:47] + '...'

    raise ParseError(
              str.format(
                  'at position {}, found {} but was expecting ' + fmt
                , self._idx
                , head
                , *args  
                )
            )


##################################################
#                                                #
##################################################
def _match_block( buf ) :

  out = []
  cnt = 0
  choices = _match_op, _match_bare

  while cnt < 2 :

    choices = choices[::-1]

    item = choices[0]( buf )
    if item is None :
      cnt += 1
      continue

    cnt = 0
    out.append(item)

  return _make_block( tuple(out) )

def _match_bare( buf ) :
  out = bytearray()
  out.extend( buf.match_until( b'%' ) )
  while buf.optional( b'%%' ) :
    out.extend( b'%' )
    out.extend( buf.match_until( b'%' ) )
  if out :
    return _make_write( bytes(out) )

def _match_op( buf ) :
  match = _optab.get( buf.peek_at(1) )
  if match is not None :
    return match( buf )

def _match_integer_literal( buf ) :
  buf.advance(2)
  out = int(buf.match_until( b'}' ))
  buf.advance()
  return _make_integer( out )

def _match_char_literal( buf ) :
  buf.advance(2)
  out = buf.match_until( b"'" )
  buf.advance()
  return _make_character( out )

def _match_format( buf ) :

  buf.advance()
  buf.optional( b':' )
  
  flags     = buf.choose( b' +#-0', min=0, max=99 )
  width     = buf.optional_integer()
  precision = buf.optional( b'.' ) and buf.optional_integer()
  spec      = buf.choose( b'doxXs' )

  return _make_output_formatted( flags, width, precision, spec )

def _match_conditional( buf ) :

  buf.advance(2)
  out = [_match_block( buf )]
  expected = b'%t', b'%e'
  while buf and not buf.optional( b'%;' ) :
    buf.match( expected[0] )
    out.append( _match_block(buf) )
    expected = expected[::-1]

  last = None
  if len(out)%2 :
    last = out.pop()

  return _make_conditional( tuple(zip(out[::2],out[1::2])), last )

def _match_push( buf ) :
  buf.advance(2)
  return _make_push( buf.choose( DIGITS )[0] - ord('0') )

def _match_put( buf ) :
  buf.advance(2)
  return _make_put( buf.choose(LOWER+UPPER) )

def _match_get( buf ) :
  buf.advance(2)
  return _make_get( buf.choose(LOWER+UPPER) )

def _match_simple( ctor ) :
  def _match_xxx( buf ) :
    buf.advance(2)
    return ctor()
  return _match_xxx


##
_optab = {
      b' ' : _match_format                        , b'!' : _match_simple( _make_logical_not )
    , b'#' : _match_format                        , b'&' : _match_simple( _make_bitwise_and )
    , b"'" : _match_char_literal                  , b'*' : _match_simple( _make_mul )
    , b'+' : _match_simple( _make_add )           , b'-' : _match_simple( _make_sub )
    , b'.' : _match_format                        , b'/' : _match_simple( _make_div )
    , b'0' : _match_format                        , b'1' : _match_format
    , b'2' : _match_format                        , b'3' : _match_format
    , b'4' : _match_format                        , b'5' : _match_format
    , b'6' : _match_format                        , b'7' : _match_format
    , b'8' : _match_format                        , b'9' : _match_format
    , b':' : _match_format                        , b'<' : _match_simple( _make_compare_lt )
    , b'=' : _match_simple( _make_compare_eq )    , b'>' : _match_simple( _make_compare_gt )
    , b'?' : _match_conditional                   , b'A' : _match_simple( _make_logical_and )
    , b'g' : _match_get                           , b'O' : _match_simple( _make_logical_or )
    , b'P' : _match_put                           , b'X' : _match_format
    , b'^' : _match_simple( _make_bitwise_xor )   , b'c' : _match_simple( _make_output_char )
    , b'd' : _match_format                        , b'i' : _match_simple( _make_inc )
    , b'l' : _match_simple( _make_length )        , b'm' : _match_simple( _make_mod )
    , b'o' : _match_format                        , b'p' : _match_push
    , b's' : _match_format                        , b'x' : _match_format
    , b'{' : _match_integer_literal               , b'|' : _match_simple( _make_bitwise_or )
    , b'~' : _match_simple( _make_bitwise_not )
  }


##################################################
#                                                #
##################################################
def parse( text ) :
  buf = Buffer(text)
  result = _match_block( buf )
  buf.end()
  return result





