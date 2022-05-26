""" TODO:
tags
actor.get_command
actor.register_observer()
command effects another command on the stack

"""
class Observer():
    def __init__(self, trigger, reaction):
        self.trigger = trigger
        self.reaction = reaction
    
    def react(self, state, meta):
        """should return command obj for the stack"""
        if self.match_notification(state, meta):
           return self.get_reaction(state, meta)

    def get_reaction(self, state, meta):
        return self.reaction
        
    def match_notification(self, state, meta):
        return self.trigger(state, meta)
        

   
