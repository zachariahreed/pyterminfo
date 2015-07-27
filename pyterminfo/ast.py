from . ops import *

__all__ = [
    'Conditional'            
  , 'dump_ast'
  , 'compute_effective_arity'
  ]

##################################################
#                                                #
##################################################
class Conditional( object ) :

  def __init__( self, blocks, last=None ) :
    self.blocks = blocks
    self.last   = last


##################################################
#                                                #
##################################################
def _compute_effective_arity( ast ) :

  arity = -1
  for op in ast :

    if isinstance(op,Write) and isinstance(op.subexprs[0],Const) :
      continue

    arity = max( arity, 0 )

    if isinstance(op,Conditional) :

      if op.last is not None :
        arity = max( 
                  _compute_effective_arity( op.last )
                , arity 
                )

      for c,b in op.blocks :
        arity = max( 
                    _compute_effective_arity( c )
                  , _compute_effective_arity( b )
                  , arity 
                  )

    elif not isinstance(op,Inc) :

      for e in op.load :
        if isinstance(e,Arg) :
          arity = max( arity, int(e) )

  return arity

def compute_effective_arity( ast, declared_arity, termcap_hacks, lint=None ) :

  arity = _compute_effective_arity( ast )

  if arity == 0 and termcap_hacks :

    if lint is not None :
      lint.termcap_style        = True
      lint.undeclared_arguments = True

    return declared_arity, declared_arity

  if arity < 0 :
    
    if lint is not None :
      lint.trivial = True

    return 0, 0

  return arity, 0


##################################################
#                                                #
##################################################
def dump_ast( op, pad='' ) :

  if isinstance(op,tuple) :
    pad += '  '
    for i in op :
      dump_ast( i, pad )

  elif isinstance(op,Conditional) :
    head = 'IF'
    for cond,body in op.blocks :
      print( pad + head )
      dump_ast( cond, pad )
      print( pad + 'THEN' )
      dump_ast( body, pad )
      head = 'ELIF'
    if op.last is not None :
      print( pad + 'ELSE' )
      dump_ast( op.last, pad )
    print( pad + 'END' )

  else :
    print( pad + str(op) )


