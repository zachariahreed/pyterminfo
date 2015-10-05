import functools

__all__ = [
    'FrozenDict'
  , 'PASS'
  , 'always'
  , 'constantly'
  , 'first'
  , 'fourth'
  , 'iextend'
  , 'memoize'
  , 'never'
  , 'second'
  , 'singleton'
  , 'third'
  , 'tuple_from_args'
  , 'tuple_map'
  , 'tuple_repeat'
  ]
  
##################################################
#                                                #
##################################################
def first( value, *args ) :
  return value

def second( *args ) :
  return args[1]

def third( *args ) :
  return args[2]

def fourth( *args ) :
  return args[3]

def constantly( value ) :
  return (lambda *args, **kwargs : value)

def always( *args, **kwargs ) :
  return True

def never( *args, **kwargs ) :
  return False

def PASS( *args, **kwargs ) :
  pass

##################################################
#                                                #
##################################################
def tuple_from_args( *args ) :
  return args

def tuple_map( f, it ) :
  return tuple(map(f,it))

def tuple_repeat( n, *args ) :
  return args * n

##################################################
#                                                #
##################################################
def iextend( it, then=None ) :
  yield from it
  while True :
    yield then

##################################################
#                                                #
##################################################
def singleton( f ) :
  return f()

def memoize( f ) :

  not_found = object()
  cache = {}

  @functools.wraps(f)
  def wrapper( *key ) :
    result = cache.get( key, not_found )
    if result is not_found :
      result = f( *key )
      cache[ key ] = result
    return result

  return wrapper

##################################################
#                                                #
##################################################
class FrozenDict( dict ) :

  def __init__( self, *args, **kwargs ) :
    super().__init__( *args, **kwargs )
    self._hash = None

  def __hash__( self ) :
    if self._hash is None :
      value = hash(self.__class__)
      for k,v in self.items() :
        value ^= hash(k) ^ hash(v)
      self._hash = value
    return self._hash

  def __str__( self ) :
    return '[' + ','.join( '%d→%d' % kv for kv in sorted(self.items()) ) + ']'

  def __setitem__( self, key, value ) :
    raise TypeError( 'cannot mutate \'FrozenDict\' object' )

  def updated( self, *args, **kwargs ) :
    raise TypeError( 'cannot mutate \'FrozenDict\' object' )




