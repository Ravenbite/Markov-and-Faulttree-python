###    MARKOV
##               
#      
import graphviz
import numpy as np 
import pandas as pd 
from random import random
from random import seed 
import matplotlib.pyplot as plt
from class_STATE import *
from class_TRANSITION import *
''''''
def errorAndExit( text : str ) -> None:
    print ( str( text ) ) 
    exit()
''''''

''''''
class MARKOV:
    def __init__( self, name : str, dt : float = 1.0 ) -> None:
        self.name = name
        self.dt   = dt
        self.states = []    # States 
        self.trans  = []    # Transitions
        self.P      = None  # Matrix P
        self.graph = graphviz.Digraph( )

    # add state to Markov
    def state( self, src : STATE ) -> None:
        self.states.append( src )

    # add transition to Markov
    def transition( self, src : TRANSITION ) -> None:
        self.trans.append( src )

    # friedlier interface to add state or transition
    def __add__( self, obj ):
        if      ( not isinstance( self, MARKOV ) ):
            errorAndExit( "Shorthand only do allow: <markov + obj>. No multiple obj or anything else showed ")
        if      ( isinstance( obj, STATE ) ):
            self.state( obj )
        elif    ( isinstance( obj, TRANSITION ) ):
            self.transition( obj )
        else:
            errorAndExit( "Second parameter is no valid obj " )
        return self

    # Compute Prop of transition via dt
    def __compute_prop__( self ) -> None:
        for transition in self.trans:
            transition.prop = self.dt * transition.rate

    # Create LGS: each row <=> Prop of State N <=> ( p1(t + dt) = ..... , ... , pN(t +dt) )
    def __init_LGS__( self ) -> None:
        for state in self.states:
            prop_result = 0.0
            #ptr = state._prop_list

            # Get all transitions except nn that point to our n
            for transition in self.trans:
                if( transition.dst == state ):
                    state._prop_list.append( transition )

            # Now sort transitions into asc order
            state._sort_row_()

            for transition in state._prop_list:     # Summe of each props   
                prop_result += transition.prop      
            prop_result = 1 - prop_result           # Kehrwert
            
            state._prop_stay = prop_result          # update value

    # compute prop of staying: 1 - (sum) 
    def __compute_stay__( self ) -> None:
        for state in self.states:
            prop_result = 0.0
            #ptr = state._prop_list

            # Get all transitions except nn that point away from node
            # Works because nn transitions are craeted afterwards :)
            for transition in self.trans:
                if( transition.src == state ):
                    state._prop_list.append( transition )

            # Now sort transitions into asc order
            #state._sort_row_()

            for transition in state._prop_list:     # Summe of each props   #ÄNDERN IN state._dlist
                prop_result += transition.prop      
            prop_result = 1 - prop_result           # Kehrwert
            
            state._prop_stay = prop_result          # update value


    # Create transitions for not moving into another state
    # Compute them with the results form initLGS
    def __hiddenTrans__( self ):
        for state in self.states:
            prop = state._prop_stay 
            hiddenTransition = TRANSITION( state, state, "", prop )
            self + hiddenTransition 
            # finaly insert missing nn into lgs row:
            state._prop_list.insert( 0, hiddenTransition )        
            state._sort_row_()  # inserting at correct index would be better than soring array :)

    def __computeP__( self ) -> list:
        matrixLen = len ( self.states )
        self.P = np.zeros( (matrixLen, matrixLen) )
        Rowcntr = 0
        for state in self.states:
            for transition in state._prop_list:
                self.P[Rowcntr,transition.dst.id-1] = transition.prop 
            Rowcntr +=1


    def prepare( self ) -> None:
        self.__compute_prop__()     # Convert Lambdas into Prop
        self.__compute_stay__()     # Compute Pnn = 1 - (sum)
        self.__hiddenTrans__()      # Create missing Pnn transitions for graph
        self.__computeP__()         # Compute matrix P
        

    def printModell( self ) -> None:
        # PRINT MODEL GRAPHVIZ
        # USE M.name as filename
        self.graph.graph_attr['rankdir'] = 'LR'
        self.graph.edge_attr.update(arrowhead='onormal', arrowtail="onormal", arrowsize="1", weight="0.3" )
        for state in self.states:
            self.graph.node( str(state), label=str(state.name), shape="circle", height="1", width="1" ) 
        for transition in self.trans:
            self.graph.edge( str(transition.src), str(transition.dst), str(transition.name)+"\n"+(str(transition.prop)[0:5]) )
        self.graph.render( self.name )

    def printP ( self ):
        print( "\nDie Übergangsmatrix lautet:")
        print( self.P )

    def simulate_stationary_distribution( self, state, iterationen):
        #stateHist = state
        #difHistory = pd.DataFrame(state)
        for iters in range(iterationen):
            state=np.dot(state, self.P)
            #stateHist=np.append(stateHist,state,axis=0)
            #difHistory = pd.DataFrame(stateHist)
        
        print( "\nDie Zustände konvergieren mit "+str(iterationen)+" * dt's nach:" )
        print( state )

        
''''''







