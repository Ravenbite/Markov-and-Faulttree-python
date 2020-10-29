###    Main
##               
#      
from class_MARKOV import *


# Create Markov
M = MARKOV( "Model E" )
# Create States
S1 = STATE( "Z1\nOK", 1 )
S2 = STATE( "Z2\nWarnzustand", 2 )
S3 = STATE( "Z3\nFehlerzustand", 3 )
S4 = STATE( "Z4\nReparaturzustand", 4 )
# Create Transitions and link them with States
T1 = TRANSITION( S1, S2, "l12", 2/365/24 )              
T2 = TRANSITION( S1, S3, "l13", 2/365/24 )            
T3 = TRANSITION( S2, S3, "l23", 2/365/24 )            
T4 = TRANSITION( S2, S4, "l24", 1/24     )            
T5 = TRANSITION( S3, S4, "l34", 1/12     )            
T6 = TRANSITION( S4, S1, "l34", 1/4      )  
# Link all into Markov
M + S1 + S2 + S3 + S4 + T21 + T23 + T32 + T13 + T31
# Lock model and compute some basic stuff for graph
M.prepare()
# Print Markov
M.printModell()
# Print P matrix
M.printP()
# Simulation
state = np.array([[1.0, 0.0, 0.0, 0.0]])                   # Start in state 1
M.simulate_stationary_distribution( state, 100 )           # Simulate 100 iterations