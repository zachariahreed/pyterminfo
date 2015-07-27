from . utils import *
from . ops import *

from collections import defaultdict

import itertools

__all__ = [
    'Block'
  , 'Left'
  , 'Right'
  , 'compute_child_link_map'
  , 'depth_first_iter'
  , 'make_block'
  , 'make_block_from_args'
  , 'make_linked'
  , 'make_linked_from_args'
  , 'tail_cons'
  ]

##################################################
#                                                #
##################################################
class Input( object ) :

  @classmethod
  def make_like( cls, inner ) :
    return cls( inner )

  def __init__( self, inner ) :
    self.inner = inner

  def __repr__( self ) :
    return str.format( '<{} {}>', self.tname, self.inner )

  def transform( self, f ) :
    return self.__class__( f(self.inner) )


class Left( Input )  : 
  tname = 'left'

class Right( Input ) : 
  tname = 'right'


##
class Block( object ) :

  seq = itertools.count(1)
  
  def __init__( 
          self
        , id
        , inputs
        , ops
        , branch
        , stack
        , require
        , output
        , stack_cumm
        , output_cumm
        , increment_cumm
        , input_stack
        ) :

    self.id              = id
    self.inputs          = inputs
    self.ops             = ops
    self.branch          = branch
    self.stack           = stack
    self.require         = require
    self.output          = output
    self.stack_cumm      = stack_cumm
    self.output_cumm     = output_cumm
    self.increment_cumm  = increment_cumm
    self.input_stack     = input_stack
 
  def __repr__( self ) :

    inputs = []
    for i in self.inputs :
      inputs.append( str( i.inner.id ) + ':' + str( i.tname[0] ) )

    return str.format(
                '<Block id={} inputs={{{}}} branch={} ops={}>'
              , self.id
              , ','.join( inputs )
              , self.branch
              , self.ops
              )

  def map_inputs( self, f ) :
    return tuple( i.transform(f) for i in self.inputs )


##
def make_block( inputs, ops, *, branch=False ) :

  stack     = 0
  require   = 0
  output    = 0
  increment = 0

  for op in ops :
    require    = max( require, op.require-stack)
    stack     += op.stack
    output    += op.output
    increment += op.increment

  if branch :
    require  = max( require, 1-stack )
    stack   -= 1

  if not inputs :

    input_stack    = 0
    stack_cumm     = stack
    increment_cumm = increment
    output_cumm    = frozenset((output,))

  else :

    input_stack     = set()
    input_output    = set()
    input_increment = set()

    for i in inputs :

      assert isinstance(i,Right) \
          or (isinstance(i,Left) and i.inner.branch)

      inner = i.inner

      input_stack.add( inner.stack_cumm )
      input_increment.add( inner.increment_cumm )
      input_output.update( inner.output_cumm )

    stack_cumm, = input_stack
    stack_cumm += stack

    increment_cumm, = input_increment
    increment_cumm += increment

    input_stack, = input_stack

    output_cumm = frozenset( o+output for o in input_output )

  return Block(
            id              = next(Block.seq)
          , inputs          = inputs
          , ops             = ops
          , branch          = branch
          , stack           = stack
          , require         = require
          , output          = output
          , stack_cumm      = stack_cumm
          , output_cumm     = output_cumm
          , increment_cumm  = increment_cumm
          , input_stack     = input_stack
          )

def make_block_from_args( inputs, *ops, **kwargs ) :
  return make_block( inputs, ops, **kwargs )

def make_linked( ctor, inputs, ops, **kwargs ) :
  return make_block( 
              (ctor(inputs),) 
                  if isinstance(inputs,Block) 
                  else tuple_map(ctor,inputs)
            , ops
            , **kwargs
            )

def make_linked_from_args( ctor, inputs, *ops, **kwargs ) :
  return make_linked( ctor, inputs, ops, **kwargs )

##################################################
#                                                #
##################################################
def tail_cons( tail, ctor=Right, ops=(), branch=False ) :

  def impl( t ) :
    return make_linked( ctor, t, ops, branch=branch )

  return tuple_map( impl, tail )


def depth_first_iter( tail ) :

  pending = [tail]                       \
               if isinstance(tail,Block) \
               else list(tail)

  seen = set()
  while pending :

    p = pending.pop()
    if p.id not in seen :
      seen.add( p.id )
      yield p
      for i in p.inputs :
        pending.append( i.inner )


##################################################
#                                                #
##################################################
class ChildLinkMap( dict ) :

  def __init__( self, head ) :
    self.head = head


##
def compute_child_link_map( tail ) :

  # Every non-terminal block in the graph
  # should have a right link. Branch blocks
  # also have a left link. Build a map from
  # block -> (left child, right child) and
  # report the head of the graph.

  head = None
  pending = list(tail)

  accum = defaultdict( lambda : [False,None,None] )
  while pending :

    t = pending.pop()
    info = accum[t]
    if info[0] :
      continue

    info[0] = True
    if t.inputs :

      for inp in t.inputs :
        idx = 1+isinstance(inp,Right)
        cinfo = accum[ inp.inner ]
        if cinfo[idx] is not None :
          raise AssertionError(
                      str.format(
                          '{} already has {} child {} - {} also claims to be this child'
                        , inp.inner
                        , inp.tname
                        , t
                        , cinfo[idx]
                        )
                    )
        cinfo[idx] = t
        pending.append( inp.inner )

    elif head is None :
      head = t

    else :
      assert t is head, (head,t)

  assert not head.inputs
  links = ChildLinkMap( head )
  for blk,(_,left,right) in accum.items() :
    assert (left is None) or (right is not None)
    assert (left is not None) == blk.branch
    links[blk] = (left,right)

  return links


