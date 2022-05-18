from ..enginecommands.attackcommand import AttackCommand
class BasicAI():
    '''class for making decision based on state and args thru static methods'''
        
    @staticmethod
    def get_target(state, attacker_id):
        for key, state_actor in state.actors.items():
            if state_actor.team != state.actors[attacker_id].team:
                return state_actor.id
    
    @classmethod
    def make_attack_command(cls, state, attacker_id):
        target_id = cls.get_target(state, attacker_id)
        attack_command = AttackCommand(attacker_id=attacker_id, target_id=target_id)
        return attack_command
    
    @staticmethod
    def choose_attack(state, attacker_id):
        return
    
    @staticmethod
    def take_turn(state, actor_id):
        turn_resources = ['attack']
        for resource in turn_resources:
            print(resource)
