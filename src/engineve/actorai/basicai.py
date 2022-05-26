from ..enginecommands.gamecommands.attackcommand import AttackCommand
class BasicAI():
    '''class for making decision based on state and args thru static methods'''
        
    @staticmethod
    def get_target(state, attacker_id):
        for key, state_actor in state.actors.items():
            if state_actor.team != state.actors[attacker_id].team:
                return key
    
    @classmethod
    def make_attack_command(cls, state, attacker_id):
        target_id = cls.get_target(state, attacker_id)
        attack_command = AttackCommand(attacker_id=attacker_id, target_id=target_id)
        return attack_command
    
    @classmethod
    def make_game_move_command(cls, state, actor_id):
        thing = cls.choose_game_move(state, actor_id)
        
        return cls.make_attack_command(state, attacker_id=actor_id)

    @staticmethod
    def choose_game_move(state, actor_id):
        return 'attack_action'
        
    
    @staticmethod
    def is_turn_completed(actor_id, state):
        '''has no more turn resources or game moves for those that are available'''
        for resource_name in state.actors[actor_id].turn_resources:
            break;    
            # check is available
            if not state.actors[actor_id].resources[resource_name].is_avalable():
                return False
            # check if there is a move available
            
        return True

    @staticmethod
    def take_turn(state, actor_id):
        '''
        
        '''        
        return
        # for resource_key in ['turn_action']  # state.actors[actor_id].turn_resources:

            
