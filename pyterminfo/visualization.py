from . import compile
from . cfg import *
from . utils import *

from byteasm.visutil import *

import collections
import pygraphviz

__all__ = [
    'set_visualization_path'
  ]

##################################################
#                                                #
##################################################
def _memory_usage_indicators( op ) :

  memory = collections.defaultdict( lambda : [False,False] )
  for e in op.load :
    memory[e][0] = True
  for e in op.store :
    memory[e][1] = True

  if not memory :
    return ''

  parts = []
  for k,(load,store) in memory.items() :
    if not store :
      op = '←'
    elif not load :
      op = '→'
    else :
      op = '↔'
    parts.append((str(k),op))

  return '[' + ','.join( v+k for (k,v) in sorted(parts) ) + ']'

##
def visualize( tail, path ) :

  G = pygraphviz.AGraph( directed=True )

  links = compute_child_link_map( tail )
  for blk in links.keys() :

    tab = Table( border=0, cellborder=0, cellpadding=3, bgcolor="white" )
    tab.add( Tagged( blk.id, color='blue', align='left', colspan=2 ) )

    for op in blk.ops :

      tab.add( 
          Tagged( op.format(), align='left' )
        , _memory_usage_indicators( op )
        )

    tab.add( 
        Tagged( 
            str.format( 
                'require={} stack={} output={} inc={}'
              , blk.require
              , blk.stack_cumm
              , ','.join( map(str,sorted(blk.output_cumm)) )
              , blk.stack_cumm
              )
          , bgcolor="gray"
          , colspan=2
          )
      )

    G.add_node( blk.id, label=str(tab), shape='record' )

  for blk,(left,right) in links.items() :
    if right is not None :
      G.add_edge( blk.id, right.id )
    if left is not None :
      G.add_edge( blk.id, left.id, color='darkorange' )


  G.draw( path, prog='dot' )
  #G.write( path[:-4] + '.dot' )



##################################################
#                                                #
##################################################
set_visualization_path = make_visualization_hook_manager( compile, visualize )
