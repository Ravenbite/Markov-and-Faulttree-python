###    Main
##               
#      
from class_MARKOV import *


# Create Markov
M = MARKOV( "Model C", 4 )                           # dt = 4h
# Create States
S1 = STATE( "Z1", 1 )
S2 = STATE( "Z2", 2 )
S3 = STATE( "Z3", 3 )
# Create Transitions and link them with States
T12 = TRANSITION( S1, S2, "λ 12", 2/365/24 )         # 2 Ausfälle im Jahr in Stunde umgerechnet
T23 = TRANSITION( S2, S3, "λ 23", 1/365/24 )         # 1 Ausfall im Jahr in Stunde umgerechnet
# Link all into Markov and lock model 
M + S1 + S2 + S3 + T12 + T23
# Lock model and compute some basic stuff for graph
M.prepare()
# Print Markov
M.printModell()
# Print P matrix
M.printP()
# Simulation
state = np.array([[0.0, 1.0, 0.0]])                 # Start in state 2
M.simulate_stationary_distribution( state, 200 )    # Simulate 200*4h
