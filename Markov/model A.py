###    Main
##               
#      
from class_MARKOV import *


# Create Markov
M = MARKOV( "Model A", 2 )                                 # dt = 2 h
# Create States
S1 = STATE( "Z1\nOK", 1 )
S2 = STATE( "Z2\nWarnzustand", 2 )
S3 = STATE( "Z3\nFehlerzustand", 3 )
S4 = STATE( "Z4\nReparaturzustand", 4 )
S5 = STATE( "Z5\nGeneralüberholung", 5 )
# Create Transitions and link them with States
T12 = TRANSITION( S1, S2, "λ 12", 2/365/24 )               # 2 Ausfälle / Jahr  in Stunden
T13 = TRANSITION( S1, S3, "λ 13", 2/365/24 )               # 2 Ausfälle / Jahr  in Stunden
T23 = TRANSITION( S2, S3, "λ 23", 2/365/24 )               # 2 Ausfälle / Jahr  in Stunden
T24 = TRANSITION( S2, S4, "λ 24", 1/24     )               # Techniker innerhalb 24h
T34 = TRANSITION( S3, S4, "λ 34", 1/12     )               # Techniker innerhalb 12h
T41 = TRANSITION( S4, S1, "λ 34", 1/4      )               # Reparatur innerhalb 4h
T45 = TRANSITION( S4, S5, "λ 45", 1/365/10/24 )            # Generalüberholung alle 10 Jahre in h
T51 = TRANSITION( S5, S1, "λ 51", 1/21/24 )                # Generalüberholung dauert 3 Wochen in h 
# Link all into Markov and lock model
M + S1 + S2 + S3 + S4 + S5 + T12 + T13 + T23 + T24 + T34 + T41 + T45 + T51
# Lock model and compute some basic stuff for graph
M.prepare()
# Print Markov
M.printModell()
# Print P
M.printP()
# Simulation
state = np.array([[1.0, 0.0, 0.0, 0.0  ]])                # Start in state 0
M.simulate_stationary_distribution( state, 2 )            # 2*2h steps
