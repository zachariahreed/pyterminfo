from . cfg import *
from . ops import *
from . utils import *

from byteasm import *

import sys

__all__ = [ 
    'choose_execution_strategy'
  , 'serialize'
  , 'serialize_nil'
  ]

##################################################
#                                                #
##################################################
class Strategy( object ) :

  @classmethod
  def name( cls ) :
    return cls.__name__[:-8]

##################################################
#                                                #
##################################################
class StackStrategy( Strategy ) :

  @staticmethod
  def cost( tail ) :

    # need context deterministic number of outputs for each
    # tail element
    if not all( len(t.output_cumm) == 1 for t in tail ) :
      return float('inf')

    # Check for writes with elements still on the stack
    for blk in depth_first_iter( tail ) :

      if len(blk.output_cumm) == 1 :
        output, = blk.output_cumm
        if not output :
          continue

      if not blk.inputs :
        continue

      stack = blk.input_stack

      for op in blk.ops :
        if op.output and stack != op.require :
          return float( 'inf' )
        stack += op.stack

    # good to go
    return 0

  @staticmethod
  def epilogue_parameter( blk ) :
    output_cumm, = blk.output_cumm
    return output_cumm

  @staticmethod
  def tail_merge_key( blk ) :
    output_cumm, = blk.output_cumm
    return blk.stack_cumm, output_cumm

  def emit_prologue( self ) :
    self.emit_load_const( self.proto.join )

  def emit_epilogue( self, n ) :
    self.emit_build_tuple( n )
    self.emit_call_function( 1 )
    self.emit_return_value()

  def emit_write( self ) :
    pass


class ListStrategy( Strategy ) :

  @staticmethod
  def cost( tail ) :
    return 100

  @staticmethod
  def epilogue_parameter( blk ) :
    pass

  @staticmethod
  def tail_merge_key( blk ) :
    return blk.stack_cumm

  def emit_prologue( self ) :
    self.emit_load_const( self.proto.join )
    self.emit_build_list( 0 )

  def emit_epilogue( self, n ) :
    self.emit_call_function( 1 )
    self.emit_return_value()

  def emit_write( self ) :
    self.emit_list_append( self._stack_depth )


##################################################
#                                                #
##################################################
class BytesStrategy( Strategy ) :

  proto = b''

  def fn_stringlike_length( self, value ) :
    if isinstance(value,bytes) :
      return len(value)
    if isinstance(value,str) :
      return len(value.encode(self._encoding))
    raise TypeError( 'expected str or bytes' )

  def fn_ensure_stringlike( self, value ) :
    if isinstance(value,bytes) :
      return value
    if isinstance(value,str) :
      return value.encode(self._encoding)
    raise TypeError( 'expected str or bytes' )

  @staticmethod
  def fn_tochar( c ) :
    # we follow the lead of ncurses here in returning 0x80
    # when the value is 0x00. possibly this behaviour should 
    # be controllable setting context compile option
    return bytes(((c or 0x80),))

  @staticmethod
  def coerce_bytes( b ) :
    return b

  @singleton
  def emit_format() :

    if sys.version_info < (3,5) :

      # yikes! dirty, dirty, dirty! until the 
      # `bytes` formatting operator lands in 3.5
      # though, this unfortunately seems like the 
      # least painful route

      _sprintf = None

      def emit_format( self, fmt, value ) :

        nonlocal _sprintf

        if _sprintf is None :

          import ctypes
          libc = ctypes.cdll.LoadLibrary( 'libc.so.6' )
          impl = libc.sprintf
          getbuf = (ctypes.c_char * 32).from_buffer

          def sprintf( fmt, arg ) :
            result = bytearray(32)
            n = impl( getbuf(result), fmt, arg )
            del result[n:]
            return result

          _sprintf = sprintf

        self.emit_call2( _sprintf, Const(bytes(fmt)), value )

    else :

      def emit_format( self, fmt, value ) :
        self.emit_std_prefix2( Const(bytes(fmt)), value )
        self.emit_binary_modulo()

    return emit_format


class StrStrategy( Strategy ) :

  proto = ''

  def fn_stringlike_length( self, value ) :
    if isinstance(value,str) :
      return len(value.encode(self._encoding))
    raise TypeError( 'expected str' )

  @staticmethod
  def fn_ensure_stringlike( value ) :
    if isinstance(value,str) :
      return value
    raise TypeError( 'expected str' )

  @staticmethod
  def fn_tochar( c ) :
    # we follow the lead of ncurses here in returning 0x80
    # when the value is 0x00. possibly this behaviour should 
    # be controllable setting context compile option
    return chr(c) if c else '\x80'

  @staticmethod
  def coerce_bytes( b ) :
    return b.decode( 'latin1' )

  def emit_format( self, fmt, value ) :
    if str(fmt) == '%d' :
      self.emit_call1( str, value )
    else :
      self.emit_std_prefix2( Const(str(fmt)), value )
      self.emit_binary_modulo()


##################################################
#                                                #
##################################################
def choose_execution_strategy( tail, lint=None ) :

  best_strat = None
  best_cost  = float( 'inf' )

  for strat in (StackStrategy,ListStrategy) :
    cost = strat.cost( tail )
    if cost < best_cost :
      best_cost  = cost
      best_strat = strat

  strat = best_strat

  if lint is not None :
    lint.strategy = strat.name().lower()

  return strat


##################################################
#                                                #
##################################################
class SerializationContextBase( EmittersMixin ) :

  def __init__( self, assembler, variables, encoding ) :
    self._assembler   = assembler
    self._variables   = variables
    self._encoding    = encoding
    self._spillidx    = 0
    self._stack_depth = 0

  def spill( self ) :
    b.emit_store_fast( 'spill' + str(self._spillidx) )
    self._spillidx += 1
    self._stack_depth -= 1

  def unspill( self ) :
    self._spillidx += 1
    b.emit_load_fast( 'spill' + str(self._spillidx) )
    self._stack_depth += 1

  def serialize_block( self, blk ) :
    self._stack_depth = blk.input_stack
    for op in blk.ops :
      stack_depth = self._stack_depth
      op.serialize( self )
      self._stack_depth = stack_depth + op.stack

  def _serialize_op( self, op ) :
    stack_depth = self._stack_depth
    op.serialize( self )
    self._stack_depth = stack_depth + op.stack

  def emit_std_prefix1( self, x0 ) :
    self._serialize_op( x0 )

  def emit_std_prefix2( self, x0, x1, commutative=False ) :

    if x1.bound :
      self._serialize_op( x0 )
      x0 = StackInput

    self._serialize_op( x1 )

    swapped = False
    if not x0.nil :

      if x0.bound :
        self._serialize_op( x0 )
        swapped = True

      elif x0.require == 1 :
        self.emit_rot_two()
        self._serialize_op( x0 )
        swapped = True

      elif x0.require == 2 :
        self.emit_rot_three()
        self._serialize_op( x0 )
        swapped = True

      else :
        self.spill()
        self._serialize_op( x0 )
        self.unspill()

      if swapped and not commutative :
        self.emit_rot_two()
        swapped = False

    return swapped


  def emit_std_prefix3( self, x0, x1, x2 ) :

    if x0.nil :
      self.emit_std_prefix2( x1, x2 )

    elif x2.bound :
      self.emit_std_prefix2( x0, x1 )
      self._serialize_op( x2 )

    else :

      self.emit_std_prefix2( x1, x2 )

      if x0.bound :
        self._serialize_op( x0 )
        self.emit_rot_three()

      elif x0.require == 1 :
        self.emit_rot_three()
        self.emit_rot_three()
        self._serialize_op( x0 )
        self.emit_rot_three()

      else :
        self.spill()
        self.spill()
        self._serialize_op( x0 )
        self.unspill()
        self.unspill()

  def emit_call1( self, f, x0 ) :
    self.emit_std_prefix2( Const(f), x0 )
    self.emit_call_function(1)

  def emit_call2( self, f, x0, x1 ) :
    self.emit_std_prefix3( Const(f), x0, x1 )
    self.emit_call_function(2)


##
@memoize
def _make_ctx_type( *strats ) :

  name_parts = []
  for s in strats :
    name_parts.append( s.name() )
  name_parts.append( 'SerializationContext' )
  name  = ''.join(name_parts)

  bases = strats
  bases += SerializationContextBase,

  return type( name, bases, {} )

def _make_ctx( strat_e, binary, *args, **kwargs ) :

  strat_s = StrStrategy
  if binary :
    strat_s = BytesStrategy

  return _make_ctx_type( strat_s, strat_e )( *args, **kwargs )


##################################################
#                                                #
##################################################
def _make_label( blk ) :
  return 'l.' + str(blk.id)

def _branch_target_p( blk, which ) :

  if len(blk.inputs) > 1 :
    return True

  return blk.inputs                       \
     and blk.inputs[0].inner.branch       \
     and isinstance(blk.inputs[0],which)

def serialize( strat, name, tail, arity, binary, encoding, variables ) :

  b = FunctionBuilder()
  for a in range(arity) :
    b.add_positional_arg( str(Arg(a+1)), default=0 )
  b.set_closure_value( 'vars', variables )

  ctx = _make_ctx( strat, binary, b._assembler, variables, encoding )

  links = compute_child_link_map( tail )

  pending = [links.head]
  while pending :

    curr = pending.pop()
    
    while curr is not None :

      if _branch_target_p( curr, Right ) :
        ctx.emit_label( _make_label( curr ) )

      ctx.serialize_block( curr )

      left,right = links[ curr ]
      if left is None :
        curr = right

      else :

        ctx.emit_pop_jump_if_false( _make_label( right ) )

        lleft,lright = links[left]
        if lleft is None :
          ctx.serialize_block( left )
          if lright is not right :
            ctx.emit_jump_forward( _make_label( lright ) )
          curr = right

        else :
          pending.append( right )
          curr = left

  return b.make( name )

##################################################
#                                                #
##################################################
def serialize_nil( name, arity, binary ) :

  b = FunctionBuilder()
  for a in range(arity) :
    b.add_positional_arg( str(Arg(a+1)), default=0 )

  b.emit_load_const( b'' if binary else '' )
  b.emit_return_value()

  return b.make( name )


