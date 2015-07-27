from . ast import *
from . cfg import *
from . ops import *
from . utils import *

import collections
import itertools

__all__ = [
    'build_annotated_cfg'
  , 'comparison_chains_to_lookup_tables'
  ]


##################################################
#                                                #
##################################################
def _transform_conditional( blocks, last ) :

  var = None

  items = {}
  for cond,body in blocks :

    if len(body) != 1 :
      return

    if len(cond) != 3 :
      return

    op, = body
    if not isinstance(op,Const) :
      return

    ivar,ival,icmp = cond
    if not isinstance(icmp,CompareEQ) :
      return

    if not isinstance(ival,Const) :
      return

    if ivar != var :
      if var is not None :
        return
      var = ivar

    items[ ival.param ] = op.param

  cond = TableLookup( FrozenDict(items), var ) \
       , NoneP()

  body = Discard(),
  if last :
    body += last

  return (cond,body),


def comparison_chains_to_lookup_tables( blk ) :

  ops = []
  for op in blk :

    if isinstance(op,Conditional) :

      has_conditional = True

      blocks = []
      for cond,body in op.blocks :
        blocks.append((
            comparison_chains_to_lookup_tables( cond )
          , comparison_chains_to_lookup_tables( body )
          ))

      last = None
      if op.last is not None :
        last = comparison_chains_to_lookup_tables( op.last )

      result = _transform_conditional( blocks, last )

      op = Conditional( result )                      \
              if result                               \
              else Conditional( tuple(blocks), last )

    ops.append(op)

  return tuple(ops)


##################################################
#                                                #
##################################################
def _cfg_block_partition_key( op ) :

  # the key generated here yields a partition the op 
  # stream such that :
  #   - each Conditional op is handled separately 
  #   - Inc ops are grouped only with other Inc ops
  #   - adjacent ops that are neither Conditional nor
  #     Inc ops are grouped together

  if isinstance(op,Conditional) :
    return id(op)

  if isinstance(op,Inc) :
    return Inc

def _contains_conditional_p( blk ) :
  return any( isinstance(op,Conditional) for op in blk )

def _build_annotated_cfg_internal( ast, tail ) :

  for cid,blk in itertools.groupby( ast, _cfg_block_partition_key ) :

    if not isinstance(cid,int) :
      tail = tail_cons( tail, ops=tuple(blk) )

    else :

      blk, = blk

      new = collections.defaultdict( list )

      for cond,body in blk.blocks :

        if _contains_conditional_p( cond ) :
          tail = _build_annotated_cfg_internal( cond, tail )
          cond = ()

        tail = tail_cons( tail, Right, cond, True )

        left = _build_annotated_cfg_internal( body, tail_cons( tail, Left ) ) \
                  if _contains_conditional_p( body )                          \
                  else tail_cons( tail, Left, body )

        for u in left :
          new[ u.stack_cumm ].append( u )

      last = blk.last
      if last is not None :
        tail = _build_annotated_cfg_internal( last, tail ) \
                if _contains_conditional_p( last )         \
                else tail_cons( tail, ops=last )

      for t in tail :
        new[ t.stack_cumm ].append( t )

      tail = tail_cons( new.values() )

  return tail

def build_annotated_cfg( ast ) :

  # build a control-flow graph, annotated with
  # state details.  two execution paths are considered
  # distinct if they leave the stack in different
  # states or if they rename a1/a2 differently
  # (though use of the Inc op).  "programs" are 
  # small, so we don't have to worry about the
  # costs of being precise.

  return _build_annotated_cfg_internal( 
              ast
            , tuple_from_args(
                  make_block_from_args( (), Prologue() )
                )
            )






