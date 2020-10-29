import graphviz
from nodes    import *
from auxi      import *

# Init all nodes of tree
def drawNodes( gr_node: node, dot ):

    for childNode in gr_node.rg_childNodes:
       
       # Check node type to determine what to do:
        if( isinstance( childNode, node ) ):
            if ( childNode.c_childNodes > 0 ):
                drawNodes( childNode, dot )
            else:
                fatalError( "Graphics: NodeRecursion: Component without event!.")
            # After recursion: createNode for yourself
            dot.node( childNode.gr_node_name, childNode.gr_graphName, shape="box")
        
        elif ( isinstance ( childNode, primaryevent ) ):
            # Create Node for primaryEvent
            dot.node( childNode.gr_event_name , childNode.gr_event_name, shape="circle")

        else:
            fatalError("Graphics: NodeRecursion: Illegal node type")         


# Init all edges of tree
#    @static.... is deprecated now. Fx will maintain functionality without static buffer
#    
@static_vars( finishedEdges= [] )
def drawEdges( gr_node: node, dot ):
 for childNode in gr_node.rg_childNodes:
       
       # Check node type to determine what to do:
        if( isinstance( childNode, node ) ):
            if ( childNode.c_childNodes > 0 ):
                drawEdges( childNode, dot )         # Recursion: childNode is now new root :)
            else:
                fatalError( "Graphics: NodeRecursion: Component without event!.")
            # After recursion: createEdge from child to parent ( gr_node ).
            # Draw from parent to child, otherwise graph is upside down
            dot.edge( gr_node.gr_node_name, childNode.gr_node_name )
        
        elif ( isinstance ( childNode, primaryevent ) ):
            # createEdge for child with parent ( gr_node ). Warning child is now a primary event no node
            dot.edge( gr_node.gr_node_name, childNode.gr_event_name  )
        else:
            fatalError("Graphics: NodeRecursion: Illegal node type")        


# Graphics interface
#   Draw tree 
#
def draw_dynamic( gr_node: node, gr_fileOutPath: str ):

    # Init Graphviz:
    dot = graphviz.Graph( )
    dot.attr(splines='ortho')

    # Draw line above root via simulating empty or invisible node above root
    dot.node("Root", "", shape='none')
    dot.node(gr_node.gr_node_name, gr_node.gr_graphName, shape='box')
    dot.edge("Root", gr_node.gr_node_name )     
      
    # Draw nodes and edges
    drawNodes( gr_node, dot )
    drawEdges( gr_node, dot )

    dot.render( gr_fileOutPath )