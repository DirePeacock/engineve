from abc import ABCMeta, abstractmethod
class PrimitiveCommand(metaclass=ABCMeta):
    '''simplest observable changes to the state. has already been evaluated'''
    @abstractmethod
    def apply(self, state):
        '''i have a'''
        pass