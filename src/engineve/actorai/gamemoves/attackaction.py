import random
import logging

from .gamemove import GameMove
from ...enginecommands.gamecommands.attackcommand import AttackCommand
from ...enginecommands.effectcommands.modifyresources import ModifyResources
from .. import pathingutils
from .. import aiutils


class AttackAction(GameMove):
    command_type = AttackCommand  # None
    name = "attack_action"
    resource_cost = {"turn_action": -1}  # if resource_cost is None else resource_cost
    attack_range = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_kwargs = {}

        for key in ("dmg_dice", "stat", "animation_frames", "dmg_range"):
            if key in kwargs.keys():
                self.command_kwargs[key] = kwargs[key]
        # if "dmg_dice" in kwargs.keys():
        #     self.command_kwargs["dmg_dice"] = kwargs["dmg_dice"]
        # if "stat" in kwargs.keys():
        #     self.command_kwargs["stat"] = kwargs["stat"]
        # if "animation_frames" in kwargs.keys():
        #     self.command_kwargs["animation_frames"] = kwargs["animation_frames"]

    def get_weight(self, state):
        return -1 if len(self.get_targets(state)) <= 0 else random.randint(1, 10)

    def get_ttk_weight(self, target_id, state):
        return max((100.0 / state.actors[target_id].hp), -0.001)

    def weigh_targets(self, state):
        return {
            target_id: self.get_ttk_weight(target_id, state)
            for target_id in self.get_targets(state)
        }

    def enemy_in_range(self, enemy_id, state):
        return self.attack_range >= pathingutils.measure_distance(
            state.actors[self.actor_id].loc, state.actors[enemy_id].loc
        )

    def make_command(self, state, *args, **kwargs) -> AttackCommand:
        # if 0 < len(self.command_kwargs):
        #     logging.debug("lookie here")
        target_weights = self.weigh_targets(state)
        if len(target_weights) == 0:
            print(self.weigh_targets(state))
        target_id = max(target_weights, key=target_weights.__getitem__)

        attack_declaration = (
            f"{state.actors[self.actor_id].name} attacks {state.actors[target_id].name}"
        )
        new_cmd = super().make_command(
            attacker_id=self.actor_id,
            target_id=target_id,
            log=attack_declaration,
            **self.command_kwargs,
        )
        new_cmd.effects.append(
            ModifyResources(new_cmd.attacker_id, changes=self.resource_cost)
        )

        return new_cmd

    def get_targets(self, state):
        enemy_ids = [eid for eid in aiutils.get_enemy_ids(self.actor_id, state)]
        enemy_ids = [
            eid
            for eid in enemy_ids
            if aiutils.is_actor_alive(eid, state) and self.enemy_in_range(eid, state)
        ]

        return enemy_ids
