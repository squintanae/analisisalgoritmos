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
def InsertionSort( S ):
  for j in range( 1, len( S ) ):
    k = S[ j ]
    i = j - 1
    while -1 < i and k < S[ i ]:
      S[ i + 1 ] = S[ i ]
      i -= 1
    # end while
    S[ i + 1 ] = k
  # end for
# end def

## eof - InsertionSort.py
