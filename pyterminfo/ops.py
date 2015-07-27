from . constants import *
from . utils import *

import functools

__all__ = [

    'Arg'

  , 'Add'        , 'BitwiseAnd' , 'BitwiseNot'
  , 'BitwiseOr'  , 'BitwiseXor' , 'CompareEQ'
  , 'CompareGT'  , 'CompareLT'  , 'Const'
  , 'Discard'    , 'Div'        , 'EnsureStringLike'
  , 'Epilogue'   , 'Format'     , 'Get'
  , 'Inc'        , 'Length'     , 'Mod'
  , 'Mul'        , 'NoneP'      , 'Not'
  , 'Prologue'   , 'Push'       , 'Put'
  , 'StackInput' , 'Sub'        , 'TableLookup'
  , 'ToChar'     , 'Write'
  ]


##################################################
#                                                #
##################################################
class Arg( int ) :
  
  def __repr__( self ) :
    return str.format( 'Arg({})', int(self) )

  def __str__( self ) :
    return 'a' + super().__str__()


##################################################
#                                                #
##################################################
class Unparameterized( object ) :

  parameterized = False

  def __init__( self, *args, **kwargs ) :

    super().__init__( *args, **kwargs )

    self.args = self.subexprs

  def make_like( self, *args, **kwargs ) :
    return self.__class__( *args, **kwargs )


class Parameterized( object ) :

  parameterized = True

  def __init__( self, param, *args, **kwargs ) :

    super().__init__( *args, **kwargs )

    if self.load is None :
      self.load = frozenset((param,))

    if self.store is None :
      self.store = frozenset((param,))

    self.args = (param,) + self.subexprs
    self.param = param

  def make_like( self, *args, **kwargs ) :
    return self.__class__( self.param, *args, **kwargs )


##
class Op( object ) :

  bound         = True
  increment     = 0
  load          = frozenset()
  nil           = False
  output        = 0
  parameterized = False
  producer      = True
  store         = frozenset()

  def __repr__( self ) :
    return self.format()

  def __eq__ ( self, other ) :
    return self.__class__ is other.__class__ \
       and self.args == other.args

  def __ne__( self, other ) :
    return not (self==other)

  def format( self ) :
    return self._format()[1]

  def _format( self, pos=0 ) :
    parts = []
    for a in self.subexprs[::-1] :
      pos,val = a._format( pos )
      parts.append(val)
    if self.parameterized :
      parts.append( str(self.param) )
    parts.append( self.__class__.__name__ )
    return pos,'(' + ' '.join(parts[::-1]) + ')'

  def bind( self, value ) :
    assert not self.bound
    return self._bind( value, *self.subexprs )

  def rewrite( self, fn ) :
    return fn( self ) \
         or self._rewrite( fn, *self.subexprs )
   

##
class ZeroArityBase( Op ) :

  arity   = 0
  require = 0
  stack   = 0
  subexprs = ()

  def _format( self, pos=None ) :

    if pos is not None and self.stack == 1 :
      return pos, str(self.param)

    return super()._format( pos )

  def _rewrite( self, fn ) :
    return self


##
class OneArityBase( Op ) :

  arity   = 1
  require = 1
  stack   = 0

  def __init__( self, e0=None ) :

    if e0 is None :
      e0 = StackInput

    require = max( e0.require, self.require-e0.stack )
    if require != self.require :
      self.require = require

    stack = e0.stack + self.stack
    if stack != self.stack :
      self.stack = stack

    if not e0.bound :
      self.bound = False

    assert not e0.store
    if e0.load :
      self.load = self.load|e0.load

    self.subexprs = e0,

  def _bind( self, value, e0 ) :
    return self.make_like( e0.bind( value ) )

  def _rewrite( self, fn, e0 ) :

    r0 = e0.rewrite( fn )
    if r0 is not e0 :
      return self.make_like( r0 )

    return self


##
class TwoArityBase( Op ) :

  arity       = 2
  commutative = False
  require     = 2
  stack       = -1

  def __init__( self, e0=None, e1=None ) :

    if e0 is None :
      e0 = StackInput
    s0 = e0.stack

    if e1 is None :
      e1 = StackInput
    s1 = e1.stack

    require = max( e0.require, e1.require-s0, self.require-s1-s0 )
    if require != self.require :
      self.require = require

    stack = self.stack + s1 + s0
    if stack != self.stack :
      self.stack = stack

    if not (e0.bound and e1.bound) :
      self.bound = False

    assert not e0.store
    assert not e1.store
    if e0.load or e1.load :
      self.load = self.load|e0.load|e1.load

    self.subexprs = e0,e1

  def _bind( self, value, e0, e1 ) :
    if not e1.bound :
      return self.make_like( e0, e1.bind(value) )
    return self.make_like( e0.bind(value), e1 )

  def _rewrite( self, fn, e0, e1 ) :

    r0 = e0.rewrite( fn )
    r1 = e1.rewrite( fn )

    if (r0 is not e0) or (r1 is not e1) :
      return self.make_like( r0, r1 )

    return self


##
def make_op( arity, parameterized=False, load=False, store=False, **kwargs ) :

  def impl( fn ) :

    abase = (ZeroArityBase,OneArityBase,TwoArityBase)[arity]
    pbase = Unparameterized
    if parameterized :
      pbase = Parameterized

    derived = type( fn.__name__, (pbase,abase), kwargs )

    derived.raw_stack   = derived.stack
    derived.serialize   = (lambda self, ctx : fn( ctx, *self.args ))

    if load is True :
      derived.load = None
    elif load is not False :
      derived.load = frozenset( Arg(int(e)) for e in load )

    if store is True :
      derived.store = None
    elif store is not False :
      derived.store = frozenset( Arg(int(e)) for e in store )

    if not (derived.require + derived.stack) :
      derived.producer = False
    
    return derived

  return impl


##################################################
#                                                #
##################################################
@make_op( 2 )
def Add( ctx, *args ) :
  ctx.emit_std_prefix2( *args, commutative=True )
  ctx.emit_binary_add()

@make_op( 2 )
def BitwiseAnd( ctx, *args  ) :
  ctx.emit_std_prefix2( *args, commutative=True )
  ctx.emit_binary_and()

@make_op( 1 )
def BitwiseNot( ctx, *args ) :
  ctx.emit_std_prefix1( *args )
  ctx.emit_unary_invert()

@make_op( 2 )
def BitwiseOr( ctx, *args  ) :
  ctx.emit_std_prefix2( *args, commutative=True )
  ctx.emit_binary_or()

@make_op( 2 )
def BitwiseXor( ctx, *args  ) :
  ctx.emit_std_prefix2( *args, commutative=True )
  ctx.emit_binary_xor()

@make_op( 2 )
def CompareEQ( ctx, *args  ) :
  ctx.emit_std_prefix2( *args, commutative=True )
  ctx.emit_compare_eq()

@make_op( 2, )
def CompareGT( ctx, *args ) :
  ctx.emit_compare_le()                                \
    if ctx.emit_std_prefix2( *args, commutative=True ) \
    else ctx.emit_compare_gt()

@make_op( 2, )
def CompareLT( ctx, *args ) :
  ctx.emit_compare_ge()                                \
    if ctx.emit_std_prefix2( *args, commutative=True ) \
    else ctx.emit_compare_lt()

@make_op( 0, parameterized=True, stack=1 )
def Const( ctx, param ) :
  if isinstance(param,bytes) :
    param = ctx.coerce_bytes(param)
  ctx.emit_load_const( param )

@make_op( 1, stack=-1 )
def Discard( ctx, x0 ) :

  n = 1
  if x0 is not None :
    n -= x0.stack

  for i in range( n ) :
    ctx.emit_pop_top()

@make_op( 2 )
def Div( ctx, *args ) :
  ctx.emit_std_prefix2( *args )
  ctx.emit_binary_floor_divide()

@make_op( 0, parameterized=True )
def Epilogue( ctx, *args ) :
  ctx.emit_epilogue( *args )

@make_op( 1 )
def EnsureStringLike( ctx, *args ) :
  ctx.emit_call1( ctx.fn_ensure_stringlike, *args )

@make_op( 1, parameterized=True )
def Format( ctx, *args ) :
  ctx.emit_format( *args )

@make_op( 0, parameterized=True, stack=1, load=True )
def Get( ctx, param ) :
  ctx.emit_load_deref( 'vars' )
  ctx.emit_load_const( VARIABLE_SLOTS[param] )
  ctx.emit_binary_subscr()

@make_op( 0, load=(1,2), store=(1,2), increment=1 )
def Inc( ctx ) :
  raise AssertionError( 'not serializable' )

@make_op( 1 )
def Length( ctx, *args ) :
  ctx.emit_call1( ctx.fn_stringlike_length, *args )

@make_op( 2, )
def Mod( ctx, *args ) :
  ctx.emit_std_prefix2( *args )
  ctx.emit_binary_modulo()

@make_op( 2 )
def Mul( ctx, *args ) :
  ctx.emit_std_prefix2( *args, commutative=True )
  ctx.emit_binary_multiply()

@make_op( 1 )
def Not( ctx, *args ) :
  ctx.emit_std_prefix1( *args )
  ctx.emit_unary_not()

@make_op( 0, require=1, stack=1 )
def NoneP( ctx ) :
  ctx.emit_dup_top()
  ctx.emit_load_const( None )
  ctx.emit_compare_is()

@make_op( 0 )
def Prologue( ctx ) :
  ctx.emit_prologue()

@make_op( 0, parameterized=True, stack=1, load=True )
def Push( ctx, param ) :
  ctx.emit_load_fast( str(param) )

@make_op( 1, parameterized=True, stack=-1, store=True )
def Put( ctx, param, x0 ) :
  ctx.emit_std_prefix1( x0 )
  ctx.emit_load_deref( 'vars' )
  ctx.emit_load_const( VARIABLE_SLOTS[param] )
  ctx.emit_store_subscr()

@make_op( 2, )
def Sub( ctx, *args ) :
  ctx.emit_std_prefix2( *args )
  ctx.emit_binary_subtract()

@make_op( 1, parameterized=True )
def TableLookup( ctx, param, x0 ) :
  ctx.emit_call1( param.get, x0 )

@make_op( 1 )
def ToChar( ctx, *args ) :
  ctx.emit_call1( ctx.fn_tochar, *args )

@make_op( 1, output=1, stack=-1 )
def Write( ctx, *args ) :
  ctx.emit_std_prefix1( *args )
  ctx.emit_write()


##################################################
#                                                #
##################################################
@singleton
class StackInput( object ) :

  bound     = False
  load      = frozenset()
  nil       = True
  require   = 1
  stack     = 0
  store     = frozenset()

  def serialize( self, *args ) :
    pass

  def bind( self, inner ) :
    return inner

  def __repr__( self ) :
    return 'StackInput'

  def format( self ) :
    return self._format()[1]

  def _format( self, pos ) :
    return (pos+1),'s{}'.format( pos ) 

  def rewrite( self, fn ) :
    return self



