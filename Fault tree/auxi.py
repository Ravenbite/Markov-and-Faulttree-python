# Auxiliary functions

def fatalError( gr_input_string: str ):
    print( "FatalError: " + str( gr_input_string ) + "\n" )
    exit()

''' This fx is not from myself. Ive copied the code from stackOverflow. Delivers static buffer for functions
    This mechanic isnt used any more but i keep this fragment as inspiration
'''
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate
