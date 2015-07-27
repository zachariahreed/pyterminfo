from . cfg import *
from . ast import *
from . ops import *
from . utils import *

import collections
import functools

__all__ = [ 
    'add_epilogue'
  , 'bind_ops'
  , 'merge_blocks'
  , 'eliminate_inc'
  , 'fixup_underflow'
  ]


##################################################
#                                                #
##################################################
def standard_transformer( fn ) :

  @functools.wraps(fn)
  def wrapper( tail, *args, **kwargs ) :

    @memoize
    def impl( blk ) :
      return fn(impl,blk,*args,**kwargs)

    return tuple_map(impl,tail)

  return wrapper


##################################################
#                                                #
##################################################
def fixup_underflow( tail, arity, lint ) :

  @memoize
  def impl( blk ) :

    if not blk.inputs :
      return 0, blk

    underflow_cumm = set()
    inputs = []
    for i in blk.inputs :
      uc,inner = impl(i.inner)
      inputs.append( i.make_like(inner) )
      underflow_cumm.add( uc )
    inputs = tuple(inputs)
    underflow_cumm, = underflow_cumm

    underflow = blk.require - blk.input_stack
    if underflow > 0 :

      begin           = underflow_cumm
      underflow_cumm += underflow
      inputs          = Right(
                            make_block(
                                inputs
                              , dummy[begin:underflow_cumm]
                              )
                          ),

    return underflow_cumm, make_block( inputs, blk.ops, branch=blk.branch )


  ##
  dummy = tuple( Push( Arg(arity-i) ) for i in range(arity) ) \
        + tuple_repeat( 64-arity, Const(0) )

  underflow_cumm, tail = zip( *map(impl,tail) )
  if lint is not None :
    lint.underflow = any( underflow_cumm )

  return tuple(tail)

def add_epilogue( tail, strat, lint ) :

  # ensure anything left on the stack is
  # properly cleaned up

  dirty_stack = False
  new = collections.defaultdict( list )

  grouped = collections.defaultdict( list )
  for e in tail :
    grouped[ strat.tail_merge_key(e) ].append( e )

  for blocks in grouped.values() :
    
    blk = make_linked( Right, blocks, () )
    stack = blk.stack_cumm
    
    if stack > 0 :
      dirty_stack = True
      blk = make_linked( Right, blocks, tuple_repeat( stack, Discard() ) )
    
    new[ strat.tail_merge_key(blk) ].append( blk )

  # add the actual epilogue block
  result = []
  for items in new.values() :

    param, = { strat.epilogue_parameter(i) for i in items }

    result.append( 
        make_linked_from_args( Right, items, Epilogue( param ) )
      )

  if lint is not None :
    lint.dirty_stack = dirty_stack

  return tuple( result )


@standard_transformer
def eliminate_inc( impl, blk, limit=1 ) :

  # the runtime behavior Inc ops are a bit painful
  # to implement, so we rewrite the program to avoid
  # having to do so. this needs to be done before
  # the merge_blocks pass though since the data 
  # required is stored only at the block level

  def _rewrite_push_op( op ) :
    if isinstance(op,Push) and int(op.param) in (1,2):
      delta = min(limit,blk.inputs[0].inner.increment_cumm)
      return Add(op,Const(delta))

  ##
  if blk.increment_cumm :

    ops = []
    for op in blk.ops :
      if not isinstance(op,Inc) :
        ops.append( op.rewrite( _rewrite_push_op ) )
    ops = tuple(ops)

    blk = make_block( blk.map_inputs( impl ), ops, branch=blk.branch )

  return blk


@standard_transformer
def merge_blocks( impl, blk ) :

  # if a chain of blocks can be represented
  # as a single block, return a new version where
  # they have been merged

  if not blk.inputs :
    return blk

  inputs = []
  for i in blk.inputs :
    inner = impl(i.inner)
    if inner.ops or inner.branch :
      inputs.append( i.make_like(inner) )
    else :
      inputs.extend( inner.inputs )

  if not any( i.inner.branch for i in inputs ) :

    suffix = []
    for e,*rest in zip( *(reversed(i.inner.ops) for i in inputs ) ):
      if not all( r==e for r in rest ) :
        break
      suffix.append(e)

    if suffix :

      n      = len(suffix)
      suffix = tuple(suffix[::-1])
      
      new = []
      for inp in inputs :

        i = inp.inner

        if len(i.ops) == n :
          new.extend( i.inputs )

        else :
          new.append( Right( make_block( i.inputs, i.ops[:-n] ) ) )

      return make_block( tuple(new), suffix+blk.ops, branch=blk.branch )

  return make_block( tuple(inputs), blk.ops, branch=blk.branch )


@standard_transformer
def bind_ops( impl, blk ) :

  ops = []
  for op in blk.ops :

    if not op.bound :

      store = set()

      for i in range(len(ops)-1,-1,-1) :

        e = ops[i]

        if e.producer :

          if not e.load.isdisjoint( store ) :
            break

          op = op.bind( e )
          del ops[i]
          if op.bound :
            break

        elif e.require or e.stack :
          break

        store |= e.store

    if not (op.bound and isinstance(op,Discard)) :
      ops.append(op)

  ops = tuple(ops)

  return make_block( blk.map_inputs( impl ), ops, branch=blk.branch )


