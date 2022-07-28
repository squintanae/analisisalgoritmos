## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

'''
Sorts a sequence
@input S a sequence of weakly orderable elements.
@output S is modified to be an ordered sequence.
@requires Elements in S should be weakly comparable (i.e. they should support
          he use of the "<" symbol).
'''
def NaiveBubbleSort( S ):
  for i in range( len( S ) ):
    for j in range( len( S ) - 1 ):
      if S[ j + 1 ] < S[ j ]:
        S[ j + 1 ], S[ j ] = S[ j ], S[ j + 1 ]
    # end for
  # end for
# end def

## eof - NaiveBubbleSort.py
