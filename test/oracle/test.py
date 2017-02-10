import argparse
import collections
import ctypes
import functools
import os
import pyterminfo
import sys

from pyterminfo.constants import *
from pyterminfo.utils import *

##################################################
#                                                #
##################################################
def die_die_die( msg ) :
  print( msg )
  sys.exit( 1 )

##################################################
#                                                #
##################################################
@singleton
class NotSet( object ) :
  def __repr__( self ) :
    return '#UNEVALUATED#'

@singleton
class HardCopy( object ) :
  def __repr__( self ) :
    return 'HardCopy'

##################################################
#                                                #
##################################################
def identity( u ) :
  return u

##################################################
#                                                #
##################################################
def encode( u ) :
  return u.encode( 'latin1' )

def maybe_encode( u ) :
  if u is None :
    return b''
  if isinstance(u,str) :
    u = u.encode( 'latin1' )
  return u

def decode( u ) :
  return u.decode( 'latin1' )

def maybe_decode( u ) :
  if u is None :
    return ''
  if isinstance(u,bytes) :
    u = u.decode( 'latin1' )
  return u

##################################################
#                                                #
##################################################
class NCurses( object ) :

  def __init__( self, lib ) :
    self._lib = lib

  def tigetflag( self, s ) :
    return self._lib.tigetflag( encode( s ) )

  def tigetnum( self, s ) :
    return self._lib.tigetnum( encode( s ) )

  def tigetstr( self, s ) :
    result = self._lib.tigetstr( encode( s ) )
    if result > 0 :
      return ctypes.string_at( result )

  def tparm( self, *args ) :

    cargs = []
    for a in args :
      if isinstance(a,str) :
        a = ctypes.c_char_p( encode( a ) )
      elif isinstance(a,bytes) :
        a = ctypes.c_char_p( a )
      elif isinstance(a,int) :
        a = ctypes.c_int(a)
      else :
        raise Exception( f'bad argument: {a!r}' )
      cargs.append(a)

    return self._lib.tparm( *cargs )

##
def ncurses( term ) :

  # load library and setup function signatures
  lib = ctypes.CDLL( '/usr/lib/libncursesw.so.6' )
  lib.use_env.argtypes   = [ ctypes.c_bool ]
  lib.setupterm.argtypes = [ ctypes.c_char_p ]
  lib.tigetstr.argtypes  = [ ctypes.c_char_p ]
  lib.tparm.restype      = ctypes.c_char_p
  lib.tigetflag.argtypes = [ ctypes.c_char_p ]
  lib.tigetflag.restype  = ctypes.c_int32
  lib.tigetnum.argtypes  = [ ctypes.c_char_p ]
  lib.tigetnum.restype   = ctypes.c_int32

  # initialize
  lib.use_env(False)
  err = ctypes.c_int()
  if lib.setupterm( encode( term ), 1, ctypes.byref(err) ) == -1 :

    # hardcopy terminal
    if err.value == 1 :
      return HardCopy

    if err.value == 0 :
      msg = f'ncurses initialization failed: "{term}" not found or invalid'
    elif err.value == -1 :
      msg = 'ncurses initialization failed: terminfo db not found' 
    else :
      msg = 'ncurses initialization failed'

    die_die_die( msg )

  # wrapper
  return NCurses( lib )


##################################################
#                                                #
##################################################
class TestValue( object ) :

  def __init__( self ) :
    self.expected = NotSet
    self.actual   = NotSet

  def test( self, cast=identity ) :
    expected = cast(self.expected)
    actual   = cast(self.actual)
    if expected != actual :
      raise AssertionError( f'expected {expected!r}, actual {actual!r}' )


##
class TestValues( object ) :

  def __getattr__( self, key ) :
    val = TestValue()
    setattr( self, key, val )
    return val


##
class TestResult( object ) :

  def __init__( self, test ) :
    self.test   = test
    self.error  = None
    self.values = TestValues()

  def maybe_show( self, detailed ) :

    status = None
    if self.error is not None :
      status = self.error
    elif detailed :
      status = 'OK'

    if status is not None :

      key    = self.test.key
      idx    = self.test.idx
      cap    = self.test.cap
      name   = self.test.name
      values = self.values.__dict__

      items = []
      for k,v in values.items() :
        if not isinstance(v,TestValue) :
          items.append((k,v))
        else :
          items.append((f'{k}:expected',repr(v.expected)))
          items.append((f'{k}:actual',repr(v.actual)))
      width = max( len(k) for (k,v) in items )

      print()
      print( f'  {name} {cap} ({key}{idx}) : {status}' )
      for k,v in items :
        print( f'    {k:>{width}} :: {v}' )

      return True


##################################################
#                                                #
##################################################
class Test( object ) :

  def __init__( self, idx, cap ) :
    self.idx  = idx
    self.cap  = cap
    self.name = CAPABILITY_VARNAMES.get( cap, cap )


class BoolTest( Test ) :

  key = 'B'

  def __call__( self, ct, pt, binary, values ) :
    values.val.expected = ct.tigetflag( self.cap )
    values.val.actual   = pt.attribs[ self.cap ]
    values.val.test(bool)


class NumericTest( Test ) :

  key = 'N'

  def __call__( self, ct, pt, binary, values ) :

    expected = ct.tigetnum( self.cap )
    if expected == -1 :
      expected = None

    values.val.expected = expected
    values.val.actual   = pt.attribs[ self.cap ]
    values.val.test()


class StringTest( Test ) :

  key = 'S'

  def __call__( self, ct, pt, binary, values ) :

    values.val.expected = ct.tigetstr( self.cap )
    if values.val.expected is None :
      values.val.expected = b''
    if not binary :
      values.val.expected = decode( values.val.expected )

    values.val.actual = pt.attribs[ self.cap ]

    values.val.test()


class ParameterizedTest( Test ) :

  key = 'P'

  def __call__( self, ct, pt, binary, values ) :

    gen = getattr(pt,self.cap)

    values.fmt.expected = ct.tigetstr( self.cap )
    if values.fmt.expected is None :
      values.fmt.expected = b''

    values.fmt.actual = gen
    if hasattr( gen, '__call__' ) :
      values.fmt.actual = gen.raw

    values.fmt.test()
    if not values.fmt.expected :
      return

    values.fmt = values.fmt.expected

    for args in getattr( self, f'_ARGS__{self.name}', self._ARGS )( gen ) :

      values.arity = len(args)
      values.args = args
      values.val.expected = ct.tparm( values.fmt, *args )
      values.val.actual = gen(*args)
      if not binary :
        values.val.actual = maybe_encode( values.val.actual )

      values.val.test()


  ##
  def _ARGS( self, gen ) :

    arity = 6
    if gen.arity is not None :
      arity = gen.arity

    args = list(range(arity+1))
    yield args[:-1]
    yield args[1:]

  def _ARGS__pkey_xmit( self, gen ) :
    yield 10, 'test01232456789'

  def _ARGS__pkey_local( self, gen ) :
    yield 10,'XXXXX'

  def _ARGS__pkey_key( self, gen ) :
    yield 10, 'QQQQQQQ'

  def _ARGS__pkey_plab( self, gen ) :
    yield 10, 'YYYYYYY', 'ZZZZZZZ'

  def _ARGS__plab_norm( self, gen ) :
    yield 10, 'test213'


##################################################
#                                                #
##################################################
def string_set( raw ) :
  items = set()
  for e in raw.split( ',' ) :
    e = e.strip()
    if e :
      items.add( e )
  return items


##
class Filter( object ) :

  def __init__( self, *, skip=None, only=None, key=None ) :
    self._skip = skip
    self._only = only

  def __call__( self, key ) :

    key = self._key( key )

    if self._skip is not None :
      if key in self._skip :
        return False
    if self._only is not None :
      if key not in self._only :
        return False
    return True


class NameFilter( Filter ) :

  def _key( self, test ) :
    return test.name


class CapFilter( Filter ) :

  def _key( self, test ) :
    return test.cap


##################################################
#                                                #
##################################################
class Output( object ) :

  def __init__( self, verbosity=0 ) :
    self._output    = False
    self._verbosity = verbosity

  def show( self, result ) :
    if result.maybe_show( self._verbosity>0 ) :
      self._output = True

  def show_summary( self, term, cnt, err ) :
    if err or self._verbosity > 0 :
      print()
    if err or self._verbosity >= 0 :
      print( f'{term} : {cnt} capabilties tested, {err} failure(s)' )


##################################################
#                                                #
##################################################
def main( out, term, binary, pred ) :

  # setup
  os.environ[ 'TERM' ] = term

  ct = ncurses( term )
  if ct is HardCopy :
    return

  pt = pyterminfo.terminfo( term, binary )

  # generate tests
  user_defined = { f'u{i}' for i in range(10) }

  pending = []
  for idx,cap in enumerate(BOOLEAN_CAPABILITIES) :
    pending.append(BoolTest(idx,cap))

  for idx,cap in enumerate(NUMERIC_CAPABILITIES) :
    pending.append(NumericTest(idx,cap))

  for idx,cap in enumerate(STRING_CAPABILITIES) :
    if cap not in CAPABILITY_ARITY or cap in user_defined :
      pending.append(StringTest(idx, cap))

  for cap in pt.extended :
    if '_' not in cap and cap not in ('AX','XT','G0','U8') :
      pending.append(StringTest(None, cap))

  for idx,cap in enumerate(STRING_CAPABILITIES) :
    if cap in CAPABILITY_ARITY and cap not in user_defined :
      pending.append(ParameterizedTest(idx, cap))


  # run
  cnt = 0
  err = 0
  for test in pending :

    if pred(test) :

      cnt += 1

      result = TestResult( test )
      try :
        test( ct, pt, binary, result.values )
      except Exception as ex :
        err += 1
        result.error = ex

      out.show( result )

  # done
  out.show_summary( term, cnt, err )

  return (not err)


##################################################
#                                                #
##################################################
parser = argparse.ArgumentParser()
parser.add_argument( 'term' )
parser.add_argument( '--bytes', action='store_true', dest='binary' )
parser.add_argument( '--str', action='store_false', dest='binary' )
parser.add_argument( '-v', action='count', dest='verbosity', default=0 )
parser.add_argument( '-q', action='count', dest='quietness', default=0 )
parser.add_argument( '--skip', type=string_set )
parser.add_argument( '--only', type=string_set )
parser.add_argument( '--filter-caps', action='store_true', default=False )
parser.add_argument( '--skip-entry', type=string_set, default=() )
parser.add_argument( '--visualize' )
args = parser.parse_args() 

if args.term != 'unknown' and args.term not in args.skip_entry :

  if args.visualize :

    import pyterminfo.visualization 
    pyterminfo.visualization.set_visualization_path( args.visualize, 'TERMINFO-{}.png' )

    import byteasm.visualization 
    byteasm.visualization.set_visualization_path( args.visualize, 'BYTECODE-{}.png' )


  out = Output( args.verbosity - args.quietness )

  ctor = NameFilter
  if args.filter_caps :
    ctor = CapFilter
  pred = ctor( skip=args.skip, only=args.only )

  if not main( term=args.term, binary=args.binary, pred=pred, out=out ) :
    sys.exit(1)

