from .actorai.basicai import BasicAI
class GameEngine():
    '''aware of aware of AI & main loop invoking commands n stuff and statemanager/command receiver'''
    def __init__(self, invoker, state_manager):
        self.engine_state = "combat"
        self.invoker = invoker
        self.state_manager = state_manager

    def main(self):

        return self.combat_main()

    def combat_main(self):
        """

        """
        for attacker_id in self.state_manager.get_combat_iter():
            # while resource
            # target_id = self._get_target(self.state_manager.actors[attacker_id])
            attack_command = BasicAI.make_attack_command(self.state_manager, attacker_id)
            # self.invoker.execute('attack', args=(attacker_id, target_id))

            self.invoker.execute(state=self.state_manager, 
                                 command=attack_command)
            # self.state_manager.manage_attack(attacker_id, target_id)
            # self.receiver.tick_stack()
