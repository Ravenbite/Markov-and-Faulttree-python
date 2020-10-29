from graphics import *
from nodes    import *

# Create components
TOP  = node( "TOP", node_type.NOT )
C    = node( "C", node_type.AND )
A    = node( "A", node_type.OR )
B    = node( "B", node_type.OR )

# Create primary events
E1   = primaryevent( "1", 1/1000, 1/4 )
E2   = primaryevent( "2", 1/1000, 1/4 )
E3   = primaryevent( "3", 1/1000, 1/4 )
E4   = primaryevent( "4", 1/1000, 1/4 )

# Build tree 
TOP.add( C )
C.add( A )
C.add( B )
A.add( E1 )
A.add( E2 )
B.add( E3 )
B.add( E4 )

# Analyse tree
print ( TOP.get_childs_recursively() )  # do not use or watch because its very naiv and bad
print ( TOP.avail() )

# Draw tree
draw_dynamic( TOP, "BS-Tree" )














