# We have to include:
import enum
from typing import Type
from functools import reduce
from auxi import *


''' namespace node::aux start '''
#
# Helper class to simulate cpp::enum 
#   -provide alias names   for user interface
#   -provide bitfield      for differencing nodetypes inside code 
#
#   -usage:
#     methods have to check whether input is a valid node type
#     methods have to save node-type-value as attribute
#     methods have to convert node-type-value into string repr
#
class node_type( enum.Enum ):
    VOID    = 1 << 0
    AND     = 1 << 1
    OR      = 1 << 2
    NOT     = 1 << 3
    COMMENT = 1 << 4

# Helper fx - return true when parameter is a valid node type  
def __node_checkType__( gr_node_input: 'node_type' ) -> bool:
    if ( type ( gr_node_input ) == type( node_type.VOID ) ):
        return True
    else:
        return False

# Helper fx - return intern-used-value-type for node
def __node_getTypeValue__( gr_node_input: 'node_type' ) -> int:
    if ( __node_checkType__( gr_node_input ) == False ):
        fatalError( "InitNode: Illegal node type.")
    return gr_node_input.value

# Helper fx - return extern-used-string-type for node
def __node_getTypeRepr__( l_node_type: 'node_type' ) -> str:
    return node_type( l_node_type ).name

# Helper fx - return string repr for graphics
def __node_type_getGraphName__( l_node_type: 'node_type' ) -> str:
    if  ( l_node_type == 1 << 1 ):
        return " (&)"
    elif( l_node_type == 1 << 2 ):
        return " (<=1)"
    elif( l_node_type == 1 << 3 ):
        return " (NOT)"
    else:
        fatalError( "DrawGraphics: GetGraphName: IllegalNodeType ")
''' namespace node::aux end '''


''' namespace node::event start '''
class primaryevent:
    def __init__( self, gr_event_name: str, d_ausfallRate: float, d_reperaturRate: float ):
        self.gr_event_name = gr_event_name
        self.d_ausfallRate = d_ausfallRate
        self.d_reperaturRate = d_reperaturRate
        self.d_unavailability = self.d_ausfallRate / ( self.d_ausfallRate + self.d_reperaturRate )
        self.d_availability = 1 - self.d_unavailability
''' namespace node::event end '''


''' namespace node '''
class node:
    def __init__( self, gr_node_name: str, gr_node_type: 'node_type' ):
        self.gr_node_name = gr_node_name                               # String    
        self.l_node_type  = __node_getTypeValue__( gr_node_type )      # Int       # ( converted str alias )
        self.d_availability = None                                     # Double   
        self.d_unavailability = None                                   # Double
        self.rg_childNodes = [ ]                                       # Range     
        self.c_childNodes = 0                                          # Count     
        self.c_max_childNodes = -1                                     # Count     # max childs allowed. -1 = infinite
        self.gr_graphName = gr_node_name + __node_type_getGraphName__( self.l_node_type )   # String    # Konkatenate node type with node name for graphics

    def add ( self, gr_node_in: 'node' ):
        if ( ( self.c_max_childNodes != -1 ) and ( self.c_childNodes >= self.c_max_childNodes ) ):
            print( " Operation not permited, node cannot have more child nodes.\n" )
            return
        self.rg_childNodes.append( gr_node_in )
        self.c_childNodes+=1

    def avail ( self ):         # compute availability via recursion
        
        # buffers
        unavailabilities = []
        availabilites = []
        
        # get node type
        if   ( self.l_node_type == 1 << 1 ):  # AND NODE
            # AND nodes have to generate product from all notavailabilites @ childs 
            unavailabilities = self.__availAND__()                                          # collect all unavailabilities from childs
            self.d_unavailability = reduce(( lambda x, y: x * y ), unavailabilities )       # compute unavailability 
            self.d_availability   = 1 - self.d_unavailability                               # compute availability

        elif ( self.l_node_type == 1 << 2 ):  # OR NODE
            # OR nodes have to generate  product from all availabilites @ childs 
            availabilites = self.__availOR__()                                              # collect all availabilities from childs
            self.d_unavailability = 1 - reduce(( lambda x, y: x * y ), availabilites )      # compute unavailability
            self.d_availability = 1 - self.d_unavailability                                 # compute availability

        elif ( self.l_node_type == 1 << 3 ): # NOT NODE
            # NOT nodes have to negate input 
            
            # Check: Node must have one child 
            if ( self.c_childNodes != 1 ):
                fatalError( "Avail: NotNode: Must have one input ")
            
            # Get avail from child and invert it 
            oldAvailability  = self.__availNOT__()
            self.d_unavailability = oldAvailability                              
            self.d_availability   = 1 - self.d_unavailability                    

        else:
            fatalError( "Avail: Not supported node type.")   

        return self.d_availability                                                          # return availability     

    def __availNOT__( self ):       # Get unavailability from child
        child = self.rg_childNodes[0]

        if   ( isinstance( child, node ) ):
            return child.avail()                                          # go for recursive call
        elif ( isinstance( child, primaryevent ) ):
            return child.d_availability                                   # end of recursion

    
    def __availAND__( self ):      # Get all unavailabilitys 
        availabilities = []
        unavailabilites = []

        # get availabilites von allen kindern:
        for gr_node in self.rg_childNodes:
            if   ( isinstance( gr_node, primaryevent ) ):
                availabilities.append( gr_node.d_availability )
            elif ( isinstance( gr_node, node) ):
                availabilities.append( gr_node.avail() )

        # now, because AND node have to compute product of unavailabilites, we have to invert each availability
        unavailabilites = [ 1 - x for x in availabilities ]

        return unavailabilites


    def __availOR__( self ):    # Get all availabilites
        availabilities = []

        # get availabilites von allen kindern:
        for gr_node in self.rg_childNodes:
            if   ( isinstance( gr_node, primaryevent ) ):
                availabilities.append( gr_node.d_availability )
            elif ( isinstance( gr_node, node) ):
                availabilities.append( gr_node.avail() )
        
        return availabilities


    def get_childs_recursively( self ) -> str:             # Interface and recursion fx
        
        gr_result = []                                     

        for gr_node in self.rg_childNodes:
            if ( isinstance( gr_node, node ) ):
                if ( gr_node.c_childNodes > 0 ):
                    gr_result.append( gr_node.get_childs_recursively() )
                    continue
                else:
                    gr_result.append( gr_node.gr_node_name )
                    continue
            elif ( isinstance ( gr_node, primaryevent ) ):
                gr_result.append( str(gr_node.gr_event_name) )
                continue
            #else because if no continue throws we land here
            fatalError( "get_childs_recursively: obj is no node or primary event!.")

        return  self.gr_node_name + str( gr_result )
''' namespace node end '''