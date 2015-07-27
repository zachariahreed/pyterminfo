from . ast import *
from . ast_transforms import *
from . cfg_transforms import *
from . parser import *
from . serialization import *
from . utils import *

__all__ = [ 
    'function_from_capability'
  ]


##################################################
#                                                #
##################################################
_visualization_hook = PASS

##################################################
#                                                #
##################################################
class Lint( object ) :
  pass

##################################################
#                                                #
##################################################
def function_from_capability( 
        name
      , raw
      , declared_arity
      , variables
      , binary          = True
      , encoding        = 'utf-8'
      , index           = None 

      # compatability options
      , increment_limit = 1
      , termcap_hacks   = True

      ) :

  # The "programs" we are compiling are short and simple,
  # and we don't need to do anything all that fancy. 
  # Statically implementing  some of the compatibility 
  # hacks that ncurses implements are a bit fun though

  if declared_arity is None :
    declared_arity = 9
  arity = declared_arity

  lint = Lint()
  lint.trivial = False
  lint.undeclared_arguments = False
  if termcap_hacks :
    lint.termcap_style = False

  if not raw :

    raw             = b''
    arity           = declared_arity
    effective_arity = 0

    lint.trivial = True

    fn = serialize_nil( name, arity, binary )

  else :

    ast = parse( raw )

    # we know what was declared, but what input variables 
    # are actually used
    effective_arity, implicit_push_count = \
      compute_effective_arity( ast, declared_arity, termcap_hacks, lint )

    if effective_arity > declared_arity :
      arity = effective_arity
      lint.undeclared_arguments = True

    # perform any simplifications that are easier
    # with Conditional blocks still intact
    ast   = comparison_chains_to_lookup_tables( ast )

    # break down Conditional blocks to build a CFG
    tail  = build_annotated_cfg( ast )

    # arrange for dummy values to be implicitly pushed onto
    # the static in the case of malformed capabilities that
    # pop an empty stack
    tail  = fixup_underflow( tail, implicit_push_count, lint )

    # there are several different slightly different strategies 
    # available here for turning the capability into a python
    # function. choose one that looks good for our particular
    # situation here
    strat = choose_execution_strategy( tail, lint )

    # 
    tail  = add_epilogue( tail, strat, lint )

    # various rewrites
    tail  = eliminate_inc( tail, limit=increment_limit )
    tail  = merge_blocks( tail )
    tail  = bind_ops( tail )

    # draw 'em perty pictures
    _visualization_hook( name, tail )

    # build the actual function
    fn = serialize( strat, name, tail, arity, binary, encoding, variables )

  fn.arity           = arity
  fn.declared_arity  = declared_arity
  fn.effective_arity = effective_arity
  fn.raw             = raw
  fn.binary          = binary
  fn.index           = index
  fn.lint            = lint

  return fn


