from abc import ABCMeta, abstractmethod

class AbstractAI(metaclass=ABCMeta):
    "The command interface, that all commands will implement"
    
    @staticmethod
    @abstractmethod
    def execute():
        """ The required execute method that all command objects will use"""
        pass
    
    @staticmethod
    @abstractmethod
    def evaluate():
        '''calculate effect and undo'''
        pass
    @staticmethod
    @abstractmethod
    def undo():
        '''calculate effect and undo'''
        pass
