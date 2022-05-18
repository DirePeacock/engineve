class Receiver():
    """I accept Commands
    How Do I get the state, 

    how do I modify tre state
        -evaluate command, apply evaluated effect
    
    TODO: I am also the Game State Manager

    how does a tick flow down to me
    """

    @staticmethod
    def do_command(state, command):
        '''applies commands to the state'''
        command.execute(state)

