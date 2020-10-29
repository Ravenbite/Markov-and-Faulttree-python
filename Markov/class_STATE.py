###    MARKOV
##               
#  
''''''
class STATE:
    def __init__( self, name : str, id : int ) -> None:
        self.name = name
        self.id   = id
        self._prop_stay    = 0.0    # Prop of no transition: 1 - ( ... )
        self._prop_list    = []     # LGS row entry with transitions
        self._row_values   = []     # LGS row entry with values
        self._row_string   = []     # LGS row entry with string

    def _sort_row_( self ) -> None:      # sort self._prop_list
        ptr = self._prop_list           
        n   = len ( self._prop_list )
        backup_state_ptr = None

        if ( n < 2 ):
            return

        for i in range(n-1):                                # bubblesort
            for j in range( 0, n-i-1):
                if( (ptr[j]).dst.id > (ptr[j+1]).dst.id ):
                    backup_state_ptr = ptr[j]               # swap
                    ptr[j]   = ptr[j+1]
                    ptr[j+1] = backup_state_ptr
                     
         
    def get_row_values( self ) -> list:
        for transition in self._prop_list:
            self._row_values.append( transition.prop )
        return self._row_values
''''''
