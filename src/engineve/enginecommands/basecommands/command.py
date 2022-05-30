from abc import ABCMeta, abstractmethod
import logging
from ...tags import TaggedClass
def DoNothing(*args, **kwargs):
    print(f"DoNothing(args:{args}, kwargs:{kwargs})")

class AbstractCommand(metaclass=ABCMeta):
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


class Command(AbstractCommand, TaggedClass):
    '''
    can be evaluated
    can do application of evaluated change
    can undo application of evaluated change
    can store tags for obeservers
    can be a composite command
    can be logged
    '''
    def __init__(self, *args, **kwargs):
        TaggedClass.__init__(self, *args, **kwargs)
        self.args=args
        self.kwargs=kwargs      
        self.effects = []
        self.inverse_effects = []
        self.evaluated = False
        self.log = "" if 'log' not in kwargs.keys() else kwargs['log']

    def execute(self, state):
        if not self.evaluated:
            self.evaluate(state)        
        
        self.apply_effects(state)

            
    def evaluate(self, state) -> None:
        '''resolves command down to primitive command'''
        self.evaluated = True
        # self.effects = [] if
        self.inverse_effects = []

    def apply_effects(self, state):
        for effect in self.effects:
            effect.apply(state)

    def undo(self, state):
        if not self.evaluated:
            self.evaluate(state)
        state.apply_effects(self.inverse_effects)
        

