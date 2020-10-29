###    MARKOV
##               
#  
from class_STATE import *
''''''
class TRANSITION:
    def __init__( self, src : STATE, dst: STATE, name : str, rate : float ) -> None:
        self.name = name
        self.rate = rate            # '#Failures / time'
        self.prop = None            # Prop of transition

        self.src  = src
        self.dst  = dst

        if( self.src == self.dst ):  # Init hidden transitions zur Laufzeit correctly
            self.prop = self.rate
''''''