from abc import ABCMeta, abstractmethod

class EngineStateInterface(metaclass=ABCMeta):
    "The command interface, that all commands will implement"
    @abstractmethod
    def periodic(self):
        """ The required execute method that all command objects will use"""
        pass
    
    @abstractmethod
    def transition():
        '''calculate effect and undo'''
        pass
    
