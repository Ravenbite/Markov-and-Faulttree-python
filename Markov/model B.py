###    Main
##               
#      
from class_MARKOV import *


# Create Markov
M = MARKOV( "Model B" )
# Create States
S1 = STATE( "Z1", 1 )
S2 = STATE( "Z2", 2 )
S3 = STATE( "Z3", 3 )
# Create Transitions and link them with States
T21 = TRANSITION( S2, S1, "-> 21", 1/2 )
T23 = TRANSITION( S2, S3, "-> 23", 1/2 )
T32 = TRANSITION( S3, S2, "-> 32", 1/2 )
T13 = TRANSITION( S1, S3, "-> 13", 3/4 )
T31 = TRANSITION( S3, S1, "-> 31", 1/4 )
# Link all into Markov
M + S1 + S2 + S3 + T21 + T23 + T32 + T13 + T31
# Lock model and compute some basic stuff for graph
M.prepare()
# Print Markov
M.printModell()
# Print P
M.printP()
# Simulation
state = np.array([[1.0, 0.0, 0.0]])                        # Start in state 1
M.simulate_stationary_distribution( state, 100 )           # Simulate 100 iterationen