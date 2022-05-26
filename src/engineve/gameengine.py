from .actorai.basicai import BasicAI
from .enginestates.combatstate import CombatState
from .enginestates.enginestate import EngineState
class GameEngine():
    '''aware of aware of AI & main loop invoking commands n stuff and statemanager/command receiver'''
    def __init__(self, invoker, game_state):
        self.engine_state = "combat"
        self.invoker = invoker
        self.game_state = game_state
        self.engine_state = EngineState()

    
    def main(self):
        self.engine_state = CombatState([actor_id for actor_id in self.game_state.actors.keys()])
        test_frames = 100000
        for i in range(0, test_frames):
            self.engine_state.periodic(self.game_state, self.invoker)
            self.invoker.periodic(self.game_state)

    
    def spawn_actors(self, actor_class, num=1, **kwargs):
        for some_actor in GameEngine.generate_actors(actor_class, num, **kwargs):
            self.game_state.add_actor(some_actor)
    
    @staticmethod
    def generate_actors(actor_class, num=1, **kwargs):
        return [actor_class(**kwargs) for i in range(0, num)]

    def _combat_main(self):
        """ aaa """
        for current_actor in self.game_state.get_combat_iter():
            while not self.game_state.actors[current_actor].is_turn_completed(self.game_state):
                new_move = None
                self.invoker.put(new_move)
                self.invoker.tick_stack(self.game_state)

            # while resource
            # target_id = self._get_target(self.state_manager.actors[attacker_id])
            
            # self.state_manager.actors[current_actor].get_attack_command(self.state_manager)
            
            # attack_command = BasicAI.make_attack_command(self.state_manager, current_actor)
            # self.invoker.execute('attack', args=(attacker_id, target_id))

            # self.invoker.execute(state=self.state_manager,
            #                      command=attack_command)
            # self.state_manager.manage_attack(attacker_id, target_id)
            # self.receiver.tick_stack()
