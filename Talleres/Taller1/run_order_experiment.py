## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

import struct, sys, time
from NaiveBubbleSort import *
from ImprovedBubbleSort import *
from InsertionSort import *

## -------------------------------------------------------------------------
def IsSorted( S ):
  f = True
  for i in range( len( S ) - 1 ):
    f = f and not( S[ i + 1 ] < S[ i ] )
  # end for
  return f
# end def

## -------------------------------------------------------------------------
def DoExperiment( S, f ):
  r = 5
  t = 0
  s = True
  for i in range( r ):
    C = S.copy( )
    start = time.time( )
    f( C )
    end = time.time( )
    s = s and IsSorted( C )
    t += float( end - start )
  # end for
  return [ s, t / float( r ) ]
# end def

## -------------------------------------------------------------------------
# Inputs
input_file = open( sys.argv[ 1 ], 'rb' )
input_buffer = input_file.read( )
input_file.close( )
b = int( sys.argv[ 2 ] )
e = int( sys.argv[ 3 ] )
s = int( sys.argv[ 4 ] )

# Data type configuration
element_type = int
element_size = 4
element_id = 'i'
N = len( input_buffer ) // element_size

# Read sequence as numbers
input_sequence = []
for i in range( N ):
  input_sequence += [ struct.unpack( element_id, input_buffer[ element_size * i : element_size * ( i + 1 ) ] )[ 0 ] ]
# end for

input_sequence.sort()

# Perform experiments
for n in range( b, e + 1, s ):
  nbr = DoExperiment( input_sequence[ 0 : n ], NaiveBubbleSort )
  ibr = DoExperiment( input_sequence[ 0 : n ], ImprovedBubbleSort )
  inr = DoExperiment( input_sequence[ 0 : n ], InsertionSort )
  if not( nbr[ 0 ] and ibr[ 0 ] and inr[ 0 ] ):
    print( "ERROR: Input sequence was not ordered" )
    sys.exit( 1 )
  # end if
  print( n, nbr[ 1 ], ibr[ 1 ], inr[ 1 ] )
# end for

## eof - run_experiment.py


